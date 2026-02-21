# 🛠 Task 설계 가이드 — Task Design Guide

## 1. 개요 (Overview)

본 문서는 **SSDAM Task를 처음부터 설계하는 실무 절차**를 정의한다.

본 가이드는:

- `02_core_concepts/`의 불변 규칙을 전제로 하며
- `03_architecture/`의 구조 모델을 따른다

설계 흐름:

```
Purpose 정의 → Contract 설계 → Evaluation 기준 → Checkpoint Policy → Recovery Strategy → 설계 검증
```

---

## 2. Step 1 — Purpose 정의

Task 설계는 반드시 **단일 Purpose 정의**로 시작한다.

### 2.1 필수 항목

| 항목 | 설명 | 예시 |
|------|------|------|
| Purpose | Task의 목표 | "REST API 엔드포인트 구현" |
| Scope | 책임 범위 | "엔드포인트 로직만 포함. 배포 제외." |
| Completion Criteria | 완료 판단 기준 | "모든 엔드포인트 컴파일 및 테스트 통과" |

---

### 2.2 검증 질문

- Purpose가 한 문장으로 설명 가능한가?
- 여러 관심사가 섞여 있지는 않은가?
- Completion Criteria가 검증 가능한가?

---

### 2.3 안티패턴

❌ "백엔드 전체 구현"  
❌ "코드 + 테스트 + 배포"  
✅ "API 엔드포인트 구현"

---

## 3. Step 2 — Contract 설계

Purpose 정의 이후:

- **Input Contract**
- **Output Contract**

를 설계한다.

---

### 3.1 Input Contract

Task 진입 조건 정의:

| 항목 | 설명 |
|------|------|
| Required Artifacts | 선행 산출물 |
| Format | 구조 / 스키마 |
| Quality Conditions | 최소 품질 기준 |
| Additional Inputs | Requirement / Policy / Constraint |

예시:

```
Input Contract:

* api-spec.yaml (Checkpoint PASS)
* constraints.md
```

---

### 3.2 Output Contract

Task 결과 정의:

| 항목 | 설명 |
|------|------|
| Artifact List | 생성 대상 |
| Format | 요구 구조 |
| Quality Criteria | PASS 기준 |
| Metadata | ID / Version / Timestamp |

예시:

```
Output Contract:

* compiled-service
* test-report.json
```

---

### 3.3 설계 원칙

- 불필요 Input 포함 금지
- Downstream 미사용 Output 강제 금지
- 구현이 아닌 구조/포맷 의존

---

## 4. Step 3 — Evaluation 기준 정의

Execution 이전에 평가 기준을 정의한다.

---

### 4.1 Evaluation 유형

| 유형 | 사용 시점 |
|------|-----------|
| Contract Validation | 포맷/스키마 검증 |
| Quality Validation | 메트릭/Threshold |
| Policy Validation | 규칙/컴플라이언스 |
| Human Review | 맥락 판단 |
| Agent Evaluation | 자동화 평가 |

---

### 4.2 정량 기준 (Quantitative Criteria)

| 기준 | Threshold | 측정 방식 |
|------|-----------|------------|
| Test Pass Rate | ≥ 95% | CI Report |
| Coverage | ≥ 80% | Coverage Tool |
| Latency (P95) | ≤ 200ms | Benchmark |
| Critical Issues | 0 | Scanner |

---

### 4.3 정성 기준 (Qualitative Criteria)

예시:

```
Architecture Consistency:

* 설계 근거 설명 가능
* Constraint 준수 확인 가능
```

---

### 4.4 검증 질문

- PASS / FAIL 결정 가능한가?
- 기준이 모호하지 않은가?
- Evidence로 정당화 가능한가?

---

## 5. Step 4 — Checkpoint Policy 정의

PASS / FAIL 결정 구조 정의.

---

### 5.1 Gate 유형

| 유형 | 적용 조건 |
|------|------------|
| Automated Policy Gate | 결정적 정량 기준 |
| Human Approval Gate | 고위험 / 불확실 |
| Hybrid Gate | 혼합 판단 |

