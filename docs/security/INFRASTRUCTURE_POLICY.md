# Infrastructure and Dependency Management Policy

## HandyCalBot Infrastructure Security Policy

**Document Version**: 1.0
**Effective Date**: January 2026
**Last Review**: January 2026
**Next Review**: January 2027
**Owner**: HandyCalBot Development Team

---

## 1. Purpose

This policy establishes standards for managing and securing the infrastructure and dependencies used by HandyCalBot. It ensures consistent, secure, and reliable operation of all system components.

---

## 2. Scope

This policy covers:
- Cloud infrastructure (VPS)
- Container runtime (Docker)
- Database systems (PostgreSQL)
- Reverse proxy (Nginx)
- Third-party dependencies (Python packages)
- CI/CD pipelines (GitHub Actions)
- External integrations (Google, Zoom, Telegram)

---

## 3. Infrastructure Architecture

### 3.1 Production Environment

```
┌─────────────────────────────────────────────────────────────┐
│  DigitalOcean VPS (Ubuntu)                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Docker Network                                          │ │
│  │  ┌──────────┐  ┌─────────────┐  ┌──────────────────┐    │ │
│  │  │  Nginx   │──│  CalendarBot│──│  PostgreSQL 15   │    │ │
│  │  │  (443)   │  │  (8000)     │  │  (5432-internal) │    │ │
│  │  └──────────┘  └─────────────┘  └──────────────────┘    │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │
         │ HTTPS (TLS 1.2+)
         │
    ─────┴───── Internet
```

### 3.2 Component Inventory

| Component | Version | Purpose | Update Frequency |
|-----------|---------|---------|------------------|
| Ubuntu Server | 22.04 LTS | Host OS | Security: immediate, LTS cycle |
| Docker | Latest stable | Container runtime | Monthly |
| Nginx | Latest stable | Reverse proxy, TLS | Monthly |
| PostgreSQL | 15 (Alpine) | Database | Security patches |
| Python | 3.11+ | Application runtime | With base image |
| Let's Encrypt | Automated | TLS certificates | Auto-renewed |

---

## 4. Infrastructure Security

### 4.1 Server Hardening

**Required Configurations**:

```bash
# SSH Configuration (/etc/ssh/sshd_config)
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers deploy

# Firewall (ufw)
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP (redirect)
ufw allow 443/tcp   # HTTPS
ufw enable
```

**Checklist**:
- [ ] SSH key-only authentication
- [ ] Root login disabled
- [ ] Firewall enabled with minimal ports
- [ ] Automatic security updates enabled
- [ ] Fail2ban installed and configured
- [ ] Unnecessary services disabled

### 4.2 Network Security

| Layer | Control |
|-------|---------|
| Network | Firewall (ufw), minimal exposed ports |
| Transport | TLS 1.2+, Let's Encrypt certificates |
| Application | Nginx security headers |
| Container | Docker network isolation |

### 4.3 Access Control

**SSH Access**:
- Key-based authentication only
- Keys rotated annually
- Access logged and auditable
- Fail2ban for brute force protection

**Database Access**:
- Internal network only (not exposed)
- Strong password (stored in GitHub Secrets)
- Application-specific user (not root)

### 4.4 Monitoring

| What | How | Alerting |
|------|-----|----------|
| Application health | `/health` endpoint | External uptime monitor |
| Container status | Docker health checks | Restart policy |
| Disk usage | System monitoring | At 80% threshold |
| Error rates | Application logs | Telegram notifications |

---

## 5. Container Management

### 5.1 Docker Security Standards

**Base Image Selection**:
- Use official images only
- Prefer minimal images (Alpine, slim variants)
- Pin specific versions (not `latest` in production)

**Dockerfile Best Practices**:
```dockerfile
# Use specific version
FROM python:3.11-slim

# Run as non-root user
RUN useradd -m appuser
USER appuser

# Minimize layers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# No secrets in image
ENV CONFIG_FILE=/config/settings.env
```

**Runtime Security**:
- No privileged containers
- Read-only filesystem where possible
- Resource limits (memory, CPU)
- Health checks configured

### 5.2 Container Lifecycle

| Action | Procedure |
|--------|-----------|
| Build | CI/CD pipeline with security scan |
| Deploy | Docker Compose with health checks |
| Update | Pull new image, recreate container |
| Rollback | Use previous image tag |

### 5.3 Image Updates

**Frequency**: Monthly or on security advisory

**Process**:
```bash
# Pull latest base images
docker pull python:3.11-slim
docker pull postgres:15-alpine
docker pull nginx:alpine

# Rebuild application
docker compose build --no-cache

# Deploy with health check
docker compose up -d
curl https://handycal.dzhurinskiy.com/health
```

---

## 6. Database Management

### 6.1 PostgreSQL Security

**Configuration**:
```
# Network
listen_addresses = 'localhost'  # Not exposed externally

# Authentication
password_encryption = scram-sha-256

# Connections
max_connections = 100
```

**Access Control**:
- Application user with minimal privileges
- No remote connections
- Connection via Docker network only

### 6.2 Backup Procedures

| Backup Type | Frequency | Retention |
|-------------|-----------|-----------|
| Full dump | Daily | 7 days |
| WAL archiving | Continuous | 7 days |

**Backup Command**:
```bash
docker exec calendarbot-db pg_dump -U calendarbot calendarbot > backup_$(date +%Y%m%d).sql
```

