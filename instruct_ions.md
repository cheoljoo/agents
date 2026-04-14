# AI 코딩 툴 Instruction 체계 완전 정리

> VSCode Copilot · Copilot CLI · Gemini CLI · Claude Code · OpenAI Codex · Cursor  
> 각 툴의 설정 파일 위치, 형식, 전역/프로젝트 분리 및 통합 전략 가이드

---

## 목차

1. [각 툴별 파일 위치 비교](#1-각-툴별-파일-위치-비교)
2. [각 툴 상세 설정법](#2-각-툴-상세-설정법)
   - [GitHub Copilot (VSCode + CLI)](#github-copilot-vscode--cli)
   - [Gemini CLI](#gemini-cli)
   - [Claude Code](#claude-code)
   - [OpenAI Codex](#openai-codex)
   - [Cursor](#cursor)
3. [Skills 저장 위치 상세](#3-skills-저장-위치-상세)
   - [Gemini CLI Skills](#gemini-cli-skills)
   - [GitHub Copilot Skills](#github-copilot-skills)
4. [AGENT.md vs AGENTS.md 완전 가이드](#4-agentmd-vs-agentsmd-완전-가이드)
5. [중복 제거 — 통합 전략](#5-중복-제거--통합-전략)
6. [권장 프로젝트 구조](#6-권장-프로젝트-구조)
7. [전역 vs 프로젝트 수준 분리 원칙](#7-전역-vs-프로젝트-수준-분리-원칙)
8. [즉시 적용 가이드](#8-즉시-적용-가이드)

---

## 1. 각 툴별 파일 위치 비교

| 툴 | 전역 (계정) | 프로젝트 | 서브디렉토리 | Agent / Skill |
|---|---|---|---|---|
| **GitHub Copilot (VSCode)** | `settings.json` 에 파일 경로 지정¹ | `.github/copilot-instructions.md` | `.github/instructions/*.md` (`applyTo` 지정) | `.github/skills/*/SKILL.md` |
| **GitHub Copilot CLI** | `~/.github/copilot-instructions.md` | `.github/copilot-instructions.md` | — | — |
| **Gemini CLI** | `~/.gemini/GEMINI.md` | `GEMINI.md` (루트) | 각 디렉토리의 `GEMINI.md` | `AGENTS.md`, `AGENT.md`, `~/.agents/skills/` |
| **Claude Code** | `~/.claude/CLAUDE.md` | `CLAUDE.md` (루트) | 각 서브디렉토리 `CLAUDE.md` | `AGENTS.md`, `AGENT.md` |
| **OpenAI Codex** | `~/.codex/AGENTS.md` | `AGENTS.md` | 서브디렉토리 `AGENTS.md` | `AGENTS.md` 내 정의 |
| **Cursor** | Cursor 설정 UI | `.cursorrules` 또는 `.cursor/rules/*.mdc` | `.cursor/rules/` | `.cursor/rules/*.mdc` |

> ¹ VSCode `settings.json`의 `github.copilot.chat.codeGeneration.instructions` 항목에 파일 경로 지정 필요

---

## 2. 각 툴 상세 설정법

### GitHub Copilot (VSCode + CLI)

#### 프로젝트 파일 구조

```
프로젝트/
├── .github/
│   ├── copilot-instructions.md        # 전체 프로젝트 지침
│   ├── instructions/
│   │   ├── coding-style.md            # applyTo: "**/*.py"
│   │   ├── testing.md                 # applyTo: "**/*.test.*"
│   │   └── review.md
│   └── skills/
│       ├── code-generation/SKILL.md
│       └── code-review/SKILL.md
```

#### `.github/instructions/*.md` 헤더 예시

```markdown
---
applyTo: "**/*.py"
---
# Python 코딩 규칙
- Type hints 필수 사용
- PEP 8 준수
```

#### VSCode `settings.json` 전역 설정

```json
{
  "github.copilot.chat.codeGeneration.instructions": [
    { "file": "${workspaceFolder}/.github/copilot-instructions.md" },
    { "text": "항상 사용자 언어에 맞춰 응답해주세요." }
  ]
}
```

#### 전역 파일 (`~/.github/copilot-instructions.md`)

CLI와 VSCode 모두 이 파일을 읽습니다. 개인 전역 규칙을 여기에 작성합니다.

```markdown
# 전역 Copilot 규칙
- 응답 언어: 사용자가 쓴 언어와 동일하게
- 코드 주석 및 변수명: 영어
- API 키, 시크릿 등 민감 정보 코드에 포함 금지
- Conventional Commits 스타일 커밋 메시지 (feat:, fix:, docs: 등)
```

---

### Gemini CLI

#### 파일 구조

```
~/.gemini/GEMINI.md           # 전역 (모든 프로젝트에 적용)
~/.agents/skills/             # 전역 사용자 정의 스킬 저장소
  └── my-skill/
      └── SKILL.md

프로젝트/
├── GEMINI.md                 # 프로젝트 루트 지침 (시스템 프롬프트보다 우선)
├── src/
│   └── GEMINI.md             # src 작업 시 추가 적용
├── AGENTS.md                 # 에이전트 레지스트리 (어떤 전문가가 있는지)
└── .agents/
    ├── security-auditor/
    │   └── AGENT.md          # 개별 에이전트 상세 정의
    └── doc-master/
        └── AGENT.md
```

#### `GEMINI.md` 우선순위와 역할

- **시스템 프롬프트보다 높은 우선순위** (Foundational Mandate)
- Gemini CLI 세션 시작 시 **자동 로드** (별도 호출 불필요)
- 프로젝트 전반의 **"헌법"** 역할 — 코딩 스타일, 금지사항, 강제 라이브러리 등

#### `GEMINI.md` 예시

```markdown
# Project Rules

## Tech Stack
- Language: Python with type hints
- Dependency: uv (pip 대신 `uv run` 사용)
- Test: pytest

## Conventions
- Commit: Conventional Commits 스타일
- Secret: .env 파일 내용 절대 노출 금지

## Sub-agents
복잡한 리팩토링이나 대량 파일 수정은 `generalist` sub-agent 활용
```

#### 전역 메모리 파일

Gemini CLI는 대화 중 학습한 내용을 `~/.gemini/GEMINI.md`에 자동 추가하기도 합니다.  
수동으로 편집하여 영구 규칙을 추가할 수 있습니다.

---

### Claude Code

#### 파일 구조

```
~/.claude/CLAUDE.md           # 전역 지침 (모든 프로젝트)
~/.claude/settings.json       # 전역 설정 (허용 툴, 권한 등)

프로젝트/
├── CLAUDE.md                 # 프로젝트 지침 (전역과 병합됨)
├── AGENTS.md                 # sub-agent 워크플로 정의
└── src/
    └── CLAUDE.md             # 서브디렉토리 추가 규칙
```

#### `CLAUDE.md` 예시

```markdown
# Project Instructions

## 개요
- 도메인: 자동차 임베디드 소프트웨어
- 코딩 표준: MISRA C:2012

## 규칙
- 외부 라이브러리 사용 금지 (표준 라이브러리만)
- 동적 메모리 할당 금지 (malloc, new) — MISRA C:2012 Rule 21.3
- 재귀 호출 금지
- 모든 함수 반환값 반드시 확인

## Skill 워크플로
작업 유형에 따라 `.github/skills/*/SKILL.md` 참조:
- 요구사항 분석 → `requirements-analysis/SKILL.md`
- 코드 생성 → `code-generation/SKILL.md`
- 코드 리뷰 → `code-review/SKILL.md`
```

#### `AGENTS.md` 예시 (Claude + OpenAI Codex 공용)

```markdown
# Sub-Agent Instructions

## code-reviewer
파일 변경 후 반드시 코드 리뷰 수행.
테스트 파일의 경우 커버리지 80% 이상 확인.

## test-writer
새 함수 작성 시 자동으로 단위 테스트 생성.
pytest 형식 사용, fixture 활용 권장.

## doc-writer
공개 API 변경 시 README.md 및 docstring 업데이트.
```

#### `~/.claude/settings.json` 예시

```json
{
  "permissions": {
    "allow": ["Bash", "Read", "Write", "Edit"],
    "deny": ["WebFetch"]
  }
}
```

---

### OpenAI Codex

#### 파일 구조

```
~/.codex/AGENTS.md            # 전역 agent 지침

프로젝트/
├── AGENTS.md                 # 프로젝트 agent 지침
└── 서브디렉토리/
    └── AGENTS.md             # 좁은 범위 agent 지침 (해당 디렉토리 작업 시 우선 적용)
```

#### `AGENTS.md` 예시

```markdown
# Agent Instructions

## 기본 규칙
- 작업 전 현재 디렉토리 구조 파악
- 변경 사항은 반드시 테스트 후 커밋
- 커밋 메시지: Conventional Commits 형식

## 금지 사항
- 환경 변수 파일(.env) 수정 금지
- 프로덕션 DB 직접 접근 금지

## 테스트
- 변경 후 `npm test` 또는 `pytest` 실행 필수
```

---

### Cursor

#### 파일 구조

```
프로젝트/
├── .cursorrules                    # 레거시 방식 (여전히 지원)
└── .cursor/
    └── rules/
        ├── global.mdc              # alwaysApply: true — 항상 적용
        ├── python.mdc              # globs: ["**/*.py"]
        ├── testing.mdc             # 테스트 파일용
        └── review.mdc              # 코드 리뷰 규칙
```

#### `.cursor/rules/python.mdc` 예시

```markdown
---
description: Python 코딩 규칙
globs: ["**/*.py"]
alwaysApply: false
---
# Python Rules
- Type hints 필수
- PEP 8 준수
- `uv run` 으로 실행
- docstring: Google 스타일
```

#### `.cursor/rules/global.mdc` 예시

```markdown
---
description: 전역 규칙
alwaysApply: true
---
# 전역 규칙
- 응답 언어: 사용자 언어와 동일
- 코드 주석: 영어
- 시크릿 코드 포함 금지
```

---

## 3. Skills 저장 위치 상세

### Gemini CLI Skills

Gemini CLI의 스킬은 **빌트인 스킬**과 **사용자 정의 스킬**로 나뉩니다.

#### 스킬 종류별 저장 위치

| 종류 | 경로 | 설명 |
|---|---|---|
| **사용자 정의 (전역)** | `~/.agents/skills/<이름>/SKILL.md` | 모든 프로젝트에서 자동 인식 ✅ |
| **사용자 정의 (프로젝트)** | `프로젝트/.agents/skills/<이름>/SKILL.md` | 해당 프로젝트에서만 사용 |
| **빌트인** | npm 전역 설치 경로 내 `bundle/builtin/` | CLI와 함께 제공, 수정 불가 |

#### 전역 사용자 정의 스킬 구조

```
~/.agents/
└── skills/
    ├── code-reviewer/
    │   └── SKILL.md          # 코드 리뷰 전용 스킬
    ├── test-writer/
    │   └── SKILL.md          # 테스트 작성 전용 스킬
    └── doc-generator/
        └── SKILL.md          # 문서 생성 전용 스킬
```

#### `SKILL.md` 예시

```markdown
# Code Reviewer Skill

## 목적
변경된 코드의 품질을 검토하고 개선점을 제안합니다.

## 수행 절차
1. `git diff` 로 변경 사항 확인
2. 코딩 컨벤션 위반 여부 점검
3. 잠재적 버그 및 보안 취약점 탐지
4. 개선 제안 목록 작성

## 완료 조건
- 모든 변경 파일 검토 완료
- 심각도별 (Critical / Warning / Info) 분류 보고서 작성
```

> 💡 새 스킬을 만들려면 Gemini CLI에서 `activate_skill(name="skill-creator")`를 호출하면 스킬 제작 가이드를 받을 수 있습니다.

---

### GitHub Copilot Skills

GitHub Copilot의 스킬은 `.github/skills/` 디렉토리에 저장합니다.

```
프로젝트/
└── .github/
    └── skills/
        ├── code-generation/
        │   └── SKILL.md
        ├── code-review/
        │   └── SKILL.md
        └── requirements-analysis/
            └── SKILL.md
```

`copilot-instructions.md`에서 작업 유형별로 스킬을 참조합니다:

```markdown
## Skill 워크플로
작업 유형에 따라 적절한 스킬을 읽고 따르세요:
- 요구사항 분석 → `.github/skills/requirements-analysis/SKILL.md`
- 코드 생성 → `.github/skills/code-generation/SKILL.md`
- 코드 리뷰 → `.github/skills/code-review/SKILL.md`
```

---

## 4. AGENT.md vs AGENTS.md 완전 가이드

이 파일들은 Gemini CLI · Claude Code · OpenAI Codex에서 **커스텀 서브 에이전트**를 정의하고 관리하는 핵심 파일입니다.  
복잡한 작업을 전문화된 에이전트들에게 위임하여 효율성과 정확도를 높일 수 있습니다.

### 역할 구분

| 파일 | 역할 | 비유 |
|---|---|---|
| `AGENTS.md` | 에이전트 **레지스트리** — 어떤 전문가들이 있고 어디에 있는지 | 회사 조직도 |
| `AGENT.md` | 개별 에이전트의 **지침서** — 페르소나, 목표, 도구, 세부 규칙 | 직무 기술서 (JD) |

### 전체 구조 예시

```
프로젝트/
├── AGENTS.md                       # 에이전트 목록 (레지스트리)
└── .agents/
    ├── security-auditor/
    │   └── AGENT.md                # 보안 감사 전문가 정의
    └── doc-master/
        └── AGENT.md                # 문서화 전문가 정의
```

### `AGENTS.md` — 에이전트 레지스트리

메인 에이전트에게 "우리 팀에 어떤 전문가들이 있고, 어디에 있는지"를 알려주는 파일입니다.

```markdown
# 프로젝트 커스텀 에이전트 목록

이 프로젝트에서 사용할 수 있는 특화된 서브 에이전트들입니다.

- [security-auditor](./.agents/security-auditor/AGENT.md): 코드 내 보안 취약점 점검 및
  민감 정보(API Key 등) 노출 여부를 전담합니다.
- [doc-master](./.agents/doc-master/AGENT.md): README, API 명세서, 인라인 주석 등
  모든 기술 문서의 품질 관리 및 최신화를 담당합니다.
```

> `[에이전트 이름](경로): 설명` 형식으로 작성하면 메인 에이전트가 상황에 맞는 전문가를 자동으로 선택합니다.

### `AGENT.md` — 개별 에이전트 지침서

각 서브 에이전트의 페르소나, 목표, 세부 규칙을 정의합니다.

**예시: `.agents/security-auditor/AGENT.md`**

```markdown
# 보안 감사 에이전트 (Security Auditor)

당신은 시니어 보안 엔지니어입니다.
이 프로젝트의 코드 변경 사항에서 보안 위협을 찾아내는 것이 목표입니다.

## 주요 임무
1. 하드코딩된 패스워드, API Key, 인증 토큰이 있는지 `grep_search`로 철저히 검사
2. `.env` 파일이나 `.git` 설정이 실수로 커밋 대상에 포함되지 않았는지 확인
3. 의존성 라이브러리(package.json 등)에서 알려진 취약점 점검 (`npm audit` 등 실행)

## 준수 사항
- 보안 결함 발견 시 즉시 작업을 중단하고 사용자에게 보고
- 수정 제안 시 반드시 보안 베스트 프랙티스를 근거로 제시
- 심각도를 Critical / High / Medium / Low 로 분류하여 보고
```

**예시: `.agents/doc-master/AGENT.md`**

```markdown
# 문서화 전문가 에이전트 (Doc Master)

당신은 테크니컬 라이터입니다.
이 프로젝트의 모든 기술 문서를 최신 상태로 유지하는 것이 목표입니다.

## 주요 임무
1. 공개 API 변경 시 README.md 업데이트
2. 새 함수/클래스에 docstring 작성 (Google 스타일)
3. CHANGELOG.md에 변경 내역 추가

## 금지 사항
- 코드 로직 변경 금지 (문서만 수정)
- 기존 문서 삭제 금지 (업데이트만 허용)
```

### 에이전트 작동 흐름

```
사용자: "내 프로젝트에 보안 문제가 없는지 확인해줘"
    │
    ▼
메인 에이전트: AGENTS.md 읽기
    │  → security-auditor가 적합함을 판단
    ▼
security-auditor 호출
    │  → AGENT.md 지침에 따라 보안 점검 수행
    │  → grep_search, npm audit 등 도구 실행
    ▼
결과 요약 → 메인 에이전트 → 사용자에게 최종 답변
```

### 언제 사용하나?

| 상황 | 사용할 파일 |
|---|---|
| 프로젝트에 새 전문가 에이전트 추가 | `AGENTS.md` 에 항목 추가 |
| 특정 전문가의 행동 방식 상세 정의 | `AGENT.md` 작성 |
| 메인 에이전트에게 팀 구성 알리기 | `AGENTS.md` |
| 에이전트의 금지사항, 도구, 절차 정의 | `AGENT.md` |

> 💡 **장점**: 프로젝트가 커질수록 메인 에이전트의 컨텍스트 부하를 줄이면서 정교한 작업을 수행할 수 있습니다.

---

## 5. 중복 제거 — 통합 전략

여러 툴에서 동일한 내용을 반복 작성하는 문제를 해결하는 전략입니다.

### 전략 A: 심볼릭 링크

공통 파일을 하나 작성하고 각 툴 파일을 심볼릭 링크로 연결합니다.

```bash
# 공통 파일 작성
mkdir -p .ai
cat > .ai/common-rules.md << 'EOF'
# 공통 규칙
- 응답 언어: 사용자 언어에 맞춤
- 코드 주석/변수명: 영어
- 시크릿/API 키 코드 포함 금지
- Conventional Commits 커밋 메시지
EOF

# 각 툴 파일에서 심볼릭 링크
ln -sf .ai/common-rules.md CLAUDE.md
ln -sf .ai/common-rules.md GEMINI.md
ln -sf .ai/common-rules.md AGENTS.md
```

> ⚠️ 일부 툴은 심볼릭 링크를 지원하지 않을 수 있으므로 확인 필요

---

### 전략 B: 툴별 파일에서 공통 파일 참조 명시

```markdown
# CLAUDE.md

> 📋 공통 규칙은 `.ai/common-rules.md` 참조

## Claude 전용 규칙
- TodoWrite 툴로 작업 목록 추적
- Bash 명령 실행 전 사용자 확인 요청
```

---

### 전략 C: 생성 스크립트 (⭐ 권장)

단일 소스에서 모든 툴의 설정 파일을 자동으로 생성합니다.

```bash
#!/bin/bash
# .ai/generate-configs.sh

COMMON=".ai/common-rules.md"
SKILLS=".ai/skills"
AGENTS=".ai/agents.md"

echo "🔄 AI 설정 파일 생성 중..."

# Claude Code
cat "$COMMON" .ai/claude-specific.md > CLAUDE.md
echo "✅ CLAUDE.md 생성"

# Gemini CLI
cat "$COMMON" .ai/gemini-specific.md > GEMINI.md
echo "✅ GEMINI.md 생성"

# GitHub Copilot
cat "$COMMON" .ai/copilot-specific.md > .github/copilot-instructions.md
echo "✅ .github/copilot-instructions.md 생성"

# AGENTS (Claude + Codex + Gemini 공용)
cp "$AGENTS" AGENTS.md
echo "✅ AGENTS.md 생성"

echo "🎉 완료!"
```

```bash
chmod +x .ai/generate-configs.sh
.ai/generate-configs.sh
```

---

## 6. 권장 프로젝트 구조

모든 툴을 지원하는 통합 프로젝트 구조입니다.

```
프로젝트/
│
├── .ai/                              # 단일 진실 소스 (모든 툴 공통)
│   ├── common-rules.md               # 공통 핵심 규칙
│   ├── claude-specific.md            # Claude 전용 추가 규칙
│   ├── gemini-specific.md            # Gemini 전용 추가 규칙
│   ├── copilot-specific.md           # Copilot 전용 추가 규칙
│   ├── agents.md                     # Sub-agent 공통 정의 소스
│   └── generate-configs.sh           # 설정 파일 자동 생성 스크립트
│
├── CLAUDE.md                         # Claude Code용 (generated)
├── GEMINI.md                         # Gemini CLI용 (generated)
├── AGENTS.md                         # Claude / Codex / Gemini 에이전트 레지스트리 (generated)
│
├── .agents/                          # 개별 에이전트 정의 (Gemini CLI · Claude)
│   ├── security-auditor/
│   │   └── AGENT.md
│   ├── doc-master/
│   │   └── AGENT.md
│   └── skills/                       # 프로젝트 전용 스킬 (Gemini CLI)
│       ├── code-review/
│       │   └── SKILL.md
│       └── test-writer/
│           └── SKILL.md
│
├── .github/
│   ├── copilot-instructions.md       # GitHub Copilot용 (generated)
│   ├── instructions/
│   │   ├── python.md                 # applyTo: "**/*.py"
│   │   ├── testing.md                # applyTo: "**/*.test.*"
│   │   └── docs.md                   # applyTo: "**/*.md"
│   └── skills/                       # GitHub Copilot 전용 스킬
│       ├── code-generation/SKILL.md
│       ├── code-review/SKILL.md
│       └── requirements-analysis/SKILL.md
│
└── .cursor/
    └── rules/
        ├── global.mdc                # alwaysApply: true
        └── language-specific.mdc
```

### 전역 스킬 디렉토리 (Gemini CLI)

```
~/.agents/
└── skills/
    ├── code-reviewer/SKILL.md        # 모든 프로젝트에서 사용 가능
    ├── test-writer/SKILL.md
    └── doc-generator/SKILL.md
```

---

## 7. 전역 vs 프로젝트 수준 분리 원칙

| 전역 (계정)에 넣을 것 | 프로젝트에 넣을 것 |
|---|---|
| 응답 언어 설정 | 프로젝트 기술 스택 (Python, Node 등) |
| 개인 코딩 스타일 선호 | 도메인 규칙 (MISRA, AUTOSAR 등) |
| 보안 금지사항 (시크릿 노출 등) | 파일 경로, 서비스 URL |
| 공통 커밋 컨벤션 | 프로젝트별 테스트 명령어 |
| 사용 금지 패턴 | Skill 워크플로 정의 |
| 개인 선호 언어/프레임워크 | 아키텍처 제약 조건 |

### 전역 파일 위치 요약

```
~/.github/copilot-instructions.md   # Copilot CLI + VSCode Copilot
~/.gemini/GEMINI.md                 # Gemini CLI 전역 지침
~/.agents/skills/                   # Gemini CLI 전역 스킬
~/.claude/CLAUDE.md                 # Claude Code
~/.codex/AGENTS.md                  # OpenAI Codex
```

---

## 8. 즉시 적용 가이드

### Step 1: 전역 공통 규칙 설정

```bash
# Copilot CLI
mkdir -p ~/.github
cat > ~/.github/copilot-instructions.md << 'EOF'
# 전역 공통 규칙
- 응답은 사용자가 쓴 언어와 동일하게 (한국어 질문 → 한국어 답변)
- 코드 주석, 변수명, 함수명은 영어로
- API 키, 시크릿, 패스워드를 코드에 포함하지 않음
- 커밋 메시지: Conventional Commits 형식 (feat:, fix:, docs: 등)
- git commit은 직접 하지 않고 사용자가 직접 처리
EOF

# Claude Code
mkdir -p ~/.claude
cat > ~/.claude/CLAUDE.md << 'EOF'
# 전역 Claude 규칙
- 응답은 사용자가 쓴 언어와 동일하게
- 코드 주석, 변수명: 영어
- 시크릿/API 키 코드 포함 금지
- 작업 전 TodoWrite로 계획 수립
EOF

# Gemini CLI (이미 있으면 추가)
mkdir -p ~/.gemini
cat >> ~/.gemini/GEMINI.md << 'EOF'

## 전역 규칙
- 응답 언어: 사용자 언어에 맞춤
- 코드 주석/변수명: 영어
- 시크릿 노출 절대 금지
EOF
```

### Step 2: 전역 Gemini CLI 스킬 설정

```bash
# 전역 스킬 디렉토리 생성
mkdir -p ~/.agents/skills/code-reviewer

cat > ~/.agents/skills/code-reviewer/SKILL.md << 'EOF'
# Code Reviewer Skill

## 목적
변경된 코드의 품질을 검토하고 개선점을 제안합니다.

## 수행 절차
1. `git diff` 로 변경 사항 확인
2. 코딩 컨벤션 위반 여부 점검
3. 잠재적 버그 및 보안 취약점 탐지
4. 심각도별 (Critical / Warning / Info) 보고서 작성
EOF
```

### Step 3: 프로젝트에 통합 구조 생성

```bash
#!/bin/bash
# 새 프로젝트에서 실행

mkdir -p .ai/skills .github/instructions .github/skills .cursor/rules
mkdir -p .agents/security-auditor .agents/doc-master .agents/skills/code-review

# 공통 규칙 파일 작성
cat > .ai/common-rules.md << 'EOF'
# 공통 프로젝트 규칙
## Tech Stack
- (여기에 프로젝트 기술 스택 기입)

## Conventions
- 커밋: Conventional Commits
- 테스트: 변경 후 반드시 실행
EOF

# 각 툴 설정 파일 생성
cp .ai/common-rules.md CLAUDE.md
cp .ai/common-rules.md GEMINI.md
cp .ai/common-rules.md .github/copilot-instructions.md

# AGENTS.md (에이전트 레지스트리) 생성
cat > AGENTS.md << 'EOF'
# 프로젝트 에이전트 목록

- [security-auditor](./.agents/security-auditor/AGENT.md): 보안 취약점 및 민감 정보 노출 점검
- [doc-master](./.agents/doc-master/AGENT.md): 기술 문서 품질 관리 및 최신화
EOF

echo "✅ AI 설정 파일 생성 완료"
```

### Step 4: `.gitignore`에서 민감 설정 제외

```gitignore
# AI 툴 로컬 설정 (전역 파일은 저장소에 포함하지 않음)
.ai/local-*.md
```

---

## 참고 링크

| 툴 | 공식 문서 |
|---|---|
| GitHub Copilot Instructions | https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot |
| Gemini CLI | https://github.com/google-gemini/gemini-cli |
| Claude Code | https://docs.anthropic.com/en/docs/claude-code |
| OpenAI Codex (AGENTS.md) | https://platform.openai.com/docs/codex |
| Cursor Rules | https://docs.cursor.com/context/rules-for-ai |


## 의견
- 일을 분업화 하는 것이 좋을 듯!
  - 분업을 했는데도 일을 하다보면 어떤 일이 계속 커지는 것이 있을 것이다. 이것이 비합리적이면 이 일을 다시 나누어 agent를 따로 두는 것이 좋을 것이다.
- 무엇보다 일들을 나누어주고 그를 manage하는 orchestrator의 역할을 하는 것을 main.py로 하는지 아니면 cmux를 써봐서 claude에서는 어떻게 이를 잘 조율하는지를 알아야 할 것으로 보인다. 

