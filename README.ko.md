# SSDAM

**Structured Skill-Driven Automation Mechanism**

**Task**를 최상위 실행 단위로 정의하고, 검증된 파이프라인을 통해 작업을 구조화하며, 모든 단계에서 품질·추적성·복구 가능성을 보장하는 Human–AI 협업 개발 운영 메커니즘입니다.

> SSDAM은 *"무엇을 했는가"* 가 아닌, *"무엇이 검증되었는가"* 를 기준으로 동작합니다.

English documentation: [README.md](./README.md)

---

## SSDAM이란?

SSDAM은 AI 에이전트와 인간이 역할을 나눠 소프트웨어 개발 프로젝트를 수행하기 위한 프레임워크입니다. 활동 중심의 비공식 진행 추적 방식 대신, 계약 기반으로 연결된 검증 파이프라인을 통해 상태 전이를 관리합니다.

모든 작업은 동일한 5단계 흐름을 거칩니다:

```
Execution(실행) → Artifact(산출물) → Evaluation(평가) → Evidence(근거) → Checkpoint(체크포인트)
```

진행은 활동이 끝났을 때, 파일이 생성되었을 때가 아니라 **Checkpoint가 통과되었을 때만** 허용됩니다.

---

## 핵심 개념

| 개념 | 설명 |
|------|------|
| **Mission** | 여러 Task로 구성된 상위 의도 컨테이너. 직접 실행 불가. |
| **Task** | 원자적 실행 단위. 명시적 입출력 계약을 가지며, 검증 가능한 Artifact를 생산하고, Checkpoint로 종료됨. |
| **Execution** | Artifact를 생산하기 위해 Task 내에서 수행되는 활동. |
| **Artifact** | Execution 결과로 생성된 검토 가능한 산출물. |
| **Evaluation** | 정의된 기준에 따라 Artifact를 검증하는 과정. |
| **Evidence** | Evaluation 결정을 뒷받침하는 객관적 근거. |
| **Checkpoint** | 유일한 PASS / FAIL 결정 게이트. 암묵적 전이 없음. |
| **Recovery** | Checkpoint 실패 시 실행되는 구조화된 대응. 입력·전략·제약·스킬 선택 중 하나를 반드시 변경해야 함. |
| **Skill** | Task가 호출하는 재사용 가능한 실행 능력. |

---

## 파이프라인

SSDAM은 2단계 Agent Skill 파이프라인으로 구성됩니다.

### Phase 1 — 스펙 생성

| 스킬 | 트리거 | 출력 |
|------|--------|------|
| `new-mission` | `/new-mission` | `mission-spec.yaml` — Task 목록, 요구사항, 거버넌스를 포함한 전체 미션 정의 |
| `new-task` | `/new-task <mission-spec-path> <TSK-NNN>` | `task-spec.TSK-NNN.yaml` — 계약, 평가 기준, 실행 계획이 완전히 명세된 Task 스펙 |

### Phase 2 — 실행 스킬

각 `task-spec`의 `execution_plan.steps`에 있는 스텝이 아래 스킬과 1:1로 대응됩니다. 순서대로 실행합니다.

```
architecture-design (필수)
       │
       ├── data-modeling
       │       └── schema-design
       │
       ├── backend-design ──── backend-implementation
       │
       └── frontend-design ─── frontend-implementation
```

| 스킬 | 트리거 | 출력 |
|------|--------|------|
| `architecture-design` | `/architecture-design <task-spec-path>` | `architecture-design.TSK-NNN.md` — 모듈 경계, 컴포넌트 다이어그램, API 계약 개요, 도메인 엔티티 |
| `data-modeling` | `/data-modeling <task-spec-path>` | `data-modeling.TSK-NNN.md` — 엔티티 정의, Mermaid ERD, 관계, 인덱스 |
| `schema-design` | `/schema-design <task-spec-path>` | `schema-design.TSK-NNN.sql` — 전체 테이블 DDL |
| `backend-design` | `/backend-design <task-spec-path>` | `backend-design.TSK-NNN.md` — API 엔드포인트, 서비스/레포지토리 레이어, 에러 처리, 테스트 전략 |
| `backend-implementation` | `/backend-implementation <task-spec-path>` | `project_root/`에 코드 직접 작성 (에이전트 자율 실행) |
| `frontend-design` | `/frontend-design <task-spec-path>` | `frontend-design.TSK-NNN.md` — 페이지, 컴포넌트 트리, 상태 관리, API 연동 |
| `frontend-implementation` | `/frontend-implementation <task-spec-path>` | `project_root/`에 코드 직접 작성 (에이전트 자율 실행) |

> `backend-design`이 완료되면 `backend-implementation`과 `frontend-design`은 병렬로 실행 가능합니다.

---

## 런타임 출력 구조

파이프라인이 실행되면 모든 산출물이 `.ssdam/` 하위 워크스페이스 폴더에 작성됩니다:

