# Deploy to Cloudflare Pages

Use this skill when a project is a **website, web tool, or digital product** that needs
a public URL. This skill is optional \u2014 non-digital projects (services, consulting pitches,
physical products, outreach campaigns) do not need to deploy anywhere.

## Prerequisites

- `CLOUDFLARE_API_TOKEN` environment variable must be set (get from Cloudflare dashboard → My Profile → API Tokens → "Edit Cloudflare Pages" permission)
- `CLOUDFLARE_ACCOUNT_ID` environment variable must be set
- `wrangler` CLI available: `npm install -g wrangler`

If these are not set, call `human_task` with priority `critical` asking the human to provide them.

## Steps

### First deploy (new project)

1. Check if the CF project exists:
   ```bash
   wrangler pages project list 2>/dev/null | grep <project-slug>
   ```

2. If it doesn't exist, create it:
   ```bash
   wrangler pages project create <project-slug> --production-branch main
   ```

3. Deploy the project directory:
   ```bash
   cd projects/<id>
   wrangler pages deploy . --project-name <project-slug> --branch main
   ```

4. Capture the deployment URL from the output and update `registry.json` with `cf_url`.

### Update existing project

```bash
cd projects/<id>
wrangler pages deploy . --project-name <cf_project> --branch main
```

### Verify deployment

After deploying, verify the URL is live:
```bash
curl -s -o /dev/null -w "%{http_code}" <cf_url>
```
Expected: 200. If not, check build logs and report via `human_task`.

## Notes

- Each project should have its own CF Pages project with the same name as its registry ID
- Static files deploy as-is; if the project needs a build step, add a `build.sh` and run it before deploying
- CF Pages free tier: unlimited sites, 500 builds/month — sufficient for the fleet
- Custom domains: configure manually via CF dashboard after the project proves fitness
