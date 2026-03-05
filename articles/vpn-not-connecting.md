# Troubleshooting Guide: VPN Not Connecting

## Problem Description
Your VPN app may fail to connect, get stuck on "Connecting", show authentication errors, or disconnect frequently. This leaves your internet traffic unprotected and prevents access to geo-restricted content.

## Possible Causes
1. **Internet connection down**: VPN needs a working internet connection first.
2. **VPN server overloaded**: The server you're connecting to may be full.
3. **Firewall blocking VPN**: Your network may block VPN protocols.
4. **Incorrect credentials**: Wrong username or password.
5. **VPN app outdated**: Old app versions may have connection bugs.
6. **ISP blocking VPN**: Some ISPs or networks block VPN traffic.

## Step-by-Step Fixes

### Fix 1: Check Internet Connection
- Disconnect from VPN and try loading a website.
- If internet doesn't work without VPN, fix your internet connection first.
- VPN needs a working internet connection to establish a tunnel.

### Fix 2: Try a Different Server
- Open your VPN app and select a different server location.
- Choose a server geographically closer to you for better speeds.
- Some servers may be overloaded — switching usually helps.

### Fix 3: Change VPN Protocol
- Go to your VPN app settings.
- Try switching protocols: WireGuard, OpenVPN (UDP), OpenVPN (TCP), IKEv2.
- WireGuard is usually fastest, OpenVPN TCP works best on restrictive networks.

### Fix 4: Restart Everything
- Close the VPN app completely.
- Restart your device.
- Restart your router.
- Open the VPN app and try connecting.

### Fix 5: Update the VPN App
- Go to your app store and update the VPN app.
- New versions include protocol improvements and bug fixes.
- Restart after updating.

### Fix 6: Disable Firewall Temporarily
- Temporarily disable Windows Firewall or your antivirus firewall.
- Try connecting to VPN.
- If it works, add the VPN app to your firewall's exception list.

## When to Contact Support
If VPN still won't connect, contact your VPN provider's support team. Most providers have 24/7 live chat support.

## FAQ
Q: Why does my VPN keep disconnecting?
A: This is usually caused by unstable internet, server issues, or battery optimization killing the app. Disable battery optimization for your VPN app.

Q: Can my ISP block VPN?
A: Yes, some ISPs and countries block VPN traffic. Use obfuscated servers (if your VPN offers them) or try the OpenVPN TCP protocol on port 443.

Q: Is it legal to use a VPN?
A: VPNs are legal in most countries. However, some countries restrict or ban VPN usage. Check your local laws.

Q: Does VPN slow down my internet?
A: Yes, VPN adds some overhead. Typically 10-30% speed reduction. Use WireGuard protocol and nearby servers to minimize speed loss.
