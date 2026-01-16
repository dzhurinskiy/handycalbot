# Claude Code Instructions

## Project Management

- Be proactive and autonomous - do as much work as needed without asking for permission
- The user manages the project, Claude codes and executes tasks
- When something needs to be done (VPS setup, deployments, fixes), just do it
- Only ask questions when truly blocked or need critical business decisions

## Git/SSH

- Always use SSH keys for Git and VPS connections, never prompt for passwords
- The VPS at 164.92.157.14 should be accessed via SSH key authentication
- GitHub remote should use SSH URL format: `git@github.com:dzhurinskiy/handycalbot.git`

## VPS Connection Management - CRITICAL RULES

**NEVER violate these rules - they prevent VPS lockups that require power cycling:**

1. **ONE SSH connection at a time** - NEVER run SSH in parallel, NEVER use background mode for SSH
2. **Chain all commands** - Use `&&` to run multiple commands in a single SSH call
3. **Always use timeout** - Every SSH command must include `-o ConnectTimeout=10`
4. **Prefer HTTPS health checks** - Use `curl https://handycal.dzhurinskiy.com/health` instead of SSH when possible
5. **Trust the CI/CD** - After `git push`, let GitHub Actions handle deployment. Don't SSH to monitor.
6. **Max 1 SSH per minute** - Wait at least 60 seconds between SSH connections

**Standard SSH command format (use the handycal alias from ~/.ssh/config):**
```bash
ssh -o ConnectTimeout=10 -o BatchMode=yes handycal "command1 && command2 && command3"
```

- `handycal` - SSH alias configured in `~/.ssh/config` with correct key and host
- `-o BatchMode=yes` - REQUIRED: prevents password prompts, fails fast if key doesn't work

**Deployment workflow (NO SSH monitoring):**
1. Make code changes
2. `git push` - triggers GitHub Actions
3. Wait for Telegram notification (success/failure)
4. Verify via HTTPS: `curl https://handycal.dzhurinskiy.com/health`
5. Only SSH if health check fails AND you need to debug

## Environment & Deployment

- GitHub Secrets are the source of truth for all environment variables
- The `.env` file is recreated during CI/CD automated deployment from GitHub Secrets
- Never manually edit `.env` on VPS - update GitHub Secrets instead and redeploy
- Production domain: `handycal.dzhurinskiy.com`

## Deployment Verification - CRITICAL

**After every `git push`, you MUST verify deployment success:**

1. **Check GitHub Actions** - Go to the repository's Actions tab or use `gh run list` to see the latest workflow runs
2. **Both CI and CD must pass**:
   - CI (lint/tests) - runs ruff linter and any tests
   - CD (deploy) - deploys to VPS
3. **If CI fails (lint errors)**:
   - Read the error output carefully
   - Fix all lint errors (unused imports, import sorting, f-strings without placeholders, unused arguments)
   - Push again and verify
4. **Repeat until fully successful** - Never consider deployment done until both CI and CD show green checkmarks

**Common lint errors to watch for:**
- Unused imports: Remove them
- Import blocks unsorted: Use `ruff --fix` or manually sort (stdlib → third-party → local)
- f-strings without placeholders: Remove the `f` prefix
- Unused function arguments: Prefix with underscore (e.g., `_context`)

**Quick verification command:**
```bash
gh run list --limit 5
```