### 6.3 Recovery Procedures

```bash
# Restore from backup
docker exec -i calendarbot-db psql -U calendarbot calendarbot < backup_YYYYMMDD.sql
```

---

## 7. Dependency Management

### 7.1 Python Dependencies

**Approved Package Sources**:
- PyPI (primary)
- GitHub (for specific requirements only)

**Version Pinning**:
```
# requirements.txt
fastapi==0.104.1
sqlalchemy==2.0.23
python-telegram-bot==21.0
```

**Update Frequency**:
- Security updates: Immediate per CVE severity
- Feature updates: Monthly review
- Major versions: Tested before adoption

### 7.2 Dependency Review Process

**Before Adding New Dependency**:
1. Check maintenance status (last commit, open issues)
2. Review security history (past CVEs)
3. Assess size and dependency tree
4. Verify license compatibility (MIT, Apache, BSD)
5. Check for alternatives with smaller footprint

**Criteria**:
| Factor | Requirement |
|--------|-------------|
| Maintenance | Active within 6 months |
| Security | No unpatched critical CVEs |
| License | OSI-approved, compatible with MIT |
| Popularity | Prefer widely-used packages |

### 7.3 Vulnerability Scanning

**Automated Scanning**:
```yaml
# CI/CD pipeline
- name: Security scan
  run: |
    pip-audit
    bandit -r src/
```

**Manual Review**:
- Monthly review of Dependabot alerts
- Quarterly dependency audit

### 7.4 Dependency Update Procedure

```bash
# 1. Review what needs updating
pip list --outdated

# 2. Update specific package
pip install --upgrade [PACKAGE]

# 3. Run tests
pytest

# 4. Check for breaking changes
# Review changelog

# 5. Update requirements
pip freeze > requirements.txt

# 6. Commit and deploy
git add requirements.txt
git commit -m "Update [PACKAGE] to [VERSION]"
git push
```

---

## 8. CI/CD Security

### 8.1 GitHub Actions Security

**Workflow Security**:
```yaml
# Use specific versions for actions
uses: actions/checkout@v4

# Limit permissions
permissions:
  contents: read

# Use secrets for credentials
env:
  ENCRYPTION_KEY: ${{ secrets.ENCRYPTION_KEY }}
```

**Secrets Management**:
- All credentials in GitHub Secrets
- Secrets never logged or exposed
- Rotation: Annual or on compromise

### 8.2 Deployment Pipeline

```
Code Push → Lint → Test → SAST Scan → Build → Deploy → Health Check
```

**Security Gates**:
- Linting must pass
- Tests must pass
- SAST scan must pass (no high/critical)
- Health check must succeed

---

## 9. Third-Party Integrations

### 9.1 API Security

| Integration | Authentication | Token Storage |
|-------------|----------------|---------------|
| Google Calendar | OAuth 2.0 | Encrypted (Fernet) |
| Zoom | OAuth 2.0 | Encrypted (Fernet) |
| Telegram | Bot Token | Environment variable |

### 9.2 Credential Rotation

| Credential | Rotation Frequency |
|------------|-------------------|
| OAuth Client Secrets | Annual |
| Encryption Key | Annual |
| Database Password | Annual |
| SSH Keys | Annual |

### 9.3 Integration Monitoring

- Monitor OAuth token refresh failures
- Alert on integration errors
- Log API call failures (not sensitive data)

---

## 10. Change Management

### 10.1 Infrastructure Changes

**Process**:
1. Document proposed change
2. Assess security impact
3. Test in development (if applicable)
4. Schedule maintenance window (if downtime)
5. Implement change
6. Verify functionality
7. Document completion

### 10.2 Emergency Changes

For critical security patches:
1. Assess urgency and risk
2. Implement fix
3. Verify functionality
4. Document retroactively

---

## 11. Disaster Recovery

### 11.1 Recovery Objectives

| Metric | Target |
|--------|--------|
| RTO (Recovery Time Objective) | 4 hours |
| RPO (Recovery Point Objective) | 24 hours |

### 11.2 Recovery Procedures

**Complete System Recovery**:
1. Provision new VPS
2. Install Docker and dependencies
3. Restore database from backup
4. Deploy application containers
5. Update DNS if needed
6. Verify functionality

**Container Recovery**:
```bash
# Pull and restart all containers
docker compose pull
docker compose up -d

# Verify
curl https://handycal.dzhurinskiy.com/health
```

---

## 12. Compliance

### 12.1 Standards Alignment

This policy aligns with:
- CIS Docker Benchmark
- CIS Ubuntu Benchmark
- OWASP Dependency Check recommendations
- NIST Cybersecurity Framework

### 12.2 Audit Trail

Maintain logs for:
- SSH access
- Docker operations
- Database access
- Deployment activities

---

## 13. Roles and Responsibilities

| Role | Infrastructure | Dependencies | CI/CD |
|------|---------------|--------------|-------|
| Developer | - | Update, review | Configure |
| Operations | Manage, patch | - | Deploy |
| Security | Audit, advise | Scan, review | Audit |

---

## 14. Review and Updates

This policy is reviewed:
- Quarterly for dependency management
- Annually for infrastructure standards
- After significant incidents
- When adopting new technologies

---

## 15. Related Documents

- Security Policy
- Incident Response Policy
- Vulnerability Management Procedures
- SSDLC Documentation

---

*Last Updated: January 2026*
