# Secure Software Development Lifecycle (SSDLC)

## HandyCalBot - SSDLC Documentation

**Document Version**: 1.0
**Last Updated**: January 2026
**Organization**: HandyCalBot

---

## 1. Executive Summary

HandyCalBot implements a Secure Software Development Lifecycle (SSDLC) that integrates security practices throughout all phases of development. This document outlines our processes, tools, and controls that ensure security is built into our application from design through deployment.

---

## 2. SSDLC Phases

### 2.1 Requirements & Design Phase

#### Security Requirements
- All features are evaluated for security implications before development
- OAuth integrations follow provider security best practices (Google, Zoom)
- Data minimization principles applied - only collect data necessary for functionality
- Privacy-by-design: Users can opt for "Privacy Mode" with reduced permissions

#### Threat Modeling
- OAuth flow threat analysis performed for all integrations
- STRIDE methodology applied to identify threats:
  - **S**poofing: Mitigated via state parameter in OAuth flows
  - **T**ampering: Mitigated via HTTPS-only communications
  - **R**epudiation: Logging of security-relevant events
  - **I**nformation Disclosure: Encryption at rest for all credentials
  - **D**enial of Service: Rate limiting on API endpoints
  - **E**levation of Privilege: Minimal OAuth scopes requested

#### Design Reviews
- Architecture decisions documented in code repository
- Security-sensitive components reviewed before implementation
- Third-party library selection includes security evaluation

### 2.2 Development Phase

#### Secure Coding Standards
- **Python Security Guidelines**: Follow OWASP Python Security Guidelines
- **Input Validation**: All user inputs validated and sanitized
- **Output Encoding**: HTML responses properly encoded
- **Authentication**: OAuth 2.0 with state parameter for CSRF protection
- **Encryption**: Fernet (AES-256) for credential storage

#### Code Review Process
- All code changes require pull request
- Automated linting (Ruff) enforces code quality
- Security-focused review for OAuth and encryption code
- No hardcoded credentials allowed

#### Development Tools
| Tool | Purpose |
|------|---------|
| Ruff | Python linter and code quality |
| Black | Code formatting |
| MyPy | Static type checking |
| Git | Version control with signed commits |

### 2.3 Testing Phase

#### Static Application Security Testing (SAST)
- **Tool**: Bandit (Python security linter)
- **Frequency**: Every commit via CI/CD pipeline
- **Coverage**: All source code in `src/` directory
- **Findings**: Reviewed and remediated before merge

#### Dynamic Application Security Testing (DAST)
- **Tools**: Manual testing, curl-based endpoint verification
- **Scope**: All public endpoints
- **Tests Include**:
  - TLS configuration verification
  - Security header validation
  - CORS policy verification
  - OAuth flow security testing

#### Dependency Scanning
- **Tool**: pip-audit, GitHub Dependabot
- **Frequency**: Weekly automated scans
- **Process**: Critical vulnerabilities addressed within 72 hours

#### Testing Coverage
```
Test Types:
├── Unit Tests (pytest)
├── Integration Tests (OAuth flow simulation)
├── Security Tests (Bandit SAST)
└── Dependency Vulnerability Scans (pip-audit)
```

### 2.4 Deployment Phase

#### CI/CD Pipeline Security
```
GitHub Actions Pipeline:
1. Code Push
2. Lint Check (Ruff)
3. Type Check (MyPy)
4. Unit Tests (pytest)
5. SAST Scan (Bandit)
6. Build Docker Image
7. Deploy to Production
8. Health Check Verification
```

#### Deployment Security Controls
- **Infrastructure**: Docker containers on isolated VPS
- **Secrets Management**: GitHub Secrets (encrypted at rest)
- **Network**: Nginx reverse proxy with TLS termination
- **Access**: SSH key-only authentication, no password access
- **Monitoring**: Container logs, health checks every 30 seconds

#### Configuration Management
- Environment variables for all secrets
- No `.env` files in version control
- Production configuration managed via GitHub Secrets
- Database credentials rotated periodically

### 2.5 Operations & Maintenance Phase

#### Security Monitoring
- Application logs monitored for errors and anomalies
- Health endpoint (`/health`) monitored externally
- Uptime monitoring with alerting

#### Patch Management
- Security updates applied within 7 days of release
- Critical vulnerabilities patched within 24-48 hours
- Dependency updates reviewed weekly

#### Incident Response
- Documented incident response procedures
- Contact points for security issues
- Post-incident review process

---

## 3. Security Controls Summary

| Control Category | Implementation |
|-----------------|----------------|
| Authentication | OAuth 2.0 with state parameter |
| Authorization | Minimal OAuth scopes |
| Encryption in Transit | TLS 1.2+ (TLS 1.3 preferred) |
| Encryption at Rest | Fernet (AES-256) for credentials |
| Input Validation | Server-side validation on all inputs |
| Logging | Security events logged (no sensitive data) |
| Error Handling | Generic error messages, detailed internal logs |
| Session Management | OAuth tokens with automatic refresh |
| CSRF Protection | State parameter in OAuth flows |
| XSS Protection | Content-Security-Policy, X-XSS-Protection headers |
| Clickjacking Protection | X-Frame-Options: SAMEORIGIN |

---

## 4. Compliance & Standards

HandyCalBot development follows these security standards and guidelines:

- **OWASP Top 10** - Web application security risks mitigation
- **OWASP ASVS** - Application Security Verification Standard
- **CWE/SANS Top 25** - Most dangerous software weaknesses
- **OAuth 2.0 Security Best Practices** (RFC 6819)
- **NIST Cybersecurity Framework** - Identify, Protect, Detect, Respond, Recover

---

## 5. Security Training

Development team security awareness includes:
- OAuth 2.0 security best practices
- Common web application vulnerabilities
- Secure coding practices for Python
- Encryption and key management
- Incident response procedures

---

## 6. Continuous Improvement

Security practices are continuously improved through:
- Regular review of security scan findings
- Analysis of new vulnerability disclosures
- Updates to security policies and procedures
- Lessons learned from incidents
- Industry best practice adoption

---

## 7. Contact

For security-related inquiries:
- **Email**: security@handycal.dzhurinskiy.com
- **GitHub Security Advisories**: https://github.com/dzhurinskiy/handycalbot/security

---

*This document is reviewed and updated quarterly or when significant changes occur to the development process.*
