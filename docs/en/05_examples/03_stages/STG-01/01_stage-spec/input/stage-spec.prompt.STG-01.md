# SSDAM Agent Prompt — Stage Specification Design

<protocol>
  <framework>
    name: SSDAM (SOLID Stage-Driven Automation Mechanism)
    purpose: A quality/validation/evidence-centered execution mechanism where Stage is the top-level purpose unit.
    core_flow: Each Stage follows → Execution → Artifact → Evaluation → Evidence → Checkpoint → (Next Stage | Recovery)
    principles:
      - Stage is a purpose unit, not a task unit.
      - Progress is defined by Checkpoint PASS, not by activity completion.
      - All decisions require Evidence. No evidence-free judgment is permitted.
      - Failure is a designed state transition event, not an exception.
    quest_setup_flow: user-input → quest-plan → stage-spec → [element chain]
  </framework>

  <position>
    template_id: stage-spec.template
    phase: stage (03_stage)
    role: Defines a single stage's purpose, contracts, evaluation criteria, checkpoint policy, and recovery mapping.
    predecessor: quest-plan.template
    successor: execution.template (element chain start)
  </position>

  <input_contract>
    source_template: quest-plan.template
    source_files:
      - quest-seed.yaml (from user-input.template)
      - quest-plan.yaml (from quest-plan.template)
    target_stage: Specified by the user (e.g., STG-01)
    required_fields_from_quest_seed:
      - metadata.quest_id → quest_id
      - stages[target].id → stage_id
      - stages[target].name → stage_name
      - stages[target].purpose → stage_purpose
      - stages[target].key_artifact → key_artifact_description
      - stages[target].mapped_requirements → requirement_ids
      - requirements[] → full requirement list (for evaluation criteria derivation)
    required_fields_from_quest_plan:
      - governance.roles → role definitions (for stage_owner)
      - governance.gates[target] → gate_type, pass_condition, final_approver
      - governance.escalation_rules → escalation context
      - stage_map.dependencies[target] → predecessor artifact, dependency rationale
      - stage_map.branch_rules[target] → on_pass (next stage), on_fail (recovery)
      - policies.quality_policy → QPOL-XX references for evaluation criteria
      - policies.recovery_policy → RPOL-XX references for recovery mapping
      - policies.traceability_policy → TPOL-XX references for evidence requirements
    how_to_use: |
      The user will paste this template together with quest-seed.yaml and quest-plan.yaml,
      and specify which stage_id to design (e.g., "Design STG-01").
      Read all required_fields from both YAML files for the target stage.
  </input_contract>

  <output_contract>
    format: YAML (.yaml file)
    output_filename: stage-spec.STG-XX.yaml
    target_template: execution.template (element chain)
    handoff_fields:
      - metadata.quest_id → element chain input
      - metadata.stage_id → element chain input
      - output_contract[].artifact_id → artifact.template input
      - evaluation_criteria[] → evaluation.template input
      - checkpoint → checkpoint.template input
      - recovery_mapping[] → recovery.template input
  </output_contract>

  <next_action>
    on_complete: |
      Output a single YAML document as stage-spec.STG-XX.yaml.
      Repeat this template for each stage in quest-plan.yaml's stage_list.
      After all stage-specs are defined, begin the element chain
      (execution → artifact → evaluation → evidence → checkpoint) for each stage.
  </next_action>
</protocol>

<system>
You are a stage design agent of the SSDAM framework.

SSDAM (SOLID Stage-Driven Automation Mechanism) is a structured execution system where:
- A quest is decomposed into **Stages** (purpose units, not task units).
- Each Stage follows: Execution → Artifact → Evaluation → Evidence → Checkpoint.
- Progress is defined by **Checkpoint PASS**, not by activity completion.
- Failure triggers **Recovery**, not termination.

Your role is to produce a single stage specification that defines:
1. **Purpose & Scope** — what this stage achieves (single responsibility)
2. **Input/Output Contracts** — what artifacts come in and go out
3. **Evaluation Criteria** — how to judge PASS/FAIL (quantitative, no ambiguity)
4. **Checkpoint Policy** — gate type, approver, policy references
5. **Recovery Mapping** — what to do on failure

SOLID principles for stage design:
- **S (Single Responsibility)**: One testable purpose per stage.
- **O (Open/Closed)**: Stage structure is stable; extend via artifact variants.
- **L (Liskov Substitution)**: Output artifacts are interchangeable if they meet contract.
- **I (Interface Segregation)**: Contracts expose only necessary attributes.
- **D (Dependency Inversion)**: Stage depends on abstract contracts, not concrete implementations.
</system>

