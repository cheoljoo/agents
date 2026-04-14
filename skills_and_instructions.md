# Skills & Instructions 통합 가이드

## 배경 / 문제 정의

AI 도구마다 커스텀 규칙을 주입하는 메커니즘이 다르다.

| 도구 | 지원 방식 | 읽는 파일 |
|------|-----------|-----------|
| **Copilot CLI** | Instructions + **Skills** | `.github/copilot-instructions.md`, `.github/skills/**/SKILL.md` |
| **VS Code Copilot** | Instructions **only** (Skills 미지원) | `.github/copilot-instructions.md`, `.vscode/settings.json`에 지정한 파일 |
| **Gemini CLI** | `GEMINI.md` + Skills | `.gemini/GEMINI.md`, `.gemini/skills/<name>/SKILL.md` |
| **Claude Code** | `CLAUDE.md` + Skills | `.claude/CLAUDE.md`, `.claude/skills/<name>/SKILL.md` |

**핵심 문제**:
- Skills를 VS Code용으로 Instructions로 변환하면 Copilot CLI가 동일 내용을 Instructions + Skills **두 번** 읽어 컨텍스트 낭비가 발생한다.
- Gemini/Claude는 각자 다른 경로(`GEMINI.md`, `CLAUDE.md`)를 사용해 도구마다 별도 파일을 유지해야 한다.

---

## 설계 원칙

1. **Single Source of Truth**: 모든 스킬 정의는 `.github/skills/<name>/SKILL.md` 에만 작성한다.
2. **전역 지침도 단일 소스**: `.github/copilot-instructions.md` 하나를 각 도구별 경로로 symlink한다.
3. **VS Code는 별도 경로에서 Instructions로 읽는다**: `.github/vscode-skills/` 는 Copilot CLI의 기본 스캔 경로(`*.instructions.md` glob)에 해당하지 않으므로 CLI가 자동 무시한다.
4. **settings.json은 merge 방식으로 갱신**: 다른 키를 덮어쓰지 않고 instructions 항목만 교체한다.
5. **`make skills-sync`로 자동 생성**: 수동으로 변환 파일을 관리하지 않는다.

---

## 디렉토리 구조

```
프로젝트 루트/
│
├── .github/
│   ├── copilot-instructions.md          ← ★ 전역 지침 소스 (직접 편집)
│   │
│   ├── skills/                          ← ★ 스킬 소스 (직접 편집)
│   │   ├── git-commit/
│   │   │   └── SKILL.md
│   │   ├── worklog-manager/
│   │   │   └── SKILL.md
│   │   ├── skill-sync-manager/
│   │   │   └── SKILL.md
│   │   └── coding-style-check/
│   │       ├── SKILL.md
│   │       └── references/              ← 스킬 전용 참조 파일 (선택)
│   │
│   └── vscode-skills/                   ← 자동 생성 (직접 편집 금지)
│       ├── git-commit.md                  → symlink → skills/git-commit/SKILL.md
│       ├── worklog-manager.md             → symlink → skills/worklog-manager/SKILL.md
│       ├── skill-sync-manager.md          → symlink → skills/skill-sync-manager/SKILL.md
│       └── coding-style-check.md          → symlink → skills/coding-style-check/SKILL.md
│
├── .gemini/                             ← 자동 생성 (직접 편집 금지)
│   ├── GEMINI.md  → ../.github/copilot-instructions.md
│   └── skills/    → ../.github/skills/
│
├── .claude/                             ← 자동 생성 (직접 편집 금지)
│   ├── CLAUDE.md  → ../.github/copilot-instructions.md
│   └── skills/    → ../.github/skills/
│
├── .vscode/
│   └── settings.json                    ← merge 방식으로 자동 갱신
│         (github.copilot.chat.codeGeneration.instructions 키만 교체)
│
└── scripts/
    ├── sync_skills.sh                   ← 동기화 메인 스크립트
    └── update_vscode_settings.py        ← settings.json merge 처리
```

---

## 각 도구별 읽기 경로

### Copilot CLI
```
.github/copilot-instructions.md       ← 항상 로드되는 전역 지침
.github/skills/<name>/SKILL.md        ← Skills (트리거 기반, 필요 시만 로드)
```
> `.github/vscode-skills/`는 `*.instructions.md` 패턴이 아니므로 자동 무시

