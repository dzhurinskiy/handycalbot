# Google OAuth Setup Guide

This guide walks you through setting up Google Calendar API credentials for HandyCalBot.

## Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown at the top → **New Project**
3. Enter project name: `HandyCalBot` (or any name you prefer)
4. Click **Create**
5. Wait for project creation, then select it from the dropdown

## Step 2: Enable Google Calendar API

1. In the left sidebar, go to **APIs & Services** → **Library**
2. Search for "Google Calendar API"
3. Click on **Google Calendar API**
4. Click **Enable**

## Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** (unless you have Google Workspace)
3. Click **Create**

Fill in the form:
- **App name**: `HandyCalBot`
- **User support email**: Your email
- **Developer contact email**: Your email
- Leave other fields empty for now
- Click **Save and Continue**

### Scopes (Data Access section)

1. Go to the **Data Access** section
2. Click **Add or Remove Scopes**
3. Search for "Google Calendar API" in the filter
4. Select these scopes:
   - `../auth/calendar.events` - "See, edit, share, and permanently delete all the calendars..."
   - `../auth/calendar.readonly` - "See and download any calendar..."
5. Click **Update**
6. Click **Save and Continue**

> **Note**: If scopes don't appear, make sure you enabled "Google Calendar API" in Step 2 first.

### Test Users (Audience section)

1. Go to the **Audience** section in the left sidebar
2. Under "Test users", click **Add Users**
3. Enter your email address
4. Click **Save**

> **Note**: While the app is in "Testing" mode, only test users can authorize the app.

## Step 4: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Select **Web application**
4. Enter name: `HandyCalBot Web Client`

### Add Authorized Redirect URIs

Click **Add URI** and enter:
```
https://handycal.dzhurinskiy.com/oauth/google/callback
```

> **Note**: Replace with your actual domain if you have one

5. Click **Create**

## Step 5: Copy Your Credentials

After creation, you'll see a popup with:
- **Client ID**: `xxxx.apps.googleusercontent.com`
- **Client Secret**: `GOCSPX-xxxx`

**Copy both values** - you'll need them for the `.env` file.

You can also download the JSON file for backup.

## Step 6: Configure the Bot

Credentials are now stored in GitHub Secrets and automatically deployed to VPS.

To update manually on VPS:
```bash
ssh root@164.92.157.14
nano /opt/handycal/.env
```

## Step 7: Publish the App (for production)

Once testing is complete:

1. Go to **OAuth consent screen** → **Audience**
2. Click **Publish App**
3. Confirm the prompts

> **Note**: Until published, only test users can authorize the app.

## Troubleshooting

### "Access blocked: This app's request is invalid"
- Check that the redirect URI exactly matches what's in Google Cloud Console
- Ensure there are no trailing slashes or typos

### "Error 403: access_denied"
- Make sure your email is added as a test user in the **Audience** section
- Or publish the app for production use

### "Error 400: redirect_uri_mismatch"
- The redirect URI must exactly match the one in Google Cloud Console
- Check for http vs https, trailing slashes, port numbers

## Security Notes

- Never commit credentials to git
- Keep Client Secret secure
- Rotate credentials if compromised
- Use separate projects for dev/staging/production

---

## Quick Reference

| Setting | Value |
|---------|-------|
| API | Google Calendar API |
| App Type | Web application |
| Redirect URI | `https://handycal.dzhurinskiy.com/oauth/google/callback` |
| Required Scopes | `calendar.events`, `calendar.readonly` |
