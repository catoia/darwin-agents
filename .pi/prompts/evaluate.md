# Weekly Evaluation Cycle

Run the full Darwin selection cycle. Execute these steps in order.

## Steps

1. **Load registry** — read `registry.json`. List all projects with `status: "alive"`.

2. **Collect metrics** for each alive project:
   ```bash
   # Run for every alive project — fetches CF analytics + revenue and writes metrics.json
   for id in $(python3 -c "import json; [print(p['id']) for p in json.load(open('registry.json'))['projects'] if p['status']=='alive']"); do
     bash scripts/fetch-metrics.sh "$id" || echo "WARNING: fetch failed for $id"
   done
   ```
   - **Digital projects**: CF analytics provides traffic/engagement. Without `CLOUDFLARE_API_TOKEN`, call `human_task` (medium) to request it.
   - **Non-digital projects** (service, consulting, physical, outreach): traffic metrics are irrelevant. Revenue comes from `projects/<id>/revenue-manual.json` — the human writes entries there after each real-world transaction. Zero is an honest score if nothing was sold.

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

8. **Fill empty slots** — if total alive projects < `registry.target_fleet_size`, run `/spawn-project` to fill. Read the value from `registry.json` (key `target_fleet_size`); default to 5 if the key is absent.

9. **Commit results**:
   ```bash
   git add registry.json projects/
   git commit -m "cycle {{cycle_number}}: evaluation complete"
   git push
   ```

10. **Report to human** — call `human_task` (medium priority) with a cycle summary: who won, who's pending kill, what was spawned, current fleet size, total estimated revenue.

Target fleet size is stored in `registry.json` under `target_fleet_size`. Adjust it there as the ecosystem matures.
