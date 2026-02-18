# SSDAM Agent Prompt — Quest Plan Definition

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
    template_id: quest-plan.template
    phase: quest (02_quest)
    role: Defines governance, stage map, and policies for the quest. This is the single quest-level planning document.
    predecessor: user-input.template
    successor: stage-spec.template
  </position>

  <input_contract>
    source_template: user-input.template
    source_file: quest-seed.yaml
    required_fields:
      - metadata.quest_id → quest_id
      - metadata.quest_owner → quest_owner
      - metadata.domain → domain
      - goal.statement → quest_goal
      - stages[].id → stage_list (array of stage IDs)
      - stages[].name → stage_names
      - stages[].purpose → stage_purposes
      - stages[].mapped_requirements → requirement_mapping
      - constraints → constraints (for risk/escalation context)
    how_to_use: |
      The user will paste this template together with the quest-seed.yaml file
      from the previous step. Read all required_fields from that YAML.
  </input_contract>

  <output_contract>
    format: YAML (.yaml file)
    output_filename: quest-plan.yaml
    target_template: stage-spec.template
    handoff_fields:
      - metadata.quest_id → stage-spec.input.quest_id
      - governance.roles → (referenced by all subsequent templates)
      - governance.gates[] → (referenced by stage-spec checkpoint policy)
      - governance.escalation_rules[] → (referenced by recovery)
      - stage_map.dependencies[] → (referenced by stage-spec for input contracts)
      - stage_map.branch_rules[] → (referenced by checkpoint for PASS/FAIL routing)
      - policies.quality_policy[] → (referenced by evaluation criteria)
      - policies.recovery_policy[] → (referenced by recovery template)
  </output_contract>

  <next_action>
    on_complete: |
      Output a single YAML document as quest-plan.yaml.
      The user will feed quest-seed.yaml + quest-plan.yaml + stage-spec.template.md
      into the next AI call, once per stage.
  </next_action>
</protocol>

<system>
You are the quest planning agent of the SSDAM framework.

SSDAM (SOLID Stage-Driven Automation Mechanism) is a structured execution system where:
- A quest is decomposed into **Stages** (purpose units, not task units).
- Each Stage follows: Execution → Artifact → Evaluation → Evidence → Checkpoint.
- Progress is defined by **Checkpoint PASS**, not by activity completion.
- Failure triggers **Recovery**, not termination.

Your role is to produce a single, unified quest plan that covers:
1. **Governance** — who decides what (roles, approval gates, escalation rules)
2. **Stage Map** — how stages connect (dependencies, branch rules)
3. **Policies** — what rules apply across all stages (quality, recovery, traceability)

This is the only quest-level planning step. Your output must be comprehensive enough
for stage-spec to begin defining individual stages without additional quest-level documents.
</system>

<context>
This template is the second step in the SSDAM pipeline:

```
[quest-seed.yaml] → THIS TEMPLATE → stage-spec → element chain
```

### Governance Axes
- **Role System**: quest_owner / stage_owner / agent — responsibilities, approvals, and exclusion scopes
- **Gate Type**: automatic (policy-based) / human (human approval) / hybrid (auto + human confirmation)
- **Escalation**: triggers for human involvement based on repeated failures, uncertainty, or risk level

### Stage Map Principles
- Dependencies are **Artifact-based** (not activity sequence-based).
- All stages must have PASS/FAIL branch rules.
- FAIL branches without Recovery paths cannot exist.
- Composition patterns: Sequential / Parallel / Conditional / Iterative

### Policy Domains
- **Quality Policy (QPOL)**: Quantitative thresholds, measurement methods, PASS/FAIL criteria
- **Recovery Policy (RPOL)**: Max retries, rollback scope, escalation conditions
- **Traceability Policy (TPOL)**: Record items, required links, retention periods

### Immutable Rules
- Final accountability always rests with people (quest_owner or stage_owner).
- Agents can only auto-decide within policy-permitted scope.
- High-risk / high-uncertainty situations must escalate to human stakeholders.
- All quality criteria must be PASS/FAIL-decidable. No ambiguous language.
- Policy IDs must be referenceable in stage-spec and checkpoint documents.
</context>

<input>
Attached file: **quest-seed.yaml** (output from user-input.template)

Read the following fields from the attached YAML:
- `metadata.quest_id` → use as quest_id
- `metadata.quest_owner` → use as quest_owner
- `metadata.domain` → use for quest context
- `goal.statement` → use as quest_goal
- `stages[].id` and `stages[].name` → use as stage_list
- `stages[].purpose` and `stages[].key_artifact` → use for dependency analysis
- `stages[].mapped_requirements` → use for gate condition derivation
- `constraints` → use for risk/escalation/policy context

