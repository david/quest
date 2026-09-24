# Goals

## `goals [slug]`

Develop or revisit a quest's goals through conversation and evidence. New quest
creation enters this conversation automatically; use `goals` for the current
quest or `goals <slug>` for an existing quest in the resolved root. If no current
quest or slug is available, ask which quest to use.

Develop shared understanding of desired outcomes, beneficiaries, motivation,
priorities, scope, and success. Flesh out the goals beyond the initial request
where useful, revisiting them as conversation and evidence reveal what matters.

## Scope

Apply the quest resolution and shared update contract. Read the quest README
first and follow only links needed to understand
existing goals, evidence, accepted decisions, and constraints. Do not silently
create a quest when none is available; use the quest lifecycle separately.

Distinguish provisional suggestions from established goals and accepted choices.
Build on clear supplied intent and respect explicit constraints. Record confirmed
goals under the result contract below; creation alone does not confirm a suggestion.

This command clarifies desired outcomes and why they matter. [Planning](planning.md)
chooses an approach to achieve them; [Acceptance Planning](acceptance.md) develops concrete
acceptance scenarios. Task breakdown turns an established plan into executable
tasks. Do not drift into those activities or implementation without authorization.

## Iterate Toward Shared Understanding

Start by orienting the user: state the outcome being clarified, what is already
settled, and the remaining decision areas. Keep this map concise and refresh it
when the conversation becomes fragmented or its purpose becomes unclear.

For every new quest, recap the understood outcomes, scope, and what would count
as success, identifying gaps rather than filling them with assumptions. Begin
developing the goals in the creation turn, rather than merely recommending goal
clarification as a later activity. A clear initial request makes this exchange
shorter; it does not remove the recap and confirmation checkpoint.

Use the conversation to develop a goal contract, not merely paraphrase the
request. Explore material implications, missing outcomes, and tradeoffs; propose
a fuller statement when useful and invite correction or expansion. Do not run a
fixed questionnaire when the relevant understanding is already available.

Group related questions when answering them together would help. Ask one at a
time when answers determine what comes next or a narrower exchange better fits
the user and the decision. Explain what consequential questions settle.

When a proposed interpretation would help the user evaluate their intent, offer
one grounded in supplied context, explain material tradeoffs, and invite the user
to amend it. Keep proposals focused on desired outcomes, priorities, and scope
rather than choosing an implementation approach. Use concrete examples to
illuminate a decision, rather than requiring separate approval for every example.

Ask the user about intent, lived experience, priorities, and consequential choices
that evidence cannot settle. Separate these decisions from factual gaps and
implementation choices. Carry ordinary implementation details into design rather
than asking the user to resolve them during goal alignment. Build on supplied
context, the quest record, and existing evidence; clarify material gaps rather
than asking the user to repeat known facts. During creation, use supplied context
and linked evidence; creation alone does not authorize a separate research or
codebase investigation.

Investigate material factual gaps within the user's authorized scope, drawing on
existing evidence first. Distinguish observed facts from assumptions and desired
outcomes. Explain how material findings affect the emerging understanding and
revisit conclusions when warranted.

Probe only what matters to this quest:

- Who benefits, and what problem or unmet need exists today?
- Why does it matter, and why address it now?
- What observable change would count as success? What would still be failure
  even if the requested deliverable existed?
- Which outcomes are essential, and which can yield when priorities conflict?
- What constraints are fixed, which are assumptions, and what is out of scope?
- What uncertainty could materially change the goal or make it unnecessary?

Challenge vague terms, contradictions, and unsupported assumptions respectfully.
Distinguish an outcome from a proposed solution: for "build a dashboard," ask
which decision or activity should improve. Do not discard a solution the user
has explicitly required; record it as a constraint alongside the underlying goal.
Offer concrete alternatives when helpful without steering the user toward an
invented requirement.

Periodically reflect back the emerging goals, boundaries, and tradeoffs. Ask for
confirmation of new or materially changed interpretations, not repeated approval
of settled answers. Accept clear confirmation without requiring a restatement;
if an important tradeoff remains unclear, explain it and ask a focused follow-up.
Keep inferred or proposed goals visibly distinct from confirmed intent; silence
is not agreement.

## Pause When Clear Enough To Proceed

Before asking another round of questions, assess whether the remaining uncertainty
affects the goal or belongs in design. Stop and summarize the agreed contract when
desired outcomes, priorities, scope, and success expectations are clear enough to
guide the work. For initial alignment, present the resulting goal contract and ask
the user to confirm or correct it before marking alignment complete. Confirmation
of that contract during the conversation is sufficient; do not ask again. Until
then, preserve supplied intent and label proposed interpretations as provisional.
Do not exhaust design branches or edge cases, or
invent numerical targets just to make a goal appear measurable. Broad success
evidence is enough here; detailed acceptance scenarios belong elsewhere.

If a material uncertainty remains, record it and the evidence needed to resolve
it.

If questions keep multiplying without improving goal clarity, narrow the scope
with the user or separate independently useful outcomes. If discovery pauses,
preserve confirmed understanding, material provisional interpretations, and the
next question or investigation, if one remains useful.

## Record The Result

Keep the current objective and material scope boundaries recoverable from
Current State. Clarifying or confirming a goal does not achieve it: do not claim
achievement without outcome evidence. Retain accepted priorities, constraints,
and rationale with the relevant context; label unresolved assumptions and
questions explicitly. Link substantial goal context when it would overwhelm the
README. Follow `quest`'s retention and file-ownership rules; preserve consequential
understanding rather than each question and confirmation.

When goals change, replace obsolete goal context and remove invalidated guidance
from affected plans and tasks under the shared update contract. If a replacement
strategy needs a separate decision, state that gap and the required next action
instead of leaving the old strategy pending reconciliation. Do not choose a new
delivery strategy without authorization.

Finish by applying the quest shared update contract to the affected sections and
`Current State`. State what is confirmed and what remains uncertain, and follow
quest's actionable handoff guidance. Goal clarification does not authorize
implementation. Initial goal confirmation is an alignment checkpoint, not approval
of a delivery plan or authorization to implement.
