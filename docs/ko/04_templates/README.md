# SSDAM Agent Prompt Hub — 04_templates

## 1. 목적
`04_templates`는 SSDAM 프레임워크의 **AI Agent용 프롬프트 모음**이다.
각 프롬프트는 `<system>`, `<context>`, `<input>`, `<instructions>`, `<output_format>` 구조로 설계되어 있으며,
에이전트가 SSDAM 규칙을 준수하면서 문서를 자율적으로 생성할 수 있도록 안내한다.

## 1.1 디렉터리 구조
```text
04_templates/
├── README.md                              ← 이 파일 (프롬프트 허브)
├── 01_project/                            ← 프로젝트 수준 프롬프트
│   ├── project-governance.template.md     ← 역할/승인/에스컬레이션 정의
│   ├── project-stage-map.template.md      ← 스테이지 순서/의존성/분기 설계
│   └── project-policy.template.md         ← 품질/회복/추적성 정책 정의
├── 02_stage/                              ← 스테이지 수준 프롬프트
│   ├── stage-spec.template.md             ← 단일 스테이지 명세 설계
│   └── stage-catalog.template.md          ← 스테이지 후보 카탈로그 구성
└── 03_elements/                           ← 실행 요소 수준 프롬프트
    ├── execution.template.md              ← 실행 기록
    ├── artifact.template.md               ← 산출물 기록
    ├── evaluation.template.md             ← 평가 기록
    ├── evidence.template.md               ← 근거 기록
    ├── checkpoint.template.md             ← 체크포인트 판정
    └── recovery.template.md               ← 회복 기록
```

## 2. 프롬프트 실행 순서
에이전트는 다음 순서로 프롬프트를 호출한다:

```
01_project 정의 → 02_stage 설계 → 03_elements 실행 기록
```

상세 흐름:
1. `project-governance` → 역할/승인 체계 확립
2. `project-stage-map` → 전체 스테이지 흐름 설계
3. `project-policy` → 품질/회복/추적성 공통 규칙 정의
4. `stage-catalog` → 스테이지 후보 선정 (선택)
5. `stage-spec` → 각 스테이지의 계약/평가/체크포인트/회복 구체화
6. 스테이지별 실행 시 `execution → artifact → evaluation → evidence → checkpoint` 순서로 호출
7. FAIL 발생 시 `recovery` 호출

## 3. 프롬프트 선택 가이드

| 상황 | 호출할 프롬프트 |
|---|---|
| 프로젝트 책임/승인/에스컬레이션 체계를 정의할 때 | `01_project/project-governance.template.md` |
| 전체 스테이지 순서/의존성/분기 경로를 설계할 때 | `01_project/project-stage-map.template.md` |
| 품질/회복/추적성의 프로젝트 공통 규칙을 정의할 때 | `01_project/project-policy.template.md` |
| 특정 스테이지 1개의 계약과 판정 규칙을 설계할 때 | `02_stage/stage-spec.template.md` |
| 초기 프로젝트에 사용할 스테이지 후보를 빠르게 고를 때 | `02_stage/stage-catalog.template.md` |
| 실행 입력 검증과 활동 내역을 기록할 때 | `03_elements/execution.template.md` |
| 산출물의 식별/버전/해시/변경 정보를 기록할 때 | `03_elements/artifact.template.md` |
| 평가 기준/지표/판정/리스크를 기록할 때 | `03_elements/evaluation.template.md` |
| 평가 근거의 출처/측정값/불변 상태를 기록할 때 | `03_elements/evidence.template.md` |
| 정책 기반 PASS/FAIL 판정과 상태 전이를 기록할 때 | `03_elements/checkpoint.template.md` |
| FAIL 이후 회복 전략과 재진입 판정을 기록할 때 | `03_elements/recovery.template.md` |

## 4. 프롬프트 공통 구조
모든 프롬프트는 다음 XML 구조를 따른다:

```xml
<system>    에이전트 역할 정의 </system>
<context>   SSDAM 규칙/원칙/제약 </context>
<input>     에이전트에게 전달할 변수 ({{변수명}}) </input>
<instructions> 단계별 실행 절차 + 자기 검증 체크리스트 </instructions>
<output_format> 출력 형식 제약 </output_format>
```

## 5. 최소 완료 기준
스테이지 1개를 `COMPLETED`로 선언하려면 최소 다음 프롬프트가 실행되어야 한다:

1. `stage-spec` 프롬프트로 스테이지 계약/평가/체크포인트/회복을 정의
2. `execution` 프롬프트로 실행 기록
3. `artifact` 프롬프트로 산출물 기록
4. `evaluation` 프롬프트로 평가 기록
5. `evidence` 프롬프트로 근거 기록
6. `checkpoint` 프롬프트에서 PASS 판정
7. PASS 시 다음 스테이지 전달 필드(`next_stage_id`, `handoff_artifact_ids`, `handoff_evidence_ids`) 모두 채움

## 6. 검증 시나리오

### 6.1 정상 흐름
1. 임의 스테이지 1개를 `stage-spec` 프롬프트로 정의
2. `execution → artifact → evaluation → evidence → checkpoint` 프롬프트를 순서대로 실행
3. Checkpoint PASS 후 다음 스테이지 전달 필드 누락 검증

### 6.2 실패/회복 흐름
1. `checkpoint` 프롬프트에서 FAIL 판정
2. `recovery` 프롬프트로 실패 분류 + 전략 선택 + 재평가
3. `FAILED → IN_PROGRESS → COMPLETED` 전이 기록 완전성 검증

### 6.3 추적성 검증
1. 요구사항 ID 1개를 `stage-spec`, `artifact`, `evaluation`, `checkpoint`에 공통 연결
2. 모든 판정 문서에 Evidence 링크가 존재하는지 검증

### 6.4 품질 검증
1. `evaluation` 프롬프트의 모든 기준이 PASS/FAIL 판정 가능 문장인지 점검
2. "대체로 좋음" 같은 모호한 표현이 없는지 점검

## 7. 가정 및 기본값
1. 출력 포맷은 Markdown으로 통일한다.
2. 모든 프롬프트는 `{{변수}}` 형식으로 입력을 받는다.
3. 모든 프롬프트는 마지막에 **자기 검증 체크리스트**를 포함한다.
4. 예시 데이터는 `04_templates`가 아닌 `05_examples`에서 관리한다.
5. 파일명/섹션명은 SSDAM 레퍼런스 용어를 그대로 사용한다.
