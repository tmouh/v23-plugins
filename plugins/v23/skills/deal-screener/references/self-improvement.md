# Self-Improvement Protocol

The skill improves over time through three mechanisms. This file is the reference for how each works.

## Mechanism 1 — Skill self-observation during a run

After producing a screening report, before signing off, the model takes a beat and reflects:

- Was there a moment where I almost missed something subtle?
- Was there a calculation I had to redo three different ways before I trusted it?
- Did the OM use a framing or trick that future OMs are likely to use again?
- Did the user redirect me, correct me, or push back during the review?
- Did I have to invent process to fill a gap in the skill's instructions?

If yes to any, **propose a lesson** in the report's "Proposed Lesson" section. Format:

```
PROPOSED LESSON:
[Imperative-voice rule]
Context: [Which deal, which trick, why it matters]
```

The user reviews and decides:
- "Yes, add it" → append to `lessons-learned.md` with the next LL-NNN, confirm
- "Modify and add" → revise and append
- "No, skip it" → don't add, move on

Be selective. A weak lesson is worse than no lesson because it pollutes the file. The bar: would I want to re-read this rule on every future screening? If not, don't propose it.

## Mechanism 2 — User-driven post-mortem

The user comes back after a deal closes (or doesn't) and says something like:
- "We missed X on the last deal — add a check for that"
- "The Acme deal blew up because of Y; add a rule"
- "From now on, always Z"

The model:
1. Acknowledges and asks for any additional context if needed
2. Drafts the rule in the lessons-learned format
3. Shows it to the user for confirmation
4. Appends to `lessons-learned.md` with the next LL-NNN
5. Confirms

If the lesson would be better expressed as an addition to one of the asset-class checklists, the red-flags library, or the output template, propose that instead — and route the addition there with the user's approval.

## Mechanism 3 — Direct skill editing

The user comes back to "improve the skill" without a specific lesson in mind:
- "I want to make the screening faster"
- "Tighten the output format"
- "Add a section on X"
- "The skill is too pushy on Y; pull it back"

The model:
1. Asks what specifically the user wants to change
2. Identifies the right file(s) to edit (SKILL.md, output-template, an asset-class checklist, etc.)
3. Drafts the change
4. Shows the diff or the new text to the user
5. Saves on confirmation

Never edit the skill silently. The user is the final arbiter.

## What goes where

When a new piece of knowledge needs to be added, route it to the right file:

| If it's about... | It goes in... |
|---|---|
| A general rule that applies across all deals | `lessons-learned.md` |
| A red flag that applies across asset classes | `red-flags.md` |
| A nuance specific to one asset class | `asset-class-[type].md` |
| A nuance specific to one V23 seat | `seat-context.md` |
| A change in the deliverable structure | `output-template.md` |
| A change in workflow or top-level behavior | `SKILL.md` |
| A change in the self-improvement protocol itself | This file |

When in doubt, ask the user where they want it.

## Quality control

Every few months — or when the user invokes "review the skill" — go through `lessons-learned.md` and:
- Check for redundancy (multiple lessons saying similar things; consolidate)
- Check for staleness (lessons referencing dated market conditions; mark as needing update)
- Check for conflicts (lessons that contradict each other)
- Check for non-rules (lessons that are observations rather than imperatives — promote or demote)

This is housekeeping. Don't do it during a deal screening; do it as a separate session.

## What this skill does NOT do automatically

- **Does not silently modify itself.** Every change to any file requires user confirmation.
- **Does not learn from a single example.** A pattern needs to recur (or be flagged by the user) before it becomes a lesson. One-off oddities don't deserve permanent rules.
- **Does not delete old lessons.** Retired lessons go in a `## Retired Lessons` section, not the trash. Keeps history.
- **Does not auto-generate from training data.** The skill grows from V23's actual deals, not from generic best practices.
