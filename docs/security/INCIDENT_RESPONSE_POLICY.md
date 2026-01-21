# Incident Management and Response Policy

## HandyCalBot Incident Response Plan

**Document Version**: 1.0
**Effective Date**: January 2026
**Last Review**: January 2026
**Next Review**: January 2027
**Owner**: HandyCalBot Development Team

---

## 1. Purpose

This policy establishes procedures for identifying, responding to, and recovering from security incidents affecting HandyCalBot. It ensures consistent and effective incident handling to minimize impact and prevent recurrence.

---

## 2. Scope

This policy covers:
- Security incidents affecting HandyCalBot systems
- Data breaches involving user information
- Service disruptions impacting availability
- Unauthorized access attempts
- Malware or compromise indicators
- Third-party integration failures

---

## 3. Incident Classification

### 3.1 Severity Levels

| Level | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| **P1 - Critical** | Service down, data breach confirmed | 15 minutes | Data exfiltration, complete outage |
| **P2 - High** | Major functionality impaired, potential breach | 1 hour | OAuth compromise, partial outage |
| **P3 - Medium** | Minor impact, no data exposure | 4 hours | Performance degradation, failed backups |
| **P4 - Low** | Minimal impact, informational | 24 hours | Failed login attempts, minor errors |

### 3.2 Incident Types

| Type | Description |
|------|-------------|
| Security Breach | Unauthorized access to systems or data |
| Data Leak | Unintended exposure of sensitive data |
| Service Outage | Application unavailability |
| OAuth Compromise | Compromised OAuth tokens or credentials |
| Dependency Vulnerability | Critical vulnerability in dependencies |
| Infrastructure Failure | VPS, database, or network issues |

---

## 4. Incident Response Team

### 4.1 Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Incident Lead** | Coordinate response, make decisions, communicate |
| **Technical Lead** | Investigate, contain, remediate technical issues |
| **Communications** | User notifications, status updates |
| **Documentation** | Record timeline, actions, lessons learned |

### 4.2 Contact Information

- **Primary Contact**: Project maintainer
- **Escalation**: GitHub Security Advisories
- **Third-Party Contacts**:
  - Google Cloud Support (OAuth issues)
  - Zoom Support (Zoom API issues)
  - DigitalOcean Support (Infrastructure)

---

## 5. Incident Response Phases

### 5.1 Phase 1: Detection & Identification

**Objective**: Identify and confirm the incident

**Detection Sources**:
- Automated monitoring alerts
- User reports
- Security scan findings
- Log analysis
- Third-party notifications

**Initial Assessment**:
1. Confirm incident is real (not false positive)
2. Determine incident type and scope
3. Assign severity level
4. Activate response team if needed

**Documentation Required**:
- Date/time of detection
- Detection method
- Initial symptoms
- Systems affected

### 5.2 Phase 2: Containment

**Objective**: Limit the damage and prevent spread

**Immediate Actions by Severity**:

**P1/P2 - Critical/High**:
```bash
# Immediate containment options:

# 1. Revoke all OAuth tokens (if compromise suspected)
ssh handycal "docker exec calendarbot-db psql -U calendarbot -d calendarbot -c 'TRUNCATE oauth_tokens;'"

# 2. Take application offline (if active attack)
ssh handycal "docker stop calendarbot"

# 3. Block suspicious IPs (if DDoS/attack)
ssh handycal "ufw deny from [ATTACKER_IP]"

# 4. Rotate credentials
# - Update GitHub Secrets
# - Redeploy application
```

**P3/P4 - Medium/Low**:
- Monitor for escalation
- Apply patches if available
- Document findings

**Containment Checklist**:
- [ ] Affected systems isolated
- [ ] Attack vector blocked
- [ ] Evidence preserved
- [ ] Stakeholders notified

### 5.3 Phase 3: Eradication

**Objective**: Remove the threat and fix vulnerabilities

**Actions**:
1. Identify root cause
2. Remove malicious artifacts
3. Patch vulnerabilities
4. Update dependencies if needed
5. Rotate compromised credentials

**For OAuth Token Compromise**:
```bash
# Revoke specific user's tokens
ssh handycal "docker exec calendarbot-db psql -U calendarbot -d calendarbot -c \"DELETE FROM oauth_tokens WHERE user_id = [USER_ID];\""

# Force re-authentication
# User will need to /connect again
```

**For Dependency Vulnerabilities**:
```bash
# Update dependencies
pip install --upgrade [PACKAGE]

# Verify fix
pip-audit

# Deploy
git push origin main
```

