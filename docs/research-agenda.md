# A falsifiable research agenda

No experiments below have been run as part of this repository. This is a proposed evaluation protocol, not reported evidence.

## H1: Shared capabilities reduce workflow duplication

**Claim:** a human interface and agent interface sharing domain contracts require less duplicated domain logic than separately built paths.

**Experiment:** implement the same task families in both architectures. Include account settings, scheduling, and a multi-service coordination task. Keep functionality, developer experience, and review standards comparable.

**Measure:** maintenance time after a domain-rule change, defects introduced, duplicated validation logic, and divergence between client outcomes. Count shared infrastructure cost rather than treating it as free.

**Weakening evidence:** the shared architecture costs more to build and maintain without reducing divergence. A small codebase or one favorable task cannot establish a general result.

## H2: Intent mediation lowers total effort without reducing control

**Experiment:** compare a conventional interface, a conversational interface, and an adaptive interface backed by the same services. Counterbalance task order; include novices and experienced users; include ambiguous requests and recovery tasks.

**Measure:** successful completion verified against provider state, elapsed time, corrective actions, comprehension of the final effect, and ability to cancel. Include approval and recovery time in total effort.

**Weakening evidence:** faster happy-path execution accompanied by worse comprehension, more harmful errors, or slower recovery. Report results per task type and user group, not only as a pooled mean.

## H3: Separating planning from authority limits unauthorized effects

**Experiment:** inject adversarial instructions into retrieved content and tool metadata; mutate approved parameters; expire grants; revoke delegation; replay requests; interrupt execution after provider completion.

**Measure:** unauthorized effects, blocked legitimate tasks, duplicate effects, unresolved outcomes, and time to reconciliation. Evaluate a strong baseline with ordinary tool permission controls.

**Weakening evidence:** the proposed separation fails to reduce unauthorized effects, or its friction makes ordinary use impractical. Zero observed violations in a finite suite is not proof of absence.

## H4: Capability discovery can support unfamiliar services

**Experiment:** hold out service providers and contract variants during planner development. Introduce timezone differences, incompatible units, schema revisions, and misleadingly similar capability names.

**Measure:** semantic composition errors, correct abstentions, verified task completion, and integration effort. Compare automatic discovery with curated integrations and strong documentation.

**Weakening evidence:** reliable performance requires provider-specific knowledge comparable to conventional integration work. Distinguish machine-readable schemas from genuine semantic interoperability.

## Measurement discipline

For each task attempt, record a terminal outcome: verified success, known failure, unresolved, or user cancellation. Define the ground-truth procedure before running the task. Do not count the planner's completion message as ground truth.

Map `Verified` to verified success and `Rejected` or `Failed` to known failure, with separate reason codes. An outstanding `Indeterminate` or `NeedsIntervention` state counts as unresolved at the observation cutoff. User cancellation applies only when the coordinator confirms that no action remains in flight and no effect occurred. After dispatch, a request to cancel is recorded separately: it cannot relabel an unresolved outcome or erase a completed effect. Any compensation is evaluated as another operation. The runtime diagram omits pre-dispatch user cancellation for brevity; its implementation must record it explicitly.

Report a cost vector rather than one flattering score:

$$
\mathbf{c} = (\text{user time}, \text{runtime cost}, \text{unauthorized effects},
\text{recovery effort}, \text{unresolved outcomes})
$$

If a scalar objective is necessary, publish the weights and a sensitivity analysis. A preference for speed should not silently erase the cost of an unauthorized action.

Preregister task selection, exclusion criteria, stopping rules, and baseline versions. Report sample counts, uncertainty intervals, failures, and the scope of each conclusion. Release reproducible fixtures without personal data or provider credentials.

## Open problems

1. How can a service advertise semantics that are both machine-usable and economically maintainable?
2. How should users inspect and revoke delegated authority across many services?
3. What does portable identity mean when providers disagree about principals and resource ownership?
4. Which evidence is sufficient for a postcondition that extends into the physical world?
5. Can discovery remain competitive if the intent router controls ranking and default execution paths?
6. Where should stable interfaces remain mandatory for accessibility, expertise, or accountability?

The central empirical question is whether intent mediation reduces the total cost of reliable action. A compelling demo establishes a possibility; deployment evidence must establish its operating limits.
