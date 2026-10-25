#!/usr/bin/env python3
"""Check release structure and provenance references, not UI/model quality.

Python 3 standard library only. The skill itself has no Python dependency.
"""

import argparse
import json
from pathlib import Path
import re
import struct
import sys


REQUIRED = (
    "README.md", "LICENSE", "VERSION", "UI_PROFILE.example.md",
    "CONTRIBUTING.md", "skills/brief-to-ui/SKILL.md",
    "skills/brief-to-ui/LICENSE.txt", "skills/brief-to-ui/agents/openai.yaml",
    "skills/brief-to-ui/references/collaboration.md",
    "skills/brief-to-ui/references/admin-patterns.md",
    "skills/brief-to-ui/references/profiles.md",
    "skills/brief-to-ui/references/visual-foundations.md",
    "skills/brief-to-ui/references/interaction-patterns.md",
    "skills/brief-to-ui/references/resource-routing.md",
    "skills/brief-to-ui/references/sources.md",
    "examples/admin-home/README.md", "examples/admin-home/prompts.json",
    "examples/admin-home/a-preferred.png", "examples/admin-home/b-generic.png",
    "examples/admin-home/a2-cardless.png", "evals/README.md",
    "evals/scenarios.json", "scripts/validate_release.py",
)
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ".py"}
SECRET_PATTERNS = (
    r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    r"\bghp_[A-Za-z0-9]{20,}\b",
    r"\bgithub_pat_[A-Za-z0-9_]{30,}\b",
)


def check_links(file, root):
    """Check local Markdown file targets; external URLs and anchors are skipped."""
    errors = []
    content = file.read_text(encoding="utf-8")
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content):
        if target.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
            continue
        local = target.split("#", 1)[0].strip("<>")
        if not local:
            continue
        resolved = (file.parent / local).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{file.relative_to(root)}: local link escapes bundle: {target}")
            continue
        if not resolved.is_file():
            errors.append(f"{file.relative_to(root)}: missing local link: {target}")
    return errors


def png_size(file):
    with file.open("rb") as stream:
        header = stream.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError("Invalid PNG header")
    return struct.unpack(">II", header[16:24])


def validate_bundle(root):
    errors = []
    if not root.is_dir():
        return {"status": "fail", "errors": ["Bundle directory does not exist"]}
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"Missing release file: {relative}")

    files = sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts)
    markdown = [p for p in files if p.suffix == ".md"]
    for file in files:
        relative = file.relative_to(root)
        if file.is_symlink():
            errors.append(f"Symlink is not a standalone release asset: {relative}")
        if file.name == ".env" or file.suffix.lower() in {".pem", ".key"}:
            errors.append(f"Unexpected private configuration file: {relative}")
        if file.suffix not in TEXT_SUFFIXES and file.name not in {"LICENSE", "VERSION", ".gitignore"}:
            continue
        try:
            content = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"Text is not UTF-8: {relative}")
            continue
        if "\ufffd" in content:
            errors.append(f"Unicode replacement character: {relative}")
        if re.search(r"[A-Za-z]:[\\/]+Users[\\/]+[^\s\\/]+", content):
            errors.append(f"Absolute Windows user path in public text: {relative}")
        if any(re.search(pattern, content) for pattern in SECRET_PATTERNS):
            errors.append(f"Possible private key or access token: {relative}")
        if file.suffix == ".json":
            try:
                json.loads(content)
            except json.JSONDecodeError as exc:
                errors.append(f"Invalid JSON in {relative}: line {exc.lineno}")

    for file in markdown:
        errors.extend(check_links(file, root))

    skill = root / "skills/brief-to-ui/SKILL.md"
    if skill.is_file():
        content = skill.read_text(encoding="utf-8")
        front = re.match(r"\A---\r?\n(.*?)\r?\n---", content, re.S)
        if not front:
            errors.append("Skill frontmatter is missing")
        else:
            for field, value in (("name", "brief-to-ui"), ("license", "MIT")):
                if not re.search(rf"^{field}: {re.escape(value)}$", front.group(1), re.M):
                    errors.append(f"Skill frontmatter {field} must be {value}")
            if not re.search(r"^description: .+", front.group(1), re.M):
                errors.append("Skill description is missing")

    source = root / "skills/brief-to-ui/references/sources.md"
    if source.is_file():
        defined = set(re.findall(r"^\| (S\d+) \|", source.read_text(encoding="utf-8"), re.M))
        used = set()
        for file in markdown:
            for group in re.findall(r"\[(S\d+(?:, S\d+)*)\]", file.read_text(encoding="utf-8")):
                used.update(group.split(", "))
        for missing in sorted(used - defined):
            errors.append(f"Unresolved source identifier: {missing}")

    standalone_license = root / "skills/brief-to-ui/LICENSE.txt"
    if (root / "LICENSE").is_file() and standalone_license.is_file():
        if (root / "LICENSE").read_bytes() != standalone_license.read_bytes():
            errors.append("Standalone skill license differs from repository license")

    scenario_file = root / "evals/scenarios.json"
    scenario_count = 0
    if scenario_file.is_file():
        try:
            scenarios = json.loads(scenario_file.read_text(encoding="utf-8"))
            if not isinstance(scenarios, list):
                raise ValueError("Scenarios must be a list")
            scenario_count = len(scenarios)
            ids = [case.get("id") for case in scenarios if isinstance(case, dict)]
            if len(ids) != scenario_count or any(not value for value in ids) or len(set(ids)) != scenario_count:
                errors.append("Scenario IDs must be nonempty and unique")
            for case in scenarios:
                if not isinstance(case, dict):
                    errors.append("Scenario must be an object")
                    continue
                for field in ("context", "request", "success_criteria", "failure_signals"):
                    if not case.get(field):
                        errors.append(f"Scenario {case.get('id')}: missing {field}")
        except (ValueError, TypeError):
            errors.append("Scenario specifications could not be parsed")

    dimensions = {}
    for relative in REQUIRED:
        if relative.endswith(".png") and (root / relative).is_file():
            try:
                dimensions[relative] = png_size(root / relative)
            except (ValueError, OSError):
                errors.append(f"Invalid example image: {relative}")
    if len(set(dimensions.values())) > 1:
        errors.append("Example image dimensions differ; record or normalize the comparison")

    return {
        "status": "fail" if errors else "pass",
        "files_checked": len(files),
        "markdown_files_checked": len(markdown),
        "scenario_specs": scenario_count,
        "example_dimensions": dimensions,
        "model_behavior_evaluated": False,
        "ui_implementation_verified": False,
        "errors": errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    report = validate_bundle(args.root.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
