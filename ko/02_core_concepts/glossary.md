# 📘 SSDAM 용어집 (Glossary)

## 🚀 Mission (미션)

**정의:**  
여러 Task로 구성된 **상위 의도(Intent) 단위**.

**핵심 특성:**

- 직접 실행되지 않음  
- 방향성과 목표 정의  
- 상태 전이는 Task를 통해서만 발생  

**오해 방지:**

- ❌ 실행 단위  
- ❌ 단순 프로젝트 이름  
- ✅ 의도 / 오케스트레이션 컨테이너  

---

## ⚙️ Task (태스크)

**정의:**  
SSDAM의 **최상위 실행 단위**.

**핵심 특성:**

- 실행 가능  
- 명확히 제한된 목적  
- 명시적 Input / Output 계약  
- 검증 가능한 Artifact 생성  
- Checkpoint로 종료  

**오해 방지:**

- ❌ 단순 할 일  
- ❌ 활동 묶음  
- ✅ 계약 기반 실행 단위  

---

## 🧠 Skill (스킬)

**정의:**  
Task에서 호출되는 **재사용 가능한 실행 능력 / 전략**.

**특성:**

- 재사용 가능  
- 컨텍스트 독립  
- 진행 단위를 정의하지 않음  

**관계:**

- Task는 하나 이상의 Skill을 호출 가능  
- Skill은 실행을 가능하게 하고, 진행은 Task가 정의  

---

## ⚙️ Execution (실행)

**정의:**  
Task 내부에서 수행되는 실제 활동.

**예시:**

- 설계  
- 구현  
- 분석  
- 문서화  
- 테스트 수행  

**특성:**

- Artifact 생성을 목적  
- Evaluation 가능한 상태로 이어져야 함  

---

## 📦 Artifact (산출물)

**정의:**  
Execution 결과로 생성되는  
**검토 및 평가 가능한 출력물**.

**예시:**

- 문서 (PRD, Spec 등)  
- 코드  
- 다이어그램  
- 테스트 리포트  
- 모델 정의  

**필수 조건:**

- 명확한 형식  
- 재검증 가능  
- Contract 준수  

---

## 🔍 Evaluation (평가)

**정의:**  
Artifact가 정의된 기준 / 계약을 만족하는지 판단하는 과정.

**유형:**

- 자동 정책 평가  
- Human Review  
- Hybrid Evaluation  

**결과:**

- PASS / FAIL  
- Confidence / Uncertainty 메타데이터 포함 가능  

---

## 🧾 Evidence (근거)

**정의:**  
Evaluation 결과를 정당화하는  
**검증 가능한 정보**.

**예시:**

- 테스트 로그  
- 정적 분석 결과  
- 리뷰 기록  
- 측정 메트릭  
- 정책 검사 결과  

**역할:**

- 의사결정 정당화  
- 추적성 확보  
- 실패 분석 지원  

---

## 🚦 Checkpoint (체크포인트)

**정의:**  
Task 종료를 결정하는  
**공식 판단 게이트**.

**결과 상태:**

- **PASS** → Next Task  
- **FAIL** → Recovery  

**특성:**

- 결정적 판단 기준  
- 정책 / Human / Hybrid 가능  

---

## 🔄 Recovery (복구)

**정의:**  
Checkpoint FAIL 이후 수행되는  
**설계된 대응 전략**.

**예시:**

- 재실행  
- 재평가  
- Task 조정  
- 전략 변경  
- 설계 수정  

**철학:**

- Failure = 예외 ❌  
- Failure = 통제 가능한 상태 전이 ✅  

---

## ❌ Failure (실패)

**정의:**  
다음 조건 중 하나 이상 발생 시 선언되는 공식 상태:

- Evaluation 기준 미충족  
- Contract 위반  
- 필수 Evidence 누락  
- 품질 기준 미달  
- 허용 리스크 초과  

**해석:**

- 예외 ❌  
- 상태 전이 이벤트 ✅  

---

## ✅ PASS

**정의:**  
Checkpoint 기준이 충족된 상태.

**의미:**

- Task 완료  
- 다음 진행 승인  

---

## ⛔ FAIL

**정의:**  
Checkpoint 기준이 충족되지 않은 상태.

**의미:**

- 진행 중단  
- Recovery 필요  

---

## 🤖 Agent (에이전트)

**정의:**  
SSDAM 내 역할 수행이 가능한 자동화 주체  
(AI / Bot / System).

**가능 역할:**

- Execution  
- Evaluation  
- Recovery  

**제약:**

- 최종 책임은 Owner에게 귀속  
- Confidence / Uncertainty 메타데이터 요구 가능  

---

## 👤 Task Owner (태스크 오너)

**정의:**  
Task에 대한 **최종 책임 주체**.

**책임 범위:**

- Contract 정의  
- Evaluation 기준 승인  
- PASS / FAIL 책임  
- Agent 판단 재정의 권한  

---

## 👤 Mission Owner (미션 오너)

**정의:**  
Mission 전체 방향성과 거버넌스 책임 주체.

**책임 범위:**

- Task 구성 정의  
- 진행 정책 승인  
- 리스크 수용 결정  

---

## 📊 Task State (태스크 상태)

**정의:**  
Task 실행 진행 상황을 나타내는 상태 값.

| State | 설명 |
|------|------|
| **PENDING** | 실행 대기 |
| **IN_PROGRESS** | 실행 중 |
| **BLOCKED** | 의존성 / 제약으로 중단 |
| **FAILED** | Checkpoint FAIL |
| **PASS** | Checkpoint PASS |

**상태 전이:**

PENDING → IN_PROGRESS  
IN_PROGRESS → PASS  
IN_PROGRESS → FAILED  
FAILED → (Recovery) → IN_PROGRESS  

---

## 🔗 Traceability (추적성)

**정의:**  
의사결정 및 산출물 연결 구조:

Requirement  
→ Task  
→ Execution  
→ Artifact  
→ Evaluation  
→ Evidence  
→ Checkpoint  

**효과:**

- 역추적 가능  
- 감사 대응  
- 실패 원인 분석  
- AI 판단 설명 가능  

---

## 🎯 Contract (계약)

**정의:**  
Task 또는 Artifact가 반드시 만족해야 하는 명세.

**구성 요소:**

- Input 조건  
- Output 조건  
- 품질 기준  
- Evaluation 기준  

---

## 📐 Deterministic Flow (결정적 흐름)

**정의:**  
상태 전이 및 판단이  
**명확하고 재현 가능한 규칙**에 의해 결정되는 특성.

---

## 🧩 Composable Task Architecture (조합 가능한 태스크 구조)

**정의:**  
독립적인 Contract 기반으로  
Task의 재사용 및 재조합이 가능한 구조.

---

## 📊 Quality Threshold (품질 기준선)

**정의:**  
PASS 판단을 위한 최소 품질 기준.

---

## 🔁 State Transition (상태 전이)

**정의:**  
SSDAM에서 진척은 활동이 아니라  
**검증 기반 상태 변화**로 정의된다.

---

## 📌 Core Summary

SSDAM에서:

- Mission = 의도 단위  
- Task = 실행 단위  
- Artifact = 진척 단위  
- Evidence = 신뢰 단위  

완료 기준:

> **Checkpoint PASS**
