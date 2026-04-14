# 📝 작업 보고서

## [2026-04-14] AI 코딩 툴 Instruction/Skills 체계 문서 리뷰

### 1. 개요
`instructions.md` 및 `skills_and_instruct_ions.md` 두 핵심 문서를 리뷰하여 이 프로젝트의 AI 툴 설정 체계를 완전히 파악함.

### 2. 주요 내용 파악

#### instructions.md
- 툴별 파일 위치 비교 (Copilot, Gemini, Claude, Codex, Cursor)
- `AGENTS.md` (에이전트 레지스트리) vs `AGENT.md` (개별 에이전트 지침서) 역할 구분
- 중복 제거 전략 3가지: symlink, 참조 명시, 생성 스크립트(권장)
- 전역 vs 프로젝트 수준 분리 원칙

#### skills_and_instruct_ions.md
- **Single Source of Truth**: `.github/skills/<name>/SKILL.md` 하나만 작성
- `make skills-sync` → `.gemini/`, `.claude/`, `.github/vscode-skills/`, `.vscode/settings.json` 자동 갱신
- VS Code Copilot은 Skills 미지원 → `.github/vscode-skills/`에 symlink하여 Instructions로 읽힘
- `scripts/update_vscode_settings.py`가 `settings.json`의 instructions 항목만 merge 갱신 (다른 설정 보존)

### 3. 현재 프로젝트 구조와의 연계
- `.github/skills/` 하위에 `git-commit`, `worklog-manager`, `skill-sync-manager`, `coding-style-check` 스킬 정의
- `make skills-sync` 실행 시 `.gemini/skills/`, `.claude/skills/`, `.github/vscode-skills/` 자동 배포

---

## [2026-04-13] Gemini CLI 기술(Skill) 인식 오류 해결

## 1. 개요
Gemini CLI에서 프로젝트 내 커스텀 기술(Skill)이 인식되지 않는 문제를 분석하고 해결함.

## 2. 문제 원인
1. **디렉토리 명칭 오류**: Gemini CLI는 `.agents` (복수형) 또는 `.gemini` 디렉토리를 탐색하지만, 현재 프로젝트는 `.agent` (단수형)로 생성되어 있었음.
2. **필수 필드 누락**: `SKILL.md`의 YAML 프론트매터에 `name` 필드가 누락되어 기술이 등록되지 않음.

## 3. 조치 사항
1. `mv .agent .agents` 명령을 통해 디렉토리 이름 수정.
2. 각 `SKILL.md` 파일에 `name: git-commit`, `name: worklog-manager` 필드 추가.

## 4. 결과
- Gemini CLI가 `.agents/skills/` 하위의 기술을 정상적으로 인식함.
- `/skills list` 명령을 통해 확인 가능.
