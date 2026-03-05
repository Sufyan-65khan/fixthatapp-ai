# Troubleshooting Guide: Two-Factor Authentication (2FA) Not Working

## Problem Description
Two-factor authentication codes may not work when trying to log into your accounts. The codes from your authenticator app might be rejected, SMS codes may not arrive, or backup codes may fail, leaving you locked out of your account.

## Possible Causes
1. **Time sync issues**: Authenticator apps need your device clock to be accurate.
2. **SMS not delivered**: Network issues can prevent text message delivery.
3. **Wrong account selected**: You may be using codes from the wrong account in your authenticator.
4. **Expired codes**: 2FA codes expire every 30 seconds — you may be entering them too late.
5. **Account recovery needed**: If you lost your 2FA device, you need account recovery.

## Step-by-Step Fixes

### Fix 1: Check Your Clock
- Make sure your device's time is set to automatic.
- On iPhone: Settings > General > Date & Time > Set Automatically.
- On Android: Settings > System > Date & Time > Automatic Date & Time.
- Google Authenticator: Open app > Menu > Settings > Time Correction for Codes > Sync Now.

### Fix 2: Enter Code Quickly
- 2FA codes change every 30 seconds.
- Wait for a fresh code to appear, then enter it immediately.
- Don't use a code that's about to expire (less than 5 seconds left).

### Fix 3: Use Backup Codes
- When you set up 2FA, you should have saved backup codes.
- Check your email, password manager, or printed copies for backup codes.
- Each backup code can usually only be used once.

### Fix 4: Check SMS Delivery
- If using SMS 2FA, make sure your phone has signal.
- Try restarting your phone.
- Check if your carrier is blocking short codes.
- Contact your carrier if SMS codes consistently don't arrive.

### Fix 5: Use an Alternative 2FA Method
- Most services offer multiple 2FA options.
- Try email verification, phone call, or security key if available.
- Check the login page for "Try another way" or "More options".

### Fix 6: Account Recovery
- If you can't access 2FA at all, use the service's account recovery process.
- Google: accounts.google.com/signin/recovery
- Apple: iforgot.apple.com
- Most services have a "Lost access to 2FA" link on the login page.

## When to Contact Support
If you're completely locked out, contact the service's support team. You'll likely need to verify your identity with personal information, ID documents, or other proof.

## FAQ
Q: What if I lost my phone with the authenticator app?
A: Use backup codes if you have them. If not, go through the account recovery process for each service. This is why it's important to save backup codes.

Q: Can I transfer my authenticator to a new phone?
A: Google Authenticator allows cloud backup and transfer. Microsoft Authenticator has cloud backup too. Export your accounts before resetting or replacing your phone.

Q: Which is more secure: SMS or authenticator app?
A: Authenticator apps are more secure. SMS can be intercepted through SIM swapping. Use an authenticator app or security key when possible.

Q: How do I avoid getting locked out of 2FA?
A: Save backup codes in a safe place, set up multiple 2FA methods, use an authenticator app with cloud backup, and keep your recovery email and phone updated.
