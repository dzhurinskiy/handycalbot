"""Static pages - landing, privacy policy, terms of service."""

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse

router = APIRouter(tags=["pages"])

# Current year for copyright
CURRENT_YEAR = datetime.now().year

# Path to static files
STATIC_DIR = Path(__file__).parent.parent / "static"

# Calendly-inspired styles
COMMON_STYLES = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #ffffff;
        }

        /* Navigation */
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-weight: 700;
            font-size: 1.25rem;
            color: #1a1a1a;
            text-decoration: none;
        }

        .logo img {
            width: 40px;
            height: 40px;
            border-radius: 8px;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        .nav-links a {
            color: #4d4d4d;
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 500;
            transition: color 0.2s;
        }

        .nav-links a:hover {
            color: #006BFF;
        }

        .nav-links .btn-primary {
            color: white;
        }

        .nav-links .btn-primary:hover {
            color: white;
        }

        /* Hero Section */
        .hero {
            text-align: center;
            padding: 5rem 2rem;
            max-width: 900px;
            margin: 0 auto;
        }

        .hero h1 {
            font-size: 3.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 1.5rem;
            line-height: 1.1;
        }

        .hero h1 span {
            color: #006BFF;
        }

        .hero p {
            font-size: 1.25rem;
            color: #4d4d4d;
            margin-bottom: 2.5rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }

        .hero-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        /* Buttons */
        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.875rem 1.75rem;
            border-radius: 40px;
            font-weight: 600;
            font-size: 1rem;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
        }

        .btn-primary {
            background: #006BFF;
            color: white;
        }

        .btn-primary:hover {
            background: #0052cc;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 107, 255, 0.3);
        }

        .btn-secondary {
            background: white;
            color: #1a1a1a;
            border: 1px solid #e0e0e0;
        }

        .btn-secondary:hover {
            background: #f5f5f5;
            border-color: #d0d0d0;
        }

        /* Features Section */
        .features {
            padding: 5rem 2rem;
            background: #f8fafc;
        }

        .features-container {
            max-width: 1100px;
            margin: 0 auto;
        }

        .features h2 {
            text-align: center;
            font-size: 2.25rem;
            font-weight: 700;
            margin-bottom: 3rem;
            color: #1a1a1a;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }

        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
        }

        .feature-icon {
            width: 48px;
            height: 48px;
            background: #e8f2ff;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        .feature-card h3 {
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }

        .feature-card p {
            color: #666;
            font-size: 0.95rem;
        }

        /* How It Works */
        .how-it-works {
            padding: 5rem 2rem;
            max-width: 900px;
            margin: 0 auto;
        }

        .how-it-works h2 {
            text-align: center;
            font-size: 2.25rem;
            font-weight: 700;
            margin-bottom: 3rem;
            color: #1a1a1a;
        }

        .steps {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        .step {
            display: flex;
            gap: 1.5rem;
            align-items: flex-start;
        }

        .step-number {
            width: 40px;
            height: 40px;
            background: #006BFF;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            flex-shrink: 0;
        }

        .step-content h3 {
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: #1a1a1a;
        }

        .step-content p {
            color: #666;
        }

        .step-content code {
            background: #f1f5f9;
            padding: 0.125rem 0.5rem;
            border-radius: 4px;
            font-size: 0.9rem;
            color: #006BFF;
        }

        /* CTA Section */
        .cta {
            background: linear-gradient(135deg, #006BFF 0%, #0052cc 100%);
            padding: 4rem 2rem;
            text-align: center;
            color: white;
        }

        .cta h2 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .cta p {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }

        .cta .btn-primary {
            background: white;
            color: #006BFF;
        }

        .cta .btn-primary:hover {
            background: #f0f0f0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        /* Footer */
        footer {
            padding: 3rem 2rem;
            background: #1a1a1a;
            color: #999;
        }

        .footer-content {
            max-width: 1100px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .footer-links {
            display: flex;
            gap: 2rem;
        }

        .footer-links a {
            color: #999;
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.2s;
        }

        .footer-links a:hover {
            color: white;
        }

        /* Legal Pages */
        .legal-header {
            background: #f8fafc;
            padding: 4rem 2rem;
            text-align: center;
            border-bottom: 1px solid #e0e0e0;
        }

        .legal-header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 0.5rem;
        }

        .legal-header p {
            color: #666;
        }

        .legal-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }

        .legal-content h2 {
            font-size: 1.375rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-top: 2.5rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #006BFF;
        }

        .legal-content h2:first-of-type {
            margin-top: 0;
        }

        .legal-content p {
            color: #4d4d4d;
            margin-bottom: 1rem;
        }

        .legal-content ul, .legal-content ol {
            color: #4d4d4d;
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }

        .legal-content li {
            margin-bottom: 0.5rem;
        }

        .legal-content a {
            color: #006BFF;
            text-decoration: none;
        }

        .legal-content a:hover {
            text-decoration: underline;
        }

        .legal-content code {
            background: #f1f5f9;
            padding: 0.125rem 0.5rem;
            border-radius: 4px;
            font-size: 0.9rem;
        }

        .last-updated {
            color: #999;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }

            .hero p {
                font-size: 1.1rem;
            }

            nav {
                flex-direction: column;
                gap: 1rem;
            }

            .nav-links {
                gap: 1rem;
            }

            .footer-content {
                flex-direction: column;
                text-align: center;
            }
        }
    </style>
"""

FAVICON_LINK = '<link rel="icon" type="image/x-icon" href="/favicon.ico">'


@router.get("/", response_class=HTMLResponse)
async def landing_page():
    """Landing page with project description."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HandyCalBot - Schedule Meetings from Telegram</title>
    <meta name="description" content="Schedule Google Calendar meetings directly from Telegram. Fast, simple, and free.">
    {FAVICON_LINK}
    {COMMON_STYLES}
</head>
<body>
    <nav>
        <a href="/" class="logo">
            <img src="/logo.jpg" alt="HandyCalBot">
            HandyCalBot
        </a>
        <div class="nav-links">
            <a href="#features">Features</a>
            <a href="/docs">Docs</a>
            <a href="/support">Support</a>
            <a href="https://t.me/handycalbot" class="btn btn-primary">Open Bot</a>
        </div>
    </nav>

    <section class="hero">
        <h1>Schedule meetings <span>directly from Telegram</span></h1>
        <p>Create Google Calendar events in seconds using inline mode. No more switching between apps.</p>
        <div class="hero-buttons">
            <a href="https://t.me/handycalbot" class="btn btn-primary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.359 8.627-.168.9-.5 1.201-.82 1.23-.697.064-1.226-.461-1.901-.904-1.056-.692-1.653-1.123-2.678-1.799-1.185-.781-.417-1.21.258-1.911.177-.184 3.247-2.977 3.307-3.23.007-.032.015-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.139-5.062 3.345-.479.329-.913.489-1.302.481-.428-.009-1.252-.242-1.865-.442-.751-.244-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.831-2.529 6.998-3.015 3.333-1.386 4.025-1.627 4.477-1.635.099-.002.321.023.465.141.121.1.154.234.169.331.015.096.034.315.019.486z"/></svg>
                Start Scheduling
            </a>
            <a href="https://github.com/dzhurinskiy/handycalbot" class="btn btn-secondary">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                View Source
            </a>
        </div>
    </section>

    <section class="features" id="features">
        <div class="features-container">
            <h2>Everything you need to schedule smarter</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">💬</div>
                    <h3>Inline Mode</h3>
                    <p>Create meetings from any Telegram chat. Just type @handycalbot and your meeting details.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📅</div>
                    <h3>Google Calendar Sync</h3>
                    <p>Events are created directly in your Google Calendar with all details synced automatically.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">👥</div>
                    <h3>Invite Attendees</h3>
                    <p>Add participants by email. They'll receive calendar invitations automatically.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔔</div>
                    <h3>Smart Reminders</h3>
                    <p>Get notified before meetings. Set custom reminders for each event or use defaults.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🌍</div>
                    <h3>Timezone Aware</h3>
                    <p>Automatic timezone detection based on your Telegram settings. Never miss a meeting.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔒</div>
                    <h3>Secure & Private</h3>
                    <p>Your data is encrypted. We only access what's needed for calendar management.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="how-it-works" id="how-it-works">
        <h2>Get started in 3 steps</h2>
        <div class="steps">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h3>Connect your calendar</h3>
                    <p>Start a chat with <a href="https://t.me/handycalbot">@handycalbot</a> and use <code>/connect</code> to link your Google Calendar.</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h3>Create a meeting</h3>
                    <p>In any chat, type <code>@handycalbot 14:30 "Team Standup"</code> and select your meeting from the dropdown.</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h3>Done!</h3>
                    <p>Your meeting is created in Google Calendar. Attendees are notified, and you'll get reminders.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="cta">
        <h2>Ready to simplify your scheduling?</h2>
        <p>Join thousands of users who schedule meetings smarter with HandyCalBot.</p>
        <a href="https://t.me/handycalbot" class="btn btn-primary">Get Started — It's Free</a>
    </section>

    <footer>
        <div class="footer-content">
            <span>© {CURRENT_YEAR} HandyCalBot. Open source project.</span>
            <div class="footer-links">
                <a href="/docs">Docs</a>
                <a href="/support">Support</a>
                <a href="/privacy">Privacy</a>
                <a href="/terms">Terms</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""


@router.get("/privacy", response_class=HTMLResponse)
async def privacy_policy():
    """Privacy Policy page."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy - HandyCalBot</title>
    {FAVICON_LINK}
    {COMMON_STYLES}
</head>
<body>
    <nav>
        <a href="/" class="logo">
            <img src="/logo.jpg" alt="HandyCalBot">
            HandyCalBot
        </a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/terms">Terms</a>
            <a href="https://t.me/handycalbot" class="btn btn-primary">Open Bot</a>
        </div>
    </nav>

    <header class="legal-header">
        <h1>Privacy Policy</h1>
        <p>How we handle your data</p>
    </header>

    <main class="legal-content">
        <p class="last-updated">Last updated: January 16, 2026</p>

        <h2>1. Introduction</h2>
        <p>
            HandyCalBot ("we", "our", or "the bot") is a Telegram bot that helps users schedule
            Google Calendar meetings. This Privacy Policy explains how we collect, use, and protect
            your information when you use our service.
        </p>

        <h2>2. Information We Collect</h2>
        <p>When you use HandyCalBot, we collect and store the following information:</p>
        <ul>
            <li><strong>Telegram User ID:</strong> Your unique Telegram identifier to associate your account with our service</li>
            <li><strong>Telegram Username:</strong> Your Telegram username (if available) for identification purposes</li>
            <li><strong>Google Calendar OAuth Tokens:</strong> Encrypted access and refresh tokens to interact with your Google Calendar on your behalf</li>
            <li><strong>Timezone Preference:</strong> Your selected timezone for scheduling meetings</li>
            <li><strong>Meeting Data:</strong> Basic meeting information (title, time, attendees) for meetings created through the bot</li>
        </ul>

        <h2>3. How We Use Your Information</h2>
        <p>We use the collected information to:</p>
        <ul>
            <li>Create, modify, and manage calendar events on your behalf</li>
            <li>Display your upcoming meetings</li>
            <li>Send meeting invitations to attendees you specify</li>
            <li>Send you reminder notifications before meetings</li>
            <li>Provide timezone-aware scheduling</li>
        </ul>

        <h2>4. Data Storage and Security</h2>
        <p>
            Your data is stored on secure servers. Google OAuth tokens are encrypted using
            industry-standard encryption (Fernet/AES) before storage. We do not store your
            Google password or have access to any Google account data beyond calendar events.
        </p>

        <h2>5. Third-Party Services</h2>
        <p>HandyCalBot integrates with:</p>
        <ul>
            <li><strong>Telegram:</strong> For bot functionality and messaging (<a href="https://telegram.org/privacy">Telegram Privacy Policy</a>)</li>
            <li><strong>Google Calendar API:</strong> For calendar management (<a href="https://policies.google.com/privacy">Google Privacy Policy</a>)</li>
        </ul>

        <h2>6. Data Sharing</h2>
        <p>
            We do not sell, trade, or otherwise transfer your personal information to third parties.
            Your calendar data is only shared with Google's servers as necessary to manage your calendar events.
        </p>

        <h2>7. Data Retention</h2>
        <p>
            We retain your data for as long as you use our service. You can request deletion of your
            data at any time by using the <code>/disconnect</code> command and contacting us.
        </p>

        <h2>8. Your Rights</h2>
        <p>You have the right to:</p>
        <ul>
            <li>Access your stored data</li>
            <li>Disconnect your Google Calendar at any time using <code>/disconnect</code></li>
            <li>Request deletion of your data</li>
            <li>Revoke our access through your <a href="https://myaccount.google.com/permissions">Google Account settings</a></li>
        </ul>

        <h2>9. Children's Privacy</h2>
        <p>
            Our service is not intended for children under 13 years of age. We do not knowingly
            collect personal information from children under 13.
        </p>

        <h2>10. Changes to This Policy</h2>
        <p>
            We may update this Privacy Policy from time to time. We will notify users of any
            significant changes through the bot or by updating this page.
        </p>

        <h2>11. Contact Us</h2>
        <p>
            If you have questions about this Privacy Policy, please open an issue on our
            <a href="https://github.com/dzhurinskiy/handycalbot/issues">GitHub repository</a>.
        </p>
    </main>

    <footer>
        <div class="footer-content">
            <span>© {CURRENT_YEAR} HandyCalBot. Open source project.</span>
            <div class="footer-links">
                <a href="/">Home</a>
                <a href="/terms">Terms</a>
                <a href="https://github.com/dzhurinskiy/handycalbot">GitHub</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""


@router.get("/terms", response_class=HTMLResponse)
async def terms_of_service():
    """Terms of Service page."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service - HandyCalBot</title>
    {FAVICON_LINK}
    {COMMON_STYLES}
</head>
<body>
    <nav>
        <a href="/" class="logo">
            <img src="/logo.jpg" alt="HandyCalBot">
            HandyCalBot
        </a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/privacy">Privacy</a>
            <a href="https://t.me/handycalbot" class="btn btn-primary">Open Bot</a>
        </div>
    </nav>

    <header class="legal-header">
        <h1>Terms of Service</h1>
        <p>Rules and guidelines for using HandyCalBot</p>
    </header>

    <main class="legal-content">
        <p class="last-updated">Last updated: January 16, 2026</p>

        <h2>1. Acceptance of Terms</h2>
        <p>
            By using HandyCalBot ("the Service"), you agree to be bound by these Terms of Service.
            If you do not agree to these terms, please do not use the Service.
        </p>

        <h2>2. Description of Service</h2>
        <p>
            HandyCalBot is a Telegram bot that allows users to create and manage Google Calendar
            events through Telegram's messaging interface. The Service is provided free of charge.
        </p>

        <h2>3. User Accounts and Authorization</h2>
        <ul>
            <li>You must have a valid Telegram account to use the Service</li>
            <li>You must authorize access to your Google Calendar to use calendar features</li>
            <li>You are responsible for maintaining the security of your accounts</li>
            <li>You may revoke access at any time through Google Account settings or the <code>/disconnect</code> command</li>
        </ul>

        <h2>4. Acceptable Use</h2>
        <p>You agree not to:</p>
        <ul>
            <li>Use the Service for any unlawful purpose</li>
            <li>Attempt to gain unauthorized access to our systems</li>
            <li>Use the Service to send spam or unwanted meeting invitations</li>
            <li>Abuse or overload our servers with excessive requests</li>
            <li>Reverse engineer or attempt to extract the source code (note: the project is open source)</li>
        </ul>

        <h2>5. Google Calendar Integration</h2>
        <p>
            The Service requires access to your Google Calendar. By connecting your calendar, you:
        </p>
        <ul>
            <li>Authorize us to create, read, and delete events on your behalf</li>
            <li>Acknowledge that meeting invitations will be sent to email addresses you provide</li>
            <li>Understand that we access only calendar data, not other Google services</li>
        </ul>

        <h2>6. Disclaimer of Warranties</h2>
        <p>
            THE SERVICE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTIES OF ANY KIND,
            EITHER EXPRESS OR IMPLIED. WE DO NOT GUARANTEE THAT THE SERVICE WILL BE UNINTERRUPTED,
            SECURE, OR ERROR-FREE.
        </p>

        <h2>7. Limitation of Liability</h2>
        <p>
            TO THE MAXIMUM EXTENT PERMITTED BY LAW, WE SHALL NOT BE LIABLE FOR ANY INDIRECT,
            INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, INCLUDING BUT NOT LIMITED TO:
        </p>
        <ul>
            <li>Lost profits or revenue</li>
            <li>Missed meetings or scheduling errors</li>
            <li>Data loss or corruption</li>
            <li>Service interruptions</li>
        </ul>

        <h2>8. Indemnification</h2>
        <p>
            You agree to indemnify and hold harmless HandyCalBot and its developers from any claims,
            damages, or expenses arising from your use of the Service or violation of these Terms.
        </p>

        <h2>9. Open Source</h2>
        <p>
            HandyCalBot is open-source software available under the MIT License. The source code
            is available at <a href="https://github.com/dzhurinskiy/handycalbot">GitHub</a>.
            You are free to use, modify, and distribute the code in accordance with the license.
        </p>

        <h2>10. Modifications to Service</h2>
        <p>
            We reserve the right to modify, suspend, or discontinue the Service at any time
            without notice. We may also update these Terms from time to time.
        </p>

        <h2>11. Termination</h2>
        <p>
            We may terminate or suspend your access to the Service at any time for any reason,
            including violation of these Terms. You may stop using the Service at any time by
            disconnecting your calendar and stopping interaction with the bot.
        </p>

        <h2>12. Governing Law</h2>
        <p>
            These Terms shall be governed by and construed in accordance with applicable laws,
            without regard to conflict of law principles.
        </p>

        <h2>13. Contact</h2>
        <p>
            For questions about these Terms, please open an issue on our
            <a href="https://github.com/dzhurinskiy/handycalbot/issues">GitHub repository</a>.
        </p>
    </main>

    <footer>
        <div class="footer-content">
            <span>© {CURRENT_YEAR} HandyCalBot. Open source project.</span>
            <div class="footer-links">
                <a href="/">Home</a>
                <a href="/privacy">Privacy</a>
                <a href="https://github.com/dzhurinskiy/handycalbot">GitHub</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""


@router.get("/docs", response_class=HTMLResponse)
async def documentation():
    """Documentation page with adding, usage, and removal guides."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation - HandyCalBot</title>
    {FAVICON_LINK}
    {COMMON_STYLES}
    <style>
        .doc-nav {{
            background: #f8fafc;
            padding: 1rem 2rem;
            border-bottom: 1px solid #e0e0e0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .doc-nav-inner {{
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
        }}
        .doc-nav a {{
            color: #4d4d4d;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            transition: all 0.2s;
        }}
        .doc-nav a:hover {{
            background: #e8f2ff;
            color: #006BFF;
        }}
        .doc-section {{
            scroll-margin-top: 80px;
        }}
        .command-box {{
            background: #1a1a1a;
            color: #f8f8f2;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            font-family: monospace;
            font-size: 0.95rem;
        }}
        .tip-box {{
            background: #e8f2ff;
            border-left: 4px solid #006BFF;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
        }}
        .tip-box strong {{
            color: #006BFF;
        }}
        .warning-box {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
        }}
        .warning-box strong {{
            color: #b45309;
        }}
        .feature-list {{
            display: grid;
            gap: 1rem;
            margin: 1.5rem 0;
        }}
        .feature-item {{
            display: flex;
            gap: 1rem;
            align-items: flex-start;
        }}
        .feature-icon {{
            width: 32px;
            height: 32px;
            background: #e8f2ff;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">
            <img src="/logo.jpg" alt="HandyCalBot">
            HandyCalBot
        </a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/support">Support</a>
            <a href="https://t.me/handycalbot" class="btn btn-primary">Open Bot</a>
        </div>
    </nav>

    <header class="legal-header">
        <h1>Documentation</h1>
        <p>Complete guide to using HandyCalBot</p>
    </header>

    <div class="doc-nav">
        <div class="doc-nav-inner">
            <a href="#adding">Adding the App</a>
            <a href="#usage">Usage Guide</a>
            <a href="#features">Features</a>
            <a href="#troubleshooting">Troubleshooting</a>
            <a href="#removing">Removing the App</a>
        </div>
    </div>

    <main class="legal-content">

        <section id="adding" class="doc-section">
            <h2>Adding the App</h2>
            <p>Follow these steps to get started with HandyCalBot:</p>

            <h3>Step 1: Start the Bot</h3>
            <p>Open Telegram and search for <strong>@handycalbot</strong>, or click this link:</p>
            <p><a href="https://t.me/handycalbot" class="btn btn-primary" style="display: inline-flex;">Open HandyCalBot</a></p>
            <p>Click <strong>Start</strong> to begin interacting with the bot.</p>

            <h3>Step 2: Connect Your Google Calendar</h3>
            <p>To create meetings, you need to connect your Google Calendar:</p>
            <div class="command-box">/connect</div>
            <p>The bot will send you an authorization link. Click it to:</p>
            <ol>
                <li>Sign in to your Google Account</li>
                <li>Review the permissions requested (calendar access)</li>
                <li>Click "Allow" to authorize HandyCalBot</li>
                <li>You'll be redirected back with a confirmation message</li>
            </ol>

            <div class="tip-box">
                <strong>Tip:</strong> You can choose "Privacy Mode" during setup to limit calendar access.
                In Privacy Mode, the bot can only create events, not read your existing calendar.
            </div>

            <h3>Step 3: Set Your Timezone</h3>
            <p>After connecting, confirm or update your timezone:</p>
            <div class="command-box">/timezone</div>
            <p>Select your timezone from the list or search for your city.</p>

            <h3>Step 4 (Optional): Connect Zoom</h3>
            <p>To add Zoom meeting links automatically:</p>
            <div class="command-box">/connectzoom</div>
            <p>Follow the same authorization process for your Zoom account.</p>
        </section>

        <section id="usage" class="doc-section">
            <h2>Usage Guide</h2>

            <h3>Creating Meetings (Inline Mode)</h3>
            <p>The primary way to create meetings is using Telegram's inline mode. In <strong>any chat</strong>, type:</p>
            <div class="command-box">@handycalbot 15:00 Team Standup</div>
            <p>A dropdown will appear with your meeting. Select it to create the event.</p>

            <p><strong>Format examples:</strong></p>
            <ul>
                <li><code>@handycalbot 14:30 Project Review</code> - Meeting at 2:30 PM today</li>
                <li><code>@handycalbot tomorrow 10:00 Weekly Sync</code> - Meeting tomorrow at 10 AM</li>
                <li><code>@handycalbot 25.01 09:00 Monthly Planning</code> - Meeting on January 25th</li>
                <li><code>@handycalbot 2h Design Workshop</code> - 2-hour meeting starting now</li>
            </ul>

            <h3>Bot Commands</h3>
            <p>Available commands you can use in the bot chat:</p>
            <ul>
                <li><code>/start</code> - Welcome message and getting started</li>
                <li><code>/help</code> - Show all available commands</li>
                <li><code>/connect</code> - Connect your Google Calendar</li>
                <li><code>/connectzoom</code> - Connect your Zoom account</li>
                <li><code>/disconnect</code> - Disconnect Google Calendar</li>
                <li><code>/disconnectzoom</code> - Disconnect Zoom account</li>
                <li><code>/settings</code> - View and change your settings</li>
                <li><code>/timezone</code> - Change your timezone</li>
                <li><code>/meetings</code> - View your upcoming meetings</li>
                <li><code>/cancel</code> - Cancel a meeting</li>
            </ul>

            <h3>Adding Attendees</h3>
            <p>After creating a meeting, you can add attendees by:</p>
            <ul>
                <li><strong>Email:</strong> Enter email addresses (e.g., john@example.com)</li>
                <li><strong>Telegram Username:</strong> Enter @username if they also use HandyCalBot</li>
            </ul>
            <p>Attendees receive calendar invitations automatically via email.</p>

            <h3>Meeting Reminders</h3>
            <p>HandyCalBot sends you Telegram notifications before your meetings. Configure reminders in:</p>
            <div class="command-box">/settings</div>
            <p>You can set custom reminder times (e.g., 15 minutes, 1 hour before).</p>
        </section>

        <section id="features" class="doc-section">
            <h2>Features</h2>

            <div class="feature-list">
                <div class="feature-item">
                    <div class="feature-icon">📅</div>
                    <div>
                        <strong>Google Calendar Sync</strong>
                        <p>Events are created directly in your Google Calendar with all details.</p>
                    </div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🎥</div>
                    <div>
                        <strong>Zoom Integration</strong>
                        <p>Automatically generate Zoom meeting links for your events.</p>
                    </div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">👥</div>
                    <div>
                        <strong>Attendee Invitations</strong>
                        <p>Invite people by email or Telegram username.</p>
                    </div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🔔</div>
                    <div>
                        <strong>Smart Reminders</strong>
                        <p>Get notified via Telegram before your meetings start.</p>
                    </div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🌍</div>
                    <div>
                        <strong>Multi-language Support</strong>
                        <p>Available in 10 languages including English, German, Spanish, French, Russian, and more.</p>
                    </div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🔒</div>
                    <div>
                        <strong>Privacy Mode</strong>
                        <p>Opt for minimal permissions - create events without reading your calendar.</p>
                    </div>
                </div>
            </div>

            <h3>Prerequisites</h3>
            <ul>
                <li>A Telegram account</li>
                <li>A Google Account with Google Calendar</li>
                <li>(Optional) A Zoom account for video meeting links</li>
            </ul>
        </section>

        <section id="troubleshooting" class="doc-section">
            <h2>Troubleshooting</h2>

            <h3>Cannot connect Google Calendar</h3>
            <ul>
                <li>Make sure you're signed into the correct Google Account</li>
                <li>Check that you clicked "Allow" on the permissions screen</li>
                <li>Try disconnecting and reconnecting: <code>/disconnect</code> then <code>/connect</code></li>
                <li>Clear your browser cache and try again</li>
            </ul>

            <h3>Meetings not appearing in calendar</h3>
            <ul>
                <li>Verify your calendar is connected: <code>/settings</code></li>
                <li>Check your timezone is set correctly: <code>/timezone</code></li>
                <li>Make sure you selected the meeting from the inline dropdown</li>
            </ul>

            <h3>Not receiving reminders</h3>
            <ul>
                <li>Check that notifications are enabled in <code>/settings</code></li>
                <li>Make sure Telegram notifications are enabled on your device</li>
                <li>Verify the meeting was created through HandyCalBot</li>
            </ul>

            <h3>Zoom link not being added</h3>
            <ul>
                <li>Ensure Zoom is connected: <code>/connectzoom</code></li>
                <li>Check that your Zoom account is active</li>
                <li>Try disconnecting and reconnecting Zoom</li>
            </ul>

            <div class="tip-box">
                <strong>Still having issues?</strong> Visit our <a href="/support">Support page</a> for more help options.
            </div>
        </section>

        <section id="removing" class="doc-section">
            <h2>Removing the App</h2>

            <h3>Disconnect Your Accounts</h3>
            <p>To disconnect HandyCalBot from your accounts:</p>

            <p><strong>1. Disconnect Google Calendar:</strong></p>
            <div class="command-box">/disconnect</div>
            <p>This removes the connection between HandyCalBot and your Google Calendar.</p>

            <p><strong>2. Disconnect Zoom (if connected):</strong></p>
            <div class="command-box">/disconnectzoom</div>

            <h3>Revoke Access from Google</h3>
            <p>For complete removal, also revoke access from your Google Account:</p>
            <ol>
                <li>Go to <a href="https://myaccount.google.com/permissions" target="_blank">Google Account Permissions</a></li>
                <li>Find "HandyCalBot" in the list of connected apps</li>
                <li>Click on it and select "Remove Access"</li>
            </ol>

            <h3>Revoke Access from Zoom</h3>
            <p>To revoke Zoom access:</p>
            <ol>
                <li>Go to <a href="https://marketplace.zoom.us/user/installed" target="_blank">Zoom App Marketplace - Installed Apps</a></li>
                <li>Find "HandyCalBot" and click "Uninstall"</li>
            </ol>

            <h3>What Happens When You Disconnect</h3>
            <div class="warning-box">
                <strong>Important:</strong> When you disconnect:
                <ul style="margin-top: 0.5rem; margin-bottom: 0;">
                    <li>Your OAuth tokens are deleted from our servers</li>
                    <li>We can no longer access your calendar or create events</li>
                    <li>Existing calendar events are NOT deleted (they remain in your Google Calendar)</li>
                    <li>Your user preferences (timezone, settings) are retained in case you reconnect</li>
                </ul>
            </div>

            <h3>Complete Data Deletion</h3>
            <p>
                To request complete deletion of all your data (including preferences and meeting history),
                please contact us through our <a href="/support">Support page</a> or open an issue on
                <a href="https://github.com/dzhurinskiy/handycalbot/issues">GitHub</a>.
            </p>

            <h3>Stop Using the Bot</h3>
            <p>You can also simply stop the bot in Telegram:</p>
            <ol>
                <li>Open the chat with @handycalbot</li>
                <li>Tap the bot name at the top</li>
                <li>Select "Stop Bot" or "Block User"</li>
            </ol>
            <p>This prevents the bot from sending you messages, but doesn't disconnect your calendar.</p>
        </section>

    </main>

    <footer>
        <div class="footer-content">
            <span>&copy; {CURRENT_YEAR} HandyCalBot. Open source project.</span>
            <div class="footer-links">
                <a href="/">Home</a>
                <a href="/privacy">Privacy</a>
                <a href="/terms">Terms</a>
                <a href="/support">Support</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""


@router.get("/support", response_class=HTMLResponse)
async def support_page():
    """Support page with contact information and help resources."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Support - HandyCalBot</title>
    {FAVICON_LINK}
    {COMMON_STYLES}
    <style>
        .support-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        .support-card {{
            background: #f8fafc;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s;
        }}
        .support-card:hover {{
            border-color: #006BFF;
            box-shadow: 0 4px 12px rgba(0, 107, 255, 0.1);
        }}
        .support-card h3 {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.75rem;
            color: #1a1a1a;
        }}
        .support-card p {{
            color: #666;
            margin-bottom: 1rem;
        }}
        .support-card a.btn {{
            width: 100%;
            justify-content: center;
        }}
        .faq-item {{
            border-bottom: 1px solid #e0e0e0;
            padding: 1.5rem 0;
        }}
        .faq-item:last-child {{
            border-bottom: none;
        }}
        .faq-item h3 {{
            color: #1a1a1a;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }}
        .faq-item p {{
            color: #4d4d4d;
            margin: 0;
        }}
        .contact-info {{
            background: linear-gradient(135deg, #006BFF 0%, #0052cc 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin: 2rem 0;
        }}
        .contact-info h3 {{
            margin-bottom: 1rem;
        }}
        .contact-info p {{
            opacity: 0.9;
            margin-bottom: 0.5rem;
        }}
        .contact-info a {{
            color: white;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo">
            <img src="/logo.jpg" alt="HandyCalBot">
            HandyCalBot
        </a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/docs">Documentation</a>
            <a href="https://t.me/handycalbot" class="btn btn-primary">Open Bot</a>
        </div>
    </nav>

    <header class="legal-header">
        <h1>Support</h1>
        <p>Get help with HandyCalBot</p>
    </header>

    <main class="legal-content">

        <h2>How Can We Help?</h2>
        <div class="support-grid">
            <div class="support-card">
                <h3>📖 Documentation</h3>
                <p>Complete guides for adding, using, and removing the app.</p>
                <a href="/docs" class="btn btn-secondary">View Documentation</a>
            </div>
            <div class="support-card">
                <h3>🐛 Report a Bug</h3>
                <p>Found an issue? Let us know on GitHub.</p>
                <a href="https://github.com/dzhurinskiy/handycalbot/issues/new?labels=bug" class="btn btn-secondary" target="_blank">Report Bug</a>
            </div>
            <div class="support-card">
                <h3>💡 Request a Feature</h3>
                <p>Have an idea to improve HandyCalBot?</p>
                <a href="https://github.com/dzhurinskiy/handycalbot/issues/new?labels=enhancement" class="btn btn-secondary" target="_blank">Request Feature</a>
            </div>
            <div class="support-card">
                <h3>💬 Community</h3>
                <p>View source code and contribute to the project.</p>
                <a href="https://github.com/dzhurinskiy/handycalbot" class="btn btn-secondary" target="_blank">GitHub Repository</a>
            </div>
        </div>

        <h2>Frequently Asked Questions</h2>
        <div class="faq-item">
            <h3>Is HandyCalBot free?</h3>
            <p>Yes! HandyCalBot is completely free to use. It's an open-source project.</p>
        </div>
        <div class="faq-item">
            <h3>Is my data secure?</h3>
            <p>Yes. We use industry-standard encryption (AES-256) to protect your OAuth tokens. We never store your Google or Zoom passwords. See our <a href="/privacy">Privacy Policy</a> for details.</p>
        </div>
        <div class="faq-item">
            <h3>Can I use HandyCalBot for work?</h3>
            <p>Absolutely! HandyCalBot works with any Google Calendar, including Google Workspace (G Suite) accounts.</p>
        </div>
        <div class="faq-item">
            <h3>How do I change my timezone?</h3>
            <p>Use the <code>/timezone</code> command in the bot chat to select your timezone.</p>
        </div>
        <div class="faq-item">
            <h3>Can I invite people who don't use Telegram?</h3>
            <p>Yes! You can invite anyone by their email address. They'll receive a standard Google Calendar invitation.</p>
        </div>
        <div class="faq-item">
            <h3>How do I disconnect my account?</h3>
            <p>Use the <code>/disconnect</code> command to disconnect Google Calendar, or <code>/disconnectzoom</code> for Zoom. See our <a href="/docs#removing">removal guide</a> for complete instructions.</p>
        </div>

        <div class="contact-info">
            <h3>Contact Us</h3>
            <p><strong>Email:</strong> <a href="mailto:support@handycal.dzhurinskiy.com">support@handycal.dzhurinskiy.com</a></p>
            <p><strong>GitHub Issues:</strong> <a href="https://github.com/dzhurinskiy/handycalbot/issues">github.com/dzhurinskiy/handycalbot/issues</a></p>
            <p><strong>Response Time:</strong> We typically respond within 24-48 hours.</p>
        </div>

        <h2>Troubleshooting Quick Links</h2>
        <ul>
            <li><a href="/docs#troubleshooting">Common issues and solutions</a></li>
            <li><a href="/docs#adding">How to connect your calendar</a></li>
            <li><a href="/docs#removing">How to disconnect and remove your data</a></li>
            <li><a href="https://myaccount.google.com/permissions" target="_blank">Manage Google permissions</a></li>
            <li><a href="https://marketplace.zoom.us/user/installed" target="_blank">Manage Zoom apps</a></li>
        </ul>

    </main>

    <footer>
        <div class="footer-content">
            <span>&copy; {CURRENT_YEAR} HandyCalBot. Open source project.</span>
            <div class="footer-links">
                <a href="/">Home</a>
                <a href="/docs">Docs</a>
                <a href="/privacy">Privacy</a>
                <a href="/terms">Terms</a>
            </div>
        </div>
    </footer>
</body>
</html>
"""


@router.get("/logo.jpg", response_class=FileResponse)
async def logo():
    """Serve the logo image."""
    logo_path = STATIC_DIR / "logo.jpg"
    return FileResponse(logo_path, media_type="image/jpeg")


@router.get("/favicon.ico", response_class=FileResponse)
async def favicon():
    """Serve favicon (uses the logo)."""
    favicon_path = STATIC_DIR / "logo.jpg"
    return FileResponse(favicon_path, media_type="image/jpeg")


@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    """Serve robots.txt."""
    robots_path = STATIC_DIR / "robots.txt"
    return PlainTextResponse(robots_path.read_text())


@router.get("/sitemap.xml", response_class=PlainTextResponse)
async def sitemap():
    """Generate sitemap.xml."""
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://handycal.dzhurinskiy.com/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://handycal.dzhurinskiy.com/docs</loc>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://handycal.dzhurinskiy.com/support</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://handycal.dzhurinskiy.com/privacy</loc>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://handycal.dzhurinskiy.com/terms</loc>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
</urlset>"""
    return PlainTextResponse(sitemap_content, media_type="application/xml")


@router.get("/.well-known/microsoft-identity-association.json", response_class=JSONResponse)
async def microsoft_identity_association():
    """Serve Microsoft identity association file for Azure AD domain verification."""
    return JSONResponse(
        content={
            "associatedApplications": [
                {"applicationId": "4a38f049-d7b7-4048-8316-a8a940c3118a"}
            ]
        }
    )
