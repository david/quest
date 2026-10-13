# Open

## `open` or `open <slug>`

Open the named quest, or without a slug the quest the skill's resolution rules
select. The session can be anywhere: in the quest directory, below it, such as
in one of its checkouts, or outside it, such as in the project directory. When
no slug is given and the rules select no quest, ask which one to open and give
the output of `list`.

For a slug with no exact match in the quest root, look for clearly similar
slugs among the root's immediate directories. Open a single clear match and say
which quest it is. If several match, list them and ask the user to choose. If
none does, say that no quest was found.

Read `QUEST.md`, then the first checkout's instructions: `work/1/CLAUDE.md`
when you are Claude Code and `work/1/AGENTS.md` otherwise, falling back to the
other file when yours does not exist. Skip this when the quest has no `work/1`,
when it holds neither file, or when the session started inside `work/1` and so
loaded them already. Follow those instructions in the work that comes after;
they are not part of the summary. Read nothing else.

## The Summary

The user opens a quest to pick its work up again, usually while switching from
another task. They arrive cold: they remember roughly what the quest is, but
not its details or the names the work gave to things. Brief them the way a
colleague would in half a minute of talking. The summary tells them three
things and nothing else, each under its own Markdown heading so that the user
can find a part at a glance:

1. **What the quest is about.** The slug and title as a first-level heading,
   then one or two sentences on the problem and the outcome the user wants, in
   your own words and not the record's objective copied out.
2. **Where we left off.** Under a second-level heading with those words, three
   to five sentences: what the work has produced so far, then where it stopped
   and why, whether that is under way, waiting on the user, paused, or
   complete. Give the result and not its history: what is now known or built,
   with its cause in a few words, and not the steps that led there or how the
   thing works inside.
3. **What to do next.** Under a second-level heading with those words, a
   numbered list of at most three items, so that the user can answer with a
   number or a few words. Each item is one question or one step in one
   sentence, with a second sentence only for something the user needs in order
   to answer. Decisions and approvals waiting on the user come
   first, as questions, and name the options when the answer is not a yes or a
   no. After them comes the step you would take on their go-ahead: the recorded
   next action or, where the record names none or leaves open something that
   step depends on, the step you suggest, marked as a suggestion. For a quest
   that is complete or paused, this is what would reopen it, or nothing.

For example:

```markdown
# slow-invoice-export: Invoice export times out for large accounts

Customers with many invoices cannot download their yearly export, because the request times out. You want the export to work for an account of any size.

## Where we left off

We found the cause. The export loads every invoice into memory before it writes the file, and that takes too long for the largest accounts. A version that writes the file as it reads is built and passes its tests, but it has not been tried on a large account. The work stopped there because that trial needs a copy of production data, which you have not approved.

## What to do next

1. May I use a copy of production data to try the new export on a large account?
2. Suggestion: if not, I build a large account locally and try it on that.
```

The record behind that example also holds how the cause was found, the timings
that were measured, the checkout and its branch, which tests pass on which
revision, and the decisions already made. None of that is in the summary,
because the user can say what to do next without it. The same goes for every
record: leave out constraints and authorizations, decisions already made, the
workspace and its ports, revisions, dates, evidence and how a finding was
reached, and the state of the record itself. Most of the record is written for
the agent that resumes the work. You have read it and you apply it in the work
that follows, and the user will ask for whatever else they want. Mention one of
these only inside the item it bears on, such as a step that needs an
authorization the user has not given, and link a file only where an item asks
the user to look at it. Something missing from the record appears only as the
step that settles it, such as a question to answer or a check to run, and only
when a listed step depends on it. Work the summary out from `QUEST.md` alone,
without following links or investigating.

A summary of this size holds a dozen sentences at most, whatever the size of
the record: a longer record has more to leave out, not more to say. When a part
has more to say than it has room for, keep what the next step depends on and
trust the user to ask for the rest. Packing the rest in makes the summary hard
to read, whether by dropping words or by lengthening sentences, so write it
this way:

- Write whole sentences in plain words, and keep the words that carry the
  reasoning, such as "because", "so", and "but".
- Put one idea in each sentence. A sentence that runs past about twenty-five
  words is carrying more than one, so keep the idea the next step depends on
  and drop the other.
- Describe a thing instead of using the name the record gives it. "The retry
  fix" means something only to whoever was there. "Retrying the upload when the
  server times out" can be read cold.
- Leave out measurements, and how something works inside, unless the user's
  choice depends on them.
- When something is uncertain, say so with a word such as "probably". Why it is
  uncertain stays in the record.

Wait for the user's direction; when the opening prompt also includes a question
or request for work, load the context needed for that request and proceed in
the same turn.

An unchecked normal task remains pending. An unchecked `Approval:` item with a
result or outcome link awaits user approval and must not cause the underlying
work to be repeated; `Current State` must identify that approval explicitly. For
quest material predating the `Approval:` convention, also preserve that behavior
when `Current State` explicitly says the item awaits approval. Do not inspect a
checkout beyond that instruction file, or modify `QUEST.md`, merely because the
quest was opened.
