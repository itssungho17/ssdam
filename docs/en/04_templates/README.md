# SSDAM Agent Skills — 04_templates

## 1. Purpose

`04_templates`는 SSDAM 프레임워크의 **Agent Skills 컬렉션**이다.
각 스킬은 [Agent Skills 사양](https://agentskills.io)을 따르며, YAML frontmatter + Markdown body로 구성된 `SKILL.md`를 중심으로 AI 에이전트가 구조화된 YAML 문서를 자율적으로 생성하도록 안내한다.

## 2. Directory Structure

```text
04_templates/
├── README.md                                  ← This file
└── skills/                                    ← Agent Skills (AgentSkills spec)
    ├── user-input/                            ← Entry: raw idea → quest-seed.yaml
    │   ├── SKILL.md
    │   ├── assets/quest-seed.schema.yaml
    │   └── references/SSDAM.md
    ├── quest-plan/                            ← Quest: governance/stage-map/policies → quest-plan.yaml
    │   ├── SKILL.md
    │   ├── assets/quest-plan.schema.yaml
    │   └── references/
    │       ├── SSDAM.md
    │       └── governance-and-policies.md
    ├── stage-spec/                            ← Stage: contracts/evaluation/checkpoint → stage-spec.STG-XX.yaml
    │   ├── SKILL.md
    │   ├── assets/stage-spec.schema.yaml
    │   └── references/
    │       ├── SSDAM.md
    │       └── stage-design-rules.md
    └── execution-plan/                        ← Element: task decomposition → execution-plan.STG-XX.yaml
        ├── SKILL.md
        ├── assets/execution-plan.schema.yaml
        └── references/
            ├── SSDAM.md
            └── default-task-flow.md
```

각 스킬은 동일한 3계층 Progressive Disclosure 패턴을 따른다:

1. **Metadata** (~100 tokens): frontmatter의 `name`, `description` — 스킬 활성화 판단용
2. **Instructions** (< 500 lines): `SKILL.md` body — 절차, 규칙, Output Rules
3. **Resources** (on-demand): `assets/`, `references/` — 스키마, 참조 문서

## 3. Template Chain

스킬은 체인을 구성하며, 각 출력이 다음 스킬의 입력이 된다:

```
[User Idea] → user-input → quest-plan → stage-spec → execution-plan → [execution ...]
               (entry)       (quest)      (stage)      (element chain)
```

| 순서 | Skill | 입력 | 출력 | 실행 횟수 |
|------|-------|------|------|-----------|
| 1 | `user-input` | 사용자 자유형 아이디어 | quest-seed.yaml | 1회 |
| 2 | `quest-plan` | quest-seed.yaml | quest-plan.yaml | 1회 |
| 3 | `stage-spec` | quest-seed.yaml + quest-plan.yaml | stage-spec.STG-XX.yaml | stage당 1회 |
| 4 | `execution-plan` | stage-spec.STG-XX.yaml + quest-seed.yaml | execution-plan.STG-XX.yaml | stage당 1회 |
| 5+ | element chain (TODO) | execution-plan → execution → artifact → evaluation → evidence → checkpoint → (recovery) | — | task당 반복 |

## 4. Skill Selection Guide

| 상황 | 사용할 Skill |
|------|-------------|
| 비정형 아이디어에서 프로젝트 시작 | `skills/user-input` |
| 퀘스트 거버넌스, 스테이지 맵, 정책 정의 | `skills/quest-plan` |
| 개별 스테이지의 계약/평가/체크포인트 설계 | `skills/stage-spec` |
| 스테이지를 실행 가능한 태스크로 분해 | `skills/execution-plan` |

## 5. Skill Common Structure

모든 스킬은 Agent Skills 사양을 따르는 공통 구조를 갖는다:

```
skill-name/
├── SKILL.md                  ← Frontmatter (name, description, compatibility, metadata)
│                                + Body (When to Use, Core Responsibility, Input/Output,
│                                  Process Steps, Output Rules)
├── assets/                   ← 출력물 스키마 (AI가 생성하는 YAML의 규격)
│   └── *.schema.yaml
└── references/               ← 참조 문서 (on-demand 로드)
    ├── SSDAM.md              ← SSDAM 프레임워크 참조 + Handoff Contract
    └── *.md                  ← 스킬별 도메인 참조
```

공통 설계 원칙:

- 각 스킬은 **자기완결적** — SSDAM 사전지식 없이 AI 모델이 실행 가능
- 출력은 항상 **구조화된 YAML** (markdown 아님)
- 언어 규칙: human-readable text는 입력 언어와 동일. YAML 키는 영어 유지
- **호환성**: ChatGPT, Claude, Cursor, Codex 등 YAML 출력 가능한 모든 AI 에이전트에서 사용 가능

## 6. Output Rules (공통)

모든 스킬의 Output Rules에 포함되는 공통 규칙:

1. Output ONLY valid YAML. No markdown, no prose, no explanations.
2. Do NOT wrap in code fences. Raw YAML directly.
3. 스키마의 모든 키 필수 포함. 추가 키 금지.
4. 특수문자 포함 문자열은 반드시 따옴표.
5. 멀티라인은 YAML block scalar (`>` 또는 `|`).
6. 인덴트 2스페이스. 탭 금지.
7. PyYAML / SnakeYAML / js-yaml 파서로 검증 가능해야 함.
8. NESTED QUOTE PROHIBITION (quest-plan, stage-spec, execution-plan).
9. 언어 규칙.

스킬별 추가 규칙:

| Skill | 추가 규칙 |
|-------|-----------|
| `execution-plan` | NO IMPLEMENTATION CODE (Rule 10), LOCAL PATH RULE (Rule 11) |

## 7. Validation Scenarios

### 7.1 Happy Path

1. `user-input`으로 quest-seed.yaml 생성
2. `quest-plan`으로 quest-plan.yaml 생성
3. `stage-spec`으로 stage-spec.STG-01.yaml 생성
4. `execution-plan`으로 execution-plan.STG-01.yaml 생성
5. Element chain (execution → artifact → evaluation → evidence → checkpoint) 실행

### 7.2 Failure/Recovery Flow

1. Checkpoint에서 FAIL 판정
2. Recovery로 실패 분류 + 전략 선택 + 재평가
3. 상태 전이 기록 검증: FAILED → IN_PROGRESS → COMPLETED

### 7.3 Traceability Validation

1. 하나의 requirement ID를 stage-spec → artifact → evaluation → checkpoint로 추적
2. 모든 판정 문서에 Evidence 링크 존재 확인

### 7.4 Quality Validation

1. 모든 evaluation criteria가 PASS/FAIL 판정 가능한 문장인지 확인
2. "generally good" 같은 모호한 표현 부재 확인

## 8. Assumptions and Defaults

1. 출력 형식은 YAML로 통일.
2. 모든 스킬은 이전 체인 단계의 YAML 파일을 입력으로 받는다.
3. 모든 스킬은 **Self-Validation 체크리스트**를 포함한다.
4. 예제 데이터는 `05_examples`에서 관리, `04_templates`에는 포함하지 않는다.
5. Element chain의 나머지 스킬 (execution, artifact, evaluation, evidence, checkpoint, recovery)은 TODO.