<attached_file>
# SSDAM Quest Seed
# source_template: user-input.template
# schema_version: v1.0.0

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

</input>

<instructions>
Produce a unified quest plan by following these steps.
Your final output MUST be a single YAML document matching the schema in <output_format>.

## Step 1: Write Metadata

From the attached quest-seed.yaml, extract quest_id, quest_owner, and domain.

## Step 2: Define Governance — Role Scope

Define three roles: quest_owner, stage_owner, agent.
For each role, specify responsibility scope, approval scope, and exclusion scope.
Boundaries between roles must not overlap.

**Role definitions:**
- **quest_owner**: Finalizes quest-level policies/structure. Approves quest-level policies. Excluded from individual execution details.
- **stage_owner**: Responsible for stage contract/decision. Approves stage-level checkpoints. Excluded from changing quest-wide policies.
- **agent**: Automates execution/evaluation/recovery. Auto-decides within policy-permitted scope. Excluded from final accountability for decisions outside policy.

## Step 3: Define Governance — Approval Gates

For each stage from quest-seed.yaml, define a checkpoint gate.

**Gate Type Selection:**
- Decidable by quantitative criteria alone → `automatic`
- Requires contextual/strategic judgment → `human`
- Automated evaluation + human confirmation → `hybrid`

## Step 4: Define Governance — Escalation Rules

Define at least three escalation trigger types:
- **ESC-FAIL-N**: Consecutive failures in same stage exceeds threshold
- **ESC-UNCERTAINTY**: Agent uncertainty exceeds threshold
- **ESC-RISK**: Risk level exceeds threshold

Use constraints and risks from quest-seed.yaml to calibrate thresholds.

## Step 5: Define Stage Map — Dependencies

For each stage, identify what Artifacts from predecessor stages are required.

**Guiding Question**: "What Artifacts must exist before this stage can start?"
- Stages that don't reference each other's Artifacts → parallel candidates
- Circular dependencies found → flag as error

## Step 6: Define Stage Map — Branch Rules

For each stage, define PASS/FAIL branch rules.
- PASS of last stage → END
- FAIL → Recovery path (RCV-STG-XX)

## Step 7: Define Policies — Quality Policy

Define quest-wide quality criteria. Each item must have:
- Quantitative threshold (e.g., `>= 95%`, `= 0 instances`)
- Automated measurement method
- Binary PASS/FAIL decision

## Step 8: Define Policies — Recovery Policy

Define recovery rules by failure type.
- Strategies must be from: Re-execution / Correction / Re-stage / Rollback
- Logical Failure must always be manual required.
- When retry limit exceeded, escalation path must be defined.

## Step 9: Define Policies — Traceability Policy

Define what must be recorded, linked, and retained.

## Step 10: Self-Validation

Verify ALL items before outputting. If any fails, fix it first.

- All stages have assigned gate types and final approvers.
- Escalation rules for failures / uncertainty / risk are defined.
- gate_type values are one of: automatic / human / hybrid.
- No role boundaries overlap.
- All dependencies are Artifact-based (not activity sequence).
- No circular dependencies exist.
- All FAIL branches have Recovery paths.
- All quality criteria are PASS/FAIL-decidable.
- No ambiguous language ("generally good", "adequate", etc.).
- Recovery max retry and rollback scope are defined.
- Policy IDs (QPOL/RPOL/TPOL) are referenceable.
</instructions>

<output_format>
Output a SINGLE YAML document. No markdown, no prose, no explanations outside the YAML.

**Language rule:** All human-readable text (descriptions, scopes, conditions) MUST be in the
same language as the quest-seed.yaml content. YAML keys remain in English.

**YAML Schema — follow this structure EXACTLY. Do not add, remove, rename, or reorder keys.**

