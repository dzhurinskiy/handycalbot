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

## VPS Connection Management

- **Limit SSH connections**: Never run multiple SSH commands in parallel to the VPS
- **Chain commands**: Use `&&` to chain multiple commands in a single SSH session instead of separate calls
- **Use timeouts**: Always use `-o ConnectTimeout=10` for SSH connections
- **Avoid background SSH**: Don't run SSH commands in background mode - they can accumulate and overwhelm the server
- **Wait between operations**: After triggering a deployment, wait for it to complete before running more SSH commands
- **Single verification**: When checking VPS status, use one SSH call with all needed commands:
  ```bash
  ssh -o ConnectTimeout=10 root@164.92.157.14 "docker compose ps && docker compose logs app --tail 20"
  ```
- **If VPS becomes unresponsive**: Wait 2-3 minutes for connections to timeout before retrying

## Environment & Deployment

- GitHub Secrets are the source of truth for all environment variables
- The `.env` file is recreated during CI/CD automated deployment from GitHub Secrets
- Never manually edit `.env` on VPS - update GitHub Secrets instead and redeploy
- Production domain: `handycal.dzhurinskiy.com`
