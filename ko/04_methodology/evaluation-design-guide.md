# 🔍 Evaluation 설계 가이드 — Evaluation Design Guide

## 1. 개요 (Overview)

본 문서는 SSDAM에서 **Evaluation 구조 설계 방법론**을 정의한다.

Evaluation은 Artifact가 다음을 충족하는지 판단한다:

- Contract 요구사항  
- 품질 기준선(Quality Threshold)  
- 정책 제약(Policy Constraints)  
- 리스크 허용 범위(Risk Tolerance)  

Evaluation 설계가 부실하면:

→ PASS/FAIL 비결정성  
→ Checkpoint 불안정  
→ 시스템 신뢰 붕괴

---

## 2. Evaluation 설계 목표

Evaluation 설계는 다음을 보장해야 한다:

- 결정적 판단 (Deterministic Judgment)  
- PASS / FAIL 명확성  
- Evidence 생성 가능성  
- Agent / Human 호환성  
- Traceability 보존  

---

## 3. Step 1 — Evaluation Purpose 정의

모든 Evaluation은 **명확한 검증 목적**을 가져야 한다.

| 항목 | 설명 |
|------|------|
| Validation Target | 평가 대상 |
| Evaluation Scope | 평가 제외 범위 |
| Decision Type | PASS / FAIL 기준 |

---

### Example

✅ "API Contract 준수 검증"  
❌ "구현이 좋아 보이는지 확인"

---

## 4. Step 2 — Evaluation 유형 선택

복수 Evaluation 유형 공존 가능

| 유형 | 목적 |
|------|------|
| Contract Validation | 포맷 / 스키마 검증 |
| Quality Validation | 메트릭 / Threshold |
| Policy Validation | 규칙 / 컴플라이언스 |
| Risk Evaluation | 리스크 허용 판단 |
| Human Review | 맥락 판단 |
| Agent Evaluation | 자동화 평가 |

---

## 5. Step 3 — PASS / FAIL 기준 정의

Evaluation 결과는 반드시:

> **Binary & Deterministic**

---

### 규칙

- PASS / FAIL בלבד  
- 모호한 표현 금지  
- Partial PASS 금지  
- 노력 / 활동 기반 판단 금지  

---

### Example

❌ "코드 품질 양호"  
✅ "Static Analysis Critical Issues = 0"

---

## 6. Step 4 — 정량 기준 정의 (Quantitative Criteria)

가능한 경우 측정 기반 기준 사용

| 기준 | Threshold | 측정 방식 |
|------|-----------|------------|
| Test Pass Rate | ≥ 95% | CI Report |
| Coverage | ≥ 80% | Coverage Tool |
| Latency (P95) | ≤ 200ms | Benchmark |
| Error Rate | ≤ 0.1% | Monitoring |

---

### 규칙

- Threshold 명시  
- Measurement 방식 명시  
- PASS/FAIL 경계 결정성 확보  

---

## 7. Step 5 — 정성 기준 정의 (Qualitative Criteria)

정량화 어려운 경우 판단 표준 정의

---

### Example

```
Architecture Consistency:

- 설계 근거 설명 가능  
- Constraint 정렬 검증 가능  
- Trade-off 문서화  
```

---

### 규칙

- 여전히 PASS/FAIL 결정 가능  
- 주관적 표현 최소화  
- Evidence 연결 가능  

---

## 8. Step 6 — Evidence 설계 정렬

Evaluation은 반드시:

> **Evidence 생성 가능 구조**

를 가져야 한다.

---

### Evidence Source 예시

- Test Report  
- Static Analysis Output  
- Review Record  
- Metrics / Logs  
- Policy Validation Result  

---

### 규칙

- Criteria ↔ Evidence 1:1 매핑  
- Evidence 출처 식별 가능  
- Timestamp 기록  

---

## 9. Step 7 — 결정성 확보 (Determinism Enforcement)

Evaluation은 보장해야 한다:

- 동일 입력 → 동일 판단  
- Criteria 명시  
- Hidden Heuristic 금지  

---

### 비결정 요소 처리

허용 조건:

- 확률적 평가 명시  
- Confidence Interval 정의  
- Human Checkpoint Escalation  

---

## 10. Step 8 — Agent / Human 호환성

Evaluation 설계 시 정의:

| 요소 | 규칙 |
|------|------|
| Agent Evaluation | Machine-parseable Criteria |
| Human Evaluation | 판단 가이드라인 |
| Hybrid Evaluation | 책임 분리 정의 |

---

### Agent 제약

- Confidence 메타데이터 출력  
- Uncertainty 메타데이터 출력  
- Evidence 기반 판단 בלבד  

---

## 11. Evaluation FAIL 조건

FAIL 발생 조건:

- Criteria 미충족  
- Evidence 부족  
- Measurement 무효  
- Policy 위반  
- Risk Threshold 초과  

---

## 12. Evaluation 설계 체크리스트

**Purpose**

- [ ] 검증 목적 정의  
- [ ] Scope 경계 정의  

**Criteria**

- [ ] PASS/FAIL 결정 가능  
- [ ] 정량 Threshold 명시  
- [ ] 정성 기준 명시  

**Evidence**

- [ ] Evidence Source 정의  
- [ ] Criteria 매핑 명확  

**Determinism**

- [ ] Criteria 결정성 확보  
- [ ] 모호한 표현 없음  

**Compatibility**

- [ ] Agent 파싱 가능 (자동 시)  
- [ ] Human 판단 가이드 존재 (수동 시)  

---

## 13. Evaluation 설계 템플릿

```md
# Evaluation: [Evaluation Name]

## Purpose
[검증 목적]

## Scope
- Included:
- Excluded:

## Evaluation Criteria
| Type | Criterion | Threshold | Measurement |

## PASS Conditions
- [...]

## FAIL Conditions
- [...]

## Evidence Mapping
| Criterion | Evidence Source |

## Determinism Rules
- [...]

## Actor Compatibility
- Agent / Human / Hybrid
```

---

## ✅ 핵심 요약 (Key Summary)

Evaluation 설계는:

> **의견 정의가 아니라  
> 결정적 검증 로직 구조화 작업이다.**

잘 설계된 Evaluation은:

- 임의 PASS/FAIL 방지  
- Checkpoint 안정화  
- Evidence 신뢰 확보  
- SSDAM 결정성 유지  
