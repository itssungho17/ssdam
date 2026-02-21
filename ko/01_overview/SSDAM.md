# 쓰담 (SSDAM, Structured Skill-Driven Automation Mechanism)

쓰담(SSDAM)은 구조화된 스킬 기반 자동화 메커니즘입니다.

SSDAM은 **개발, 설계, 그리고 Human–AI 협업을 위한 운영 메커니즘**으로,  
**Task를 최상위 실행 단위로 정의**하고,  
다음의 구조화된 흐름을 통해 작업을 수행하고 검증한다:

**Execution → Artifact → Evaluation → Evidence → Checkpoint**

이를 통해 **품질(Quality), 추적성(Traceability), 복구 가능성(Recoverability)**을 동시에 확보한다.

SSDAM은 단순한 활동 관리가 아닌  
**“검증된 상태 전이(Validated State Transitions)” 중심 모델**을 지향한다.

---

## 🎯 1. 목적 (Objectives)

SSDAM의 목표:

- Task 중심 실행 모델 확립  
- Artifact 중심 개발 구조 구축  
- 검증 가능하고 감사 가능한 의사결정 구조 확보  
- 실패를 통제 가능한 시스템 이벤트로 전환  
- 에이전트 기반 개발의 신뢰성 강화  

---

## 🧱 2. 핵심 모델 (Core Model)

Start → Task 1 → Task 2 → ... → Task N → END

각 Task는 다음 흐름을 따른다:

Execution → Artifact → Evaluation → Evidence → Checkpoint → Next Task / Recovery

---

| 요소 | 설명 |
|------|------|
| **Mission** | 여러 Task들의 **순차적 집합** |
| **Task** | **실행 가능한 작업 단위** (명시적 계약 및 종료 기준 포함) |
| **Skill** | 재사용 가능한 실행 능력 / 전략 |
| **Execution** | Task 내에서 수행되는 활동 |
| **Artifact** | Execution의 검토 가능한 결과물 |
| **Evaluation** | Artifact에 대한 검증 / 판단 과정 |
| **Evidence** | Evaluation 결과를 정당화하는 근거 |
| **Checkpoint** | PASS / FAIL 결정 게이트 |
| **Next Task** | Checkpoint PASS 시 진행 대상 |
| **Recovery** | Checkpoint FAIL 시 수행되는 복구 전략 |

---

## 🧩 3. Mission & Task 모델

### 🚀 Mission

Mission은 **상위 의도(Intent) 단위**이다.

- 여러 Task로 구성됨  
- 방향성 있는 목표 정의  
- 직접 실행되지 않음  
- 오케스트레이션 컨테이너 역할  

Mission은 직접 실행되지 않는다.  
**상태 전이는 Task를 통해서만 발생한다.**

---

### ⚙️ Task

Task는 SSDAM의 **원자적 실행 단위**이다.

Task는:

- 실행 가능해야 함  
- 명확한 목표를 가짐  
- Input / Output 계약 정의  
- 검증 가능한 Artifact 생성  
- Evaluation 지원  
- Evidence 기반 판단 요구  
- Checkpoint로 종료됨  

---

### ✅ Task 정의 기준

- 명확히 제한된 목적  
- 명시적 Input / Output 계약  
- 결정적 실행 기대치  
- 검증 가능한 Artifact  
- 정의된 Evaluation 기준  
- Evidence 요구사항  
- Checkpoint 종료 규칙  

---

### 📥 Task 입력 (Inputs)

- 선행 Task의 Artifact  
- 관련 Evidence  
- 계약 / 요구사항 / 정책  

---

### 📤 Task 출력 (Outputs)

- 검토 가능한 Artifact  
- Evaluation 결과  
- 생성된 Evidence  

---

### 🔄 Task 종료 (Termination)

Task 완료는 **Checkpoint Evaluation**으로 결정된다:

- **PASS** → Next Task 진행  
- **FAIL** → 실패 기록 + Recovery 수행  

---

### ✅ Checkpoint PASS 조건

Checkpoint PASS는 다음을 요구한다:

- 유효한 Artifact  
- 완료된 Evaluation  
- Evidence 존재  

---

