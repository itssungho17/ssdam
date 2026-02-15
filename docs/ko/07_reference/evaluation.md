# 📏 Evaluation — 산출물 검증 메커니즘

## 1. 정의

**Evaluation**은 스테이지에서 생성된 **Artifact(산출물)** 이  
정의된 **계약(Contract)**, **품질 기준(Quality Criteria)**, **종료 조건(Exit Criteria)**  
을 충족하는지 판단하는 **검증 행위**이다.

SSDAM에서 Evaluation은:

> **“검토”가 아니라  
> “판정 가능한 검증 단계”**

---

## 2. 목적

Evaluation의 핵심 목적:

- 산출물의 유효성 검증
- 계약 준수 여부 판단
- 품질 임계값 확인
- PASS / FAIL 판정 근거 확보
- 다음 상태 전이 정당화

---

## 3. 위치 (Execution Flow 내 역할)

```

Execution → Artifact → **Evaluation** → Evidence → Checkpoint

```

Evaluation은:

- Artifact를 입력으로 받고
- 판정 결과를 생성하며
- Evidence 생성을 유도한다

---

## 4. 입력

Evaluation의 입력:

- 검증 대상 Artifact
- 스테이지 계약 / 요구사항
- 평가 기준 / 정책
- 품질 임계값
- 관련 Evidence (필요 시)

---

## 5. 출력

Evaluation의 출력:

- 평가 결과 (PASS / FAIL)
- 평가 리포트
- 생성 또는 연결된 Evidence
- 품질 지표 (Metric Snapshot)
- 리스크 / 불확실성 정보

---

## 6. Evaluation 유형

### ✅ 6.1 계약 검증 (Contract Evaluation)

검증 대상:

- 요구사항 충족 여부
- 입력/출력 계약 준수
- 인터페이스 일치성

예:

- API 응답 구조 일치
- 스키마 준수
- 필수 필드 존재

---

### ✅ 6.2 품질 검증 (Quality Evaluation)

검증 대상:

- 정확성
- 완전성
- 일관성
- 성능
- 안정성

예:

- 테스트 통과율
- 커버리지
- 성능 지표
- 오류율

---

### ✅ 6.3 정책 검증 (Policy Evaluation)

검증 대상:

- 조직 규칙
- 보안 정책
- 스타일 가이드
- 규제 준수

예:

- 코드 컨벤션
- 보안 취약점
- 라이선스 규칙

---

### ✅ 6.4 휴먼 리뷰 (Human Evaluation)

특징:

- 고위험 판단
- 전략적 검토
- 맥락 기반 평가

적용:

- 아키텍처 결정
- UX 품질
- 비즈니스 정합성

---

### ✅ 6.5 에이전트 평가 (Agent Evaluation)

특징:

- 자동화 가능
- 반복 검증 적합
- 대량 처리 유리

필수 포함 메타데이터:

- 신뢰도 (Confidence)
- 불확실성 (Uncertainty)
- 사용 모델 / 버전
- 평가 기준 ID

---

## 7. PASS / FAIL 규칙

Evaluation은 판정 가능해야 한다.

### ✅ PASS 조건

- 계약 기준 충족
- 품질 임계값 이상
- 필수 Evidence 확보

---

### ❌ FAIL 조건

- 계약 위반
- 품질 기준 미달
- Evidence 부족
- 불확실성 임계 초과

---

---

## 8. Evidence와의 관계

Evaluation 결과는 반드시 **Evidence**로 정당화되어야 한다.

```

Evaluation → Evidence

```

Evidence 예:

- 테스트 리포트
- 로그
- 분석 결과
- 리뷰 코멘트
- 측정 지표

**근거 없는 Evaluation은 무효**

---

## 9. 체크포인트와의 관계

Checkpoint 판정은 Evaluation 출력에 의존한다.

```

Evaluation Result → Checkpoint Decision

```

Checkpoint는:

- PASS / FAIL 결정
- 상태 전이 승인
- Recovery 트리거

---

## 10. 품질 지표 (Metrics)

Evaluation은 정량 지표를 포함할 수 있다.

예:

| 지표 | 설명 |
|------|------|
| Coverage | 테스트 커버리지 |
| Error Rate | 오류 비율 |
| Latency | 응답 지연 |
| Consistency Score | 일관성 평가 |
| Confidence | 평가 신뢰도 |

---

## 11. 에이전트 평가 메타데이터

에이전트 기반 Evaluation 필수 항목:

| 항목 | 설명 |
|------|------|
| Model | 사용 모델 |
| Version | 모델 버전 |
| Criteria | 평가 기준 ID |
| Confidence | 신뢰도 |
| Uncertainty | 불확실성 |
| Timestamp | 평가 시점 |

---

## 12. 안티패턴

### ❌ 형식적 평가

- PASS만 위한 평가
- 실질 검증 없음

---

### ❌ 근거 없는 판정

- Evidence 누락
- 감각 기반 판단

---

### ❌ 모호한 기준

- PASS/FAIL 불명확
- 측정 불가능

---

### ❌ Evaluation 생략

- Artifact 존재만으로 진행
- Checkpoint 왜곡

---

## 13. Evaluation 설계 원칙

- 판정 가능해야 한다
- 기준은 명시적이어야 한다
- Evidence 연결 필수
- 자동화 가능성 고려
- 재현 가능해야 한다

---

## 14. 예시 템플릿

```md
## Evaluation Report

**Stage:**  
**Artifact:**  
**Evaluator:** (Human / Agent)

### Criteria
- [ ] Contract satisfied
- [ ] Quality threshold met
- [ ] Evidence attached

### Metrics
| Metric | Value |
|--------|-------|

### Result
PASS / FAIL

### Evidence
- Link / File / Reference

### Notes
- Risks
- Observations
- Uncertainty
```

---

## ✅ 핵심 요약

Evaluation은:

> **“확인 단계”가 아니라
> “상태 전이를 허용하거나 차단하는 검증 게이트”**

SSDAM에서:

* 진행은 Execution이 아니라 Evaluation으로 결정되며
* 완료는 Artifact가 아니라 PASS 판정으로 선언된다