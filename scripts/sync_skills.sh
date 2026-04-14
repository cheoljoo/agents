#!/bin/bash
# sync_skills.sh
#
# Single source of truth: .github/skills/<name>/SKILL.md
#
# Synchronizes to:
#   1. .gemini/  (Gemini CLI)  — GEMINI.md + skills/ symlink
#   2. .claude/  (Claude Code) — CLAUDE.md + skills/ symlink
#   3. .github/vscode-skills/  (VS Code)  — per-skill symlinks
#   4. .vscode/settings.json   (VS Code)  — instructions list (merge, no overwrite)

SRC_SKILLS_DIR=".github/skills"
GLOBAL_INST=".github/copilot-instructions.md"

# ---------- 1. Gemini CLI ----------
rm -rf .gemini && mkdir -p .gemini
if [ -f "$GLOBAL_INST" ]; then
    ln -s "../$GLOBAL_INST" ".gemini/GEMINI.md"
fi
if [ -d "$SRC_SKILLS_DIR" ]; then
    ln -s "../$SRC_SKILLS_DIR" ".gemini/skills"
fi
echo "[1] Gemini CLI: .gemini/GEMINI.md + .gemini/skills -> $SRC_SKILLS_DIR"

# ---------- 2. Claude Code ----------
rm -rf .claude && mkdir -p .claude
if [ -f "$GLOBAL_INST" ]; then
    ln -s "../$GLOBAL_INST" ".claude/CLAUDE.md"
fi
if [ -d "$SRC_SKILLS_DIR" ]; then
    ln -s "../$SRC_SKILLS_DIR" ".claude/skills"
fi
echo "[2] Claude Code: .claude/CLAUDE.md + .claude/skills -> $SRC_SKILLS_DIR"

# ---------- 3. VS Code: per-skill symlinks ----------
VSCODE_SKILLS_DIR=".github/vscode-skills"
mkdir -p "$VSCODE_SKILLS_DIR"

# Remove stale symlinks for skills that no longer exist
for existing in "$VSCODE_SKILLS_DIR"/*.md; do
    [ -L "$existing" ] || continue
    skill_name=$(basename "$existing" .md)
    if [ ! -d "$SRC_SKILLS_DIR/$skill_name" ]; then
        rm "$existing"
        echo "[3] Removed stale symlink: $existing"
    fi
done

# Create/update symlinks for current skills
for skill_path in "$SRC_SKILLS_DIR"/*/; do
    [ -d "$skill_path" ] || continue
    skill_name=$(basename "$skill_path")
    skill_md="$skill_path/SKILL.md"
    [ -f "$skill_md" ] || continue
    target="$VSCODE_SKILLS_DIR/${skill_name}.md"
    expected="../../$SRC_SKILLS_DIR/$skill_name/SKILL.md"
    if [ -L "$target" ] && [ "$(readlink "$target")" = "$expected" ]; then
        : # already correct
    else
        ln -sf "$expected" "$target"
        echo "[3] VS Code symlink: $target"
    fi
done

# ---------- 4. .vscode/settings.json (merge) ----------
python3 scripts/update_vscode_settings.py \
    --settings ".vscode/settings.json" \
    --vscode-skills-dir "$VSCODE_SKILLS_DIR"

echo "Skill synchronization complete."
