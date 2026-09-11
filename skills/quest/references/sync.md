# Sync

Bring the current quest's durable record up to date with the conversation and
available evidence. Accept `sync quest`, or `sync` when the context clearly
refers to quest state.

Resolve the quest using the skill's root-resolution rules and the active quest
context. Ask which quest to use only when the target is not clear. Read its
`README.md` first, then apply the shared update contract to material changes,
including affected supporting records and `Current State`. If nothing material
changed, no edit is needed.

This operation updates quest records; it does not imply Git synchronization or
continuing the quest's next task.
