#!/usr/bin/env python3
"""Offline regression tests for output contracts, host policy and false positives."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCANNER = Path(__file__).resolve().parents[1] / 'scripts/audit_skills.py'

class ScannerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.skill = self.root / 'sample'
        self.skill.mkdir()
        self.write()

    def write(self, body='Review the requested artifact.\n', description='Review an artifact when requested.'):
        (self.skill / 'SKILL.md').write_text('---\nname: sample\ndescription: ' + json.dumps(description) + '\n---\n' + body)

    def run_scan(self, *args, path=None):
        proc = subprocess.run([sys.executable, str(SCANNER), str(path or self.skill), '--json', *args], capture_output=True, text=True)
        return proc.returncode, json.loads(proc.stdout) if proc.stdout else None

    def policy(self, text):
        (self.skill / 'agents').mkdir(exist_ok=True)
        (self.skill / 'agents/openai.yaml').write_text(text)

    def test_clean(self):
        code, result = self.run_scan()
        self.assertEqual(code, 0)
        self.assertEqual(result['findings'], [])
        self.assertEqual(result['files'][0]['invocation'], 'unknown')

    def test_codex_explicit_policy(self):
        self.write(description='Use when explicitly invoked to review an artifact.')
        self.policy('policy:\n  allow_implicit_invocation: false\n')
        code, result = self.run_scan('--host', 'codex')
        self.assertEqual(code, 0)
        self.assertEqual(result['files'][0]['invocation'], 'explicit-only')
        self.assertFalse(any(f['id'] == 'P4' for f in result['findings']))

    def test_generic_does_not_guess_policy(self):
        self.policy('policy:\n  allow_implicit_invocation: false\n')
        self.assertEqual(self.run_scan()[1]['files'][0]['invocation'], 'unknown')

    def test_codex_frontmatter_flag_not_policy(self):
        p = self.skill / 'SKILL.md'
        p.write_text(p.read_text().replace('name: sample', 'name: sample\ndisable-model-invocation: true'))
        result = self.run_scan('--host', 'codex')[1]
        self.assertEqual(result['files'][0]['invocation'], 'implicit-allowed')

    def test_invalid_policy(self):
        self.policy('policy:\n  allow_implicit_invocation: "false"\n')
        code, result = self.run_scan('--host', 'codex')
        self.assertEqual(code, 1)
        self.assertEqual(result['files'][0]['invocation'], 'unknown')
        self.assertTrue(result['findings'][0]['file'].endswith('openai.yaml'))

    def test_multiline_yaml(self):
        (self.skill / 'SKILL.md').write_text('---\nname: sample\ndescription: >-\n  Review artifacts\n  when requested.\n---\nReview.\n')
        code, result = self.run_scan()
        self.assertEqual(code, 0)
        self.assertEqual(result['files'][0]['description_chars'], len('Review artifacts when requested.'))

    def test_invalid_yaml(self):
        (self.skill / 'SKILL.md').write_text('---\nname: [broken\n---\n')
        self.assertEqual(self.run_scan()[0], 1)

    def test_missing_field(self):
        (self.skill / 'SKILL.md').write_text('---\nname: sample\n---\n')
        self.assertEqual(self.run_scan()[0], 1)

    def test_wrong_type(self):
        (self.skill / 'SKILL.md').write_text('---\nname: sample\ndescription: [one, two]\n---\n')
        self.assertEqual(self.run_scan()[0], 1)

    def test_unknown_keys_not_rejection(self):
        p = self.skill / 'SKILL.md'
        p.write_text(p.read_text().replace('name: sample', 'name: sample\nmodelInvocable: true'))
        self.assertEqual(self.run_scan()[0], 0)

    def test_missing_and_empty_input(self):
        self.assertEqual(self.run_scan(path=self.root / 'missing')[0], 2)
        empty = self.root / 'empty'; empty.mkdir()
        self.assertEqual(self.run_scan(path=empty)[0], 2)

    def test_mixed_missing_input(self):
        self.assertEqual(self.run_scan(str(self.root / 'missing'))[0], 2)

    def test_budget_is_opt_in_candidate(self):
        self.write(description='Review requested artifacts. ' * 30)
        self.assertFalse(any(f['id'] == 'T1' for f in self.run_scan()[1]['findings']))
        code, result = self.run_scan('--max-description', '500')
        self.assertEqual(code, 0)
        self.assertTrue(any(f['id'] == 'T1' and f['evidence'] == 'candidate' for f in result['findings']))
        self.assertEqual(self.run_scan('--max-description', '0')[0], 2)

    def test_fenced_examples_and_comments(self):
        self.write('````markdown\n```\nAlways run the full test suite.\n```\n````\n<!-- Never proceed without approval. -->\n')
        self.assertTrue(all(f.get('context') == 'example-or-comment' and f.get('confidence') == 'low' for f in self.run_scan()[1]['findings']))

    def test_real_instruction_after_fence(self):
        self.write('~~~\nExample\n~~~\nAlways run the full test suite.\n')
        result = self.run_scan()[1]
        self.assertTrue(any(f['id'] == 'M1' for f in result['findings']))
        self.assertTrue(all(f['evidence'] == 'candidate' for f in result['findings']))

    def test_chinese_coverage_honest(self):
        self.write('每次修改必须运行全部测试。\n')
        coverage = self.run_scan()[1]['coverage']
        self.assertEqual(coverage['heuristic_languages'], ['en'])
        self.assertFalse(coverage['behavior_tested'])

    def test_link_resolution_and_line(self):
        (self.skill / 'guide with space.md').write_text('Guide')
        self.write('[valid](guide%20with%20space.md)\n[missing](absent.md)\n')
        links = [f for f in self.run_scan()[1]['findings'] if f['id'] == 'C3']
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0]['line'], 6)

    def test_instruction_file(self):
        path = self.root / 'AGENTS.md'; path.write_text('Always run the full test suite.\n')
        code, result = self.run_scan(path=path)
        self.assertEqual(code, 0)
        self.assertTrue(any(f['id'] == 'M1' for f in result['findings']))

    def test_duplicate_input(self):
        result = self.run_scan(str(self.skill / 'SKILL.md'))[1]
        self.assertEqual(result['coverage']['files_scanned'], 1)

    def test_symlink_catalog_and_cycle(self):
        catalog = self.root / 'catalog'; catalog.mkdir()
        (catalog / 'linked').symlink_to(self.skill, target_is_directory=True)
        (catalog / 'again').symlink_to(self.skill, target_is_directory=True)
        (catalog / 'loop').symlink_to(catalog, target_is_directory=True)
        (catalog / 'broken').symlink_to(self.root / 'absent')
        code, result = self.run_scan(path=catalog)
        self.assertEqual(code, 0)
        self.assertEqual(result['coverage']['files_scanned'], 1)
        self.assertEqual({s['reason'] for s in result['coverage']['skipped']}, {'duplicate-or-cycle', 'broken-symlink'})

    def test_duplicate_yaml_keys(self):
        self.policy('policy:\n  allow_implicit_invocation: false\n  allow_implicit_invocation: true\n')
        code, result = self.run_scan('--host', 'codex')
        self.assertEqual(code, 1)
        self.assertEqual(result['files'][0]['invocation'], 'unknown')
        self.assertIn('Duplicate YAML key', result['findings'][0]['message'])
        p = self.skill / 'SKILL.md'
        p.write_text(p.read_text().replace('name: sample', 'name: sample\nname: other'))
        self.assertEqual(self.run_scan()[0], 1)

    def test_yaml_merge_override(self):
        self.policy('defaults: &defaults\n  allow_implicit_invocation: true\npolicy:\n  <<: *defaults\n  allow_implicit_invocation: false\n')
        code, result = self.run_scan('--host', 'codex')
        self.assertEqual(code, 0)
        self.assertEqual(result['files'][0]['invocation'], 'explicit-only')

    def test_normative_code_block(self):
        self.write('```text\nNever proceed without approval.\n```\nFollow the block above.\n')
        findings = self.run_scan()[1]['findings']
        self.assertTrue(any(f['id'] == 'M2' and f['confidence'] == 'low' for f in findings))

    def test_windows_path(self):
        self.write(r'Run C:\Users\alice\tools\build.cmd' + '\n')
        self.assertTrue(any(f['id'] == 'P3' for f in self.run_scan()[1]['findings']))

if __name__ == '__main__':
    unittest.main(verbosity=2)
