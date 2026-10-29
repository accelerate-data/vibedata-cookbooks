---
id: ssis-package-to-versioned-pipeline
title: Rebuild an SSIS package as dlt, dbt and restartable control-flow code and prove parity and recovery
trigger:
  - A nightly load still runs as an SSIS package whose data flow, precedence constraints and restart behaviour live only in a .dtsx file, with no tests, and the person who understood it has left.
  - The team is leaving SSIS and needs the package's reads, transformation, sinks and control flow as versioned dlt, dbt and runnable code that can be reviewed as a pull request.
  - Someone has to show the rebuilt sinks match what the package writes, and that a failed run restarted, or a successful run repeated, never writes a row twice or loses a committed effect.
description: Rebuild one exported SSIS package as a dlt pipeline for its external reads, dbt models for its data flow and committed control-flow code that publishes, restarts and reruns as approved, with a verdict for every package region, each sink proven against the package's approved reference output and recovery proven by injected failure.
pitch: Rebuild an SSIS package as dlt, dbt and runnable control-flow code, then prove each sink matches the package and that a failed run restarts cleanly.
job_category: re-engineer
area: transformation
readiness: supported
function:
  - cross-functional
domain_objects:
  - ssis_package
  - dlt_pipeline
  - dbt_model
  - control_flow
  - sink
  - reject_path
  - reference_output
  - conversion_report
  - parity_report
  - recovery_proof
works_with:
  platforms:
    - duckdb_local
    - motherduck
    - redshift
  tools:
    - dlt
    - dbt
qualifiers:
  - Needs the exported package, its parameter values and connection references, and read access to its sources.
  - Needs the package's own output on the agreed window, or an approved reference built from its declared semantics.
  - Studio has no SSIS runtime; the package is read from its export and never run, edited or retired.
  - A task body or setting the export lacks stays visible as blocked or not in the package, never guessed.
related:
  - adf-mapping-data-flow-to-dlt-dbt
  - visual-etl-mapping-to-dlt-dbt
  - assess-synapse-ssis-for-fabric
  - stored-procedure-to-dbt
  - legacy-sql-to-dbt
evidence:
  features:
    - capturing-requirements
    - generating-dlt-pipeline
    - ingestion-data-testing
    - generating-dbt-model
    - running-dbt-in-sandbox
    - verifying
  evals: []
---

## Prompt

Rebuild the <package_name> SSIS package in the current Intent so that <consumers> can review it as code and later move to it: its external reads become a dlt pipeline, its data flow becomes dbt models, and its control flow, transaction scope, restart and rerun behaviour become committed code that runs. Inherit the Intent's repository, platform, Domain, sources and approved requirements, and resolve only the semantics they leave open. Give every region of the exported package one verdict, rebuilt, rebuilt with a stated difference, blocked or not in the package, and prove each sink in <sinks> against the package's approved reference output on <agreed_window> at the approved precision. Prove recovery separately: a run that fails part way and is restarted, and a successful run repeated, leave the sinks as the approved rules define, with no row written twice and no committed effect lost. Reproduce what the package does, including behaviour that looks wrong, and report it as follow-up work; state how to cut over and recover data without claiming that reverting code undoes data already written, leave the package and consumers unchanged and state what the comparison cannot prove.

## Verified by

- Every region of the exported package, including parameters, connections, sources, steps, data-flow components, precedence constraints, containers, checkpoint settings and script and mail tasks, has one verdict with its reason and evidence, and the verdict counts add up to the regions.
- A region or task body the export does not hold is shown as blocked or not in the package with that reason, never rebuilt from a guess, and a step that cannot act records what it would have done and that nothing was done; the run follows the approved handling.
- Every external read is carried by a dlt pipeline into the intended destination, and each landed source has the row count of its source on the agreed window under the approved filters.
- Each approved sink equals the package's approved reference output on the agreed window under the approved equality contract, as a multiset in both directions and never by row order; a remaining difference is listed with its cause and parity is not claimed for it.
- Published results equal values derived independently from the sources and the package's declared semantics, including a hand-worked result for each awkward input the window carries, such as a null or unmatched key, a row matching no split output, a duplicate, a boundary value and a rounding tie.
- Each input record is traceable to all of its output contributions or to an approved disposition shown or counted with its reason, and per-sink contributions add back to the inputs under the package's own join, split and aggregate semantics with no residue.
- Each conditional branch follows its approved expression and population, each state the approved rule requires shown is shown to change what the branch governs, and the decision with its inputs is recorded per run.
- Where the approved rule groups writes, a failure inside the group leaves every sink in it as it was; a failure after the group commits and before its record, then restarted, leaves the sinks equal to a clean run with nothing doubled and no committed effect lost.
- A rerun after success leaves every sink as a clean run leaves it with no row duplicated, and writes nothing where the approved rule skips a completed batch; where the approved write rule is keyed per batch, a run for a second key leaves the first key's rows unchanged and no key duplicated.
- Each recovery and branch guarantee is shown to fail when its safeguard is removed, so a passing result cannot come from a check that cannot fail.
- The cutover and recovery method is stated: a bounded window with per-sink reconciliation, data recovery by repeating a batch or restoring a snapshot, and no claim that reverting code undoes data already written; the package keeps running and consumers are unchanged.
- Anything the comparison cannot prove is stated, including a reference not taken from a live package run, a sink with no package counterpart, and package behaviour such as checkpoint timing that is kept out of parity.

