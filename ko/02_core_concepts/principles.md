# 📜 SSDAM 원칙 (Principles)

## 🎯 목적 (Objective)

SSDAM Principles는 메커니즘의 설계, 확장, 운영 전반에서  
**반드시 유지되어야 하는 불변 규칙(Immutable Rules)**을 정의한다.

본 문서는:

- SSDAM 호환성 기준
- 설계 및 확장 의사결정 가이드
- 구조적 드리프트 방지 규칙
- Human / Agent 협업 불변성

을 제공한다.

---

## 🧱 Principle 1 — Task는 최상위 실행 단위

SSDAM에서 **Task는 최상위 실행 가능 단위**이다.

- 단순 작업이 아닌 계약 기반 실행 단위  
- 진행은 Task 상태 전이로 정의됨  

**불변 규칙**

- 단일 목적(Single Purpose)  
- 명시적 종료 기준(Exit Criteria)  
- 검증 가능한 Artifact 생성  

**안티패턴**

- 다중 목적 Task  
- 종료 기준 없는 Task  
- Artifact 없는 Task  

---

## 🚀 Principle 2 — Mission은 의도를 정의, 실행하지 않는다

Mission은 여러 Task로 구성된 **의도(Intent) 단위**이다.

**불변 규칙**

- Mission은 직접 실행되지 않음  
- 상태 전이는 Task를 통해서만 발생  

**안티패턴**

- 실행 가능한 Mission  
- Mission을 Task처럼 취급  

---

## 🧩 Principle 3 — 계약(Contract) 기반 Task 설계

모든 Task는 **명시적 Contract**를 기반으로 동작해야 한다.

**불변 규칙**

- Input / Output Contract 필수  
- Contract 모호성 금지  
- 구현 의존 Contract 금지  

---

## 🔄 Principle 4 — Artifact 중심 진척

SSDAM에서 진척은 활동이 아니라  
**Artifact 생성 및 검증**으로 정의된다.

**규칙**

- Execution ≠ Progress  
- Artifact 존재 ≠ Completion  
- Checkpoint PASS = Progress  

**불변 규칙**

- 모든 Task는 Artifact 생성  
- Artifact는 검토 가능  
- Artifact는 평가 가능  

---

## ✅ Principle 5 — Evidence 기반 의사결정

모든 판단은 반드시 **Evidence로 정당화**되어야 한다.

**규칙**

Decision → Evidence required

**불변 규칙**

- Evidence 없는 PASS 금지  
- Evidence 없는 FAIL 금지  
- Evidence 없는 Evaluation 무효  

---

## 🚦 Principle 6 — Checkpoint 권위

Checkpoint는 Task 종료 및 상태 전이를 결정하는  
**유일한 판단 메커니즘**이다.

**불변 규칙**

- PASS / FAIL만 허용  
- 조건부 PASS 금지  
- 암묵적 전이 금지  

---

## 🔁 Principle 7 — Failure는 설계된 이벤트

실패는 예외가 아니라  
**설계된 상태 전이 이벤트**이다.

**규칙**

FAIL → 기록 → Evidence 보존 → Recovery

**불변 규칙**

- 실패 은폐 금지  
- 실패 무시 금지  
- Recovery 없는 실패 금지  

---

## 🔗 Principle 8 — End-to-End Traceability

SSDAM 의사결정 연결 구조:

Requirement  
→ Task  
→ Execution  
→ Artifact  
→ Evaluation  
→ Evidence  
→ Checkpoint  

**불변 규칙**

- Traceability 단절 금지  
- 변경 이력 보존  
- 역추적 가능성 유지  

---

## 🤖 Principle 9 — Human / Agent 책임 모델

SSDAM은 Human / Agent 공존을 전제한다.

**규칙**

- Agent = 역할 수행자  
- Human = 책임 주체  

**불변 규칙**

- 최종 책임은 Owner에게 귀속  
- Agent 판단 Override 가능  
- 고위험 / 고불확실성 → Human 우선  

---

## 📐 Principle 10 — Deterministic Flow

SSDAM은 **결정적 상태 전이 구조**를 유지한다.

**불변 규칙**

- 모호한 종료 기준 금지  
- 암묵적 상태 전이 금지  
- 비결정적 Checkpoint 금지  

---

## 🧩 Principle 11 — 구조적 Recovery 강제

Recovery는 반드시 구조적 변화를 포함해야 한다.

**불변 규칙**

Recovery는 최소 하나 변경:

- Input  
- Execution 전략  
- Constraints  
- Skill 선택  

**안티패턴**

- 무의미한 반복 재시도  
- 근거 없는 재실행  

---

## 🧩 Principle 12 — SSDAM 호환성 제약

다음은 SSDAM 비호환:

- Checkpoint 우회  
- Evidence 제거  
- Traceability 단절  
- Failure 구조 무시  
- 모호한 Contract 정의  

---

## ✅ 요약 (Summary)

SSDAM Principles는 다음을 강제한다:

- Task 중심 실행  
- Mission 중심 구조화  
- Artifact 중심 진척  
- Evidence 기반 판단  
- 결정적 상태 전이  
- Failure & Recovery 구조  
- End-to-End Traceability  
- 안정적 Human / Agent 협업  

SSDAM은 다음에 기반한다:

> **“무엇을 수행했는가”가 아니라  
> “무엇이 검증되었는가”**
