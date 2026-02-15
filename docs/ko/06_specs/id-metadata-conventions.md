# 🧾 ID & Metadata Conventions

## 1. 목적

이 문서는 SSDAM 문서 전반에서 사용하는  
ID 규칙, 메타데이터 규칙, 참조 표기 규칙을 통일한다.

---

## 2. 공통 원칙

- 모든 문서는 고유 식별자를 가진다.
- ID는 의미 있는 접두사 + 번호 체계를 따른다.
- 식별자와 시점(`timestamp`)은 항상 함께 기록한다.
- 링크는 사람과 에이전트가 모두 파싱 가능한 형태로 유지한다.

---

## 3. ID 스키마

| 대상 | 접두사 | 형식 예시 | 패턴 |
|---|---|---|---|
| Project | `PRJ` | `PRJ-001` | `^PRJ-[0-9]{3,}$` |
| Requirement | `REQ` | `REQ-012` | `^REQ-[0-9]{3,}$` |
| Stage | `STG` | `STG-03` | `^STG-[0-9]{2,}$` |
| Execution | `EXE` | `EXE-0042` | `^EXE-[0-9]{3,}$` |
| Artifact | `ART` | `ART-104` | `^ART-[0-9]{3,}$` |
| Evaluation | `EVAL` | `EVAL-104` | `^EVAL-[0-9]{3,}$` |
| Evidence | `EVD` | `EVD-104` | `^EVD-[0-9]{3,}$` |
| Checkpoint | `CP` | `CP-STG-03` | `^CP-(STG-[0-9]{2,}|[A-Z0-9-]+)$` |
| Recovery | `RCV` | `RCV-STG-03-01` | `^RCV-[A-Z0-9-]+$` |
| Quality Policy | `QPOL` | `QPOL-01` | `^QPOL-[0-9]{2,}$` |
| Recovery Policy | `RPOL` | `RPOL-02` | `^RPOL-[0-9]{2,}$` |
| Traceability Policy | `TPOL` | `TPOL-01` | `^TPOL-[0-9]{2,}$` |

---

## 4. 번호 부여 규칙

- 같은 접두사 내 ID는 재사용하지 않는다.
- 삭제된 항목 ID도 재할당하지 않는다.
- 운영 중간 삽입이 필요하면 끝 번호를 증가시킨다. (`STG-02` 다음 삽입도 `STG-11` 허용)
- 사람이 읽는 순서와 ID 순서는 다를 수 있다. 순서는 `project-stage-map`으로 관리한다.

---

## 5. timestamp 규칙

권장 형식: ISO-8601 UTC

```
YYYY-MM-DDTHH:mm:ssZ
```

예시:
- `2026-02-15T09:30:00Z`

허용:
- 로컬 오프셋 표기 (`+09:00`)는 Evidence 원천 시점 기록에만 허용

금지:
- 날짜만 기록 (`2026-02-15`)
- 타임존 없는 시각 (`2026-02-15T09:30:00`)

---

## 6. actor 필드 규칙

`actor(human/agent/policy)` 필드는 아래 값만 사용한다.

- `human`
- `agent`
- `policy`

필요 시 보조 필드 추가:
- `actor_id` (예: `user:kim`, `agent:gpt-ops-v2`)
- `actor_role` (예: `stage_owner`, `reviewer`)

---

## 7. version 규칙

권장: SemVer (`vMAJOR.MINOR.PATCH`)

- `MAJOR`: 호환성 깨짐
- `MINOR`: 호환 가능한 확장
- `PATCH`: 오탈자/비기능 수정

정책 문서는 `policy_version`을 반드시 기록한다.

---

## 8. 무결성/해시 규칙

- Artifact/Evidence는 가능한 한 해시를 기록한다.
- 권장 알고리즘: `sha256`
- 서명 저장소를 쓰는 경우 `lock_method`에 명시한다.

예시:
- `hash: sha256:8f3b...`
- `lock_method: signature`

---

## 9. 참조 표기 규칙

문서 내 참조는 아래 우선순위를 따른다.

1. ID 참조 (`artifact_id: ART-104`)
2. 경로 참조 (`location: docs/output/auth-spec.md`)
3. 외부 URI 참조 (`source_ref: https://...`)

필수:
- ID 참조만으로 의미를 알 수 없는 경우 경로/URI를 함께 기록한다.
- 외부 URI는 수집 시각(`collected_at`)을 함께 남긴다.

---

## 10. 파일명 권장 규칙

- 템플릿: `*.template.md`
- 인스턴스: `<type>-<id>.md` 권장

예시:
- `stage-spec-STG-03.md`
- `evaluation-EVAL-104.md`
- `checkpoint-CP-STG-03.md`

---

## 11. 검증 체크리스트

- [ ] 모든 문서에 필수 ID와 timestamp가 있다.
- [ ] `actor` 값이 허용 집합(`human/agent/policy`)을 벗어나지 않는다.
- [ ] 정책 ID가 Checkpoint/Stage Spec에서 참조 가능하다.
- [ ] Artifact/Evidence에 해시 또는 잠금 정보가 있다.
- [ ] FAIL 기록이 Recovery ID로 연결된다.

---

## 12. 요약

ID와 메타데이터 규칙은 SSDAM의 추적성과 자동화 호환성을 위한 기반이다.  
규칙이 느슨해지면 PASS/FAIL 판정의 재현 가능성이 즉시 떨어진다.
