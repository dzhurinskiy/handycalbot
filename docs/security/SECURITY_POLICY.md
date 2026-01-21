# Security Policy

## HandyCalBot Information Security Policy

**Document Version**: 1.0
**Effective Date**: January 2026
**Last Review**: January 2026
**Next Review**: January 2027
**Owner**: HandyCalBot Development Team

---

## 1. Purpose

This Security Policy establishes the security principles, requirements, and responsibilities for the development, deployment, and operation of HandyCalBot. It ensures the confidentiality, integrity, and availability of user data and system resources.

---

## 2. Scope

This policy applies to:
- All HandyCalBot application components
- Development and production environments
- All team members with system access
- Third-party integrations (Google, Zoom, Telegram)
- All data processed by the application

---

## 3. Security Principles

### 3.1 Defense in Depth
Multiple layers of security controls protect against various attack vectors. No single control is relied upon exclusively.

### 3.2 Least Privilege
Access rights are limited to the minimum necessary for legitimate purposes. OAuth scopes request only required permissions.

### 3.3 Privacy by Design
Privacy considerations are integrated into system design. Users can choose "Privacy Mode" for minimal data access.

### 3.4 Secure by Default
Default configurations prioritize security. Features requiring elevated privileges must be explicitly enabled.

---

## 4. Access Control

### 4.1 Authentication Requirements

| System | Authentication Method |
|--------|----------------------|
| VPS Access | SSH key-only (password disabled) |
| GitHub | 2FA required, SSH keys |
| OAuth Integrations | OAuth 2.0 with state parameter |
| Database | Internal network only, credentials rotated |

### 4.2 Authorization

- Role-based access control for team members
- Minimal OAuth scopes for third-party integrations:
  - Google: `calendar.events`, `userinfo.email`
  - Zoom: `meeting:write`, `user:read`
- No administrative interfaces exposed to internet

### 4.3 Session Management

- OAuth tokens automatically refreshed before expiration
- Session state validated on each request
- CSRF protection via state parameter

---

## 5. Data Protection

### 5.1 Data Classification

| Classification | Examples | Protection |
|---------------|----------|------------|
| Confidential | OAuth tokens, API keys | Encrypted at rest and in transit |
| Internal | User settings, meeting data | Encrypted in transit, access controlled |
| Public | Landing page, help text | No special protection required |

### 5.2 Encryption Standards

| Data State | Standard |
|------------|----------|
| In Transit | TLS 1.2+ (TLS 1.3 preferred) |
| At Rest | Fernet (AES-256-CBC with HMAC) |
| Backups | Encrypted at rest |

### 5.3 Data Retention

- OAuth tokens: Retained until user disconnects or revokes
- Meeting data: Retained for reminder functionality, deleted after meeting
- Logs: Retained for 30 days, no sensitive data logged
- User settings: Retained until user deletes account

### 5.4 Data Minimization

- Only essential data collected
- No Zoom meeting content accessed or stored
- No calendar event content stored beyond reminder needs
- No user passwords stored (OAuth-only)

---

## 6. Network Security

### 6.1 Network Architecture

```
Internet → Cloudflare (optional) → Nginx (TLS termination) → Docker Container → Database
```

### 6.2 Firewall Rules

| Port | Service | Access |
|------|---------|--------|
| 22 | SSH | Restricted IPs, key-only |
| 80 | HTTP | Public (redirects to HTTPS) |
| 443 | HTTPS | Public |
| 5432 | PostgreSQL | Internal only |
| 8000 | Application | Internal only (via nginx) |

### 6.3 TLS Configuration

- Minimum TLS version: 1.2
- Preferred TLS version: 1.3
- Strong cipher suites only
- Automatic certificate renewal via Let's Encrypt

---

## 7. Application Security

### 7.1 Secure Development

- Code reviews required for all changes
- Automated security scanning (SAST) in CI/CD
- Dependency vulnerability scanning
- No hardcoded credentials

### 7.2 Input Validation

- All user inputs validated server-side
- Output encoding for HTML responses
- Parameterized queries via ORM
- File upload restrictions (if applicable)

### 7.3 Error Handling

- Generic error messages to users
- Detailed errors logged internally
- No stack traces exposed
- No sensitive data in error messages

### 7.4 Security Headers

Required headers for all responses:
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (recommended)

---

## 8. Infrastructure Security

### 8.1 Server Hardening

- Minimal OS installation
- Regular security updates
- SSH key-only authentication
- Fail2ban for brute force protection
- Automatic security updates enabled

### 8.2 Container Security

- Official base images only
- Non-root container user
- Read-only filesystem where possible
- No privileged containers
- Regular image updates

### 8.3 Secrets Management

- Environment variables for all secrets
- GitHub Secrets for CI/CD
- No secrets in source code
- Secrets rotated periodically

---

## 9. Monitoring & Logging

### 9.1 Logging Requirements

| Log Type | Retention | Contains PII |
|----------|-----------|--------------|
| Application logs | 30 days | No |
| Access logs | 30 days | IP addresses only |
| Error logs | 30 days | No sensitive data |
| Security events | 90 days | Minimal |

### 9.2 Monitoring

- Health endpoint monitoring (`/health`)
- Container resource monitoring
- Error rate alerting
- Uptime monitoring

### 9.3 Prohibited Logging

- OAuth access tokens
- Refresh tokens
- User passwords
- Complete request/response bodies with sensitive data

---

## 10. Third-Party Security

### 10.1 Vendor Assessment

Third-party services are evaluated for:
- Security certifications (SOC 2, ISO 27001)
- Data handling practices
- Encryption standards
- Incident response capabilities

### 10.2 Approved Third Parties

| Vendor | Purpose | Security |
|--------|---------|----------|
| Google | Calendar integration | SOC 2, ISO 27001 |
| Zoom | Meeting links | SOC 2, ISO 27001 |
| Telegram | Bot platform | Encrypted communications |
| GitHub | Source control, CI/CD | SOC 2 |
| DigitalOcean | Infrastructure | SOC 2, ISO 27001 |
| Let's Encrypt | TLS certificates | WebTrust certified |

---

## 11. Compliance

### 11.1 Regulatory Compliance

- GDPR: Data minimization, user rights, encryption
- CCPA: Privacy policy, data access rights
- OAuth Provider Terms: Google, Zoom API policies

### 11.2 Security Standards

The following standards guide our security practices:
- OWASP Top 10
- OWASP ASVS
- CWE/SANS Top 25
- NIST Cybersecurity Framework

---

## 12. Policy Enforcement

### 12.1 Compliance Verification

- Quarterly security reviews
- Annual penetration testing
- Continuous automated scanning
- Code review requirements

### 12.2 Exceptions

Any exceptions to this policy must be:
- Documented with business justification
- Approved by the project owner
- Time-limited with review date
- Compensating controls identified

---

## 13. Related Documents

- Incident Response Policy
- Vulnerability Management Procedures
- Infrastructure Management Policy
- Privacy Policy (https://handycal.dzhurinskiy.com/privacy)

---

## 14. Contact

Security inquiries: security@handycal.dzhurinskiy.com
GitHub Security: https://github.com/dzhurinskiy/handycalbot/security

---

*This policy is reviewed annually and updated as needed to address emerging threats and changing requirements.*
