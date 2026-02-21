# 🎯 Mission 설계 가이드 — Mission Design Guide

## 1. 개요 (Overview)

본 문서는 **SSDAM Mission 설계 방법론**을 정의한다.

Mission은 SSDAM에서:

- 최상위 실행 구조
- 여러 Task의 순차적/구조적 집합
- Validation 중심 진행 단위
- 거버넌스 경계

이다.

설계 흐름:

```
Mission Objective → Mission Scope → Task 분해 → Dependency 구조 → Mission Policies → Mission Validation
```

---

## 2. Step 1 — Mission Objective 정의

Mission은 반드시 **단일 Objective**로 시작한다.

### 필수 속성

| 속성 | 설명 |
|------|------|
| Clarity | 한 문장 표현 가능 |
| Verifiability | 완료 여부 판단 가능 |
| Outcome-Oriented | 활동이 아닌 결과 중심 |

---

### Example

✅ "검증된 인증 기능을 포함한 웹 애플리케이션 제공"  
❌ "웹 앱 개발"

---

## 3. Step 2 — Mission Scope 정의

Mission 경계 설정

| Scope 유형 | 설명 |
|------------|------|
| Included | 포함 책임 |
| Excluded | 제외 책임 |
| Constraints | Timeline / Budget / Quality / Risk |

---

### Example

**Included:** Backend / Frontend / Testing  
**Excluded:** Marketing / Analytics

---

## 4. Step 3 — Task 분해

Mission Objective를 **독립 검증 가능한 Task**로 분해한다.

### 분해 규칙

- Task는 단일 Purpose
- Artifact 생성 필수
- Checkpoint 종료 가능
- Validation 정의 필수

---

## 5. Step 4 — Dependency 구조 정의

Task 의존성 구조 설계

권장 모델:

> **Directed Acyclic Graph (DAG)**

### 규칙

- 순환 의존 금지
- Artifact 기반 의존성
- Hard / Soft 명확 구분

---

## 6. Step 5 — Mission-Level Policies 정의

Mission 전체를 지배하는 정책 정의

---

### 6.1 Recovery Policy

- 최대 복구 시도 횟수
- Escalation 기준
- Rollback 범위

---

### 6.2 Quality Policy

- 전역 품질 기준선
- Cross-task Validation 규칙

---

### 6.3 Agent Policy

- Agent 허용 역할
- Human Checkpoint Task
- Confidence Threshold

---

### 6.4 Traceability Policy

- Evidence 보존 기간
- Logging 규칙
- Audit 대응성

---

## 7. Step 6 — Mission 완료 기준 정의

Mission 완료는:

❌ 모든 Task 실행  
❌ Artifact 존재  

Mission 완료는:

✅ **최종 Mission Checkpoint PASS**

---

### 완료 조건

- 필수 Task COMPLETED
- 필수 Artifact VALIDATED
- 필수 Evidence 보존
- Mission PASS 기준 충족

---

## 8. Step 7 — Mission 실패 전략 정의

Mission FAIL 조건:

- Critical Task FAIL (복구 불가)
- Policy 위반
- Risk Threshold 초과

---

### 실패 대응

1. FAIL 기록
2. Evidence 보존
3. Recovery / 재설계

---

## 9. Mission 설계 체크리스트

**Objective**

- [ ] 단일 Objective 정의
- [ ] 검증 가능한 완료 기준

**Scope**

- [ ] Included / Excluded 정의
- [ ] Constraints 정의

**Tasks**

- [ ] 적절한 분해
- [ ] 단일 Purpose Task

**Dependencies**

- [ ] Artifact 기반
- [ ] 순환 구조 없음

**Policies**

- [ ] Recovery Policy
- [ ] Quality Policy
- [ ] Agent Policy
- [ ] Traceability Policy

**Completion**

- [ ] PASS 기준 정의
- [ ] FAIL 기준 정의

---

## 10. Mission 설계 템플릿

```md
# Mission: [Mission Name]

## Objective
[한 문장]

## Scope
- Included:
- Excluded:
- Constraints:

## Task List
| # | Task | Purpose | Artifact |

## Dependency Structure
[DAG / Mermaid]

## Mission Policies
### Recovery
### Quality
### Agent
### Traceability

## Completion Criteria
- PASS:
- FAIL:

## Failure Strategy
- Conditions:
- Response:
```

---

## ✅ 핵심 요약 (Key Summary)

Mission 설계는:

> **Task를 묶는 작업이 아니라  
> Validation 중심 실행 시스템을 구조화하는 작업이다.**

잘 설계된 Mission은:

- 결정성 유지
- 실패 전파 통제
- Task 오케스트레이션 안정화
- Traceability 기반 완료 보장