## 🧠 Skill vs Task

| 요소 | 역할 |
|------|------|
| Skill | 재사용 가능한 실행 능력 / 방법 |
| Task  | 컨텍스트가 적용된 실행 단위 |

Task는 하나 이상의 Skill을 호출할 수 있다.  
Skill은 진행 단위를 정의하지 않는다.  
**진행은 Task 단위로만 정의된다.**

---

## 🔁 4. 실패 처리 철학 (Failure Handling Philosophy)

SSDAM에서 실패는:

> **통제 가능한 상태 전이 이벤트**

실패 선언 조건:

- Evaluation 기준 미충족  
- Artifact 계약 위반  
- 필수 Evidence 누락  
- 품질 기준 미달  
- 허용 리스크 초과  

---

### 🛠 실패 처리 절차

1. 실패 분류  
2. Evidence 보존  
3. Recovery 전략 선택  
4. 재실행 / 재평가 / Task 조정  

---

### 🚫 반복 실패 통제 규칙

구조적 변경 없이 반복 실패는 금지된다.

Recovery는 최소 하나 이상 변경해야 한다:

- Input  
- Execution 전략  
- 제약 조건  
- Skill 선택  

---

## 🔗 5. 추적성 원칙 (Traceability Principle)

SSDAM의 의사결정 연결 구조:

Requirement  
→ Task  
→ Execution  
→ Artifact  
→ Evaluation  
→ Evidence  
→ Checkpoint  

추적성은 다음 상황에서도 유지되어야 한다:

- 변경 / 수정  
- 실패 / 복구  
- 재평가  
- Human ↔ Agent 판단 전환  

---

## 🤖 6. Agent 호환성 (Agent Compatibility)

SSDAM은 **Human / AI Agent 공존 모델**을 지원한다.

| 역할 | 수행 주체 |
|------|----------|
| Execution | Human / Agent |
| Evaluation | Human / Agent |
| Checkpoint | 정책 / Human |
| Recovery | Human / Agent |

---

### 🧭 책임 원칙

Agents execute and evaluate.  
Ownership defines accountability.

에이전트는 실행 및 평가를 수행할 수 있으나,  
최종 책임은 **Task Owner / Mission Owner**에게 귀속된다.

---

### 🧠 Agent 평가 요구사항

Agent 기반 Evaluation은 반드시 포함:

- Confidence 메타데이터  
- Uncertainty 메타데이터  

---

### 🚦 Checkpoint 유형

- 자동 정책 게이트  
- Human 승인 게이트  
- Hybrid 게이트  

---

## 📊 Task 상태 (Task States)

- PENDING  
- IN_PROGRESS  
- BLOCKED  
- FAILED  
- PASS  

---

## 📐 7. 설계 목표 (Design Goals / Invariants)

SSDAM의 불변 특성:

- **Deterministic Flow**  
- **Artifact-Driven Progress**  
- **Evidence-Backed Decisions**  
- **Explicit Failure Control**  
- **Composable Task Architecture**  
- **Traceable Decisions**  
- **Recoverable Failures**

위 특성을 위반하는 변형은  
**SSDAM 호환으로 간주되지 않는다.**

---

### 🔍 Deterministic Flow 정의

Determinism 적용 대상:

- 상태 전이 규칙  
- 계약 해석  
- Evaluation 기준  

---

## ✅ 8. 요약 (Summary)

SSDAM은:

> **단순한 작업 관리 시스템이 아니라,  
> 품질·검증·근거 중심 실행 메커니즘이다.**

진행은:

- 활동(Activity)이 아닌  
- **검증된 상태 전이**로 정의된다.

---

### 📌 개념 단위

- **Mission** → 의도 단위  
- **Task** → 실행 단위  
- **Artifact** → 진척 단위  
- **Evidence** → 신뢰 단위  

---

실패는 예외(Exception)가 아니라  
**설계된 시스템 이벤트**이다.

Recovery는 수정(Fix)이 아니라  
**정의된 복구 전략의 실행**이다.

---

SSDAM은 궁극적으로:

> **“무엇을 했는가”가 아니라  
> “무엇이 검증되었는가”에 기반한다.**
