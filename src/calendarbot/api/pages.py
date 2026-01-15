"""Static pages - landing, privacy policy, terms of service."""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["pages"])

# Common styles for all pages
COMMON_STYLES = """
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 2rem;
            text-align: center;
        }
        header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        main {
            background: white;
            padding: 3rem 2rem;
            margin: 2rem auto;
            max-width: 800px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #1a202c;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        h2 {
            font-size: 1.5rem;
            border-bottom: 2px solid #667eea;
            padding-bottom: 0.5rem;
        }
        p {
            margin-bottom: 1rem;
        }
        ul, ol {
            margin-left: 2rem;
            margin-bottom: 1rem;
        }
        li {
            margin-bottom: 0.5rem;
        }
        a {
            color: #667eea;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            margin: 0.5rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            text-decoration: none;
        }
        .button-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        .button-secondary:hover {
            background: #f0f0ff;
        }
        footer {
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.9rem;
        }
        footer a {
            color: #666;
            margin: 0 0.5rem;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .feature {
            text-align: center;
            padding: 1.5rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .last-updated {
            color: #666;
            font-style: italic;
            margin-bottom: 2rem;
        }
    </style>
"""


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
    <meta name="description" content="A Telegram bot that helps you schedule Google Calendar meetings directly from any chat.">
    {COMMON_STYLES}
</head>
<body>
    <header>
        <h1>HandyCalBot</h1>
        <p>Schedule Google Calendar meetings directly from Telegram</p>
    </header>

    <main>
        <div style="text-align: center; margin-bottom: 2rem;">
            <a href="https://t.me/handycalbot" class="button">Open in Telegram</a>
            <a href="https://github.com/dzhurinskiy/handycalbot" class="button button-secondary">View on GitHub</a>
        </div>

        <h2>What is HandyCalBot?</h2>
        <p>
            HandyCalBot is an open-source Telegram bot that lets you create Google Calendar events
            without leaving your chat. Simply mention the bot with meeting details, and it handles the rest.
        </p>

        <div class="features">
            <div class="feature">
                <div class="feature-icon">💬</div>
                <h3>Inline Mode</h3>
                <p>Create meetings from any chat using @handycalbot</p>
            </div>
            <div class="feature">
                <div class="feature-icon">📅</div>
                <h3>Google Calendar</h3>
                <p>Events sync directly to your calendar</p>
            </div>
            <div class="feature">
                <div class="feature-icon">👥</div>
                <h3>Invite Attendees</h3>
                <p>Add participants by email address</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🌍</div>
                <h3>Timezone Support</h3>
                <p>Automatic timezone detection</p>
            </div>
        </div>

        <h2>How to Use</h2>
        <ol>
            <li>Start a chat with <a href="https://t.me/handycalbot">@handycalbot</a></li>
            <li>Connect your Google Calendar with <code>/connect</code></li>
            <li>In any chat, type: <code>@handycalbot 14:30 "Meeting Title" email@example.com</code></li>
            <li>Click "Create Meeting" to confirm</li>
        </ol>

        <h2>Open Source</h2>
        <p>
            HandyCalBot is open source and available on
            <a href="https://github.com/dzhurinskiy/handycalbot">GitHub</a>.
            Contributions are welcome!
        </p>
    </main>

    <footer>
        <p>
            <a href="/privacy">Privacy Policy</a> |
            <a href="/terms">Terms of Service</a> |
            <a href="https://github.com/dzhurinskiy/handycalbot">GitHub</a>
        </p>
        <p style="margin-top: 1rem;">&copy; 2025 HandyCalBot. All rights reserved.</p>
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
    {COMMON_STYLES}
</head>
<body>
    <header>
        <h1>Privacy Policy</h1>
        <p>HandyCalBot</p>
    </header>

    <main>
        <p class="last-updated">Last updated: January 15, 2025</p>

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
        <p>
            <a href="/">Home</a> |
            <a href="/terms">Terms of Service</a> |
            <a href="https://github.com/dzhurinskiy/handycalbot">GitHub</a>
        </p>
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
    {COMMON_STYLES}
</head>
<body>
    <header>
        <h1>Terms of Service</h1>
        <p>HandyCalBot</p>
    </header>

    <main>
        <p class="last-updated">Last updated: January 15, 2025</p>

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
        <p>
            <a href="/">Home</a> |
            <a href="/privacy">Privacy Policy</a> |
            <a href="https://github.com/dzhurinskiy/handycalbot">GitHub</a>
        </p>
    </footer>
</body>
</html>
"""
