# 00_overview

## 1. 목적
`00_overview`는 SSDAM 문서 세트의 **진입점**이다.  
처음 읽는 사람도 전체 구조, 읽기 순서, 최소 실행 경로를 빠르게 이해하도록 돕는다.

---

## 2. 문서 구성

| 문서 | 역할 |
|---|---|
| `00_overview/README.md` | 문서 지도와 읽기 순서 |
| `00_overview/quickstart.md` | 최소 실행 경로(1개 Stage 완료) |

---

## 3. SSDAM 문서 지도

| 레이어 | 경로 | 질문 |
|---|---|---|
| 개요 | `SSDAM.md` | SSDAM이 무엇인가? |
| 원칙 | `01_principles/principles.md` | 절대 깨면 안 되는 규칙은 무엇인가? |
| 아키텍처 | `02_architecture/*.md` | 요소와 상태 전이는 어떻게 연결되는가? |
| 방법론 | `03_methodology/*.md` | 실제 설계/계획은 어떤 절차로 하는가? |
| 템플릿 | `04_templates/**` | 문서를 어떤 형식으로 기록하는가? |
| 스펙 | `06_specs/*.md` | 용어/ID/메타데이터 규칙은 무엇인가? |
| 레퍼런스 | `07_reference/*.md` | 각 요소의 정의와 판정 기준은 무엇인가? |

---

## 4. 권장 읽기 순서

### 4.1 처음 도입하는 경우
1. `SSDAM.md`
2. `01_principles/principles.md`
3. `02_architecture/flow-architecture.md`
4. `00_overview/quickstart.md`
5. `04_templates/README.md`

### 4.2 Stage를 설계하는 경우
1. `03_methodology/stage-design-guide.md`
2. `07_reference/execution.md`
3. `07_reference/evaluation.md`
4. `07_reference/checkpoint.md`
5. `04_templates/02_stage/stage-spec.template.md`

### 4.3 프로젝트를 운영하는 경우
1. `03_methodology/project-planning-guide.md`
2. `07_reference/traceability.md`
3. `06_specs/id-metadata-conventions.md`
4. `04_templates/01_project/*.template.md`

---

## 5. 최소 온보딩 체크리스트

- [ ] PASS/FAIL만으로 상태 전이가 이루어진다는 점을 이해했다.
- [ ] `execution -> artifact -> evaluation -> evidence -> checkpoint` 순서를 생략 없이 적용한다.
- [ ] 모든 판정이 Evidence 링크를 갖도록 강제한다.
- [ ] FAIL 시 Recovery 경로를 사전에 정의했다.
- [ ] 공통 ID 규칙을 프로젝트 전반에 동일하게 적용한다.

---

## 6. 시작 포인트

- 빠르게 시작: `00_overview/quickstart.md`
- 템플릿부터 시작: `04_templates/README.md`
- 정의 확인: `06_specs/glossary.md`
