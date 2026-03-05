# Troubleshooting Guide: Xbox Live Connection Issues

## Problem Description
Xbox Live may fail to connect, preventing you from playing online games, accessing the store, or chatting with friends. You might see error codes or "Can't connect to Xbox Live" messages.

## Possible Causes
1. **Xbox Live service outage**: Microsoft servers may be down.
2. **Network configuration**: Your router or NAT type may be blocking connections.
3. **Internet connection issues**: Weak or unstable internet.
4. **DNS issues**: Incorrect DNS settings can prevent connections.
5. **Console software outdated**: Your Xbox may need a system update.

## Step-by-Step Fixes

### Fix 1: Check Xbox Live Status
- Visit support.xbox.com/en-US/xbox-live-status.
- If services are down, wait for Microsoft to fix it.
- Check specific services — some may work while others are down.

### Fix 2: Test Network Connection
- On Xbox: Settings > General > Network Settings > Test Network Connection.
- This will identify specific problems with your connection.
- Follow any suggestions Xbox provides.

### Fix 3: Restart Console and Router
- Press and hold the Xbox power button for 10 seconds to hard reset.
- Unplug your router for 30 seconds, then plug it back in.
- Wait for both to fully restart and try connecting.

### Fix 4: Fix NAT Type
- Open NAT is best for Xbox Live. Check in Network Settings.
- Enable UPnP on your router (access at 192.168.1.1 or similar).
- Alternatively, set up port forwarding for Xbox Live ports: TCP 3074, UDP 3074, 88, 500, 3544, 4500.

### Fix 5: Change DNS Settings
- Go to Settings > Network > Advanced Settings > DNS Settings.
- Set Primary DNS to 8.8.8.8 and Secondary to 8.8.4.4 (Google DNS).
- Or use 1.1.1.1 and 1.0.0.1 (Cloudflare DNS).

### Fix 6: Use Wired Connection
- Connect your Xbox directly to the router with an ethernet cable.
- Wired connections are more stable and have lower latency.
- If you must use Wi-Fi, move closer to the router.

## When to Contact Support
If you still can't connect, contact Xbox support at support.xbox.com. Provide your error code for faster assistance.

## FAQ
Q: What does NAT type mean for Xbox?
A: Open NAT allows all connections, Moderate has some restrictions, and Strict severely limits online features. Aim for Open NAT.

Q: Can I play Xbox games without Xbox Live?
A: Single-player games work offline. Online multiplayer requires Xbox Game Pass Core or Ultimate subscription.

Q: Why do I get disconnected during games?
A: This is usually a network stability issue. Use ethernet, close other bandwidth-heavy applications, and check for router firmware updates.

Q: How do I fix error code 0x87dd0006?
A: This is a sign-in error. Restart your console, check Xbox Live status, and make sure your Microsoft account credentials are correct.