```
.ssdam/
└── {workspace-id}/
    ├── input/
    │   └── mission-input.yaml       ← new-mission이 자동 생성
    └── output/
        ├── mission-spec.yaml        ← new-mission 생성
        ├── task-spec.TSK-001.yaml   ← new-task 생성
        ├── task-spec.TSK-002.yaml
        └── design/
            ├── architecture-design.TSK-001.md
            ├── data-modeling.TSK-001.md
            ├── schema-design.TSK-001.sql
            ├── backend-design.TSK-001.md
            └── frontend-design.TSK-001.md
```

---

## 프로젝트 구조

```
ssdam/
├── templetes/               ← Agent Skill 정의 (AI 에이전트가 읽음)
│   ├── new-mission/
│   ├── new-task/
│   ├── architecture-design/
│   ├── data-modeling/
│   ├── schema-design/
│   ├── backend-design/
│   ├── backend-implementation/
│   ├── frontend-design/
│   └── frontend-implementation/
│
├── examples/
│   └── 01_ddalggak/         ← SSDAM 예제 프로젝트 (TBD)
│       ├── README.md
│       └── README.ko.md
│
├── en/                      ← 영문 문서
│   ├── 01_overview/
│   ├── 02_core_concepts/
│   ├── 03_architecture/
│   ├── 04_methodology/
│   └── 05_references/
│
└── ko/                      ← 한국어 문서
    ├── 01_overview/
    ├── 02_core_concepts/
    ├── 03_architecture/
    ├── 04_methodology/
    └── 05_references/
```

각 스킬 폴더 구성:
- `SKILL.md` — AI 에이전트가 읽는 실행 절차 정의
- `references/input.template.yaml` — 입력 계약 템플릿
- `references/output.template.yaml` — 출력 계약 템플릿
- `references/rules.md` — 컨벤션 및 안티패턴
- `scripts/` — 검증 및 보조 스크립트

---

## 시작하기

### 1. Mission 정의

AI 에이전트를 `new-mission` 스킬로 호출합니다:

```
/new-mission <원하는 아이디어 또는 기능 목록>
```

에이전트가 프로젝트를 스캔하고 질문을 통해 정보를 수집한 뒤, `.ssdam/{workspace-id}/output/mission-spec.yaml`을 생성합니다.

### 2. Task 스펙 생성

미션의 각 Task에 대해:

```
/new-task .ssdam/{workspace-id}/output/mission-spec.yaml <TSK-NNN>
```

에이전트가 미션 스펙을 읽고 검증한 뒤, 완전히 명세된 `task-spec.TSK-001.yaml`을 생성합니다.

### 3. Task 실행

task-spec의 `execution_plan.steps`를 순서대로 실행합니다:

```
/architecture-design .ssdam/{workspace-id}/output/task-spec.TSK-001.yaml
/data-modeling       .ssdam/{workspace-id}/output/task-spec.TSK-001.yaml
/schema-design       .ssdam/{workspace-id}/output/task-spec.TSK-001.yaml
/backend-design      .ssdam/{workspace-id}/output/task-spec.TSK-001.yaml
/backend-implementation .ssdam/{workspace-id}/output/task-spec.TSK-001.yaml
```

---

## 설계 원칙

1. **Task가 최상위 실행 단위** — Task는 원자적이며, Mission은 컨테이너입니다.
2. **계약 기반 설계** — 모든 Task는 명시적인 입출력 계약을 가집니다.
3. **Artifact 기반 진행** — 진행은 완료된 활동이 아닌 검증된 Artifact로 측정됩니다.
4. **Evidence 기반 의사결정** — 근거 없는 PASS 또는 FAIL은 없습니다.
5. **Checkpoint 권위** — 전진 또는 복구는 Checkpoint를 통해서만 가능합니다.
6. **실패는 설계된 이벤트** — 실패는 분류되고 보존되며, 정의된 전략으로 복구됩니다.
7. **종단간 추적성** — 요구사항 → Task → Artifact → Evaluation → Checkpoint 전 구간 추적.
8. **Human / Agent 책임 모델** — 에이전트는 실행하고, 인간은 책임을 소유합니다.

---

## 문서

전체 문서는 `en/`(영문)과 `ko/`(한국어) 디렉토리에서 확인할 수 있습니다.

| 섹션 | 내용 |
|------|------|
| `ko/01_overview/` | SSDAM 개요 |
| `ko/02_core_concepts/` | 원칙, 용어집, ID 컨벤션 |
| `ko/03_architecture/` | 흐름 아키텍처, 미션/태스크 모델, 의존성 모델, 복구 전략 |
| `ko/04_methodology/` | Mission 및 Task 설계 가이드 |
| `ko/05_references/` | 요소 레퍼런스: Artifact, Checkpoint, Evaluation, Evidence, Execution, Recovery, Traceability |

---

## 라이선스

[LICENSE.txt](./LICENSE.txt)를 참고하세요.
