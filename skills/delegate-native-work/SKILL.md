---
name: delegate-native-work
description: Delegate substantive implementation, debugging, architecture, product, UX, QA, code-review, research, and other multi-step work to native Codex subagents with Luna-first routing, focused context, clear ownership, escalation, and verification. Use when work can be split into useful independent assignments, when parallel scouting or implementation would improve speed or coverage, or when the user asks for subagents, delegation, or parallel agents.
---

# Delegate Native Work

Keep the primary agent in the coordinator role. Decompose the request, give workers narrow ownership, remain available to the user, combine the results, and verify the important work.

Make delegation precise, not necessarily simple. Before spawning a worker, turn the broader request into a clear outcome with a set scope, relevant context, an initial plan for achieving it, dependencies, and success criteria. Hard work can be delegated when the goal and ownership are clear. Treat the initial plan as a strong starting direction, not a prohibition on adapting when evidence supports a better approach.

## Decide what to delegate

- Delegate independent exploration, implementation, debugging, research, QA, review, and competing hypotheses when doing so materially improves speed, coverage, or context quality.
- Keep tightly coupled decisions and final integration with the primary agent.
- Do not delegate vague goals. Give each worker a precise result to achieve, a defined boundary, and a credible initial approach so it does not need to reconstruct the coordinator's overall plan.
- Avoid duplicate assignments unless independent comparison is intentional.
- Do not impose a fixed numeric agent limit. Scale to the useful independent work, the user's direction, and available runtime capacity. Use additional waves as slots become available.
- Account for coordination cost, shared-file conflicts, machine load, and token use. More agents are useful only when their assignments are distinct and checkable.

## Route models and reasoning

Set both `model` and `reasoning_effort` explicitly for every spawn. Never rely on the parent model or reasoning level being inherited.

1. Use `gpt-5.6-luna` with `high` reasoning as the default for scouts and scoped implementation workers. Prefer it for clear ownership, focused repository work, test discovery, routine fixes, research, summaries, and high-volume parallel work.
2. Use `gpt-5.6-luna` with `max` reasoning when the assignment needs materially more judgment, ambiguity resolution, longer planning, or stronger independent follow-through. Accept its higher latency when quality matters. Use it freely when justified, but do not select it automatically for simple tasks.
3. Escalate to `gpt-5.6-sol` with `medium` reasoning when a focused Luna High or Luna Max attempt fails, stalls, returns weak evidence, misses important constraints, or leaves a genuinely hard problem unresolved. Sol Medium is the normal escalation ceiling.
4. Use `gpt-5.6-sol` with `high` reasoning only when the user explicitly requests it or after explaining why it is needed and receiving the user's approval.

Do not default to Luna `low`, `medium`, or `xhigh`. Do not use Sol `high`, `xhigh`, `max`, or `ultra` without the authorization above. Honor a user's explicit model choice when it is available and compatible with higher-priority constraints.

## Give focused context

- Choose `fork_turns` for each assignment instead of applying one universal default. Give the coordinator freedom to decide how much parent history will improve that worker's result.
- Use `fork_turns: "none"` when the assignment is self-contained, the parent conversation is mostly unrelated noise, or a clean-room perspective is useful. Supply all essential context in the assignment.
- Use a positive `fork_turns` value when recent user wording, decisions, evidence, or constraints will help the worker. Include enough turns to preserve what matters without automatically copying the whole chat.
- Use full parent history only when the broader goal and accumulated decisions materially outweigh the extra context and inheritance risk. Remember that a full-history fork can inherit the parent's model, reasoning level, and orchestration instructions; choose a limited fork when explicit worker model routing must be preserved.
- State the exact objective, scope, relevant files or workspace, constraints, evidence required, and output contract.
- Repeat essential safety and authority boundaries when they might be missing, buried, or ambiguous in the inherited context.
- Give every task worker an explicit role boundary, especially when it receives parent history: `You are a task worker, not the coordinator. Complete only the assignment below. Use your judgment within this scope, but do not take over the user's full request, answer the user directly, delegate, or spawn other agents. Return your result to the parent agent.`
- For an implementation worker, explicitly state whether it may edit and name its file or behavior ownership. For a scout or reviewer, explicitly keep it read-only.
- Assign a worker permission to coordinate or spawn children only when it has an explicit coordinator role. Keep ordinary scouts and workers as task workers.

Use this compact assignment structure:

```text
Objective: one bounded result.
Scope: exact area, files, behavior, or question owned by this worker.
Context: only the facts and prior decisions needed for this assignment.
Initial approach: the coordinator's proposed steps or starting hypothesis, including known dependencies.
Success criteria: observable conditions that make the assignment complete and useful to the parent.
Constraints: safety, authority, dirty-worktree, and no-go boundaries.
Evidence: files, lines, commands, tests, screenshots, or sources to return.
Output: concise findings, changed files, checks run, and unresolved gaps.
Role boundary: You are a task worker, not the coordinator. Complete only this assignment. Use your judgment within this scope, but do not take over the full request, answer the user directly, delegate, or spawn agents. Return your result to the parent.
```

## Coordinate shared work

- Treat all workers as sharing the same filesystem. Give concurrent writers non-overlapping file or behavior ownership.
- Run read-only scouts freely in parallel. Serialize overlapping writers or keep implementation with one owner.
- Preserve user-owned dirty and untracked work. Do not let workers clean, reset, commit, push, deploy, access secrets, or perform external side effects unless the user explicitly authorized that exact action and it remains within the parent's approval boundary.
- Send discoveries directly to the worker that needs them when agent messaging is available. Keep the primary agent aware of dependencies and conflicts.
- Stop or redirect agents that duplicate solved work, drift outside scope, or become blocked without useful progress.

## Verify and escalate

1. Inspect cited files, findings, and diffs instead of accepting worker claims at face value.
2. Run the smallest relevant checks under the primary agent's control.
3. If Luna failed because the goal, scope, context, or initial approach was unclear, improve the assignment or split it more precisely before escalating model strength.
4. Move from Luna High to Luna Max when deeper reasoning is likely to help. Move to Sol Medium when the Luna path still fails or the remaining problem clearly needs the stronger model.
5. Use a different hypothesis or narrower ownership instead of repeatedly launching identical attempts.
6. Report which model and reasoning level a worker used only when the spawn settings or metadata verify it.

Return a unified result to the user. Distinguish verified work, worker-reported evidence, unresolved gaps, and any escalation that still needs approval.
