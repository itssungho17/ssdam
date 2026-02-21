# 🔗 Traceability — SSDAM Reference

## 1. 정의

Traceability는 SSDAM에서 의사결정과 변경 이력을  
**요구사항부터 Checkpoint까지 단절 없이 연결**하는 구조다.

---

## 2. 목적

- 의사결정 근거 역추적 가능성 확보
- 변경 영향 분석 가능
- 감사/검토 대응 가능
- Agent 판정 설명 가능성 확보

---

## 3. 추적 체인

SSDAM 기본 체인:

```
Requirement -> Task -> Execution -> Artifact -> Evaluation -> Evidence -> Checkpoint
```

FAIL 발생 시 확장 체인:

```
Checkpoint(FAIL) -> Recovery -> Re-Evaluation -> Evidence -> Checkpoint
```

---

## 4. 문서별 필수 링크

| 문서 | 필수 식별자 | 필수 연결 |
|---|---|---|
| Task Spec | `project_id`, `task_id`, `requirement_ids` | `policy_id`, `checkpoint_id` |
| Execution | `execution_id`, `task_id` | 입력 계약 근거, 생성 `artifact_id` |
| Artifact | `artifact_id`, `task_id` | `requirement_ids`, 위치/버전/해시 |
| Evaluation | `evaluation_id`, `artifact_id` | `criterion_id`, metric, 결과 |
| Evidence | `evidence_id`, `evaluation_id` | source, measured_value, immutable 정보 |
| Checkpoint | `checkpoint_id`, `task_id` | `evaluation_id`, `evidence_id`, `policy_id` |
| Recovery | `recovery_id`, `task_id` | source checkpoint, 변경 대상, 재평가 결과 |

---

## 5. 불변 규칙

- 링크 없는 판정은 무효다.
- FAIL 기록은 삭제/덮어쓰기 금지다.
- 동일 체인에서 ID 재사용은 금지한다. (새 실행 사이클은 새 ID)
- 참조 대상은 버전/시점이 식별 가능해야 한다.
- 상태 전이는 Checkpoint 결과와 일치해야 한다.

---

## 6. 변경 시 추적 절차

1. 변경 대상 Artifact 식별 (`artifact_id`)
2. 변경 사유를 Requirement 또는 정책 ID와 연결
3. 새 Evaluation 수행 (`evaluation_id` 신규)
4. 새 Evidence 생성/고정 (`evidence_id` 신규)
5. 새 Checkpoint 판정 기록 (`checkpoint_id` 유지 가능, 판정 기록은 신규 시점)

핵심:
- "수정했음"이 아니라 "무엇을 근거로 재판정했는가"를 남긴다.

---

## 7. 감사 관점 최소 질의

- 특정 `requirement_id`를 만족한다고 판정한 Checkpoint는 무엇인가?
- 해당 판정의 Evidence 출처와 생성 시점은 무엇인가?
- FAIL 이후 어떤 Recovery 전략이 선택되었는가?
- 동일 Task 반복 FAIL 횟수가 정책 임계값을 초과했는가?

---

## 8. 품질 지표

| 지표 | 정의 | 목표 예시 |
|---|---|---|
| 링크 완결률 | 필수 ID/참조 필드 충족 비율 | 100% |
| 근거 연결률 | Checkpoint 중 Evidence 링크 보유 비율 | 100% |
| 재현 가능률 | 판정 재현 가능한 기록 비율 | >= 95% |
| FAIL 회복 추적률 | FAIL 건 중 Recovery 연결 비율 | 100% |

---

## 9. 안티패턴

- ❌ 문서별 ID는 있는데 서로 연결되지 않음
- ❌ PASS 기록만 있고 FAIL/Recovery 기록이 없음
- ❌ Evidence 출처가 불명확하거나 변조 방지 정보가 없음
- ❌ 정책 ID 변경 이력이 남지 않음

---

## 10. 체크리스트

- [ ] 모든 Checkpoint가 `evaluation_id`와 `evidence_id`를 참조한다.
- [ ] 모든 Artifact가 `requirement_ids`와 연결된다.
- [ ] FAIL 건이 `recovery_id`로 연결된다.
- [ ] 감사 시 요구되는 시점/주체/정책 버전 정보가 존재한다.

---

## 11. 요약

Traceability는 기록이 아니라 **판정 신뢰성의 구조**다.  
SSDAM에서 진행은 추적 가능한 전이로만 인정된다.
