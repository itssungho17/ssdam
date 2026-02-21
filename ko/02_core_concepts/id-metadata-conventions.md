# 🧾 ID & 메타데이터 규약 (ID & Metadata Conventions)

## 1. 목적 (Purpose)

본 문서는 SSDAM 전반에서 사용되는  
**식별자(ID), 메타데이터, 참조 표기 규칙**을 표준화한다.

목표:

- 결정적 추적성 확보
- Human / Agent 파싱 호환성
- 모호성 제거
- 구조적 무결성 유지

---

## 2. 공통 원칙 (Common Principles)

- 모든 구조 요소는 **고유 ID 필수**
- ID는 안정적이며 재사용 불가
- ID와 Timestamp는 항상 함께 기록
- 참조는 Human / Agent 모두 해석 가능
- 메타데이터는 암묵적 표현 금지

---

## 3. ID 스키마 (ID Schema)

| 대상 | Prefix | Example | Pattern |
|------|--------|---------|---------|
| Mission | `MIS` | `MIS-20260221-001` | `^MIS-[0-9]{8}-[0-9]{3}$` |
| Task | `TSK` | `TSK-042` | `^TSK-[0-9]{3,}$` |
| Requirement | `REQ` | `REQ-012` | `^REQ-[0-9]{3,}$` |
| Execution | `EXE` | `EXE-0042` | `^EXE-[0-9]{3,}$` |
| Artifact | `ART` | `ART-104` | `^ART-[0-9]{3,}$` |
| Evaluation | `EVAL` | `EVAL-104` | `^EVAL-[0-9]{3,}$` |
| Evidence | `EVD` | `EVD-104` | `^EVD-[0-9]{3,}$` |
| Checkpoint | `CP` | `CP-TSK-042` | `^CP-[A-Z0-9-]+$` |
| Recovery | `RCV` | `RCV-TSK-042-01` | `^RCV-[A-Z0-9-]+$` |
| Quality Policy | `QPOL` | `QPOL-01` | `^QPOL-[0-9]{2,}$` |
| Recovery Policy | `RPOL` | `RPOL-02` | `^RPOL-[0-9]{2,}$` |
| Traceability Policy | `TPOL` | `TPOL-01` | `^TPOL-[0-9]{2,}$` |

---

## 4. ID 할당 규칙 (ID Assignment Rules)

- ID 재사용 절대 금지
- 삭제된 ID는 영구 은퇴
- ID에 런타임 상태 인코딩 금지
- 순서는 Composition 구조로 관리

삽입 규칙:

중간 삽입 필요 시 → 기존 ID 변경 없이 신규 ID 증가

---

## 5. Timestamp 규칙

**필수 형식:** ISO‑8601 UTC

```
YYYY-MM-DDTHH:mm:ssZ
```

예시:

`2026-02-21T05:30:00Z`

**허용:**

- Evidence 출처 기록 시 Local Offset (`+09:00`)

**금지:**

❌ 날짜만 기록  
❌ Timezone 누락  

---

## 6. Actor 필드 규칙

허용 값:

- `human`
- `agent`
- `policy`

보조 필드 (선택):

- `actor_id`
- `actor_role`

예시:

```
actor: agent
actor_id: agent:gpt-reviewer-v1
actor_role: evaluator
```

---

## 7. 버전 규칙 (Versioning Rules)

권장: **SemVer**

`vMAJOR.MINOR.PATCH`

| 구성 | 의미 |
|------|------|
| MAJOR | 구조적 호환성 깨짐 |
| MINOR | 호환 확장 |
| PATCH | 비기능 수정 |

정책 문서 필수:

`policy_version`

---

## 8. 무결성 & 해시 규칙

Artifact / Evidence 기록 권장:

- Hash (권장: sha256)
- Lock / Freeze 방식

예시:

```
hash: sha256:8f3b...
lock_method: immutable
```

---

## 9. 참조 표기 규칙 (Reference Notation)

우선순위:

1️⃣ ID Reference  
2️⃣ Path Reference  
3️⃣ External URI  

예시:

```
artifact_id: ART-104
location: docs/artifacts/schema.mmd
source_ref: https://...
```

규칙:

- ID 단독 참조는 문맥 명확 시 허용
- 외부 URI는 `collected_at` 필수

---

## 10. 파일명 규칙 (Filename Conventions)

권장 패턴:

| 유형 | 패턴 |
|------|------|
| Template | `*.template.md` |
| Instance | `<type>-<id>.md` |

예시:

- `task-spec-TSK-042.md`
- `evaluation-EVAL-104.md`
- `checkpoint-CP-TSK-042.md`

---

## 11. 메타데이터 최소 필수 필드

최소 요구:

- `id`
- `timestamp`
- `actor`

권장:

- `version`
- `hash`
- `policy_ref`

---

## 12. 검증 체크리스트 (Validation Checklist)

- [ ] 고유 ID 존재
- [ ] UTC Timestamp 기록
- [ ] Actor 값 유효
- [ ] Version 기록 (해당 시)
- [ ] Hash 기록 (해당 시)
- [ ] 참조 해석 가능

---

## ✅ 핵심 요약 (Key Summary)

ID & 메타데이터 규약은 보장한다:

- PASS / FAIL 결정 추적성
- Agent 파싱 안정성
- 변경 이력 무결성
- 문서 간 참조 일관성

ID 규칙이 느슨해지는 순간:

→ Traceability 붕괴  
→ 결정성 붕괴  
→ SSDAM 비호환 상태 전이
