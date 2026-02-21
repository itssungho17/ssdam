# ⚙️ Execution — SSDAM Reference

## 1. 정의

**Execution**은 Task 내부에서 목적 달성을 위해 수행되는
**구체적 작업 활동(Activity Set)** 이다.

Execution은 단순 작업 나열이 아니라:

> **"산출물을 생성하기 위한 의도된 행위의 집합"**

---

## 2. 역할

Execution의 핵심 역할:

- Task 목적 실현
- 검증 가능한 Artifact 생성
- Evaluation 대상 제공
- 변경 및 실패의 관찰 가능성 확보

Execution 자체는 완료 상태를 의미하지 않는다.
완료는 **Checkpoint PASS**로만 선언된다.

---

## 3. Execution의 책임 범위

Execution은 다음을 책임진다:

| 책임 | 설명 |
|------|------|
| 목적 정렬 | Task 목표와 직접 연결 |
| 산출물 생성 | 검증 가능한 Artifact 생성 |
| 계약 준수 | 정의된 입력/출력 계약 유지 |
| 재현 가능성 | 동일 조건에서 재실행 가능 |
| 추적 가능성 | 수행 이력 기록 가능 |

Execution은 **품질 보증 책임을 가지지 않는다**.
품질 판단은 Evaluation 단계의 역할이다.

---

## 4. 입력 (Inputs)

Execution의 입력은 다음 중 하나 이상:

- 선행 Task의 Artifact
- Evidence
- 요구사항 / 명세 / 정책
- 환경 설정 / 제약 조건

### ✅ 입력 조건

- 명시적 정의
- 참조 가능
- 버전 식별 가능
- 계약 위반 없음

---

## 5. 출력 (Outputs)

Execution은 반드시 다음을 생성해야 한다:

- **Artifact (필수)**
- 실행 로그 / 변경 이력 (권장)
- 평가 준비 상태 (필수)

### ❌ 허용되지 않는 출력

- 검증 불가능한 결과
- 암묵적 상태 변경
- 근거 없는 판단

---

## 6. 실행 규칙

Execution은 다음 규칙을 따른다:

1. **목적 지향성**
   - Task 목표와 직접 연결되어야 함

2. **산출물 중심성**
   - 활동이 아니라 Artifact 생성이 핵심

3. **계약 기반 수행**
   - 정의된 Input/Output 계약 준수

4. **재현 가능성**
   - 동일 입력 → 동일 결과 가능 구조

5. **관찰 가능성**
   - 수행 흔적(Log / Diff / Trace) 남김

---

## 7. Execution Lifecycle

```
준비 → 수행 → Artifact 생성 → 종료
```

| 단계 | 설명 |
|------|------|
| 준비 | 입력 검증 / 환경 확인 |
| 수행 | 정의된 작업 실행 |
| 생성 | Artifact 산출 |
| 종료 | Evaluation 단계로 전달 |

Execution 종료 ≠ Task 종료

---

## 8. 품질 관련 원칙

Execution은 품질을 판단하지 않는다.

✔ Execution → 결과 생성
✔ Evaluation → 품질 판단

Execution 단계에서 수행 가능한 품질 활동:

- 정적 분석 실행
- 테스트 수행
- 검증 데이터 생성

하지만 **PASS/FAIL 판정은 금지**

---

## 9. 실패와 Execution

Execution 실패 유형:

| 유형 | 예시 |
|------|------|
| 기술 실패 | 빌드 실패, 런타임 오류 |
| 계약 실패 | 입력 형식 위반 |
| 산출 실패 | Artifact 미생성 |
| 환경 실패 | 의존성 누락 |

Execution 실패 시:

→ 즉시 Task FAIL 아님
→ Evidence 수집 후 Evaluation 단계 판단

---

## 10. Anti-Patterns

### ❌ 활동 중심 Execution
- Artifact 없는 작업 수행

### ❌ 목적 불일치 Execution
- Task 목표와 무관한 작업

### ❌ 암묵적 변경
- 기록 없는 상태 변경

### ❌ 평가 혼합
- Execution 단계에서 PASS 선언

---

## 11. 권장 메트릭

| 메트릭 | 의미 |
|--------|------|
| Artifact 생성률 | Execution 유효성 |
| 재실행 안정성 | 결정성 |
| 실패 유형 분포 | 구조적 문제 탐지 |
| 평균 실행 시간 | 병목 분석 |

---

## 12. 예시

### 🧱 Task: ERD 정의

**Execution**
- Mermaid ERD 작성
- 엔티티 관계 모델링
- 네이밍 규칙 적용

**Artifact**
- `schema.mmd`

---

### 🧱 Task: Backend Slice

**Execution**
- Controller 구현
- UseCase 작성
- Repository 인터페이스 정의

**Artifact**
- 컴파일 가능한 코드
- 테스트 통과 결과

---

## 13. Agent 고려사항

에이전트 Execution 시 요구 조건:

- 입력 계약 엄격 준수
- 변경 이력 자동 기록
- 비결정성 최소화
- 실패 원인 구조화

에이전트는 다음을 수행 가능:

✔ 코드 생성
✔ 문서 작성
✔ 테스트 실행

하지만:

❌ PASS 판정 권한 없음 (Checkpoint 전)

---

## ✅ 핵심 요약

Execution은:

> **"목적 달성을 위한 행위"가 아니라
> "Artifact 생성을 위한 구조화된 수행 단계"**

SSDAM에서 Execution의 가치는:

- 무엇을 했는가 ❌
- 무엇을 생성했는가 ✔
- 무엇이 검증 가능한가 ✔