<context>
This template is the third step in the SSDAM pipeline:

```
[quest-seed.yaml + quest-plan.yaml] → THIS TEMPLATE (per stage) → element chain
```

### Stage Design Principles
- A Stage is a **purpose unit**, not a task bundle.
- Purpose must be expressible in a single testable sentence.
- All input/output must be **Artifact-based** (concrete, verifiable outputs).
- Evaluation criteria must be **PASS/FAIL-decidable** with quantitative thresholds.
- No ambiguous language: "generally good", "adequate", "appropriate" are forbidden.

### Input Contract Rules
- First stage (no predecessor): input_item = "none", artifact_id = "none"
- Other stages: input must reference specific artifact_ids from predecessor stage's output

### Output Contract Rules
- artifact_id format: `ART-STG-XX-NNN` (e.g., ART-STG-01-001)
- Each artifact must have a concrete contract specification (format, structure, content)
- Artifacts must be reviewable and evaluable

### Evaluation Criteria Rules
- Must reference QPOL-XX from quest-plan.yaml
- Each criterion must have a quantitative pass_threshold
- Measurement method must be automated or clearly defined manual process

### Checkpoint Rules
- Must match gate_type from quest-plan.yaml's gates[target]
- gate_type: automatic (quantitative only) / human (requires judgment) / hybrid (auto + human)

### Recovery Rules
- Must reference RPOL-XX from quest-plan.yaml
- Strategies must be from: Re-execution / Correction / Re-stage / Rollback
- Escalation triggers must link to ESC rules from quest-plan.yaml

### Immutable Rules
- Final accountability rests with stage_owner (person), not agent.
- All criteria must be PASS/FAIL-decidable. No ambiguous language.
- Every FAIL path must have a Recovery mapping.
</context>

<input>
Attached files:
1. **quest-seed.yaml** (output from user-input.template)
2. **quest-plan.yaml** (output from quest-plan.template)

Target stage: **STG-01** (소유 자료 3Depth 조회·상세 보기)

Read the following fields from quest-seed.yaml for the target stage:
- `metadata.quest_id` → use as quest_id
- `stages[target].id` → use as stage_id
- `stages[target].name` → use as stage_name
- `stages[target].purpose` → use as purpose basis
- `stages[target].key_artifact` → use as output contract basis
- `stages[target].mapped_requirements` → use as requirement_ids
- `requirements[]` → use for evaluation criteria derivation

Read the following fields from quest-plan.yaml for the target stage:
- `governance.gates[target]` → use for checkpoint (gate_type, pass_condition, final_approver)
- `governance.escalation_rules[]` → use for recovery escalation context
- `stage_map.dependencies[target]` → use for input contract (predecessor artifact)
- `stage_map.branch_rules[target]` → use for handoff (on_pass → next_stage_id)
- `policies.quality_policy[]` → use for evaluation criteria (QPOL references)
- `policies.recovery_policy[]` → use for recovery mapping (RPOL references)
- `policies.traceability_policy[]` → use for evidence requirements

<attached_file>
# SSDAM Quest Seed
# source_template: user-input.template
# schema_version: v0.2.0

idea_validation:
  status: PASS
  checks:
    has_goal: true
    has_testable_outcome: true
    is_actionable: true

metadata:
  quest_id: "QST-20260216-001"
  quest_name: "이미지/동영상 라이브러리 + 업로드 + 마켓(구매) 토이 웹앱"
  quest_owner: "undefined"
  domain: "software development (web application)"
  timestamp: "2026-02-16T18:00:00+09:00"

goal:
  statement: "Spring Boot + PostgreSQL + Svelte로 이미지/동영상 파일을 3Depth로 관리하고(보기/편집), 업로드·공개 설정·검색·구매·구매내역 확인까지 가능한 학습용 토이 웹앱을 구현한다."
  success_criteria:
    - id: SC-01
      description: "기본 제공 자료와 구매한 자료가 '소유 자료 페이지'에서 3Depth(폴더→하위폴더→자료)로 조회되면 PASS."
    - id: SC-02
      description: "사용자가 이미지/동영상 파일만 업로드할 수 있고, 업로드된 파일의 이름 변경 및 공개/비공개 설정을 변경할 수 있으면 PASS."
    - id: SC-03
      description: "다른 사용자가 공개한 파일을 이름/태그로 검색하여 조회하고, 구매 처리 후 구매 표시(테두리/체크 등)와 구매 목록 반영이 되면 PASS."
  out_of_scope:
    - "실제 결제 PG 연동(카드/간편결제 등) 및 정산"
    - "DRM/워터마크/저작권 분쟁 처리"
    - "대규모 트래픽/대용량 미디어 스트리밍 최적화(CDN, 트랜스코딩 파이프라인 등)"

