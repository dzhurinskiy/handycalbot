"""Static pages - landing, privacy policy, terms of service."""

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse

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
            <a href="#how-it-works">How it works</a>
            <a href="https://github.com/dzhurinskiy/handycalbot">GitHub</a>
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
                <a href="/privacy">Privacy</a>
                <a href="/terms">Terms</a>
                <a href="https://github.com/dzhurinskiy/handycalbot">GitHub</a>
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
