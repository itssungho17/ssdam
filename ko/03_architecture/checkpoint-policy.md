# 🚦 Checkpoint Policy — 판단 게이트 프레임워크

## 1. 개요 (Overview)

본 문서는 SSDAM에서 **Checkpoint 평가를 지배하는 정책, 규칙, 판단 기준**을 정의한다.

Checkpoint는 다음을 결정하는 **유일한 권위 메커니즘**이다:

- Task 종료
- PASS / FAIL 결정
- 상태 전이
- 다음 진행 승인

---

## 2. Checkpoint 정의 (Definition)

**Checkpoint:**

> Task가 정의된 완료 기준을 충족했는지  
> Artifact, Evaluation, Evidence를 기반으로 판단하는 공식 결정 게이트

Checkpoint 판단은 반드시:

- 명시적이어야 하며
- Evidence 기반이어야 하며
- Policy에 의해 지배되어야 하며
- Traceable 해야 한다

---

## 3. PASS / FAIL 배타성

**불변 규칙 (Immutable Rules):**

- PASS 또는 FAIL만 허용
- 조건부 PASS 금지
- 암묵적 PASS 금지
- 검증 유예 금지

❌ "일단 진행"  
❌ "문제 없어 보임"  
✅ PASS / FAIL 만 허용

---

## 4. 판단 입력 요소 (Decision Inputs)

Checkpoint 평가 필수 입력:

| 입력 | 설명 |
|------|------|
| Artifact | Execution 결과 |
| Evaluation Result | 기준 충족 여부 |
| Evidence | 판단 근거 |
| Policy Criteria | 판단 규칙 |
| Constraints | 품질 / 리스크 / 범위 제한 |

필수 입력 누락 → Checkpoint 무효

---

## 5. Evidence 충분성 규칙

**규칙:**

> 충분한 Evidence 없는 PASS 금지

Evidence 요구 조건:

- 객관성
- 재현 가능성 (해당 시)
- 출처 식별 가능
- Timestamp 포함

---

## 6. Checkpoint 유형

### 6.1 Automated Checkpoint

정책 엔진 / 룰 시스템 기반 판단.

적용 조건:

- 높은 결정성
- 명확한 기준
- 정량 평가 가능

---

### 6.2 Human Checkpoint

Reviewer / Owner 판단.

적용 조건:

- 높은 불확실성
- 고위험 결정
- 해석 필요 상황

---

### 6.3 Hybrid Checkpoint

자동 평가 → Human 확인.

---

## 7. 판단 기준 범주

Checkpoint는 다음을 평가 가능:

- Contract 준수
- 품질 기준선(Quality Threshold)
- Evidence 유효성
- 리스크 허용 범위
- 정책 제약
- 보안 / 컴플라이언스

---

## 8. 품질 기준선 강제

PASS 조건:

- Quality ≥ 정의된 Threshold

FAIL 조건:

- Quality 미달
- 메트릭 누락
- 측정 무효

---

## 9. 리스크 기반 Escalation

다음 조건 시 Human 판단 필수:

| 조건 | 조치 |
|------|------|
| Risk ≥ Threshold | Human Gate |
| Uncertainty ≥ Threshold | Human Validation |
| Evidence 충돌 | Human Arbitration |
| Policy 모호성 | Human Override |

---

## 10. FAIL 처리 정책

FAIL 시:

1. 결정 기록
2. Evidence 보존
3. Artifact 상태 보존
4. Recovery 트리거

FAIL → READY / PASS 암묵 전이 금지

---

## 11. PASS 처리 정책

PASS 시:

1. 결정 기록
2. Artifact Freeze (해당 시)
3. Evidence 연결
4. Next Task 승인

---

## 12. 판단 Traceability

Checkpoint 기록 필수 항목:

| 항목 | 설명 |
|------|------|
| Timestamp | 판단 시점 |
| Actor | Human / Agent / Policy |
| Inputs | Artifact / Evidence |
| Criteria | 적용 규칙 |
| Outcome | PASS / FAIL |
| Confidence | 선택 메타데이터 |
| Uncertainty | 선택 메타데이터 |

---

## 13. 안티패턴 (Anti-Patterns)

❌ Evidence 없는 PASS  
❌ 노력/활동 기반 PASS  
❌ 근거 없는 FAIL  
❌ 암묵적 판단  
❌ Checkpoint 우회  
❌ 사후 PASS 선언  

---

## ✅ 핵심 요약 (Key Summary)

Checkpoint Policy는 보장한다:

- 결정적 판단
- Evidence 기반 진행
- 명시적 PASS / FAIL 권위
- 통제된 Task 종료

Checkpoint는 승인 의식이 아니라:

> **검증 권위 메커니즘이다.**
