# KOSPI50 Multi-Agent Data Pipeline

이 프로젝트는 `uv`를 활용하여 KOSPI50 종목의 주가 및 재무 데이터를 자동으로 수집하고 검증하는 **멀티 에이전트 오케스트레이션** 시스템입니다.

## 🚀 주요 특징

- **자동화된 워크플로우**: Orchestrator(Manager)가 하위 에이전트들의 실행 순서와 상태를 제어합니다.
- **역할 분담 (Separation of Concerns)**: 수집(주가/재무)과 검증(품질 관리) 에이전트를 분리하여 유지보수성을 높였습니다.
- **안전한 실행**: `uv`를 사용하여 독립적인 가상 환경에서 의존성 충돌 없이 실행됩니다.

## 🏗 시스템 구조

1.  **Orchestrator (`main.py`)**: 전체 워크플로우를 관리하며, 에이전트 간의 통신 및 최종 피드백을 제공합니다.
2.  **Daily Stock Agent (`agents/daily_stock`)**: `FinanceDataReader`를 통해 일일 OHLCV, 10개월 이동평균 등을 수집합니다.
3.  **Fundamental Agent (`agents/fundamentals`)**: PER, PBR, 시가총액(Marcap) 등 기업 가치 지표를 수집합니다.
4.  **Validation Agent (`agents/validator`)**: 수집된 데이터의 정합성(누락, 불일치 등)을 검증하고 보고서를 작성합니다.

## 🛠 실행 방법

모든 에이전트를 한 번에 실행하려면 아래 명령어를 사용하세요.

```bash
uv run main.py
```

## 📂 출력 결과

- `data/daily/*.csv`: 종목별 주가 데이터
- `data/fundamentals/*.csv`: 종목별 재무 지표 데이터
- `data/validation_report.txt`: 최종 검증 결과 보고서

## 📈 투자 분석 위원회 (Investment Committee) - KOSPI Top 10

KOSPI 시가총액 상위 10개 종목에 대해 기술적, 기본적, 정성적 분석을 수행하여 최종 투자 의견을 도출하는 시스템입니다.

### 실행 방법
```bash
uv run investment/main.py
```

### 구성 에이전트
1. **Quant Agent**: 이동평균 교차 등 기술적 지표 분석 (Bullish/Bearish)
2. **Fundamental Agent**: PER/PBR 기반 밸류에이션 분석 (Undervalued/Overvalued)
3. **News Agent**: 뉴스 심리 분석 (Positive/Neutral)
4. **Manager Agent**: 위 세 에이전트의 의견을 종합하여 최종 `Buy/Hold/Sell` 결정

---

## 🌟 확장 제안: AI 기반 멀티 에이전트 (Future Roadmap)

단순 스크립트 실행을 넘어, LLM(Large Language Model)을 도입하여 더 강력한 피드백과 완성도 높은 솔루션을 얻을 수 있는 시나리오입니다.

### 1. 자가 치유(Self-Healing) 코드 에이전트
에러 발생 시 사람이 개입하지 않고 시스템이 스스로 코드를 수정합니다.
- **Agent 1 (Coder)**: 기능을 구현하고 실행합니다.
- **Agent 2 (Debugger)**: 에러 로그를 분석하여 AI에게 해결책을 묻고 코드를 수정합니다.
- **Agent 3 (Reviewer)**: 수정된 코드가 보안 및 스타일 가이드를 준수하는지 최종 승인합니다.

### 2. 투자 전략 위원회 (Investment Committee)
데이터 수집을 넘어 다각도 분석을 통한 의사결정을 내립니다.
- **Agent 1 (Quant)**: 이동평균, 거래량 등 기술적 지표를 분석합니다.
- **Agent 2 (Fundamentalist)**: 재무 제표와 밸류에이션을 분석합니다.
- **Agent 3 (News Analyst)**: 실시간 뉴스 및 산업 동향(정성 데이터)을 분석합니다.
- **Agent 4 (Manager)**: 에이전트 간의 토론을 주재하여 최종 투자 보고서를 작성합니다.

### 3. 자동 문서화 및 QA (Doc & QA)
프로젝트의 생명 주기를 자동으로 관리합니다.
- **Agent 1 (Developer)**: 코드 변경 사항을 적용합니다.
- **Agent 2 (Documenter)**: 코드를 분석하여 `README.md` 및 API 명세서를 자동 업데이트합니다.
- **Agent 3 (Tester)**: 변경된 로직에 대한 테스트 케이스를 생성하고 엣지 케이스를 검증합니다.

## 🛠 추천 멀티 에이전트 프레임워크

더 고도화된 에이전트 시스템 구축을 위해 다음 도구들을 추천합니다:

- **LangGraph**: 복잡한 상태 관리와 순환형(Cyclic) 에이전트 워크플로우 구축에 최적화되어 있습니다.
- **CrewAI**: 역할 기반(Role-based) 에이전트들이 협업하여 목표를 달성하는 구조를 쉽게 만들 수 있습니다.
---

## 🤖 Gemini CLI Skills & Project Management

이 프로젝트는 Gemini CLI의 **커스텀 기술(Skills)**을 활용하여 작업 로그 관리 및 개발 표준을 자동화합니다.

### 🛠 구성된 기술
1. **git-commit**: Git 커밋 메시지 작성 규칙을 준수하도록 가이드합니다.
2. **worklog-manager**: "일을 정리 해주세요" 명령으로 `README.md`, `report.md`, `worklog.md`, `lessons.md`, `data/worklog.json`을 자동 업데이트합니다.

### 📂 기술 저장 위치
- `.agents/skills/`: 프로젝트 전용 기술(Skills)이 저장되는 디렉토리입니다. `SKILL.md` 파일을 통해 정의됩니다.

### 📝 작업 관리 파일
- `worklog.md`: 월별/일별 상세 작업 내역 (인간 가독용)
- `data/worklog.json`: 분석용 구조화 데이터
- `report.md`: 주요 분석 결과 및 기술적 의사결정 기록
- `lessons.md`: 개발 과정에서 얻은 주요 교훈 및 해결책
- `mm.md`: 커밋 메시지 및 작업 요약 초안
