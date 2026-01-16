# Google OAuth Verification Video Script

This document contains instructions for creating the YouTube video required for Google OAuth verification.

## Video Recording Setup

### Software Recommendation

**OBS Studio** is perfect for this. Configuration:

1. **Scene Setup:**
   - Add "Display Capture" for showing screens
   - Add "Audio Input Capture" for microphone
   - Resolution: 1920x1080 (minimum 720p)

2. **Recording Settings:**
   - Format: MP4
   - Encoder: x264 or NVENC
   - Quality: High (CRF 18-22)

3. **No editing needed** - Google prefers authentic, unedited walkthroughs. OBS records directly to a finished file.

---

## Video Script

### PART 1: Introduction (30 seconds)

**SHOW:** Your face or app logo

**SAY:**
> "Hello, I'm demonstrating HandyCalBot, a Telegram bot that helps users schedule Google Calendar meetings directly from Telegram chats. I'll show how OAuth consent works and explain how we use each requested scope."

---

### PART 2: Show App Details in Google Cloud Console (1-2 minutes)

**SHOW:** Google Cloud Console → APIs & Services → Credentials

**SAY:**
> "Here is the Google Cloud Console for our project."

**SHOW and READ aloud:**
- **Project Name**
- **OAuth 2.0 Client ID** (the actual client ID string)
- **Application type:** Web application
- **Authorized redirect URIs:** `https://handycal.dzhurinskiy.com/oauth/google/callback`

**THEN GO TO:** OAuth consent screen

**SHOW and READ aloud:**
- **App Name:** HandyCalBot
- **User support email**
- **Developer contact email**
- **Scopes requested** (list them)

---

### PART 3: Demonstrate the OAuth Flow (2-3 minutes)

**SHOW:** Telegram on desktop or phone

**SAY:**
> "Now I'll demonstrate the complete user authorization flow."

**STEP 1:** Open Telegram, search for `@handycalbot`

**SAY:**
> "Users start by finding our bot on Telegram."

**STEP 2:** Type `/start`

**SHOW:** The welcome message appears

**SAY:**
> "The bot greets users and explains how to connect their calendar."

**STEP 3:** Type `/connect`

**SHOW:** The "Connect Google Calendar" button appears

**SAY:**
> "When users type /connect, they receive a button to authorize Google Calendar access."

**STEP 4:** Click the button → Google OAuth consent screen appears

**SHOW:** The Google consent screen with:
- App name (HandyCalBot)
- The two scopes being requested
- Your email domain

**SAY:**
> "Users are redirected to Google's official OAuth consent screen. Notice it clearly shows:
> 1. The app name: HandyCalBot
> 2. The permissions being requested - I'll explain each one in detail shortly."

**STEP 5:** Click "Allow" / Grant access

**SHOW:** Redirect to success page → "Connected!" message

**SAY:**
> "After granting permission, users are redirected to our success page and receive a confirmation in Telegram."

**SHOW:** Telegram message confirming connection + timezone selection

---

### PART 4: Explain Each Scope and How It's Used (2-3 minutes)

**SHOW:** Split screen or text overlay listing scopes

**SAY:**

#### Scope 1: `calendar.events`

> "The first scope is `https://www.googleapis.com/auth/calendar.events`. This allows us to create, modify, and delete calendar events."

**SHOW:** Demonstration in Telegram:
1. Type in any chat: `@handycalbot 14:30 "Team Meeting" test@example.com`
2. Show the inline result appearing
3. Click to create the meeting
4. Show success message

**SAY:**
> "Here's how we use it: users type the bot name with meeting details. The bot creates an event in Google Calendar with the specified time, title, and attendees. We also use this scope to cancel meetings when users request it via the /cancel command."

#### Scope 2: `calendar.readonly`

> "The second scope is `https://www.googleapis.com/auth/calendar.readonly`. This allows us to read calendar data."

**SHOW:** Type `/meetings` in Telegram, show the list of upcoming meetings

**SAY:**
> "We use this scope to display the user's upcoming meetings when they type /meetings. This helps users see what's already scheduled before creating new events."

---

### PART 5: Show Data Security (30 seconds - optional but recommended)

**SAY:**
> "Regarding data security: OAuth tokens are encrypted before storage using AES encryption. Users can disconnect at any time using /disconnect, or revoke access directly from their Google Account settings. We only access calendar data - no emails, contacts, or other Google services."

**SHOW:** Type `/disconnect` to demonstrate easy revocation

---

### PART 6: Summary (30 seconds)

**SAY:**
> "To summarize: HandyCalBot uses two Google Calendar scopes:
> 1. calendar.events - to create and delete meetings for users
> 2. calendar.readonly - to display upcoming meetings
>
> The app is open source, available on GitHub, and users maintain full control over their data. Thank you for reviewing."

---

## Checklist Before Recording

- [ ] Have your Google Cloud Console logged in and ready
- [ ] Have Telegram open with a test account
- [ ] Disconnect calendar first (so you can show fresh OAuth flow)
- [ ] Test microphone audio levels in OBS
- [ ] Close notifications and other apps
- [ ] Video length target: **3-5 minutes** total

## Upload Instructions

1. Upload to YouTube as **Unlisted** (not Public needed)
2. Copy the URL and paste it in Google's verification form

---

## Reference: OAuth Scopes Used

| Scope | Purpose |
|-------|---------|
| `https://www.googleapis.com/auth/calendar.events` | Create, modify, delete calendar events |
| `https://www.googleapis.com/auth/calendar.readonly` | Read/list upcoming meetings |
