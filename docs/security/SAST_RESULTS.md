# Static Application Security Testing (SAST) Results

## HandyCalBot - SAST Scan Report

**Scan Date**: January 20, 2026
**Tool**: Bandit v1.9.3 (Python Security Linter)
**Target**: `src/calendarbot/` (All Python source code)
**Python Version**: 3.13.5

---

## Executive Summary

| Severity | Count | Status |
|----------|-------|--------|
| High | 0 | ✅ Pass |
| Medium | 2 | ⚠️ False Positives (Reviewed) |
| Low | 3 | ⚠️ False Positives (Reviewed) |
| **Total Issues** | **5** | **All Reviewed & Accepted** |

**Overall Assessment**: PASS - No actionable security vulnerabilities found.

---

## Scan Metrics

```
Total lines of code: 12,379
Total lines skipped (#nosec): 0
Files scanned: All Python files in src/
Scan duration: < 5 seconds
```

---

## Findings Detail

### Finding 1: B608 - Possible SQL Injection (FALSE POSITIVE)

**Severity**: Medium | **Confidence**: Low
**CWE**: CWE-89 (SQL Injection)
**Location**: `src/calendarbot/api/pages.py:453`

**Code Context**:
```python
def landing_page():
    return f"""
<!DOCTYPE html>
<html lang="en">
...
"""
```

**Assessment**: ✅ **FALSE POSITIVE**

This is a static HTML template string, not a SQL query. The f-string contains only:
- Static HTML content
- Pre-defined CSS constants (`COMMON_STYLES`, `FAVICON_LINK`)
- Current year constant (`CURRENT_YEAR`)

No user input is interpolated. No database interaction occurs.

**Remediation**: None required.

---

### Finding 2: B106 - Hardcoded Password in Function Argument (FALSE POSITIVE)

**Severity**: Low | **Confidence**: Medium
**CWE**: CWE-259 (Hardcoded Password)
**Location**: `src/calendarbot/bot/handlers/donation.py:177`

**Code Context**:
```python
await context.bot.send_invoice(
    ...
    provider_token="",  # Empty for Telegram Stars
    ...
)
```

**Assessment**: ✅ **FALSE POSITIVE**

This is the **required format** for Telegram Stars payments. Per Telegram Bot API documentation, the `provider_token` must be an empty string when using Telegram Stars as the payment currency. This is not a hardcoded password.

**Remediation**: None required.

---

### Finding 3: B104 - Binding to All Interfaces (ACCEPTED RISK)

**Severity**: Medium | **Confidence**: Medium
**CWE**: CWE-605 (Multiple Binds to Same Port)
**Location**: `src/calendarbot/config.py:40`

**Code Context**:
```python
app_host: str = "0.0.0.0"
app_port: int = 8000
```

**Assessment**: ✅ **ACCEPTED RISK**

This is **intentional and required** for Docker containerization. The application runs inside a Docker container and must bind to `0.0.0.0` to be accessible from the host. The actual security boundary is provided by:

1. Docker network isolation
2. Nginx reverse proxy (only exposes ports 80/443)
3. Firewall rules (only ports 80, 443, 22 open)

**Mitigations in Place**:
- Container is not exposed directly to internet
- Nginx handles all external traffic
- Production environment variables override defaults

**Remediation**: None required.

---

### Finding 4: B105 - Hardcoded Password String (FALSE POSITIVE)

**Severity**: Low | **Confidence**: Medium
**CWE**: CWE-259 (Hardcoded Password)
**Location**: `src/calendarbot/integrations/google.py:13`

**Code Context**:
```python
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
```

**Assessment**: ✅ **FALSE POSITIVE**

This is a **public OAuth endpoint URL**, not a password. Google's OAuth token endpoint is publicly documented:
- https://developers.google.com/identity/protocols/oauth2/web-server

Bandit incorrectly flags strings containing "token" as potential passwords.

**Remediation**: None required.

---

### Finding 5: B105 - Hardcoded Password String (FALSE POSITIVE)

**Severity**: Low | **Confidence**: Medium
**CWE**: CWE-259 (Hardcoded Password)
**Location**: `src/calendarbot/integrations/zoom.py:14`

**Code Context**:
```python
ZOOM_TOKEN_URL = "https://zoom.us/oauth/token"
```

**Assessment**: ✅ **FALSE POSITIVE**

This is a **public OAuth endpoint URL**, not a password. Zoom's OAuth token endpoint is publicly documented:
- https://developers.zoom.us/docs/integrations/oauth/

**Remediation**: None required.

---

## Dependency Vulnerability Scan

**Tool**: pip-audit
**Scan Date**: January 20, 2026 (Updated)

### Findings

**No known vulnerabilities found** ✅

All dependencies have been updated to secure versions:

| Package | Previous Version | Updated Version | CVEs Fixed |
|---------|------------------|-----------------|------------|
| starlette | 0.38.6 | 0.50.0 | CVE-2024-47874, CVE-2025-54121 |
| urllib3 | 2.5.0 | 2.6.3 | CVE-2025-66418, CVE-2025-66471, CVE-2026-21441 |
| fonttools | 4.60.1 | 4.61.1 | CVE-2025-66034 |
| ecdsa | 0.19.1 | (removed) | CVE-2024-23342 (orphaned dependency) |

**Remediation Status**: ✅ COMPLETE
- All known vulnerabilities have been remediated
- Dependency constraints added to `pyproject.toml` to prevent regression

---

## Security Controls Verified

The SAST scan verifies the following security practices:

✅ No hardcoded credentials in source code
✅ No obvious SQL injection vulnerabilities
✅ No command injection patterns detected
✅ No insecure random number generation
✅ No insecure hash algorithms (MD5/SHA1 for security)
✅ No insecure SSL/TLS configurations
✅ No debug code in production paths
✅ No assert statements with side effects

---

## Conclusion

The SAST scan found **no actionable security vulnerabilities**. All flagged items are either false positives or accepted risks with appropriate mitigations in place. The codebase demonstrates secure coding practices and appropriate security controls.

---

## Appendix: Raw Scan Output

```
[main]  INFO    profile include tests: None
[main]  INFO    profile exclude tests: None
[main]  INFO    running on Python 3.13.5

Run started:2026-01-20 19:14:00.711954+00:00

Code scanned:
    Total lines of code: 12379
    Total lines skipped (#nosec): 0

Run metrics:
    Total issues (by severity):
        Undefined: 0
        Low: 3
        Medium: 2
        High: 0
    Total issues (by confidence):
        Undefined: 0
        Low: 1
        Medium: 4
        High: 0
```

---

*Report generated by Bandit v1.9.3 with manual review and assessment.*