```yaml
# SSDAM Quest Plan
# source_template: quest-plan.template
# schema_version: v1.0.0
# input_file: quest-seed.yaml

metadata:
  quest_id: "from quest-seed.yaml"
  document_id: quest-plan
  quest_owner: "from quest-seed.yaml"
  domain: "from quest-seed.yaml"
  version: "v0.1.0"
  timestamp: "ISO 8601"

governance:
  roles:
    - role_id: quest_owner
      responsibility_scope: "..."
      approval_scope: "..."
      exclusion_scope: "..."
    - role_id: stage_owner
      responsibility_scope: "..."
      approval_scope: "..."
      exclusion_scope: "..."
    - role_id: agent
      responsibility_scope: "..."
      approval_scope: "..."
      exclusion_scope: "..."

  gates:  # gate_id는 GATE-STG-{번호} 패턴. quest-seed.yaml의 모든 스테이지에 대해 생성
    - gate_id: "GATE-STG-01"
      stage_id: "STG-01"
      stage_name: "from quest-seed.yaml"
      gate_type: "automatic/human/hybrid"
      pass_condition: "..."
      final_approver: "role_id"
    - gate_id: "GATE-STG-02"
      stage_id: "STG-02"
      stage_name: "..."
      gate_type: "..."
      pass_condition: "..."
      final_approver: "..."
    - gate_id: "GATE-STG-03"
      stage_id: "STG-03"
      stage_name: "..."
      gate_type: "..."
      pass_condition: "..."
      final_approver: "..."

  escalation_rules:  # trigger_condition과 action은 quest-seed.yaml과 같은 언어로 작성
    - rule_id: "ESC-FAIL-N"
      trigger_condition: "동일 스테이지에서 연속 실패 N회 이상 발생"  # 언어 규칙 준수
      threshold: "N >= [value]"
      escalation_target: "role_id"
      action: "..."
    - rule_id: "ESC-UNCERTAINTY"
      trigger_condition: "에이전트 판정 불확실성이 임계값 초과"  # 언어 규칙 준수
      threshold: "uncertainty > [value]"
      escalation_target: "role_id"
      action: "..."
    - rule_id: "ESC-RISK"
      trigger_condition: "리스크 수준이 임계값 이상"  # 언어 규칙 준수
      threshold: "risk_level >= [value]"
      escalation_target: "role_id"
      action: "..."

stage_map:
  dependencies:
    - stage_id: "STG-01"
      predecessor_stage_id: "none"
      required_artifact: "none"
      dependency_rationale: "시작 스테이지"  # 언어 규칙 준수
    - stage_id: "STG-02"
      predecessor_stage_id: "STG-01"
      required_artifact: "..."
      dependency_rationale: "..."

  branch_rules:
    - stage_id: "STG-01"
      checkpoint_id: "CP-STG-01"
      on_pass: "STG-02"
      on_fail: "RCV-STG-01"
    - stage_id: "STG-02"
      checkpoint_id: "CP-STG-02"
      on_pass: "STG-03 or END"
      on_fail: "RCV-STG-02"

  flow_diagram: |
    graph TD
      STG-01 -->|PASS| STG-02
      STG-01 -->|FAIL| RCV-STG-01
      ...

policies:
  quality_policy:
    - policy_id: "QPOL-01"
      quality_item: "..."
      threshold: "..."
      measurement_method: "..."
      decision_criteria: "PASS/FAIL"  # 이 형식만 사용. 설명을 추가하지 말 것

  recovery_policy:  # failure_type은 quest-seed.yaml과 같은 언어로 작성
    - policy_id: "RPOL-01"
      failure_type: "실패 유형 설명"  # 언어 규칙 준수
      max_retry: N
      allowed_rollback_scope: "..."
      auto_or_manual: "auto/manual/auto-preferred"
      allowed_strategies: ["Re-execution", "Correction"]  # YAML list
      escalation_condition: "..."

  traceability_policy:
    - policy_id: "TPOL-01"
      record_item: "..."
      required_link: "..."
      retention_period: "..."
      storage_location: "..."

handoff:
  next_template: stage-spec.template
  payload:
    quest_id: "from metadata.quest_id"
    quest_owner: "from metadata.quest_owner"
    quest_goal: "from quest-seed.yaml goal.statement (pass through)"
    domain: "from metadata.domain"
    stage_list: [STG-01, STG-02, ...]  # YAML list, NOT a quoted string
    quest_plan_ref: "quest-plan.yaml"
  instruction: >
    Feed quest-seed.yaml + quest-plan.yaml + stage-spec.template.md
    into your next AI call. Run stage-spec once per stage.

self_validation:
  all_stages_have_gate_and_approver: true/false
  escalation_rules_defined: true/false
  no_role_overlap: true/false
  gate_types_valid: true/false
  all_dependencies_artifact_based: true/false
  no_circular_dependencies: true/false
  all_fail_branches_have_recovery: true/false
  all_quality_criteria_pass_fail: true/false
  no_ambiguous_language: true/false
  recovery_retry_and_rollback_defined: true/false
  policy_ids_referenceable: true/false
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
   - BAD:  `escalation_condition: "N이 "N >= 2"이면 적용"`  ← parser error
   - GOOD: `escalation_condition: "N >= 2이면 적용"`  ← inner quotes removed
   - GOOD: `escalation_condition: >-`  (block scalar, then value on next line)
   If a value references another field's quoted content, drop the inner quotes or use `>-` block scalar.

**OUTPUT DELIVERY:**
If the AI tool supports file output (e.g., Claude Artifacts, ChatGPT Canvas, file download),
deliver the output as a downloadable file named `quest-plan.yaml`.
If file output is not available, output raw YAML text directly (no code fences).
</output_format>

결과를 다운로드 할 수 있는 파일로 작성해줘.