requirements:
  - id: REQ-001
    statement: "시스템은 기본 제공 이미지/동영상 자료를 3Depth(폴더→하위폴더→자료) 구조로 조회할 수 있어야 한다."
    priority: must
  - id: REQ-002
    statement: "시스템은 소유 자료 페이지에서 사용자의 소유 자료(기본 제공 + 구매한 자료)를 숨김 처리된 자료를 제외하고 목록으로 표시해야 한다."
    priority: must
  - id: REQ-003
    statement: "시스템은 소유 자료 페이지에서 더블클릭(또는 동등한 상호작용)으로 자료 상세 보기(이미지 확대/동영상 재생 포함)를 제공해야 한다."
    priority: must
  - id: REQ-004
    statement: "시스템은 소유 자료 페이지에서 편집 모드 시 자료의 이름 변경/이동/복사/숨기기 기능을 제공해야 한다."
    priority: should
  - id: REQ-005
    statement: "시스템은 사용자가 이미지/동영상 파일만 업로드할 수 있도록 제한해야 하며, 업로드된 파일을 업로드 일자 기준으로 조회할 수 있어야 한다."
    priority: must
  - id: REQ-006
    statement: "시스템은 사용자가 업로드한 파일에 대해 이름 변경 및 타 사용자에게 표시 여부(공개/비공개)를 설정할 수 있어야 하며, 각 파일의 구매 횟수를 표시해야 한다."
    priority: should
  - id: REQ-007
    statement: "시스템은 다른 사용자가 공개한 파일을 목록으로 조회할 수 있어야 하며, 이름 또는 #태그로 검색할 수 있어야 한다."
    priority: must
  - id: REQ-008
    statement: "시스템은 다른 사용자가 공개한 파일에 대해 구매 기능을 제공해야 하며, 구매 완료된 파일은 구매 표시(테두리/체크 등) 또는 구매 항목 숨기기로 구분할 수 있어야 한다."
    priority: must

stages:
  - id: STG-01
    name: "소유 자료 3Depth 조회·상세 보기"
    purpose: "기본 제공 자료와 구매 자료를 3Depth로 탐색하고 상세 보기까지 가능한 소유 자료 조회 경험을 확정한다."
    key_artifact: "3Depth 자료 탐색/상세 보기 동작이 확인 가능한 소유 자료 페이지(프론트 + 백엔드 API + DB 스키마 최소 세트)"
    mapped_requirements: [REQ-001, REQ-002, REQ-003]
  - id: STG-02
    name: "소유 자료 편집 및 업로드 관리"
    purpose: "소유 자료의 편집(이름/이동/복사/숨김)과 사용자 업로드 자료의 제한 업로드·조회·공개 설정을 확정한다."
    key_artifact: "편집 모드가 포함된 소유 자료 페이지 + 업로드/내 업로드 관리 페이지 + 관련 API/DB 스키마"
    mapped_requirements: [REQ-004, REQ-005, REQ-006]
  - id: STG-03
    name: "공개 자료 마켓·검색·구매 흐름"
    purpose: "타 사용자 공개 자료의 조회/검색과 구매 처리, 구매 표시 및 소유 자료 반영을 통해 마켓 가치 흐름을 완결한다."
    key_artifact: "공개 자료 페이지(검색/구매/구매표시) + 구매 기록/권한 반영 로직 + 관련 API/DB 스키마"
    mapped_requirements: [REQ-007, REQ-008, REQ-002]

constraints:
  timeline: "undefined"
  budget: "undefined"
  backend_stack: "Spring Boot + PostgreSQL"
  frontend_stack: "Svelte"
  project_root: "/home/user/toy-media-app"
  team: "undefined"
  risks:
    - "미디어 파일 저장 방식(로컬/오브젝트 스토리지)과 서빙 방식 선택에 따라 구현 난이도가 크게 달라질 수 있음"
    - "구매/소유 권한 모델(소유/공개/구매내역) 설계가 불명확하면 페이지 간 데이터 정합성이 깨질 수 있음"
  existing_artifacts: []

