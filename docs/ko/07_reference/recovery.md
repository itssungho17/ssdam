# 🔧 Recovery — 회복 메커니즘

## 1. 목적

Recovery는 SSDAM에서 **FAIL 상태 이후 시스템을 안정적인 실행 흐름으로 복귀시키기 위한 구조적 메커니즘**이다.

Recovery의 목표:

- 실패의 무질서한 확산 방지
- 근거 기반 재진입 보장
- 품질 저하 없는 재실행
- 상태 전이 무결성 유지

Recovery는 단순 수정 활동이 아니라:

> **설계된 실패 대응 전략의 실행 단계**

---

## 2. 정의

| 요소 | 설명 |
|------|------|
| **Recovery** | 체크포인트 FAIL 이후 수행되는 회복 활동 |
| **Recovery Trigger** | Recovery를 시작시키는 실패 조건 |
| **Recovery Strategy** | 실패 유형에 대응하는 회복 방식 |
| **Recovery Artifact** | 회복 과정에서 생성되는 산출물 |
| **Recovery Evidence** | 회복 판단을 정당화하는 근거 |

---

## 3. Recovery 발생 조건

Recovery는 다음 중 하나 이상 충족 시 시작된다:

- 체크포인트 FAIL 판정
- 평가 기준 미충족
- 계약 위반
- 필수 근거 누락
- 품질 임계값 미달

FAIL 선언은 Recovery의 **유일한 진입 트리거**이다.

---

## 4. Recovery 설계 원칙

### ✅ 4.1 결정성 유지

Recovery는 즉흥적 대응이 아니라  
**사전에 정의된 전략 기반으로 수행**되어야 한다.

금지 사항:

- 감정적 수정
- 근거 없는 재시도
- 실패 원인 분석 생략

---

### ✅ 4.2 실패 원인 분리

Recovery 이전에 반드시 수행:

1. Failure Classification
2. Root Cause Identification
3. Evidence Preservation

---

### ✅ 4.3 상태 전이 무결성

Recovery는 기존 흐름을 덮어쓰지 않는다.

유지 조건:

- FAIL 기록 보존
- 기존 Artifact 유지
- 변경 이력 추적 가능

---

### ✅ 4.4 근거 중심 회복

Recovery 완료는 수정 여부가 아니라:

> **체크포인트 재통과**

---

## 5. 실패 분류 기반 전략

| Failure Type | 설명 | Recovery Strategy |
|--------------|------|------------------|
| **Validation Failure** | 평가 기준 미충족 | 수정 후 재평가 |
| **Contract Violation** | 입력/출력 계약 위반 | 계약 정합성 복구 |
| **Missing Evidence** | 근거 누락 | 근거 보강 |
| **Quality Failure** | 품질 기준 미달 | 리팩토링 / 재구현 |
| **Logical Failure** | 설계/논리 오류 | 구조 재설계 |
| **Dependency Failure** | 외부 요소 실패 | 대체 경로 / 재시도 |

---

## 6. Recovery 전략 패턴

### 🔁 6.1 Re-execution

조건:

- 실행 오류
- 비결정적 실패

방식:

- 동일 입력 유지
- 환경 보정 후 재실행

---

### 🛠 6.2 Artifact Correction

조건:

- 산출물 품질 문제
- 부분적 오류

방식:

- 최소 수정 원칙
- 변경 근거 명시

---

### 🧩 6.3 Re-stage

조건:

- Stage 목적 실패
- 구조적 붕괴

방식:

- Stage 폐기
- 새로운 Stage 정의

---

### 🔄 6.4 Evaluation Re-definition

조건:

- 평가 기준 오류
- 잘못된 정책

방식:

- 기준 수정
- 영향 범위 추적

---

### 🚑 6.5 Rollback

조건:

- 회복 불가
- 고위험 실패

방식:

- 이전 Checkpoint PASS 상태로 복귀

---

## 7. Recovery 산출물

Recovery는 반드시 **Artifact를 생성**해야 한다.

예:

- 수정된 설계 문서
- 리팩토링 코드
- 보강된 테스트
- 실패 분석 보고서

---

## 8. Recovery Evidence

필수 포함:

- 실패 원인
- 수행 전략
- 변경 내용
- 재평가 결과

Evidence 없는 Recovery는 무효이다.

---

## 9. Recovery 완료 조건

Recovery 종료는 다음 조건 충족 시 선언된다:

- 재평가 PASS
- 계약 충족 확인
- 품질 기준 충족
- 근거 검증 완료

---

## 10. 안티 패턴

| Anti-pattern | 문제 |
|--------------|------|
| ❌ 무조건 재시도 | 실패 원인 은폐 |
| ❌ FAIL 기록 삭제 | 추적성 붕괴 |
| ❌ 근거 없는 수정 | 품질 리스크 |
| ❌ 과도한 재설계 | 비용 폭증 |
| ❌ 평가 생략 | 체크포인트 무력화 |

---

## 11. 설계 가이드라인

### ✅ Recovery 전략 사전 정의

각 Stage는 다음을 명시해야 한다:

- 예상 실패 유형
- 대응 전략
- 재진입 조건

---

### ✅ 자동 vs 수동 회복 구분

| 유형 | 적용 상황 |
|------|------------|
| **자동 Recovery** | 반복 가능 / 저위험 |
| **수동 Recovery** | 고위험 / 판단 필요 |
| **하이브리드** | 조건부 자동화 |

---

### ✅ 에스컬레이션 규칙

다음 조건 시 사람 개입:

- 반복 FAIL
- 불확실성 증가
- 근거 충돌
- 정책 위반 가능성

---

## 12. 예시 시나리오

### 📌 Case 1 — 테스트 FAIL

Failure Type: Quality Failure  
Strategy: Artifact Correction  
Actions:

1. 실패 테스트 분석
2. 코드 수정
3. 테스트 재실행
4. PASS 확인
5. Evidence 기록

---

### 📌 Case 2 — 계약 위반

Failure Type: Contract Violation  
Strategy: Contract Recovery  

1. 계약 정의 재검토
2. 입력/출력 수정
3. 영향 Stage 추적
4. 재평가

---

### 📌 Case 3 — 설계 붕괴

Failure Type: Logical Failure  
Strategy: Re-stage  

1. Stage 목적 재정의
2. 구조 재설계
3. 신규 Artifact 생성

---

## 13. Recovery 메트릭

| Metric | 의미 |
|--------|------|
| **Recovery Rate** | FAIL 대비 회복 성공률 |
| **Mean Recovery Time (MRT)** | 평균 회복 시간 |
| **Repeat Failure Ratio** | 동일 실패 재발 비율 |
| **Rollback Frequency** | 롤백 발생 빈도 |

---

## ✅ 14. 체크리스트

- [ ] 실패 원인 분류 완료
- [ ] Evidence 보존
- [ ] 전략 선택 근거 명시
- [ ] Artifact 수정/생성
- [ ] 재평가 수행
- [ ] PASS 확인
- [ ] Recovery 기록 저장

---

## 🔒 15. 불변 규칙

Recovery는:

- FAIL을 숨기지 않는다
- 기록을 삭제하지 않는다
- 근거 없이 종료되지 않는다
- 평가 없이 완료되지 않는다

---

## 🧭 요약

Recovery는 SSDAM의 **품질 안전장치이자 흐름 복구 엔진**이다.

> 실패를 제거하는 것이 아니라  
> 실패 이후에도 시스템의 신뢰성과 결정성을 유지하는 메커니즘

SSDAM에서 회복은 선택이 아니라:

> **설계된 필수 단계**