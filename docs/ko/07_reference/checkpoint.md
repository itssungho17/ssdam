# 🚦 Checkpoint — SSDAM Reference

## 1. 정의 (Definition)

**Checkpoint**는 스테이지 종료 시점에서 수행되는  
**PASS / FAIL 판정 메커니즘**이다.

SSDAM에서 Checkpoint는 단순 완료 확인이 아니라:

> **“상태 전이(State Transition)를 승인 또는 거부하는 결정 지점”**

이다.

---

## 2. 목적 (Purpose)

Checkpoint의 역할:

- 스테이지 종료 여부 결정
- 산출물 품질 검증
- 계약 준수 여부 확인
- 근거 기반 의사결정 강제
- 다음 스테이지 진행 통제
- 실패 이벤트 구조화

---

## 3. Checkpoint 위치

Checkpoint는 다음 흐름의 마지막 단계에 위치한다:

```

Execution → Artifact → Evaluation → Evidence → 🚦 Checkpoint

```

Checkpoint 이전 조건:

✔ 산출물 존재  
✔ 평가 수행 완료  
✔ 근거 확보 완료  

---

## 4. 판정 유형 (Decision Types)

| 판정 | 의미 | 결과 |
|------|------|------|
| **PASS** | 스테이지 목표 충족 | 다음 스테이지 진행 |
| **FAIL** | 목표 또는 계약 미충족 | 실패 기록 + Recovery |

---

## 5. PASS 조건

다음 조건을 모두 충족해야 한다:

- 정의된 목표 달성
- 산출물 계약 준수
- 평가 기준 통과
- 필수 근거 존재
- 품질 임계값 충족

PASS는 “작업 완료”가 아니라:

> **“검증된 상태 전이 승인”**

을 의미한다.

---

## 6. FAIL 조건

다음 중 하나 이상 해당 시 FAIL:

- 평가 기준 미달
- 산출물 계약 위반
- 근거 부족 또는 누락
- 품질 임계값 미달
- 위험 수준 허용치 초과

FAIL은 예외가 아니라:

> **“통제 가능한 실패 이벤트 선언”**

이다.

---

## 7. Checkpoint 구성 요소

Checkpoint는 다음 요소로 구성된다:

| 요소 | 설명 |
|------|------|
| **Input** | Artifact + Evaluation + Evidence |
| **Policy** | PASS / FAIL 판정 규칙 |
| **Decision** | PASS / FAIL |
| **Output** | 상태 전이 결과 |
| **Trace** | 판정 근거 기록 |

---

## 8. 정책 기반 판정 (Policy-Governed)

Checkpoint 판정은 반드시 **명시적 정책**에 의해 수행된다.

정책 예시:

- 품질 기준 (Coverage ≥ 80%)
- 성능 기준 (Latency ≤ 200ms)
- 규격 준수 (Schema Validation PASS)
- 리뷰 승인 (Human Approval)

정책 없는 Checkpoint는 SSDAM 위반이다.

---

## 9. Checkpoint 유형

| 유형 | 설명 |
|------|------|
| **자동 정책 게이트** | 규칙 기반 자동 판정 |
| **사람 승인 게이트** | 리뷰/승인 필요 |
| **하이브리드 게이트** | 자동 평가 + 사람 판단 |

---

## 10. 상태 전이 규칙

Checkpoint는 다음 상태 전이를 제어한다:

```

IN_PROGRESS → (PASS) → COMPLETED
IN_PROGRESS → (FAIL) → FAILED
FAILED → (Recovery) → RE-EXECUTION / RE-STAGE

```

---

## 11. 추적성 요구사항 (Traceability)

Checkpoint는 반드시 기록해야 한다:

- 판정 결과 (PASS / FAIL)
- 적용 정책
- 평가 요약
- 근거 링크
- 판정 시각
- 수행 주체 (Human / Agent / Policy)

---

## 12. 에이전트 환경에서의 역할

AI Agent가 Checkpoint에 관여할 경우:

필수 메타데이터:

- 신뢰도 (Confidence)
- 불확실성 (Uncertainty)
- 사용된 평가 기준
- 근거 출처

고위험 FAIL / 불확실성 증가 시:

→ Human Escalation

---

## 13. 안티 패턴 (Anti-Patterns)

❌ 산출물만 보고 PASS  
❌ 근거 없는 승인  
❌ 정책 없는 판정  
❌ FAIL 무시 후 다음 단계 진행  
❌ 평가 생략  

---

## 14. 핵심 원칙 요약

Checkpoint는:

> **“완료 확인 지점”이 아니라  
> “검증된 상태 전이 승인 장치”**

이다.

SSDAM에서:

- 완료 = PASS
- 실패 = FAIL
- 진행 = 승인된 전이

---

## ✅ 결론

Checkpoint는 SSDAM의 **품질 방어선**이며  
시스템 결정성을 보장하는 핵심 통제 메커니즘이다.