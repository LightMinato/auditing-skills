#!/usr/bin/env python3
"""Read-only structural checks and heuristic candidates; no model execution."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML is required: python3 -m pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(2)

FAMILIES = [
    ('C4', re.compile('\\bbefore (?:every|each|any) (?:edit|change|task|response|request|modification)\\b[^.\\n]{0,60}\\bread\\b|\\bread (?:all of )?the following (?:files|docs|documents)?\\s*(?:first|before)\\b|\\b(?:always|first|start by) read(?:ing)?\\b[^.\\n]{0,80}\\b(?:before|prior to|first)\\b|\\b(?:must|should|need to) read\\b[^.\\n]{0,60}\\b(?:before|prior to)\\b|\\breview the (?:whole|entire) (?:repo|repository|project|codebase) (?:first|before)\\b|\\bunderstand the (?:entire|whole) (?:codebase|project) (?:first|before)\\b', 34)),
    ('M2', re.compile("\\b(?:never|do not|don't|must not)\\s+(?:ever\\s+)?(?:proceed|continue|start|make changes|edit|modify|run)\\b[^.\\n]{0,40}\\bwithout\\b[^.\\n]{0,30}\\b(?:approval|permission|confirmation|asking|consent)|\\balways (?:ask|check with|confirm with)\\b[^.\\n]{0,20}\\b(?:the )?(?:user|human)\\b|\\brequire(?:s|d)? (?:explicit )?(?:user )?(?:approval|permission|confirmation)\\b|\\bask for (?:my|user|human) (?:approval|permission|confirmation)\\b|\\bwait for (?:my|the user'?s?|human) (?:approval|confirmation|go-?ahead)\\b", 34)),
    ('M3', re.compile('\\bstop (?:and|to) (?:wait|report|check in|review|ask)\\b|\\b(?:report|check) back (?:to the user )?before (?:continuing|proceeding|implementing|finishing)\\b|\\bdo not continue until\\b|\\bwait for (?:my )?(?:review|feedback|response|sign-?off)\\b|\\bpause (?:and|for) (?:review|approval|confirmation)\\b|\\bafter the first (?:pass|implementation|draft)\\b[^.\\n]{0,40}\\b(?:stop|report|check in|pause)\\b', 34)),
    ('M1', re.compile("\\b(?:always|be sure to|make sure to|don'?t forget to)\\s+(?:write|add|run|create)\\s+(?:the\\s+)?(?:full\\s+|unit\\s+|integration\\s+|comprehensive\\s+|new\\s+)?tests?\\b|\\bwrite tests for (?:every|all|each)\\b|\\brun the (?:full|entire|whole) test suite\\b|\\bverify (?:your )?(?:work|changes) (?:by|with) (?:running )?tests\\b|\\btest(?:ing)? is (?:required|mandatory)\\b", 34)),
    ('M5', re.compile("\\bthink step[- ]by[- ]step\\b|\\brestate the (?:task|request|requirements|user'?s intent)\\b|\\bexplain your (?:reasoning|plan|approach) (?:first|before)\\b|\\bdescribe what you (?:will|are going to) do before\\b|\\bshow your (?:work|thinking)\\b|\\bfirst,? (?:make|create|write) a plan\\b[^.\\n]{0,40}\\b(?:wait|then share|and share)\\b", 34)),
    ('S2', re.compile('\\b(?:in this exact|in the following|in this specific) order\\b|\\bdo not skip (?:any )?steps?\\b|\\bfollow these steps (?:exactly|in order|without deviation)\\b|\\bmust be (?:done|performed|executed) in order\\b', 34)),
    ('S3', re.compile('^#{1,4}\\s+(?:what is\\b|introduction to\\b|background\\b|overview of\\b|primer on\\b)', 42)),
    ('P3', re.compile('(?<![\\w/])/(?:Users|home)/[\\w.-]+|\\b[A-Z]:\\\\\\\\', 32)),
]


def line_at(text, offset):
    return text.count("\n", 0, offset) + 1


def excluded_spans(text):
    spans = [(m.start(), m.end()) for m in re.finditer(r"<!--.*?-->", text, re.S)]
    opening = None
    pos = 0
    for line in text.splitlines(keepends=True):
        match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if match:
            fence, tail = match.groups()
            if opening is None:
                opening = (fence[0], len(fence), pos)
            elif fence[0] == opening[0] and len(fence) >= opening[1] and not tail.strip():
                spans.append((opening[2], pos + len(line)))
                opening = None
        pos += len(line)
    if opening:
        spans.append((opening[2], len(text)))
    return spans


def yaml_mapping(text):
    value = yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError("expected a YAML mapping")
    return value


def audit(path, host, max_description):
    text = path.read_text(encoding="utf-8-sig")
    findings = []
    def add(check, message, line=1, quote="", confirmed=False):
        findings.append(dict(id=check, file=str(path), line=line, quote=quote[:240],
                             evidence="structural" if confirmed else "candidate",
                             severity="error" if confirmed else "info", message=message))
    skill = path.name == "SKILL.md"
    info = dict(path=str(path), invocation="unknown", description_chars=0)
    body, offset = text, 0
    if skill:
        match = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
        if not match:
            add("P1", "Missing or unclosed YAML frontmatter.", confirmed=True)
            return info, findings
        body, offset = text[match.end():], match.end()
        try:
            fm = yaml_mapping(match.group(1))
        except (yaml.YAMLError, ValueError) as exc:
            add("P1", "Invalid YAML frontmatter: " + str(exc), confirmed=True)
            return info, findings
        for key in ("name", "description"):
            if not isinstance(fm.get(key), str) or not fm[key].strip():
                add("P1", key + " must be a nonempty string.", confirmed=True)
        name, desc = fm.get("name"), fm.get("description")
        if isinstance(name, str) and name != path.parent.name:
            add("P2", "Name differs from directory; verify the target host's naming rules.", quote=name)
        if isinstance(name, str) and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            add("P1", "Name differs from the portable lowercase-hyphen convention; host acceptance unverified.", quote=name)
        if host == "codex":
            info["invocation"] = "implicit-allowed"
            config = path.parent / "agents/openai.yaml"
            if config.exists():
                try:
                    data = yaml_mapping(config.read_text(encoding="utf-8-sig"))
                    policy = data.get("policy", {})
                    if not isinstance(policy, dict):
                        raise ValueError("policy must be a mapping")
                    allowed = policy.get("allow_implicit_invocation", True)
                    if not isinstance(allowed, bool):
                        raise ValueError("allow_implicit_invocation must be a boolean")
                    info["invocation"] = "implicit-allowed" if allowed else "explicit-only"
                except (yaml.YAMLError, ValueError) as exc:
                    info["invocation"] = "unknown"
                    add("P4", "Invalid agents/openai.yaml: " + str(exc), confirmed=True)
                    findings[-1]["file"] = str(config)
            if "disable-model-invocation" in fm:
                add("P4", "Frontmatter invocation flag is not interpreted as Codex policy; inspect agents/openai.yaml.")
        if isinstance(desc, str):
            info["description_chars"] = len(desc)
            if max_description is not None and len(desc) > max_description:
                add("T1", "Description exceeds the supplied review budget; actual host truncation is unverified.", quote=desc)
            if re.search(r"\b(?:always|whenever|any time|working with)\b", desc, re.I):
                add("T2", "Potentially broad trigger; test realistic neighboring requests.", quote=desc)
            if host == "codex" and info["invocation"] == "implicit-allowed" and re.search(r"explicitly invoked|invoked explicitly", desc, re.I):
                add("P4", "Description suggests explicit-only use but Codex policy allows implicit selection; inspect intent.", quote=desc)
        if len(body) > 12000 or len(body.splitlines()) > 200:
            add("C1", "Large entrypoint; assess whether conditional resources would help, not length alone.")
    spans = excluded_spans(body)
    for check, pattern in FAMILIES:
        for match in pattern.finditer(body):
            if any(a <= match.start() < b for a, b in spans):
                continue
            add(check, "Pattern candidate only: inspect scope, negation, examples and the failure this rule prevents.",
                line_at(text, offset + match.start()), match.group())
    for match in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", body):
        if any(a <= match.start() < b for a, b in spans):
            continue
        target = match.group(1).split("#")[0]
        if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or "<" in target:
            continue
        from urllib.parse import unquote
        if not (path.parent / unquote(target)).exists():
            add("C3", "Relative link target not found; verify that this is an actionable link, not an example.",
                line_at(text, offset + match.start()), target)
    return info, findings


def discover(paths):
    found = set()
    for raw in paths:
        path = Path(raw).expanduser()
        if not path.exists():
            raise ValueError("Input does not exist: " + str(path))
        if path.is_file():
            if path.name not in ("SKILL.md", "AGENTS.md", "CLAUDE.md"):
                raise ValueError("Expected SKILL.md, AGENTS.md or CLAUDE.md: " + str(path))
            found.add(path.resolve())
        elif (path / "SKILL.md").is_file():
            found.add((path / "SKILL.md").resolve())
        else:
            found.update(p.resolve() for p in path.rglob("SKILL.md")
                         if not any(part.startswith(".") and part != ".system" for part in p.relative_to(path).parts))
    if not found:
        raise ValueError("No skill or instruction files found in the supplied paths")
    return sorted(found)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Explicit skill, catalog, or instruction-file paths")
    parser.add_argument("--host", choices=("generic", "codex"), default="generic")
    parser.add_argument("--max-description", type=int, help="Optional review budget, not a claim about host limits")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_intermixed_args(argv)
    if args.max_description is not None and args.max_description < 1:
        parser.error("--max-description must be positive")
    try:
        paths = discover(args.paths)
        results = [audit(p, args.host, args.max_description) for p in paths]
    except (OSError, UnicodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    findings = [f for _, fs in results for f in fs]
    payload = dict(schema_version=1, host=args.host,
                   coverage=dict(files_scanned=len(paths),
                                 scope="Selected entrypoints only; references require semantic review",
                                 heuristic_languages=["en"],
                                 behavior_tested=False, host_loading_tested=False,
                                 description_budget=args.max_description),
                   files=[i for i, _ in results], findings=findings)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Scanned {len(paths)} entrypoints; host={args.host}. English heuristics only; no behavioral evaluation.")
        for f in findings:
            print(f"[{f['evidence']}] {f['id']} {f['file']}:{f['line']}: {f['message']}")
        print("No findings is not proof of a good skill. Review relevant references and realistic requests.")
    return 1 if any(f["evidence"] == "structural" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
