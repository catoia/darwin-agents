# Task Log: B2B Cold Email Consulting

Task agents append their results here after completion.

---


---

## [2026-04-29] Task: Email Copywriter — 3-Email Cold Sequence

**Agent:** Task agent (email-copywriter)  
**Output:** `projects/b2b-cold-email-consulting/email-templates.md`

### Template Structure Overview

Created a complete 3-email cold sequence targeting B2B SaaS founders (Seed–Series A):

| Email | Day | Subject | Length | Purpose |
|---|---|---|---|---|
| Email 1: The Hook | 0 | `{{FirstName}}, quick cold email feedback?` | ~90 words | Personalized hook + 1 actionable tip + soft CTA |
| Email 2: The Nudge | 3 | `Re: quick cold email feedback?` | ~70 words | New value (CTA placement tip) + re-offer |
| Email 3: The Breakup | 7 | `Last one, then I'll stop` | ~50 words | Pattern interrupt + final tip + graceful exit |

**Personalization variables:** `{{FirstName}}`, `{{Company}}`, `{{Hook}}`, `{{SpecificTip}}`

**Hook variants (5 triggers):** LinkedIn post, fundraise announcement, Product Hunt launch, sales hiring signal, recent content/podcast.

**Industry-specific tip variants (4 industries × 3 tips = 12 total):** Devtools, Fintech, HR Tech, Martech.

---

### Key Differentiators From Generic Cold Emails

1. **Value before ask.** Every email delivers one concrete, actionable fix before making any request. The reader gets value whether they book or not — this builds trust and reduces delete-rate.

2. **Trigger-based personalization.** The `{{Hook}}` system connects outreach to a real recent event (funding, launch, hiring). This makes email 1 feel researched, not blasted.

3. **Industry-specific tips.** Instead of generic "improve your subject line" advice, the tips are calibrated to the cognitive mode of each buyer type (devtools = ROI first; fintech = trust signals; HR = risk mitigation; martech = revenue attribution).

4. **Progressive value across the sequence.** Each email introduces a *new* tip rather than repeating the pitch. By email 3, even non-converters have received 3 useful insights — making a future reply more likely.

5. **Plain-text format.** No HTML, no logos, no formatted signatures. Cold emails in plain text land in primary inbox more reliably and read as peer-to-peer, not vendor blast.

6. **Hard stop at email 3.** The breakup email signals respect for their time and exits cleanly. This protects sender reputation and leaves the door open for future contact.

---

### Conversion Hypothesis

**Why this sequence should work:**

The primary bottleneck for cold email consulting pitches is *trust* — a stranger claiming to fix your emails is easy to ignore. This sequence bypasses that by proving competence in the email itself. Each touch delivers one real fix, making the implicit message: "If I gave you this for free in 80 words, imagine what 15 minutes looks like."

The industry-specific tips increase relevance significantly. A devtools founder who reads "your subject line sounds like a product announcement — try leading with the outcome" is far more likely to self-identify with the problem than someone who reads generic subject-line advice.

Expected benchmarks based on this approach:
- Open rate: 45–60% (short subject, plain text, from a real person name)
- Reply rate: 8–15% (value-first, low friction ask)
- Teardown booking rate: 4–8% of cold list
- Teardown → paid session conversion: 30–40% (founder has already seen proof of value)

**Target outcome:** 10 teardown calls per 200 outreach emails → 3–4 paid sessions @ $200 = $600–$800 per campaign run.