handoff:
  next_template: quest-plan.template
  payload:
    quest_id: "QST-20260216-001"
    quest_owner: "undefined"
    quest_goal: "Spring Boot + PostgreSQL + Svelte로 이미지/동영상 파일을 3Depth로 관리하고(보기/편집), 업로드·공개 설정·검색·구매·구매내역 확인까지 가능한 학습용 토이 웹앱을 구현한다."
    domain: "software development (web application)"
    stage_list: [STG-01, STG-02, STG-03]
    requirement_ids: [REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008]
  instruction: >
    Feed this YAML file together with quest-plan.template.md
    into your next AI call.

self_validation:
  goal_is_testable: true
  all_requirements_pass_fail: true
  all_requirements_mapped: true
  all_stages_single_purpose: true
  handoff_complete: true
  no_vague_terms: true
  constraints_filled: true
</attached_file>

<attached_file>
# SSDAM Quest Plan
# source_template: quest-plan.template
# schema_version: v0.2.0
# input_file: quest-seed.yaml

metadata:
  quest_id: "QST-20260216-001"
  document_id: quest-plan
  quest_owner: "undefined"
  domain: "software development (web application)"
  version: "v0.1.0"
  timestamp: "2026-02-16T19:00:00+09:00"

governance:
  roles:
    - role_id: quest_owner
      responsibility_scope: "퀘스트 전체 구조(스테이지 구성/연결)와 전역 정책(QPOL/RPOL/TPOL) 수립 및 변경 승인"
      approval_scope: "quest-plan.yaml의 governance, stage_map, policies 최종 승인 및 변경 승인"
      exclusion_scope: "개별 스테이지의 구체 구현(코드/테스트/화면/쿼리) 결정 및 실행 활동에는 관여하지 않음"
    - role_id: stage_owner
      responsibility_scope: "담당 스테이지의 입력/출력 계약, 평가 기준, 체크포인트(PASS/FAIL) 충족 책임 및 산출물 품질 보증"
      approval_scope: "담당 스테이지의 체크포인트(CP-STG-XX) PASS/FAIL 판정 최종 승인(quest_owner 에스컬레이션 이전 단계)"
      exclusion_scope: "퀘스트 전역 정책(QPOL/RPOL/TPOL) 및 스테이지 맵(의존성/분기) 변경 권한 없음"
    - role_id: agent
      responsibility_scope: "정의된 정책 범위 내에서 실행/검증/증거 수집/회복 절차를 자동화하고, PASS/FAIL 판정 근거를 산출"
      approval_scope: "정책에 의해 자동 판정이 허용된 항목의 1차 판정 및 결과 리포트 생성"
      exclusion_scope: "정책 범위를 넘어서는 최종 의사결정(특히 논리/권한/정합성 설계 변경) 및 책임을 지지 않음"

  gates:
    - gate_id: "GATE-STG-01"
      stage_id: "STG-01"
      stage_name: "소유 자료 3Depth 조회·상세 보기"
      gate_type: "hybrid"
      pass_condition: "SC-01이 충족되고, API 통합 테스트 통과율이 >= 95%이며, E2E(탐색/상세보기) 시나리오 실패가 = 0이면 PASS"
      final_approver: "stage_owner"
    - gate_id: "GATE-STG-02"
      stage_id: "STG-02"
      stage_name: "소유 자료 편집 및 업로드 관리"
      gate_type: "hybrid"
      pass_condition: "SC-02가 충족되고, 업로드 파일 타입 검증(이미지/동영상 외) 차단 누락이 = 0이며, 편집(이름/이동/복사/숨김/공개설정) E2E 시나리오 실패가 = 0이면 PASS"
      final_approver: "stage_owner"
    - gate_id: "GATE-STG-03"
      stage_id: "STG-03"
      stage_name: "공개 자료 마켓·검색·구매 흐름"
      gate_type: "hybrid"
      pass_condition: "SC-03이 충족되고, 구매 처리 트랜잭션 정합성 오류(중복 구매 기록/소유 반영 누락/권한 누락)가 = 0이며, 검색(이름/태그) E2E 시나리오 실패가 = 0이면 PASS"
      final_approver: "stage_owner"

  escalation_rules:
    - rule_id: "ESC-FAIL-N"
      trigger_condition: "동일 스테이지에서 연속 실패 N회 이상 발생"
      threshold: "N >= 2"
      escalation_target: "quest_owner"
      action: "원인 분석 보고서(증거 포함)를 제출하고, 스테이지 범위/정책/의존성 변경이 필요하면 quest_owner 승인 하에 재설계(Re-stage)로 전환"
    - rule_id: "ESC-UNCERTAINTY"
      trigger_condition: "에이전트 판정 불확실성이 임계값 초과"
      threshold: "uncertainty > 0.35"
      escalation_target: "stage_owner"
      action: "판정 근거(로그/테스트/재현 절차)를 첨부하여 stage_owner에게 결정을 요청하고, 자동 판정은 중지(수동 승인 전환)"
    - rule_id: "ESC-RISK"
      trigger_condition: "리스크 수준이 임계값 이상"
      threshold: "risk_level >= 2"
      escalation_target: "quest_owner"
      action: "리스크 항목(저장/서빙 선택, 소유/구매 권한 모델)의 결정안을 2안 이상 제시하고, 선택 결과를 정책/설계 문서에 기록 후 진행"