### 5.4 Phase 4: Recovery

**Objective**: Restore normal operations

**Recovery Steps**:
1. Verify systems are clean
2. Restore from backup if needed
3. Restart services
4. Monitor for recurrence
5. Verify functionality

**Recovery Verification**:
```bash
# Health check
curl https://handycal.dzhurinskiy.com/health

# Verify OAuth flow
# Test Google and Zoom connections

# Check logs for errors
ssh handycal "docker logs calendarbot --tail=100"
```

**User Communication**:
- Notify affected users
- Provide remediation steps if needed
- Update status page

### 5.5 Phase 5: Lessons Learned

**Objective**: Improve future response

**Post-Incident Review**:
- Conduct within 5 business days of resolution
- All responders participate
- Document timeline and actions
- Identify improvement opportunities

**Review Questions**:
1. What happened and when?
2. How was it detected?
3. What went well in the response?
4. What could be improved?
5. What preventive measures should be implemented?

**Documentation**:
- Incident report
- Timeline of events
- Root cause analysis
- Action items with owners and deadlines

---

## 6. Communication Guidelines

### 6.1 Internal Communication

| Audience | Channel | Timing |
|----------|---------|--------|
| Response Team | Direct message | Immediate |
| Stakeholders | Email/Slack | Within 1 hour (P1/P2) |

### 6.2 External Communication

| Audience | Channel | Timing |
|----------|---------|--------|
| Affected Users | Telegram message | After containment |
| All Users | Status page/GitHub | For significant outages |
| Third Parties | Direct contact | If their systems affected |

### 6.3 Communication Templates

**User Notification (Data Breach)**:
```
Security Notice: We detected unauthorized access to [DESCRIPTION].
Affected: [WHAT DATA]
Action Taken: [CONTAINMENT STEPS]
Your Action: [USER STEPS - e.g., reconnect account]
Questions: security@handycal.dzhurinskiy.com
```

**Status Update (Outage)**:
```
[TIMESTAMP] Status Update
Issue: [DESCRIPTION]
Impact: [WHAT'S AFFECTED]
Status: [Investigating/Identified/Monitoring/Resolved]
ETA: [IF KNOWN]
```

---

## 7. Specific Incident Playbooks

### 7.1 OAuth Token Compromise

**Indicators**:
- Unusual API activity
- User reports unauthorized meetings
- Failed refresh token attempts

**Response**:
1. Identify affected users
2. Revoke affected tokens from database
3. Notify users to re-authenticate
4. Investigate root cause
5. Review for additional compromised accounts

### 7.2 Service Outage

**Indicators**:
- Health check failures
- User reports of errors
- Monitoring alerts

**Response**:
1. Check container status: `docker ps`
2. Check logs: `docker logs calendarbot --tail=100`
3. Check database: `docker exec calendarbot-db pg_isready`
4. Restart if needed: `docker compose up -d`
5. Verify recovery via health endpoint

### 7.3 Dependency Vulnerability

**Indicators**:
- pip-audit alerts
- Dependabot notifications
- CVE announcements

**Response**:
1. Assess severity and exploitability
2. Update dependency
3. Test functionality
4. Deploy update
5. Verify via security scan

---

## 8. Evidence Preservation

### 8.1 Evidence to Collect

- Application logs
- Access logs
- Database snapshots
- Network captures (if applicable)
- Screenshots of indicators

### 8.2 Chain of Custody

- Document who accessed evidence
- Store copies securely
- Do not modify original logs
- Note timestamps in UTC

---

## 9. Metrics and Reporting

### 9.1 Incident Metrics

| Metric | Target |
|--------|--------|
| Mean Time to Detect (MTTD) | < 1 hour |
| Mean Time to Respond (MTTR) | < 4 hours |
| Mean Time to Resolve | < 24 hours (P1/P2) |
| Post-incident review completion | 100% for P1/P2 |

### 9.2 Reporting Requirements

- P1/P2: Incident report within 5 days
- P3/P4: Document in issue tracker
- Annual: Summary of incidents and trends

---

## 10. Training and Testing

### 10.1 Training Requirements

- All team members familiar with this policy
- Annual review of incident procedures
- Role-specific training for response team

### 10.2 Testing

- Quarterly review of runbooks
- Annual tabletop exercise
- Post-major-change validation

---

## 11. Policy Review

This policy is reviewed:
- Annually (minimum)
- After significant incidents
- After major system changes
- When new threats emerge

---

*Last Updated: January 2026*
