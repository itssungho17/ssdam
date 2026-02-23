# SSDAM Quickstart — Cursor에서 시작하기

이 문서는 Cursor에서 SSDAM AgentSkills를 처음 사용하는 사람을 위한 빠른 시작 가이드입니다.

---

## 전체 흐름

```
[준비]  templetes → .cursor/skills 복사 + package.json 수정
   ↓
[SPEC]  /new-mission  →  mission-spec.yaml            ✅
   ↓
[SPEC]  /new-task     →  task-spec.TSK-NNN.yaml       ✅
   ↓
[EXEC]  /architecture-design  →  architecture-design.TSK-NNN.md   ✅
        /data-modeling         →  data-modeling.TSK-NNN.md         ✅
        /schema-design         →  schema-design.TSK-NNN.sql        ✅
        /backend-design        →  backend-design.TSK-NNN.md        🚧
        /backend-implementation →  코드 작성 (project_root)        🚧
        /frontend-design       →  frontend-design.TSK-NNN.md       🚧
        /frontend-implementation → 코드 작성 (project_root)        🚧
   ↓
[완료]  Checkpoint PASS → 다음 Task로
```

✅ 검증 완료 &nbsp;&nbsp; 🚧 개발 중

> 어느 단계에서든 결과물이 의도와 다를 경우, 해당 파일을 수정하고 그 지점부터 다시 시작합니다.

---

## 스킬 상태

> **검증된 스킬만 프로덕션 환경에서 사용하세요.**
> 개발 중인 스킬은 출력 품질이 불안정할 수 있습니다.

| 스킬 | 상태 |
|------|------|
| `new-mission` | ✅ **검증 완료** |
| `new-task` | ✅ **검증 완료** |
| `architecture-design` | ✅ **검증 완료** |
| `data-modeling` | ✅ **검증 완료** |
| `schema-design` | ✅ **검증 완료** |
| `backend-design` | 🚧 개발 중 |
| `backend-implementation` | 🚧 개발 중 |
| `frontend-design` | 🚧 개발 중 |
| `frontend-implementation` | 🚧 개발 중 |

---

## Step 1 — 스킬 설치

프로젝트 루트에 `.cursor/skills` 폴더를 생성하고, `templetes/` 안의 모든 폴더를 그 안에 복사합니다.

```
your-project/
└── .cursor/
    └── skills/
        ├── new-mission/
        ├── new-task/
        ├── architecture-design/
        ├── data-modeling/
        ├── schema-design/
        ├── backend-design/
        ├── backend-implementation/
        ├── frontend-design/
        └── frontend-implementation/
```

---

## Step 2 — 프로젝트 정보 입력

`.cursor/skills/new-mission/assets/package.json` 을 열어 프로젝트에 맞게 수정합니다.

```json
{
    "mission_owner": "사용자 이름",
    "project_context": {
        "backend_stack": "FastAPI, Python, Pydantic, SqlModel",
        "frontend_stack": "Svelte, TypeScript, TailwindCSS, Vite",
        "database": "PostgreSQL"
    }
}
```

| 필드 | 설명 |
|------|------|
| `mission_owner` | 미션 담당자 이름 |
| `backend_stack` | 백엔드 기술 스택 |
| `frontend_stack` | 프론트엔드 기술 스택 |
| `database` | 데이터베이스 |

---

## Step 3 — Mission 생성

Cursor Agent 채팅에 구현하고자 하는 아이디어 또는 기능 목록을 입력합니다.

```
/new-mission {구현하고자 하는 아이디어 또는 기능 목록}
```

**예시:**
```
/new-mission 미디어 파일 마켓플레이스. 사용자가 이미지와 영상을 업로드하고 판매할 수 있으며, 구매자는 파일을 다운로드할 수 있다.
```

완료되면 아래 두 파일이 생성됩니다:

```
.ssdam/{workspace-id}/
├── input/
│   └── mission-input.yaml    ← 스킬이 자동 생성
└── output/
    └── mission-spec.yaml     ← 미션 전체 정의
```

내용이 의도와 다르면 Cursor Agent를 통해 수정하거나 파일을 직접 편집합니다.

---

## Step 4 — Task 스펙 생성

미션의 각 Task에 대해 아래 명령을 실행합니다.

```
/new-task @mission-spec.yaml TSK-001
```

완료되면 아래 파일이 생성됩니다:

```
.ssdam/{workspace-id}/output/
└── task-spec.TSK-001.yaml    ← 계약, 평가 기준, 실행 계획 포함
```

`task-spec` 파일 내 `execution_plan.steps`를 확인합니다.
이 목록이 다음 단계에서 실행할 스킬의 순서를 정의합니다.

---

## Step 5 — Execution 스킬 실행

`task-spec.TSK-NNN.yaml`의 `execution_plan.steps`를 참고하여 `EXEC-01`부터 순서대로 실행합니다.

```
/{exec_type} @task-spec.TSK-001.yaml {exec_id}
```

**예시 순서:**
```
/architecture-design  @task-spec.TSK-001.yaml EXEC-01
/data-modeling        @task-spec.TSK-001.yaml EXEC-02
/schema-design        @task-spec.TSK-001.yaml EXEC-03
/backend-design       @task-spec.TSK-001.yaml EXEC-04
/backend-implementation @task-spec.TSK-001.yaml EXEC-05
```

> `task-spec`에 포함되지 않은 스킬은 실행하지 않습니다. 어떤 스텝이 포함되는지는 Task의 성격(백엔드 전용, 풀스택 등)에 따라 달라집니다.

---

## Step 6 — 중간 수정 루프

결과물이 의도와 다를 경우, 해당 파일을 수정하고 그 지점부터 다시 실행합니다.
이전 단계로 돌아가는 것은 언제든 가능합니다.

```
예: architecture-design 결과가 마음에 들지 않는 경우
 → architecture-design.TSK-001.md 파일을 직접 수정
 → /data-modeling @task-spec.TSK-001.yaml EXEC-02  (다음 단계부터 재개)
```

---

## 파일 위치 요약

| 파일 | 경로 |
|------|------|
| 스킬 정의 | `.cursor/skills/{skill-name}/SKILL.md` |
| 프로젝트 설정 | `.cursor/skills/new-mission/assets/package.json` |
| Mission 입력 | `.ssdam/{id}/input/mission-input.yaml` |
| Mission 스펙 | `.ssdam/{id}/output/mission-spec.yaml` |
| Task 스펙 | `.ssdam/{id}/output/task-spec.TSK-NNN.yaml` |
| 설계 산출물 | `.ssdam/{id}/output/design/{skill-name}.TSK-NNN.md` |
| 스키마 산출물 | `.ssdam/{id}/output/design/schema-design.TSK-NNN.sql` |
| 구현 코드 | `{project_root}/` (직접 작성) |