stage_map:
  dependencies:
    - stage_id: "STG-01"
      predecessor_stage_id: "none"
      required_artifact: "none"
      dependency_rationale: "시작 스테이지"
    - stage_id: "STG-02"
      predecessor_stage_id: "STG-01"
      required_artifact: "3Depth 자료 탐색/상세 보기 동작이 확인 가능한 소유 자료 페이지(프론트 + 백엔드 API + DB 스키마 최소 세트)"
      dependency_rationale: "소유 자료의 기본 조회/상세 보기 산출물이 있어야 편집/업로드 기능의 정합성을 검증할 수 있음"
    - stage_id: "STG-03"
      predecessor_stage_id: "STG-02"
      required_artifact: "편집 모드가 포함된 소유 자료 페이지 + 업로드/내 업로드 관리 페이지 + 관련 API/DB 스키마"
      dependency_rationale: "소유/업로드/공개 설정 및 권한 모델이 확정되어야 공개 마켓/구매 반영 정합성을 보장할 수 있음"

  branch_rules:
    - stage_id: "STG-01"
      checkpoint_id: "CP-STG-01"
      on_pass: "STG-02"
      on_fail: "RCV-STG-01"
    - stage_id: "STG-02"
      checkpoint_id: "CP-STG-02"
      on_pass: "STG-03"
      on_fail: "RCV-STG-02"
    - stage_id: "STG-03"
      checkpoint_id: "CP-STG-03"
      on_pass: "END"
      on_fail: "RCV-STG-03"

  flow_diagram: |
    graph TD
      STG-01 -->|PASS| STG-02
      STG-01 -->|FAIL| RCV-STG-01
      STG-02 -->|PASS| STG-03
      STG-02 -->|FAIL| RCV-STG-02
      STG-03 -->|PASS| END
      STG-03 -->|FAIL| RCV-STG-03

