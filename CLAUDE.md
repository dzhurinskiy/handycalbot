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

## Environment & Deployment

- GitHub Secrets are the source of truth for all environment variables
- The `.env` file is recreated during CI/CD automated deployment from GitHub Secrets
- Never manually edit `.env` on VPS - update GitHub Secrets instead and redeploy
- Production domain: `handycal.dzhurinskiy.com`
