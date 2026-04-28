# Mutate Project (Clone a Winner)

You are creating a genetic mutation of an existing successful project. This is how the ecosystem evolves.

**Parent project ID:** {{parent_id}}

## Steps

1. **Read the parent** — study `projects/{{parent_id}}/AGENTS.md`, its metrics in `registry.json`, and its deployed content. Understand *why* it won.

2. **Design the mutation** — pick ONE of these strategies (choose based on what the data suggests):
   - **Niche pivot**: same format, different target audience or keyword cluster
   - **Format upgrade**: same topic, different medium (e.g., text → interactive tool)
   - **Monetization upgrade**: same content, different revenue mechanism
   - **Audience expansion**: same core, broader or narrower audience
   - **Competitive differentiation**: same space, but address the gap the parent left

3. **Create the mutation** — new slug = `{{parent_id}}-m<N>` where N is the mutation number. Scaffold `projects/<new-id>/` with:
   - `AGENTS.md` referencing the parent and documenting the mutation strategy
   - Fresh content/code building on the parent's strengths
   - `metrics.json` (empty)

4. **Deploy** to Cloudflare Pages using `/skill:deploy-cloudflare`

5. **Register** in `registry.json` with `"parent_id": "{{parent_id}}"` and `"generation": <parent_generation + 1>`

6. **Notify human** via `human_task` (low priority) — include parent URL, mutation strategy, and new URL.

The mutation should be meaningfully different from the parent, not just a copy. Evolution only works if mutations create real variation.