### VS Code Copilot
```
.github/copilot-instructions.md       ← 항상 로드
.github/vscode-skills/<name>.md       ← settings.json에 지정 → Instructions로 인식
```
> `.github/skills/`는 VS Code가 직접 읽지 않음 (Skills 미지원)

### Gemini CLI
```
.gemini/GEMINI.md   → ../.github/copilot-instructions.md   ← 전역 지침
.gemini/skills/     → ../.github/skills/                   ← 스킬 목록
```

### Claude Code
```
.claude/CLAUDE.md   → ../.github/copilot-instructions.md   ← 전역 지침
.claude/skills/     → ../.github/skills/                   ← 스킬 목록
```

---

## skill-sync 동작 (`make skills-sync`)

### 실행 방법
```bash
make skills-sync
```

### `scripts/sync_skills.sh` 처리 흐름

```
.github/copilot-instructions.md
        ├─ symlink ──→  .gemini/GEMINI.md       (Gemini CLI 전역 지침)
        └─ symlink ──→  .claude/CLAUDE.md       (Claude Code 전역 지침)

.github/skills/   (디렉토리 전체)
        ├─ symlink ──→  .gemini/skills/          (Gemini CLI 스킬)
        └─ symlink ──→  .claude/skills/          (Claude Code 스킬)

.github/skills/<name>/SKILL.md   (개별 파일)
        └─ symlink ──→  .github/vscode-skills/<name>.md
                                │
                                └─ 경로 목록 merge ──→  .vscode/settings.json
                                   (update_vscode_settings.py)
```

### `scripts/update_vscode_settings.py` merge 규칙
- 기존 settings.json 읽기 → `.github/vscode-skills/` 접두사 항목만 제거 → 새 목록 추가
- **다른 설정 키(`editor.tabSize` 등)는 절대 건드리지 않음**
- 스킬이 삭제되면 해당 항목도 자동 제거됨

### 새 스킬 추가 시 절차
1. `.github/skills/<new-skill>/SKILL.md` 파일 생성
2. `make skills-sync` 실행
3. 4개 대상 모두 자동 갱신:
   - `.gemini/skills/` (symlink이므로 즉시 반영)
   - `.claude/skills/` (symlink이므로 즉시 반영)
   - `.github/vscode-skills/<new-skill>.md` (symlink 생성)
   - `.vscode/settings.json` (merge 갱신)

---

## SKILL.md 파일 형식

```markdown
---
name: skill-name
description: "트리거 문구 — 스킬 설명"
---

# 스킬: 제목

사용자가 **"트리거 문구"** 라고 입력하면 아래를 수행한다.

## 수행 절차
1. 단계 1
2. 단계 2
```

- `name`: Copilot CLI `/skills` 목록에 표시되는 이름
- `description`: 스킬 호출 트리거 문구 포함

---

## 파일별 편집 가능 여부

| 경로 | 편집 | 설명 |
|------|------|------|
| `.github/copilot-instructions.md` | ✅ 직접 편집 | 전역 지침 소스 |
| `.github/skills/<name>/SKILL.md` | ✅ 직접 편집 | 스킬 소스 |
| `.github/vscode-skills/` | ❌ 자동 생성 | symlink, sync으로만 갱신 |
| `.gemini/` | ❌ 자동 생성 | symlink, sync으로만 갱신 |
| `.claude/` | ❌ 자동 생성 | symlink, sync으로만 갱신 |
| `.vscode/settings.json` | ⚠️ 부분 허용 | instructions 외 키는 자유롭게 편집 가능 |

---

## 비교: 단일 파일 vs Skills 방식

| 항목 | 단일 파일 (GEMINI.md / CLAUDE.md) | Skills (`SKILL.md`) |
|------|------|------|
| 설정 간단 | ✅ | ❌ sync 스크립트 필요 |
| 트리거 기반 실행 | ❌ 항상 전체 로드 | ✅ 호출 시만 로드 |
| 메모리 효율 | ❌ 항상 전체 컨텍스트 점유 | ✅ 필요 시만 로드 |
| 여러 도구 호환 | ✅ 도구별 파일만 작성 | ✅ sync로 자동 배포 |
| 유지보수 | ❌ 파일 비대화 | ✅ 스킬별 독립 파일 |
| 파일 범위 지정 | ❌ | ✅ (applyTo glob 지원) |