## Agent guidance

### Instructions

Inherit the Intent's repository, platform, Domain, sources and approved requirements. Read the exported package end to end first, giving every region a stable identifier the inventory can cite, and settle where the package's reference output on the agreed window comes from before any code exists. Write the expected outcome of each awkward input by hand, then build the reference and check it against that, so a wrong reference cannot agree with itself. Carry each external read into the dlt pipeline, the data flow into dbt models that build candidate results, and the control flow into code that owns step order, the approved transaction scope, the durable step record, restart and rerun. Prove recovery on a separate copy of the same state for each injected failure, run through the same entry point with the same parameters as the restart, and show that each safeguard is detected when removed. Compare each sink with the reference, list every difference with its cause and each package defect as follow-up work, and state what the comparison cannot prove, including any branch the inputs do not exercise.

### Compose

- capturing-requirements
- configuring-dlt-destination
- generating-dlt-pipeline
- ingestion-data-testing
- generating-dbt-model
- running-dbt-in-sandbox
- verifying

### Ask first

- If unresolved, which package and parameter values are converted, which input window forms the comparison, and where the package's own output on it comes from, a recorded run or a reference built from its declared semantics, and who approves it?
- If unresolved, what counts as equal at each sink: exact or an approved precision, which decimal scale and rounding rule, which names, columns, column order and types, and whether the package's runtime columns are reproduced, dropped or only reported?
- If unresolved, what happens to a region the code cannot express or the export lacks: stop the run, set it aside and report it, or use a named substitute or labelled authored value reported as a difference, and what does a step that cannot act record?
- If unresolved, how are rows with a null or unmatched lookup key, a row matching no split output or several, and duplicates handled: which rule wins when a row has several defects, what makes two rows duplicates and which is kept, are they listed or only counted, and where does each go?
- If unresolved, which rows and which threshold decide each conditional branch, and must both its on and off states be shown?
- If unresolved, which steps must succeed or fail together, what may a reader see while a run is in flight, and is the package's checkpoint behaviour reproduced or replaced with its difference reported?
- If unresolved, how does a restart or rerun behave: resume at the failed step or rerun whole, what does a rerun after success do, how is each sink written on a repeat, and which key identifies a batch?
- If unresolved, what is the cutover: how long do the package and the code run side by side, who approves the per-sink reconciliation, and how is data recovered after a bad run?

### Guardrails

- Do not edit, run or retire the package, and do not commit connection strings, passwords or credentials from its export or parameter file; refer to secrets by location only.
- Do not invent the body of a task or the value of a setting the export does not hold; show it as blocked or not in the package, and mark as the Intent's own any value authored only to make a reference producible.
- Do not correct a defect of the package, such as a checkpoint recorded before its transaction commits or a split that sends a row nowhere; reproduce it, list it as follow-up work and route any wanted change to a separate change.
- Do not record a step done before the effect it claims is durable, and do not publish a sink outside the approved transaction scope.
- Do not let a restart or rerun write a row twice or skip an effect that was not committed; identify each batch by the approved key.
- Do not treat a matching row count, a green build or a passing test as proof of parity or recovery; the proof is the approved comparison and a run per injected failure, each on its own copy of the same state.
- Do not compare on row order, widen the precision, narrow the window or change the reference to make a comparison pass.
- Do not claim parity for a sink, window or branch the comparison did not cover, or equate a reference built from declared semantics with a live package run.
- Do not arm a schedule, move consumers, cut over or retire the package, and do not claim reverting code undoes data already written.