policies:
  quality_policy:
    - policy_id: "QPOL-01"
      quality_item: "백엔드 자동 테스트 통과율"
      threshold: ">= 95%"
      measurement_method: "Spring Boot 테스트 실행 결과(JUnit/Gradle 또는 Maven)에서 통과율 계산"
      decision_criteria: "PASS/FAIL"
    - policy_id: "QPOL-02"
      quality_item: "프론트엔드 E2E 핵심 시나리오 실패 건수"
      threshold: "= 0"
      measurement_method: "Playwright/Cypress E2E 실행 결과에서 핵심 시나리오 실패 건수 집계"
      decision_criteria: "PASS/FAIL"
    - policy_id: "QPOL-03"
      quality_item: "정적 분석/린트 오류 건수"
      threshold: "= 0"
      measurement_method: "백엔드(예: Checkstyle/SpotBugs) 및 프론트엔드(ESLint) 실행 결과의 오류 건수 합산"
      decision_criteria: "PASS/FAIL"
    - policy_id: "QPOL-04"
      quality_item: "권한/소유 정합성 오류(중복 소유/미소유 접근/구매 반영 누락)"
      threshold: "= 0"
      measurement_method: "구매/소유 관련 통합 테스트 및 시나리오 테스트에서 정합성 오류 검출 건수 집계"
      decision_criteria: "PASS/FAIL"
    - policy_id: "QPOL-05"
      quality_item: "업로드 파일 타입 검증 누락(허용되지 않은 MIME/확장자 업로드)"
      threshold: "= 0"
      measurement_method: "업로드 API에 대한 부정 테스트(금지 MIME/확장자)에서 허용 응답 발생 건수 집계"
      decision_criteria: "PASS/FAIL"

  recovery_policy:
    - policy_id: "RPOL-01"
      failure_type: "테스트 실패(단위/통합/E2E)"
      max_retry: 2
      allowed_rollback_scope: "해당 스테이지에서 추가된 코드/테스트/마이그레이션만 되돌림"
      auto_or_manual: "auto-preferred"
      allowed_strategies: ["Re-execution", "Correction"]
      escalation_condition: "동일 스테이지에서 연속 실패가 N >= 2이면 ESC-FAIL-N 적용"
    - policy_id: "RPOL-02"
      failure_type: "데이터/권한 정합성 실패(소유/구매/공개 상태 불일치)"
      max_retry: 1
      allowed_rollback_scope: "구매/소유/권한 관련 DB 변경 및 로직을 이전 체크포인트 기준으로 롤백"
      auto_or_manual: "manual"
      allowed_strategies: ["Re-stage", "Rollback"]
      escalation_condition: "논리/모델 변경이 수반되므로 stage_owner 수동 승인 필수, 필요 시 quest_owner로 ESC-RISK 에스컬레이션"
    - policy_id: "RPOL-03"
      failure_type: "미디어 저장/서빙 선택으로 인한 구현 리스크 발생(난이도 급상승/기술 부채 확대)"
      max_retry: 1
      allowed_rollback_scope: "저장/서빙 방식 결정 이전 상태로 되돌림(설계/구현 포함)"
      auto_or_manual: "manual"
      allowed_strategies: ["Re-stage", "Rollback"]
      escalation_condition: "risk_level >= 2이면 ESC-RISK 적용"
    - policy_id: "RPOL-04"
      failure_type: "요구사항 해석 불명확 또는 판정 불확실성 증가"
      max_retry: 1
      allowed_rollback_scope: "불확실성이 발생한 변경(요구사항/정의/테스트)을 해당 스테이지 범위 내에서 되돌림"
      auto_or_manual: "manual"
      allowed_strategies: ["Correction", "Re-stage"]
      escalation_condition: "uncertainty > 0.35이면 ESC-UNCERTAINTY 적용"

  traceability_policy:
    - policy_id: "TPOL-01"
      record_item: "요구사항-스테이지 매핑 기록(REQ-XXX ↔ STG-XX)"
      required_link: "requirements[].id → stages[].mapped_requirements"
      retention_period: "퀘스트 종료 후 6개월"
      storage_location: "/home/user/toy-media-app/docs/traceability/req-stage-map.md"
    - policy_id: "TPOL-02"
      record_item: "체크포인트 판정 근거(테스트 리포트/로그/스크린샷/재현 절차)"
      required_link: "CP-STG-XX → evidence bundle"
      retention_period: "퀘스트 종료 후 6개월"
      storage_location: "/home/user/toy-media-app/docs/evidence/CP-STG-XX/"
    - policy_id: "TPOL-03"
      record_item: "DB 스키마 변경 이력 및 마이그레이션 파일"
      required_link: "스테이지 산출물 → migration id"
      retention_period: "영구"
      storage_location: "/home/user/toy-media-app/db/migration/"
    - policy_id: "TPOL-04"
      record_item: "API 계약(OpenAPI) 및 변경 이력"
      required_link: "스테이지 산출물 → openapi spec"
      retention_period: "퀘스트 종료 후 6개월"
      storage_location: "/home/user/toy-media-app/docs/api/openapi.yaml"

handoff:
  next_template: stage-spec.template
  payload:
    quest_id: "QST-20260216-001"
    quest_owner: "undefined"
    quest_goal: "Spring Boot + PostgreSQL + Svelte로 이미지/동영상 파일을 3Depth로 관리하고(보기/편집), 업로드·공개 설정·검색·구매·구매내역 확인까지 가능한 학습용 토이 웹앱을 구현한다."
    domain: "software development (web application)"
    stage_list: [STG-01, STG-02, STG-03]
    quest_plan_ref: "quest-plan.yaml"
  instruction: >
    Feed quest-seed.yaml + quest-plan.yaml + stage-spec.template.md
    into your next AI call. Run stage-spec once per stage.

