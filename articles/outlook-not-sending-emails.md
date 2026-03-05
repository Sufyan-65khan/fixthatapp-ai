# Troubleshooting Guide: Outlook Not Sending Emails

## Problem Description
Microsoft Outlook may fail to send emails, showing errors like "Send/Receive Error", keeping emails stuck in the Outbox, or displaying server connection errors. This affects both desktop and web versions of Outlook.

## Possible Causes
1. **Internet connection**: Outlook needs stable internet to send emails.
2. **Large attachments**: Files exceeding the size limit (25MB for most accounts) block sending.
3. **Outbox stuck**: Emails may get stuck in the Outbox due to formatting or size issues.
4. **Account authentication**: Your password may have changed or expired.
5. **Server settings wrong**: Incorrect SMTP settings prevent sending.

## Step-by-Step Fixes

### Fix 1: Check Internet Connection
- Make sure you're connected to the internet.
- Check if you can browse websites normally.
- Try sending from Outlook on the web (outlook.live.com) to isolate the issue.

### Fix 2: Check the Outbox
- Go to the Outbox folder and open any stuck emails.
- Check if attachments are too large (over 25MB).
- Delete the stuck email, reduce attachment size, and try again.

### Fix 3: Re-enter Your Password
- Go to File > Account Settings > Account Settings.
- Select your email account and click "Repair".
- Re-enter your password when prompted.

### Fix 4: Work Offline Toggle
- Check if "Work Offline" is enabled in the Send/Receive tab.
- If it's highlighted, click it to go back online.
- Outlook won't send emails while in offline mode.

### Fix 5: Create a New Outlook Profile
- Go to Control Panel > Mail > Show Profiles > Add.
- Create a new profile and set up your email account.
- Set the new profile as default and restart Outlook.

### Fix 6: Repair Office Installation
- Go to Settings > Apps > Microsoft Office > Modify > Repair.
- Choose "Online Repair" for a thorough fix.
- Restart your computer after the repair completes.

## When to Contact Support
If emails still won't send, contact Microsoft support at support.microsoft.com or your IT administrator for work accounts.

## FAQ
Q: Why are my emails stuck in the Outbox?
A: Usually due to large attachments, lost internet connection, or authentication issues. Open the stuck email, reduce its size, and try again.

Q: What's the maximum attachment size in Outlook?
A: 25MB for Outlook.com and most Exchange accounts. For larger files, use OneDrive and share a link instead.

Q: Can I recall a sent email in Outlook?
A: In the desktop app with Exchange, go to Sent Items > open the email > Message tab > Actions > Recall This Message. This only works if the recipient hasn't read it yet.

Q: Why does Outlook keep asking for my password?
A: Your password may have changed, or your authentication token expired. Re-enter your credentials or enable modern authentication.
