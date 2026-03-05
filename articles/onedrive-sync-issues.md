# Troubleshooting Guide: OneDrive Sync Issues

## Problem Description
Microsoft OneDrive may stop syncing files, showing sync errors, pending uploads, or files not appearing across devices. The OneDrive icon may show a red X or exclamation mark indicating sync problems.

## Possible Causes
1. **Storage quota full**: Your OneDrive storage may be full.
2. **File name or path issues**: Special characters or long paths can prevent syncing.
3. **Conflicting files**: Files edited simultaneously on different devices.
4. **OneDrive paused**: Syncing may be manually paused.
5. **Outdated OneDrive**: Old versions may have sync bugs.

## Step-by-Step Fixes

### Fix 1: Check Sync Status
- Click the OneDrive icon in the system tray.
- If paused, click "Resume syncing".
- Look for error messages and affected files.

### Fix 2: Check Storage
- Click OneDrive icon > Settings > Account.
- Check your storage usage.
- Free accounts get 5 GB. Delete files or upgrade to Microsoft 365 for 1 TB.

### Fix 3: Fix File Issues
- Shorten file names and paths (max 400 characters total).
- Remove special characters: # % & { } \ < > * ? / ! ' " : @ + ` | =
- Reduce file sizes — OneDrive has a 250 GB per-file limit.

### Fix 4: Reset OneDrive
- Press Win+R and type: `%localappdata%\Microsoft\OneDrive\onedrive.exe /reset`
- Wait 2 minutes, then OneDrive should restart automatically.
- If it doesn't restart, launch OneDrive from the Start menu.

### Fix 5: Unlink and Relink Account
- Click OneDrive icon > Settings > Account > Unlink this PC.
- Restart OneDrive and sign in again.
- Your files will re-sync from the cloud.

### Fix 6: Reinstall OneDrive
- Uninstall OneDrive from Settings > Apps.
- Download the latest version from onedrive.com.
- Install, sign in, and let files re-sync.

## When to Contact Support
If sync issues persist, visit support.microsoft.com/onedrive for help. Microsoft 365 subscribers get included support.

## FAQ
Q: Will resetting OneDrive delete my files?
A: No, files in the cloud are safe. Resetting only resets the local sync engine. Files may need to re-download.

Q: Why does OneDrive show "Processing changes"?
A: OneDrive is scanning for changes. This happens after reset or reconnection. Wait for it to complete — it can take hours for large libraries.

Q: Can OneDrive sync external drives?
A: No, OneDrive can only sync folders within the OneDrive folder on your main drive. Move files there or use symbolic links.

Q: Why is OneDrive using so much CPU?
A: This usually happens during initial sync or after reset. It should calm down after syncing is complete. If persistent, try pausing and resuming sync.
