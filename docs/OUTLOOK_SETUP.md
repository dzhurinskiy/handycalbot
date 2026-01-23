# Microsoft Outlook Calendar Setup Guide

This guide walks you through setting up Microsoft Azure AD app registration for HandyCalBot's Outlook Calendar integration with Microsoft Teams support.

## Step 1: Create an Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com/)
2. Sign in with your Microsoft account
3. Search for "App registrations" in the top search bar
4. Click **App registrations**
5. Click **New registration**

Fill in the form:
- **Name**: `HandyCalBot` (or any name you prefer)
- **Supported account types**: Select **Accounts in any organizational directory and personal Microsoft accounts**
- **Redirect URI**: Select **Web** and enter your callback URL
- Click **Register**

## Step 2: Configure Redirect URI

1. In your app registration, go to **Authentication** in the left sidebar
2. Under **Platform configurations**, ensure **Web** is added
3. Add the redirect URI:
```
https://handycal.dzhurinskiy.com/oauth/outlook/callback
```

> **Note**: Replace with your actual domain if self-hosting

4. Under **Implicit grant and hybrid flows**, leave both checkboxes unchecked
5. Click **Save**

## Step 3: Configure API Permissions

1. Go to **API permissions** in the left sidebar
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Select **Delegated permissions**
5. Search for and add these permissions:

| Permission | Description |
|------------|-------------|
| `Calendars.ReadWrite` | Read and write user calendars |
| `OnlineMeetings.ReadWrite` | Read and write online meetings (for Teams links) |
| `User.Read` | Sign in and read user profile |
| `offline_access` | Maintain access to data (for refresh tokens) |

6. Click **Add permissions**

> **Note**: If you're using this for an organization, you may need admin consent. Click **Grant admin consent for [Organization]** if available.

## Step 4: Create Client Secret

1. Go to **Certificates & secrets** in the left sidebar
2. Under **Client secrets**, click **New client secret**
3. Enter a description: `HandyCalBot Secret`
4. Select expiration: **24 months** (recommended) or your preferred duration
5. Click **Add**
6. **Immediately copy the secret value** - it won't be shown again!

> **Warning**: Copy the **Value**, not the Secret ID. The value looks like `abc123~xyz...`

## Step 5: Copy Your Credentials

Go to **Overview** in the left sidebar and copy:

| Setting | Where to Find |
|---------|---------------|
| **Application (client) ID** | Overview page, labeled "Application (client) ID" |
| **Client Secret** | Certificates & secrets page (from Step 4) |

Your Client ID looks like: `12345678-1234-1234-1234-123456789abc`

## Step 6: Configure the Bot

Add these environment variables to your deployment:

```bash
OUTLOOK_CLIENT_ID=your-application-client-id
OUTLOOK_CLIENT_SECRET=your-client-secret-value
OUTLOOK_REDIRECT_URI=https://handycal.dzhurinskiy.com/oauth/outlook/callback
```

### Using GitHub Secrets (recommended for CI/CD)

1. Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `OUTLOOK_CLIENT_ID`
   - `OUTLOOK_CLIENT_SECRET`
   - `OUTLOOK_REDIRECT_URI`

### Manual VPS Configuration

```bash
ssh root@your-server-ip
nano /opt/handycal/.env
# Add the three environment variables
```

## Step 7: Test the Integration

1. Start the bot
2. Send `/connectoutlook` to the bot
3. Click the connection button
4. Sign in with your Microsoft account
5. Grant the requested permissions
6. You should see a success message

## Troubleshooting

### "AADSTS50011: The reply URL specified in the request does not match"
- Ensure the redirect URI in Azure AD exactly matches your `.env` file
- Check for trailing slashes, http vs https, and correct domain

### "AADSTS7000218: The request body must contain the following parameter: 'client_assertion' or 'client_secret'"
- Ensure `OUTLOOK_CLIENT_SECRET` is set correctly
- The secret value (not the ID) must be used

### "AADSTS650052: The app needs access to a service that your organization has not subscribed to"
- Your organization may have restrictions on which apps can access Microsoft 365
- Contact your IT administrator or use a personal Microsoft account for testing

### "AADSTS90102: 'redirect_uri' value must be a valid absolute URI"
- Ensure the redirect URI starts with `https://`
- The URI must be an exact match (case-sensitive)

### "Consent required" or permission errors
- For organizational accounts, admin consent may be required
- Ask your Azure AD administrator to grant consent, or use a personal Microsoft account

### Teams meeting links not appearing
- Ensure `OnlineMeetings.ReadWrite` permission is granted
- Teams meeting creation requires a Microsoft 365 license with Teams enabled
- Personal Microsoft accounts may have limited Teams functionality

## Security Notes

- Never commit credentials to git
- Keep Client Secret secure and rotate before expiration
- Use separate app registrations for dev/staging/production
- Monitor the Azure AD sign-in logs for suspicious activity
- Consider using certificate authentication for production environments

## API Endpoints Used

| Operation | Endpoint |
|-----------|----------|
| Authorization | `https://login.microsoftonline.com/common/oauth2/v2.0/authorize` |
| Token Exchange | `https://login.microsoftonline.com/common/oauth2/v2.0/token` |
| Create Event | `POST https://graph.microsoft.com/v1.0/me/calendar/events` |
| List Events | `GET https://graph.microsoft.com/v1.0/me/calendar/events` |
| Update Event | `PATCH https://graph.microsoft.com/v1.0/me/calendar/events/{id}` |
| Delete Event | `DELETE https://graph.microsoft.com/v1.0/me/calendar/events/{id}` |
| Get User | `GET https://graph.microsoft.com/v1.0/me` |

## Teams Meeting Integration

To create a Teams meeting link with your calendar event, the bot sets:
```json
{
  "isOnlineMeeting": true,
  "onlineMeetingProvider": "teamsForBusiness"
}
```

The Teams join URL is returned in the response at `onlineMeeting.joinUrl`.

---

## Quick Reference

| Setting | Value |
|---------|-------|
| API | Microsoft Graph API |
| App Type | Web application |
| Account Types | Any organizational directory + personal accounts |
| Redirect URI | `https://handycal.dzhurinskiy.com/oauth/outlook/callback` |
| Required Permissions | `Calendars.ReadWrite`, `OnlineMeetings.ReadWrite`, `User.Read`, `offline_access` |