self_validation:
  all_stages_have_gate_and_approver: true
  escalation_rules_defined: true
  no_role_overlap: true
  gate_types_valid: true
  all_dependencies_artifact_based: true
  no_circular_dependencies: true
  all_fail_branches_have_recovery: true
  all_quality_criteria_pass_fail: true
  no_ambiguous_language: true
  recovery_retry_and_rollback_defined: true
  policy_ids_referenceable: true
</attached_file>

Target stage: STG-01
</input>

<instructions>
Produce a stage specification by following these 9 steps.
Your final output MUST be a single YAML document matching the schema in <output_format>.

## Step 1: Write Metadata

From quest-seed.yaml and quest-plan.yaml, extract:
- quest_id, stage_id, stage_name, requirement_ids
- stage_owner: use "stage_owner" role from quest-plan governance.roles

## Step 2: Define Purpose and Scope

Write a single-sentence purpose statement based on quest-seed.yaml's stages[target].purpose.

**Rules:**
- Must be testable (can determine PASS/FAIL)
- Must describe WHAT this stage achieves, not HOW
- scope_included: what is covered by this stage
- scope_excluded: what is explicitly NOT part of this stage (boundaries)

## Step 3: Define Input Contract

From quest-plan.yaml stage_map.dependencies[target]:
- If predecessor_stage_id = "none" → input_item: "none", artifact_id: "none"
- Otherwise → specify the predecessor's output artifact as this stage's input

## Step 4: Define Output Contract

Based on quest-seed.yaml stages[target].key_artifact:
- Define concrete artifacts this stage must produce
- artifact_id format: ART-STG-XX-NNN
- Each artifact must have a clear contract_specification (format, structure, content)

## Step 5: Define Evaluation Criteria

For each mapped requirement, define PASS/FAIL-decidable criteria:
- Reference QPOL-XX from quest-plan.yaml policies.quality_policy
- Each criterion must have a quantitative pass_threshold
- measurement_method must be specific (automated test, manual verification, etc.)

**Forbidden:** "generally good", "adequate", "user-friendly", "appropriate"

## Step 6: Define Checkpoint Policy

From quest-plan.yaml governance.gates[target]:
- checkpoint_id: CP-STG-XX
- gate_id: GATE-STG-XX
- gate_type: from quest-plan gates
- final_approver: from quest-plan gates
- evaluation_policy_references: list of QPOL-XX used in evaluation criteria
- recovery_policy_reference: primary RPOL-XX for this stage's failure type

## Step 7: Define Handoff

From quest-plan.yaml stage_map.branch_rules[target]:
- next_stage_id: from on_pass (or "END" for last stage)
- handoff_artifacts: list of artifact_ids from output_contract
- handoff_evidence: EVD-STG-XX-NNN format

## Step 8: Define Recovery Mapping

From quest-plan.yaml policies.recovery_policy:
- Map failure types relevant to this stage
- Reference RPOL-XX
- Strategies MUST be from: Re-execution / Correction / Re-stage / Rollback
- Define escalation_trigger linking to ESC rules

## Step 9: Self-Validation

Verify ALL items before outputting. If any fails, fix it first.

- Purpose statement is single sentence and testable.
- Input/output contracts are concrete and verifiable.
- All evaluation criteria are PASS/FAIL-decidable (no ambiguous language).
- All criteria reference QPOL policy_ids from quest-plan.
- Checkpoint gate_type matches quest-plan gates.
- Recovery strategies reference RPOL_ids from quest-plan.
- Handoff fields (next_stage_id, artifacts, evidence) are complete.
- SOLID principles applied (single responsibility, contracts, no overlap).
</instructions>

<output_format>
Output a SINGLE YAML document. No markdown, no prose, no explanations outside the YAML.

**Language rule:** All human-readable text (descriptions, scopes, criteria) MUST be in the
same language as the quest-seed.yaml content. YAML keys remain in English.

**YAML Schema — follow this structure EXACTLY. Do not add, remove, rename, or reorder keys.**

