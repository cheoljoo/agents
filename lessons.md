# 💡 교훈 (Lessons Learned)

## 2026-04-14 — AI 툴별 Skills vs Instructions 차이
- **VS Code Copilot은 Skills 미지원**: Copilot CLI는 `.github/skills/*/SKILL.md`를 트리거 기반으로 읽지만, VS Code Copilot은 Instructions만 지원한다. 따라서 `.github/vscode-skills/`에 symlink를 만들어 `settings.json`에서 Instructions로 등록해야 VS Code에서도 스킬 내용이 반영된다.
- **Single Source of Truth 원칙**: 스킬을 여러 도구(Gemini, Claude, Copilot)에서 공유할 때 각 도구 경로에 별도 파일을 만들지 않고, `.github/skills/`를 단일 소스로 두고 symlink로 배포하는 것이 유지보수에 유리하다.
- **settings.json merge 방식**: `update_vscode_settings.py`는 `instructions` 항목만 교체하고 `editor.tabSize` 등 다른 설정은 건드리지 않는다. 직접 수정 시 이 패턴을 따라야 한다.

## 2026-04-13 — Gemini CLI 기술 인식 규칙
- **디렉토리 이름**: 기술(Skill)을 프로젝트 로컬에 저장할 때는 반드시 `.agents/skills/` 또는 `.gemini/skills/` (복수형) 디렉토리를 사용해야 함.
- **YAML 필수값**: `SKILL.md` 상단 YAML 설정에는 `name`과 `description`이 모두 포함되어야 기술이 활성화됨.
