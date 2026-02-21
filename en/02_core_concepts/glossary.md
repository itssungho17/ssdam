# 📘 SSDAM Glossary

## 🚀 Mission

**Definition:**\
A higher-level **intent unit** composed of multiple Tasks executed
sequentially.

**Core Characteristics:**

-   Not directly executable\
-   Defines directional goal / outcome\
-   State transitions occur only through Tasks

**Misconception Prevention:**

-   ❌ Executable unit\
-   ❌ Simple project label\
-   ✅ Intent / orchestration container

------------------------------------------------------------------------

## ⚙️ Task

**Definition:**\
The **top-level executable unit** in SSDAM.

**Core Characteristics:**

-   Executable\
-   Clearly scoped purpose\
-   Explicit Input / Output Contract\
-   Produces verifiable Artifacts\
-   Terminates via Checkpoint

**Misconception Prevention:**

-   ❌ Just a to-do item\
-   ❌ Activity bundle\
-   ✅ Contract-driven execution unit

------------------------------------------------------------------------

## 🧠 Skill

**Definition:**\
A reusable **execution capability / strategy** invoked by Tasks.

**Characteristics:**

-   Reusable\
-   Context-independent\
-   Does not define progression

**Relationship:**

-   A Task may invoke one or more Skills\
-   Skills enable execution, Tasks define progress

------------------------------------------------------------------------

## ⚙️ Execution

**Definition:**\
Actual activities performed within a Task.

**Examples:**

-   Design\
-   Implementation\
-   Analysis\
-   Documentation\
-   Test execution

**Characteristics:**

-   Performed to generate Artifacts\
-   Must lead to an evaluatable state

------------------------------------------------------------------------

## 📦 Artifact

**Definition:**\
A **reviewable and evaluable output** resulting from Execution.

**Examples:**

-   Documents (PRD, Spec, etc.)\
-   Code\
-   Diagrams\
-   Test reports\
-   Model definitions

**Required Conditions:**

-   Clear format\
-   Re-verifiable\
-   Contract compliant

------------------------------------------------------------------------

## 🔍 Evaluation

**Definition:**\
The process of determining whether an Artifact satisfies defined
criteria or contracts.

**Types:**

-   Automated policy evaluation\
-   Human review\
-   Hybrid evaluation

**Results:**

-   PASS / FAIL\
-   Confidence / Uncertainty metadata possible

------------------------------------------------------------------------

## 🧾 Evidence

**Definition:**\
**Verifiable information** that justifies Evaluation results.

**Examples:**

-   Test logs\
-   Static analysis results\
-   Review records\
-   Measurement metrics\
-   Policy check results

**Role:**

-   Justifies decisions\
-   Ensures traceability\
-   Enables failure analysis

------------------------------------------------------------------------

## 🚦 Checkpoint

**Definition:**\
A formal decision gate determining Task termination.

**Result States:**

-   **PASS** → Next Task\
-   **FAIL** → Recovery

**Characteristics:**

-   Deterministic judgment criteria\
-   Policy / Human / Hybrid capable

------------------------------------------------------------------------

## 🔄 Recovery

**Definition:**\
A **designed response strategy** executed after Checkpoint FAIL.

**Examples:**

-   Re-execution\
-   Re-evaluation\
-   Task adjustment\
-   Strategy modification\
-   Redesign

**Philosophy:**

-   Failure = Exception ❌\
-   Failure = Controllable state transition ✅

------------------------------------------------------------------------

## ❌ Failure

**Definition:**\
An officially declared state when one or more conditions occur:

-   Evaluation criteria not satisfied\
-   Contract violation\
-   Missing mandatory Evidence\
-   Quality threshold not met\
-   Risk level exceeds tolerance

**Interpretation:**

-   Exception ❌\
-   State transition event ✅

------------------------------------------------------------------------

## ✅ PASS

**Definition:**\
State where Checkpoint criteria are satisfied.

**Meaning:**

-   Task completed\
-   Progression authorized

------------------------------------------------------------------------

## ⛔ FAIL

**Definition:**\
State where Checkpoint criteria are not satisfied.

**Meaning:**

-   Progression halted\
-   Recovery required

------------------------------------------------------------------------

## 🤖 Agent

**Definition:**\
An automated entity capable of performing roles within SSDAM (AI / Bot /
System).

**Capable Roles:**

-   Execution\
-   Evaluation\
-   Recovery

**Constraints:**

-   Final responsibility attributed to Owner\
-   Confidence / Uncertainty metadata may be required

------------------------------------------------------------------------

## 👤 Task Owner

**Definition:**\
The **final responsible entity** for a Task.

**Responsibilities:**

-   Contract definition\
-   Evaluation criteria approval\
-   PASS / FAIL accountability\
-   Authority to override Agent judgment

------------------------------------------------------------------------

## 👤 Mission Owner

**Definition:**\
The entity responsible for Mission-level direction and governance.

**Responsibilities:**

-   Task composition definition\
-   Progression policy approval\
-   Risk acceptance decisions

------------------------------------------------------------------------

## 📊 Task State

**Definition:**\
State value representing Task execution progress.

  State             Description
  ----------------- ----------------------------------------
  **PENDING**       Waiting to start
  **IN_PROGRESS**   Currently executing
  **BLOCKED**       Suspended due to dependency/constraint
  **FAILED**        Terminated with Checkpoint FAIL
  **PASS**          Terminated with Checkpoint PASS

**State Transitions:**

PENDING → IN_PROGRESS\
IN_PROGRESS → PASS\
IN_PROGRESS → FAILED\
FAILED → (Recovery) → IN_PROGRESS

------------------------------------------------------------------------

## 🔗 Traceability

**Definition:**\
The structure linking decisions and artifacts:

Requirement\
→ Task\
→ Execution\
→ Artifact\
→ Evaluation\
→ Evidence\
→ Checkpoint

**Effects:**

-   Backward traceability\
-   Audit readiness\
-   Root cause analysis\
-   AI judgment explainability

------------------------------------------------------------------------

## 🎯 Contract

**Definition:**\
Specifications or requirements that a Task or Artifact must satisfy.

**Components:**

-   Input conditions\
-   Output conditions\
-   Quality criteria\
-   Evaluation criteria

------------------------------------------------------------------------

## 📐 Deterministic Flow

**Definition:**\
A property where state transitions and Checkpoint judgments are governed
by **clear, reproducible rules**.

------------------------------------------------------------------------

## 🧩 Composable Task Architecture

**Definition:**\
An architecture enabling Tasks to be reused and recomposed based on
independent Contracts.

------------------------------------------------------------------------

## 📊 Quality Threshold

**Definition:**\
The minimum quality standard required for PASS judgment.

------------------------------------------------------------------------

## 🔁 State Transition

**Definition:**\
In SSDAM, progression is defined not as activity completion but as\
**verified state change**.

------------------------------------------------------------------------

## 📌 Core Summary

In SSDAM:

-   Mission = Unit of intent\
-   Task = Unit of execution\
-   Artifact = Unit of advancement\
-   Evidence = Unit of trust

Completion Criteria:

> **Checkpoint PASS**