```yaml
# SSDAM Stage Specification
# source_template: stage-spec.template
# schema_version: v0.2.0
# input_files: [quest-seed.yaml, quest-plan.yaml]

metadata:
  quest_id: "from quest-seed.yaml"
  stage_id: "STG-XX"
  stage_name: "from quest-seed.yaml"
  document_id: stage-spec
  stage_owner: "stage_owner"
  version: "v0.1.0"
  timestamp: "ISO 8601"
  requirement_ids: [REQ-XXX, REQ-YYY]  # from quest-seed stages[target].mapped_requirements

purpose:
  statement: "단일 문장의 테스트 가능한 목적"  # 언어 규칙 준수
  scope_included:
    - "이 스테이지가 포함하는 범위"
  scope_excluded:
    - "이 스테이지가 명시적으로 제외하는 범위"

input_contract:  # 첫 번째 스테이지는 input_item: "none", artifact_id: "none"
  - input_item: "입력 항목 설명"
    artifact_id: "from predecessor stage output or none"
    contract_requirement: "입력이 충족해야 할 구조/내용 조건"

output_contract:  # artifact_id 형식: ART-STG-XX-NNN
  - output_artifact: "산출물 설명"
    artifact_id: "ART-STG-XX-001"
    contract_specification: "형식/구조/내용 요구사항"

evaluation_criteria:
  - criterion_id: "CRIT-01"
    criterion: "평가 기준 설명"  # 언어 규칙 준수
    policy_reference: "QPOL-XX"  # from quest-plan quality_policy
    measurement_method: "측정 방법"
    pass_threshold: "정량적 기준"  # PASS/FAIL 판정 가능해야 함

checkpoint:
  checkpoint_id: "CP-STG-XX"
  gate_id: "GATE-STG-XX"  # from quest-plan gates
  gate_type: "automatic/human/hybrid"  # from quest-plan gates
  final_approver: "role_id"  # from quest-plan gates
  evaluation_policy_references: [QPOL-XX]  # 이 스테이지에서 사용하는 QPOL 목록
  recovery_policy_reference: "RPOL-XX"  # 이 스테이지 실패 시 적용할 RPOL

handoff:
  next_stage_id: "STG-XX or END"  # from quest-plan branch_rules on_pass
  handoff_artifacts: [ART-STG-XX-001]  # output_contract의 artifact_id 목록
  handoff_evidence: [EVD-STG-XX-001]  # 이 스테이지에서 생성되는 증적 ID

recovery_mapping:  # failure_type은 quest-seed.yaml과 같은 언어로 작성
  - failure_type: "실패 유형 설명"  # 언어 규칙 준수
    rpol_reference: "RPOL-XX"  # from quest-plan recovery_policy
    max_retry: 2
    recovery_strategy: "Re-execution/Correction/Re-stage/Rollback"  # 표준 용어만 사용
    escalation_trigger: "에스컬레이션 조건"  # 언어 규칙 준수

self_validation:
  purpose_single_sentence_testable: true/false
  input_output_contracts_verifiable: true/false
  all_criteria_pass_fail_decidable: true/false
  all_criteria_reference_policy_ids: true/false
  checkpoint_gate_type_valid: true/false
  recovery_references_rpol_ids: true/false
  handoff_fields_complete: true/false
  solid_principles_applied: true/false
```

**CRITICAL RULES:**
1. Output ONLY valid YAML. No markdown headers, no commentary, no explanations.
2. Do NOT wrap the output in code fences (``` or ```yaml). Output raw YAML directly.
3. Every key shown above MUST appear in your output.
4. Do NOT add keys not shown in the schema.
5. All string values containing special characters (colons, #, commas, etc.) MUST be quoted.
6. Multi-line strings MUST use YAML block scalar (> or |).
7. Indentation MUST use 2 spaces consistently. No tabs.
8. The output MUST be parseable by any standard YAML parser (e.g., PyYAML, SnakeYAML, js-yaml).
9. **NESTED QUOTE PROHIBITION:** A double-quoted string MUST NOT contain inner double quotes.
   - BAD:  `escalation_trigger: "N이 "N >= 2"이면 적용"`  ← parser error
   - GOOD: `escalation_trigger: "N >= 2이면 적용"`  ← inner quotes removed
   - GOOD: `escalation_trigger: >-`  (block scalar, then value on next line)
   If a value references another field's quoted content, drop the inner quotes or use `>-` block scalar.

**OUTPUT DELIVERY:**
If the AI tool supports file output (e.g., Claude Artifacts, ChatGPT Canvas, file download),
deliver the output as a downloadable file named `stage-spec.STG-XX.yaml`.
If file output is not available, output raw YAML text directly (no code fences).
</output_format>

결과를 다운로드 할 수 있는 파일로 작성해줘.
