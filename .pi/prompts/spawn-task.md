# Spawn Task Agent

Use this when you want to delegate a specific, bounded piece of work to a focused sub-agent.
You are the project agent. The agent you are spawning reports to you.

## Steps

1. **Define the task clearly** — what exactly should the task agent do, what files it can touch,
   and what "done" looks like. Vague tasks produce vague results.

2. **Write a task brief** to `projects/{{project_id}}/tasks/{{task_slug}}-brief.md`:
   ```markdown
   # Task: {{task_title}}
   
   **Project:** {{project_id}}
   **Requested by:** project-agent
   **Created:** <ISO timestamp>
   
   ## What to do
   <clear description>
   
   ## Files you may touch
   - projects/{{project_id}}/<specific paths>
   
   ## Definition of done
   <measurable outcome>
   
   ## Report back
   Append results to projects/{{project_id}}/task-log.md when finished.
   ```

3. **Spawn the task agent** via bash:
   ```bash
   pi --no-session \
      --provider github-copilot \
      --model claude-sonnet-4.5 \
      --context-files projects/{{project_id}}/AGENTS.md \
      --context-files projects/{{project_id}}/tasks/{{task_slug}}-brief.md \
      --append-system-prompt "You are a task agent. Read your brief carefully. Stay within scope. Report back to task-log.md when done." \
      -p "Execute the task described in your brief."
   ```

4. **After the task agent finishes**, read `task-log.md`, review the output, and decide:
   - Accept → deploy if needed, update `metrics.json` if results affect fitness
   - Revise → spawn another task agent with corrected instructions referencing the previous attempt
   - Revert → `git checkout` the affected files and document why in `experiments.md`

## Examples of good task agent scopes

- "Write 5 SEO article stubs targeting these 5 keywords, save as articles/*.html"
- "Run a Lighthouse audit on index.html and fix the top 3 performance issues"
- "Research the top 10 competitors for {{niche}} and produce a gap analysis in research/competitors.md"
- "Rewrite the homepage headline and hero copy, A/B test setup: save two variants as index-a.html and index-b.html"
- "Scan all internal links on the site and fix any broken ones"

## What task agents CANNOT do

- Access other projects' directories
- Modify `registry.json`
- Make purchases or sign up for services
- Spawn their own sub-agents (only project agents can spawn)
