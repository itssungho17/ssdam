# 📦 Artifact — SSDAM Reference

## 1. 정의

**Artifact**는 Execution의 결과로 생성되는  
**검증 가능하고 평가 가능한 산출물**이다.

SSDAM에서 Artifact는 단순 결과물이 아니라:

> **“상태 전이를 가능하게 하는 공식적 증거 대상”**

---

## 2. 역할

Artifact의 핵심 역할:

- Evaluation 입력 제공
- Evidence 생성 기반 제공
- Checkpoint 판단 대상
- 추적성(Traceability) 연결 노드

SSDAM에서 진행은 활동이 아니라  
**Artifact 생성 및 검증**으로 정의된다.

---

## 3. 필수 특성

모든 Artifact는 다음 특성을 가져야 한다:

| 특성 | 설명 |
|------|------|
| **검증 가능성** | 객관적 평가 가능 |
| **명시성** | 형태와 내용이 명확 |
| **재현 가능성** | 동일 조건 재생성 가능 |
| **식별 가능성** | 버전 / ID / 해시 등 |
| **추적 가능성** | 요구사항·Stage 연결 |

---

## 4. Artifact 유형

### 🧱 문서형
- PRD
- Architecture Spec
- ADR
- Design Doc

### 🧩 모델형
- ERD (Mermaid)
- UML
- State Diagram

### 💻 코드형
- Source Code
- Config
- Script

### 🧪 검증형
- Test Report
- Coverage Result
- Benchmark Result

### 🚀 운영형
- Deployment Plan
- Release Note
- Runbook

---

## 5. Artifact 생성 규칙

Artifact는 반드시:

1. Execution 결과일 것
2. 명시적 구조를 가질 것
3. 평가 가능 상태일 것
4. 계약(Input/Output) 준수
5. 저장 및 참조 가능

---

## 6. Artifact 품질 기준

Artifact는 다음 기준을 만족해야 한다:

| 기준 | 질문 |
|------|------|
| 완전성 | 필요한 정보가 모두 존재하는가 |
| 일관성 | 내부 모순이 없는가 |
| 명확성 | 해석 ambiguity 최소화 |
| 검증성 | 평가 가능 구조인가 |
| 계약 준수 | 정의된 요구사항 충족 여부 |

---

## 7. Anti-Patterns

### ❌ 암묵적 Artifact
- 구두 합의
- 기록 없는 결정

### ❌ 검증 불가능 Artifact
- “대충 완료”
- 기준 없는 산출물

### ❌ 추적 불가능 Artifact
- 요구사항 연결 없음
- 버전 정보 없음

### ❌ 평가 불가능 Artifact
- PASS/FAIL 판단 불가 구조

---

## 8. Artifact와 상태 전이

SSDAM에서:

✔ Artifact 존재 → 진행 조건 일부 충족  
✔ Artifact 검증 PASS → 상태 전이 가능

Artifact 생성만으로 Stage 완료 아님.

---

## 9. 변경 관리

Artifact 변경 시:

- 버전 증가
- 변경 이력 기록
- 영향 Stage 추적
- Evidence 재검증 필요 여부 판단

### 🔁 변경 유형

| 유형 | 설명 |
|------|------|
| 수정 | 내용 보정 |
| 확장 | 범위 증가 |
| 축소 | 범위 감소 |
| 폐기 | Artifact 무효화 |

---

## 10. Artifact 저장 원칙

Artifact는:

- 영속 저장 가능
- 접근 가능
- 무결성 보장
- 링크 가능

권장 요소:

- Version
- Author / Agent
- Timestamp
- Hash / Signature
- Related Stage

---

## 11. Evidence와의 관계

Artifact는 **평가 대상**,  
Evidence는 **평가 근거**.

```

Execution → Artifact → Evaluation → Evidence

```

Artifact ≠ Evidence

---

## 12. Agent 고려사항

에이전트 생성 Artifact 요구 조건:

- 구조화된 포맷
- 명확한 계약 준수
- 불확실성 메타데이터 포함 가능
- 재현 가능성 확보

에이전트 Artifact는 반드시:

✔ 사람이 검토 가능  
✔ 자동 평가 가능  

---

## 13. 예시

### 🧱 Stage: 요구사항 정의

**Artifact**
- `PRD.md`

---

### 🧱 Stage: 데이터 설계

**Artifact**
- `schema.mmd`
- `migration.sql`

---

### 🧱 Stage: 테스트

**Artifact**
- `test-report.json`
- `coverage.xml`

---

## ✅ 핵심 요약

Artifact는:

> **“결과물”이 아니라  
> “검증과 상태 전이를 가능하게 하는 공식 객체”**

SSDAM에서 Artifact의 의미:

- 활동 기록 ❌
- 검증 대상 ✔
- 의사결정 입력 ✔
- 추적성 노드 ✔