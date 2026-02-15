# 📘 SSDAM Glossary

## 🧱 Stage (스테이지)

**정의:**  
SSDAM에서의 최상위 목적 단위. 작업 묶음이 아니라 **명확한 목적(Purpose)** 을 갖는 구조적 단위.

**핵심 특성:**

- 단일 책임 (Single Responsibility)
- 명확한 입력 / 출력 계약
- 검증 가능한 Artifact 생성
- Checkpoint 기반 종료

**오해 방지:**

- ❌ Task 묶음
- ❌ 단순 단계
- ✅ 목적 중심 실행 단위

---

## ⚙️ Execution (실행)

**정의:**  
Stage 내부에서 수행되는 실제 활동.

**포함 요소 예시:**

- 설계
- 구현
- 분석
- 문서화
- 테스트 수행

**특성:**

- Artifact 생성 목적
- 평가 가능 상태로 귀결되어야 함

---

## 📦 Artifact (산출물)

**정의:**  
Execution의 **검토 / 평가 가능한 결과물**.

**예시:**

- 문서 (PRD, Spec 등)
- 코드
- 다이어그램
- 테스트 리포트
- 모델 정의

**필수 조건:**

- 명확한 형식
- 재검증 가능
- 계약 준수

---

## 🔍 Evaluation (평가)

**정의:**  
Artifact가 정의된 기준 / 계약을 충족하는지 판단하는 과정.

**유형:**

- 자동 정책 평가
- 사람 리뷰
- 하이브리드 평가

**결과:**

- PASS / FAIL
- Confidence / Uncertainty 메타데이터 가능

---

## 🧾 Evidence (근거)

**정의:**  
Evaluation 결과를 **정당화하는 검증 가능한 정보**.

**예시:**

- 테스트 로그
- 정적 분석 결과
- 리뷰 기록
- 측정 지표
- 정책 체크 결과

**역할:**

- 의사결정 정당화
- 추적성 확보
- 실패 분석 기반

---

## 🚦 Checkpoint (체크포인트)

**정의:**  
Stage 종료를 판정하는 공식 평가 지점.

**결과 상태:**

- **PASS** → Next Stage
- **FAIL** → Recovery

**특성:**

- 결정적 판정 기준
- 정책 / 사람 / 하이브리드 가능

---

## 🔄 Recovery (회복)

**정의:**  
Checkpoint FAIL 이후 수행되는 **설계된 대응 전략**.

**유형 예시:**

- 재실행 (Re-execution)
- 재평가 (Re-evaluation)
- Stage 롤백
- 보정 작업
- 재설계

**철학:**

- 실패 = 예외(Exception) ❌  
- 실패 = 통제 가능한 상태 전이 이벤트 ✅

---

## 🔗 Traceability (추적성)

**정의:**  
의사결정 및 변경 이력을 다음 체인으로 연결하는 구조.

```

Requirement → Stage → Execution → Artifact → Evaluation → Evidence → Checkpoint

```

**보장 효과:**

- 역추적 가능성
- 감사 대응
- 실패 원인 분석
- AI 판단 설명 가능성

---

## 📥 Stage Input (스테이지 입력)

**구성 요소:**

- 선행 Artifact
- 관련 Evidence
- 요구사항 / 계약
- 정책 / 제약 조건

---

## 📤 Stage Output (스테이지 출력)

**구성 요소:**

- Artifact
- Evaluation 결과
- Evidence
- 상태 전이 결과

---

## ❌ Failure (실패)

**정의:**  
다음 조건 중 하나 이상 충족 시 선언되는 공식 상태:

- 평가 기준 미충족
- 계약 위반
- 필수 Evidence 누락
- 품질 임계값 미달
- 위험 수준 허용치 초과

**해석:**

- 예외(Exception) ❌  
- 상태 전이 이벤트 ✅

---

## ✅ PASS

**정의:**  
Checkpoint 기준 충족 상태.

**의미:**

- Stage 완료
- Next Stage 진행 허용

---

## ⛔ FAIL

**정의:**  
Checkpoint 기준 미충족 상태.

**의미:**

- 진행 중단
- Recovery 필수

---

## 🤖 Agent (에이전트)

**정의:**  
SSDAM 내 역할 수행이 가능한 자동화 주체 (AI / Bot / System).

**수행 가능 역할:**

- Execution
- Evaluation
- Recovery

**제약:**

- 최종 책임은 Stage Owner 귀속
- 신뢰도 / 불확실성 메타데이터 필요 가능

---

## 👤 Stage Owner (스테이지 소유자)

**정의:**  
해당 Stage의 **최종 책임 주체**.

**책임 범위:**

- 계약 정의
- 평가 기준 승인
- PASS / FAIL 책임
- Agent 판단 재정의 권한

---

## 🔄 Stage State (스테이지 상태)

**정의:**
스테이지의 실행 진행 상황을 나타내는 상태값.

**상태 목록:**

| 상태 | 설명 |
|------|------|
| **IN_PROGRESS** | 스테이지 실행 중 |
| **COMPLETED** | Checkpoint PASS로 종료 |
| **FAILED** | Checkpoint FAIL로 종료 |

**상태 전이 규칙:**

```
IN_PROGRESS → (PASS) → COMPLETED
IN_PROGRESS → (FAIL) → FAILED
FAILED → (Recovery) → IN_PROGRESS
```

---

## 📐 Deterministic Flow (결정적 흐름)

**정의:**  
상태 전이와 Checkpoint 판정이 **명확하고 재현 가능한 규칙**에 의해 결정되는 특성.

---

## 🧩 Composable Stage Architecture (조합 가능한 스테이지 구조)

**정의:**  
Stage가 독립적 계약과 인터페이스를 기반으로  
재사용 / 재조합 가능하도록 설계된 구조.

---

## 🎯 Contract (계약)

**정의:**  
Stage 또는 Artifact가 충족해야 하는 명세 / 요구조건.

**포함 요소:**

- 입력 조건
- 출력 조건
- 품질 기준
- 평가 기준

---

## 📊 Quality Threshold (품질 임계값)

**정의:**  
PASS 판정을 위한 최소 품질 기준.

---

## 🔁 State Transition (상태 전이)

**정의:**  
SSDAM에서 진행은 활동이 아니라  
**검증 결과 기반 상태 변화**로 정의됨.

---

## 📌 핵심 요약

SSDAM에서:

- Stage = 진행 단위  
- Artifact = 진척 단위  
- Evidence = 신뢰 단위  

완료는 결과물이 아니라:

> **Checkpoint PASS**
