# Realm Init

`realm init [directory]` makes a project a realm: it sets up quest memory, not
a workflow. Use the given directory, or else the session's working directory,
and confirm the target when it is ambiguous. It needs no existing quest root.
Never make the skill directory a realm, and create no quest, checkout,
database, or running service.

Stop without changing anything when the target is a Git repository or lies
inside one, where it or a parent holds a `.git` entry: the quest root and
`lore/` must stay out of every repository. Tell the user to run `realm init`
from a directory outside the repository, such as one that holds it.

Read the target's `AGENTS.md` and any existing quest setup first. Reuse an
existing `quests/` and template; never create a parallel root or migrate
quests, and ask before changing a conflicting layout or rule. Remove a `Quest
root:` line left by an earlier version, but when it names a directory other
than the realm's `quests`, first ask what to do with the quests there.
Rerunning must keep existing files and add no duplicate instructions.

1. Create `quests/` unless it exists. If the [snapshot command](snapshot.md)
   refuses an existing root, keep its records and ask before moving them.
2. Add, or narrowly update, a quest setup section in the realm's `AGENTS.md`,
   keeping unrelated instructions. It says that quests live in `quests/`, that
   a quest's `QUEST.md` is read first and records its workspace paths, and
   that work in a checkout follows that repository's instructions. Do not
   create per-quest `AGENTS.md` files.
3. Create `lore/` and add a Lore section to `AGENTS.md` as
   [Lore](lore.md#the-lore-section) describes, or bring an existing one to
   that format.
4. Create `quest-template/`, whose contents every new quest copies. It stays
   empty until the realm has something each quest starts with, such as editor
   settings or a `.gitignore`, which snapshots honor. Never put secrets in it,
   and do not overwrite or empty an existing one; propose changes instead.

Add only the conventions the realm needs:

- For code, name the repository that `worktrees/1` is cloned from, and only
  what it does differently from the skill's checkout rules, such as a default
  branch other than `main` or how branches are named. Keep an established
  alternative, such as worktrees of the realm's repository or one shared
  checkout, and ask before changing it; for such a realm, record where a
  quest's code lives and how its commands load quest configuration.
- When a quest needs values of its own, such as a port, a database name, or a
  socket path, say how a new quest chooses and records them. Prefer the realm's
  existing allocator. Otherwise pick an available port, compare it with those
  active quests record, and record it in `QUEST.md`; a check is not a
  reservation. Checkouts in one quest share its values unless the section says
  otherwise.
- Keep provisioning, checkout creation, dependency installation, and service
  startup as separate instructions, each subject to its own authorization.

Validate the result, and report the files changed, setup choices left open,
and any validation limits.
