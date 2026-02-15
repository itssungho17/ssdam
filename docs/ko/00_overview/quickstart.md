# SSDAM Quickstart

## 1. 목표
이 문서는 SSDAM을 처음 적용할 때  
**Stage 1개를 `COMPLETED`로 끝내는 최소 경로**를 제공한다.

예상 소요: 30~60분

---

## 2. 준비물

- 프로젝트 식별자 (`PRJ-XXX`)
- 요구사항 ID 최소 1개 (`REQ-001`)
- Stage 이름 1개 (`STG-01`)
- 기본 정책 임계값 (예: 테스트 통과율, 리뷰 승인 기준)

ID 형식은 `06_specs/id-metadata-conventions.md`를 따른다.

---

## 3. Step 1 — 프로젝트 공통 문서 3개 작성

1. `04_templates/01_project/project-governance.template.md`
2. `04_templates/01_project/project-policy.template.md`
3. `04_templates/01_project/project-stage-map.template.md`

완료 조건:
- 역할/승인 권한/에스컬레이션이 정의되어 있다.
- 정책 ID(`QPOL/RPOL/TPOL`)가 정의되어 있다.
- `STG-01`의 PASS/FAIL 분기 경로가 존재한다.

---

## 4. Step 2 — Stage 계약 작성

`04_templates/02_stage/stage-spec.template.md`를 열고 `STG-01`을 작성한다.

필수:
- 단일 목적 1개
- 입력 계약/출력 계약
- PASS/FAIL 가능한 평가 기준
- 체크포인트 정책(`checkpoint_id`, `policy_id`)
- 실패 유형별 Recovery 매핑

---

## 5. Step 3 — 실행 체인 5문서 기록

아래 순서를 반드시 유지한다.

1. `04_templates/03_elements/execution.template.md`
2. `04_templates/03_elements/artifact.template.md`
3. `04_templates/03_elements/evaluation.template.md`
4. `04_templates/03_elements/evidence.template.md`
5. `04_templates/03_elements/checkpoint.template.md`

판정 규칙:
- `checkpoint.decision = PASS`이면 `to_state = COMPLETED`
- `checkpoint.decision = FAIL`이면 `to_state = FAILED` + `recovery_id` 필수

---

## 6. Step 4 — FAIL 경로 1회 리허설

`checkpoint`를 FAIL로 가정하여 아래를 작성한다.

1. `04_templates/03_elements/recovery.template.md`
2. 재평가 결과와 Evidence 링크
3. 재진입 전이(`FAILED -> IN_PROGRESS -> ...`) 기록

목적:
- 실패가 예외가 아니라 설계된 이벤트임을 팀이 동일하게 이해하도록 한다.

---

## 7. Step 5 — 완료 검증

다음을 모두 만족하면 Quickstart 완료:

- [ ] `stage-spec`에 PASS/FAIL/Recovery가 사전 정의되어 있다.
- [ ] 실행 체인 5문서가 동일 `stage_id`로 연결된다.
- [ ] Checkpoint 판정이 Evidence 링크를 포함한다.
- [ ] FAIL 시 Recovery 문서와 재평가 결과가 연결된다.
- [ ] 추적 체인이 단절되지 않는다.

추적 체인 기준: `07_reference/traceability.md`

---

## 8. 산출물 최소 세트

- 프로젝트 문서: `project-governance`, `project-policy`, `project-stage-map`
- Stage 문서: `stage-spec`
- 실행 문서: `execution`, `artifact`, `evaluation`, `evidence`, `checkpoint`
- 실패 리허설 문서: `recovery` (권장)

---

## 9. 자주 발생하는 실수

- ❌ Artifact만 만들고 Checkpoint를 생략
- ❌ PASS/FAIL 기준에 모호한 문장 사용 ("대체로 양호")
- ❌ Evidence 링크 없이 판정
- ❌ FAIL 기록을 덮어쓰기

정답:
- 모든 판정은 정책 + 근거 + 기록으로 남긴다.
