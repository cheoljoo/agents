#!/usr/bin/env python3
"""
Update .vscode/settings.json by merging the
github.copilot.chat.codeGeneration.instructions list
without overwriting other existing settings.

Usage:
    python3 scripts/update_vscode_settings.py \
        --settings .vscode/settings.json \
        --vscode-skills-dir .github/vscode-skills
"""

import argparse
import json
import os
import sys


def load_settings(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Warning: could not parse {path}: {e}. Starting fresh.", file=sys.stderr)
    return {}


def collect_skill_entries(vscode_skills_dir: str) -> list[dict]:
    """Return sorted list of {file: ...} entries for all *.md in vscode-skills/."""
    if not os.path.isdir(vscode_skills_dir):
        print(f"Warning: {vscode_skills_dir} not found.", file=sys.stderr)
        return []
    entries = []
    for name in sorted(os.listdir(vscode_skills_dir)):
        if name.endswith(".md"):
            entries.append({"file": f"{vscode_skills_dir}/{name}"})
    return entries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", default=".vscode/settings.json")
    parser.add_argument("--vscode-skills-dir", default=".github/vscode-skills")
    args = parser.parse_args()

    settings = load_settings(args.settings)
    new_entries = collect_skill_entries(args.vscode_skills_dir)

    key = "github.copilot.chat.codeGeneration.instructions"

    # Merge: keep existing entries that are NOT in our managed vscode-skills dir,
    # then replace with freshly scanned list for that dir.
    existing = settings.get(key, [])
    managed_prefix = args.vscode_skills_dir.rstrip("/") + "/"
    kept = [e for e in existing if not e.get("file", "").startswith(managed_prefix)]

    settings[key] = kept + new_entries

    os.makedirs(os.path.dirname(args.settings) or ".", exist_ok=True)
    with open(args.settings, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Updated {args.settings}  ({len(kept)} kept + {len(new_entries)} skill entries)")


if __name__ == "__main__":
    main()
