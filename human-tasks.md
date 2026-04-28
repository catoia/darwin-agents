# Human Task Inbox

This file is the **single place** where agents queue tasks that require human judgment.
Agents append here — they never block waiting for answers.
You (the human) reply inline below each open task, then set its status to `done`.

## How to respond

Find the open task, add your reply **immediately below the Context section**, then change `**Status:** open` to `**Status:** done`. Example:

```markdown
### Context
Should we kill project X with fitness 2.1?

**Human response:** yes, confirmed — kill it
**Status:** done
```

The god agent reads this at the start of every session and acts on `done` entries with a human response.
Do not delete entries — the history is the audit trail.

---

<!-- AGENTS: append new tasks at the bottom. Never edit existing entries — only the human edits Status and adds Human response. -->

