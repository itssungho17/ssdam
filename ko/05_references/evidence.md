# 📎 Evidence — 근거 정의

## 1. 개념 정의

**Evidence(근거)** 는  
Evaluation(평가) 결과를 **정당화하고 검증 가능하게 만드는 객관적 정보 집합**이다.

SSDAM에서 Evidence는:

> **“판단의 이유”가 아니라  
> “판단을 재현·검증할 수 있는 증거 구조”**

---

## 2. 역할

Evidence의 핵심 역할:

- 평가 결과 정당화
- 의사결정 검증 가능성 확보
- 체크포인트 판정 신뢰성 강화
- 추적성 체인 연결
- 실패 분석 가능성 제공

---

## 3. 위치 (Execution Model 내)

```

Execution → Artifact → Evaluation → Evidence → Checkpoint

```

Evidence는 Evaluation의 부산물이 아니라:

> **Checkpoint 판정의 필수 입력 요소**

---

## 4. Evidence 필수 속성

| 속성 | 설명 |
|------|------|
| **객관성** | 주관적 의견이 아닌 검증 가능한 정보 |
| **재현 가능성** | 동일 조건에서 동일 판단 가능 |
| **추적 가능성** | 출처 및 생성 과정 확인 가능 |
| **불변성** | 기록 후 임의 수정 금지 |
| **연결성** | Evaluation / Artifact와 링크 가능 |

---

## 5. Evidence 유형

### ✅ 5.1 정량 근거 (Quantitative)

- 테스트 통과율
- 성능 지표 (latency, memory, throughput)
- 커버리지
- 오류율
- 비용 수치

**예시**
```

API 응답 평균 82ms (SLA < 100ms 충족)
테스트 통과율 97.3%

```

---

### ✅ 5.2 정성 근거 (Qualitative)

- 리뷰 승인 기록
- 설계 검토 의견
- UX 평가 결과
- 정책 적합성 판단

**예시**
```

Architecture Review PASS
Security Policy Compliance Confirmed

```

---

### ✅ 5.3 산출물 기반 근거 (Artifact-derived)

- 빌드 로그
- 테스트 리포트
- 정적 분석 결과
- CI/CD 결과

---

### ✅ 5.4 외부 검증 근거

- 감사 결과
- 사용자 테스트 결과
- 운영 메트릭
- 규제 적합성 문서

---

## 6. Evidence 품질 기준

Evidence는 단순 첨부 자료가 아니다.  
다음 기준을 충족해야 한다:

- 검증 가능
- 출처 명확
- 시점 기록 포함
- 변조 방지
- Evaluation과 직접 연결

---

## 7. Evidence 생성 원칙

### ✅ MUST

- Evaluation 결과와 1:1 대응
- 측정/판단 기준 명시
- 생성 시점 기록
- 원본 데이터 보존
- 링크 가능 구조 유지

---

### ❌ MUST NOT

- 모호한 표현  
  → "좋음", "괜찮음", "문제 없어 보임"

- 검증 불가능 주장  
  → "대체로 안정적"

- 근거 없는 PASS 선언

---

## 8. Evidence 라이프사이클

```

생성 → 기록 → 고정(Frozen) → 참조 → 감사/분석

```

| 단계 | 설명 |
|------|------|
| 생성 | Evaluation 수행 시 생성 |
| 기록 | 시스템/문서에 저장 |
| 고정 | 변경 금지 상태 |
| 참조 | Checkpoint / 추적성 / 회복에 사용 |
| 분석 | 실패 원인 / 품질 감사 |

---

## 9. Checkpoint와 관계

Checkpoint는 다음을 기반으로 판단한다:

- Artifact 존재 여부 ❌
- Activity 수행 여부 ❌
- **Evidence 충족 여부 ✅**

---

## 10. 실패와 Evidence

FAIL 발생 시 Evidence는:

- 실패 분류 기준 제공
- 원인 분석 자료
- 회복 전략 선택 근거
- 재평가 기준

---

## 11. 메타데이터 요구사항 (Agent 평가 포함)

AI/Agent 기반 Evidence는 추가 속성을 가진다:

| 항목 | 설명 |
|------|------|
| 신뢰도 (Confidence) | 평가 신뢰 수준 |
| 불확실성 (Uncertainty) | 판단 불확실성 |
| 평가 모델 | 사용된 Agent/Policy |
| 입력 데이터 범위 | 평가 대상 범위 |

---

## 12. 예시

### ✅ GOOD Evidence

```

Unit Test: 124 / 124 PASS
Coverage: 86.2%
P95 Latency: 94ms
Security Scan: No Critical Issues
Reviewer Approval: PASS

```

---

### ❌ BAD Evidence

```

테스트 잘 됨
속도 빠름
문제 없음

```

---

## 13. Anti-Patterns

| Anti-Pattern | 문제 |
|-------------|------|
| Opinion as Evidence | 주관적 판단 |
| Missing Source | 추적 불가 |
| Editable Evidence | 변조 위험 |
| Aggregated Without Context | 평가 기준 불명 |
| PASS Without Evidence | SSDAM 위반 |

---

## 14. 실전 체크리스트

### ✅ Evidence 준비 점검

- [ ] Evaluation 기준 명확
- [ ] 측정값 존재
- [ ] 출처 기록됨
- [ ] 시점 포함
- [ ] Artifact 연결됨
- [ ] 변경 불가 상태

---

## ✅ 핵심 요약

Evidence는:

> **“왜 PASS인가?”를 설명하는 문장이 아니라  
> “PASS가 검증 가능함을 증명하는 구조”**

SSDAM에서 신뢰는:

- 활동(Activity) ❌
- 산출물 존재 ❌
- **근거(Evidence) ✅**
