# Weekly Evaluation Cycle

Run the full Darwin selection cycle. Execute these steps in order.

## Steps

1. **Load registry** — read `registry.json`. List all projects with `status: "alive"`.

2. **Collect metrics** for each alive project:
   ```bash
   # Run for every alive project — this fetches CF analytics + revenue and writes metrics.json
   for id in $(python3 -c "import json; [print(p['id']) for p in json.load(open('registry.json'))['projects'] if p['status']=='alive']"); do
     bash scripts/fetch-metrics.sh "$id" || echo "WARNING: fetch failed for $id"
   done
   ```
   If `CLOUDFLARE_API_TOKEN` is not set, call `human_task` (medium priority) asking for it before
   proceeding — without traffic data the fitness scores will be incomplete.

3. **Score each project** using the fitness formula:
   ```
   fitness = (revenue * 0.6) + (traffic_score * 0.25) + (engagement_score * 0.15)
   ```
   - revenue: raw USD for the period
   - traffic_score: normalize unique visitors to 0–100 (fleet-relative)
   - engagement_score: normalize avg session + return visitor rate to 0–100

4. **Update registry** — append results to `fitness_history` for each project, increment `cycles_alive`.

5. **Identify tier** — sort by fitness:
   - Top 25%: winners → will be mutated (use `/mutate-project`)
   - Bottom 25%: losers → eligible for kill IF `cycles_alive >= 2`
   - Middle 50%: survivors

6. **Kill losers** — for each project eligible for killing:
   - Call `human_task` with `high` priority listing the project, its fitness, and requesting confirmation
   - Set `status: "pending-kill"` in registry (actual deletion happens after human confirms)

7. **Mutate winners** — for each top-tier project, run `/mutate-project` with its ID.

8. **Fill empty slots** — if total alive projects < target fleet size, run `/spawn-project` to fill.

9. **Commit results**:
   ```bash
   git add registry.json projects/
   git commit -m "cycle {{cycle_number}}: evaluation complete"
   git push
   ```

10. **Report to human** — call `human_task` (medium priority) with a cycle summary: who won, who's pending kill, what was spawned, current fleet size, total estimated revenue.

Target fleet size: **5 projects** initially. Adjust in `registry.json` as the ecosystem matures.