---

### 5.2 Policy 필수 정의

- PASS 조건
- FAIL 조건
- 판단 권위 주체
- 기록 데이터

---

## 6. Step 5 — Recovery Strategy 사전 정의

실패 대응 전략을 사전에 설계한다.

---

### 6.1 예상 실패 유형

| Failure Type | Example |
|-------------|----------|
| Validation Failure | 테스트 실패 |
| Contract Violation | 포맷 불일치 |
| Missing Evidence | 로그 누락 |
| Quality Failure | 기준 미달 |
| Logical Failure | 설계 불일치 |
| Dependency Failure | 외부 장애 |

---

### 6.2 Recovery 매핑

| Failure | Strategy |
|---------|----------|
| Validation Failure | 수정 → 재평가 |
| Contract Violation | 구조 수정 |
| Missing Evidence | 보완 |
| Quality Failure | 리팩터링 |
| Logical Failure | 재설계 |
| Dependency Failure | 재시도 / Fallback |

---

### 6.3 Escalation 규칙

- Retry 제한 횟수
- Human 개입 조건
- Uncertainty Threshold

---

## 7. Step 6 — 설계 검증

### 7.1 SSDAM 호환 체크리스트

**Purpose**

- [ ] 단일 목적 정의
- [ ] 한 문장 명확성
- [ ] 검증 가능한 완료 기준

**Contracts**

- [ ] Input Contract 정의
- [ ] Output Contract 정의
- [ ] 불필요 IO 없음
- [ ] 포맷 명시

**Evaluation**

- [ ] 평가 유형 정의
- [ ] Threshold 정의
- [ ] PASS/FAIL 결정 가능
- [ ] Evidence 기반 가능

**Checkpoint**

- [ ] Gate 유형 선택
- [ ] PASS/FAIL 조건 정의
- [ ] 판단 권위 정의

**Recovery**

- [ ] 실패 유형 정의
- [ ] 전략 매핑 완료
- [ ] Escalation 정의

---

## 8. Task 설계 템플릿

```md
# Task: [Task Name]

## Purpose
[한 문장]

## Scope
- Included:
- Excluded:

## Input Contract
| Artifact | Format | Source |

## Output Contract
| Artifact | Format | Usage |

## Evaluation Criteria
| Type | Criterion | Threshold | Measurement |

## Checkpoint Policy
- Gate Type:
- PASS Conditions:
- FAIL Conditions:
- Decision Authority:

## Recovery Strategy
| Expected Failure | Strategy |

## Escalation
- Retry Limits:
- Human Intervention Conditions:
```

---

## 9. Practical Example

### Task: REST API 엔드포인트 구현

**Purpose:**  
정의된 API Spec 기반 엔드포인트 구현

**Scope:**

- Included: Endpoint Logic
- Excluded: Deployment

**Input Contract:**

| Artifact | Format |
|----------|--------|
| api-spec.yaml | YAML |
| schema.mmd | Mermaid |

**Output Contract:**

| Artifact | Format |
|----------|--------|
| compiled-service | Binary |
| test-report.json | JSON |

**Evaluation Criteria:**

| Type | Criterion | Threshold |
|------|-----------|-----------|
| Contract Validation | API 준수 | 100% |
| Quality Validation | Tests PASS | ≥ 95% |
| Agent Evaluation | Static Analysis | PASS |

**Checkpoint Policy:**

- PASS: 모든 Validation PASS
- FAIL: 하나라도 기준 미충족

**Recovery Strategy:**

| Failure | Strategy |
|---------|----------|
| Test FAIL | 수정 → 재실행 |
| Contract 위반 | 구조 수정 → 재검증 |

---

## ✅ 핵심 요약 (Key Summary)

Task 설계는:

> **활동 목록 정의가 아니라  
> Purpose · Contract · Evaluation · Recovery 구조를 사전에 고정하는 작업이다.**

설계가 불완전하면:

→ 실행 혼란  
→ 결정 비결정성  
→ Traceability 붕괴
