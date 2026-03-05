# Troubleshooting Guide: Wi-Fi Connected But No Internet

## Problem Description
Your device shows it's connected to Wi-Fi, but you can't access any websites or use online apps. You may see "Connected, no internet" or "No internet access" messages on your phone, laptop, or tablet.

## Possible Causes
1. **Router not connected to ISP**: Your router may have lost its internet connection.
2. **DNS issues**: Your device may not be able to resolve domain names.
3. **IP address conflict**: Multiple devices may have the same IP address.
4. **ISP outage**: Your internet service provider may be experiencing problems.
5. **Captive portal**: You may need to sign in on a public Wi-Fi network.
6. **Firewall or VPN blocking**: Security software may be blocking connections.

## Step-by-Step Fixes

### Fix 1: Restart Your Router and Modem
- Unplug both your router and modem from power.
- Wait 30 seconds.
- Plug in the modem first, wait until all lights are stable.
- Then plug in the router and wait for it to fully start.
- Try connecting again.

### Fix 2: Forget and Reconnect to Wi-Fi
- Go to your device's Wi-Fi settings.
- Tap the network name > Forget Network.
- Reconnect by selecting the network and entering the password.

### Fix 3: Change DNS Settings
- Change to Google DNS (8.8.8.8 / 8.8.4.4) or Cloudflare DNS (1.1.1.1 / 1.0.0.1).
- On Windows: Network Settings > Change Adapter Options > Properties > IPv4 > Use the following DNS.
- On iPhone: Wi-Fi > tap network > Configure DNS > Manual > add servers.
- On Android: Wi-Fi > tap network > Advanced > change DNS.

### Fix 4: Renew IP Address
- On Windows: Open Command Prompt as admin, type `ipconfig /release` then `ipconfig /renew`.
- On Mac: System Preferences > Network > Advanced > TCP/IP > Renew DHCP Lease.
- On iPhone: Wi-Fi > tap (i) next to network > Renew Lease.

### Fix 5: Check for ISP Outage
- Call your ISP or check their website/app for outage reports.
- Check downdetector.com for your ISP.
- If there's an outage, wait for the ISP to fix it.

### Fix 6: Disable VPN or Proxy
- If using a VPN, disconnect it temporarily.
- Check for proxy settings: Settings > Network > Proxy > make sure it's off.
- Try accessing the internet without VPN/proxy.

## When to Contact Support
If none of the fixes work, contact your ISP. The issue may be with your internet connection or router hardware.

## FAQ
Q: Why does my phone say "Connected, no internet"?
A: Your phone is connected to the router, but the router doesn't have internet. This is usually an ISP issue or a router configuration problem.

Q: Can a router work without internet?
A: Yes, a router can create a local Wi-Fi network without internet. Devices can connect to each other but can't access websites.

Q: Why does only one device have no internet?
A: If other devices work fine, the issue is with that specific device. Try forgetting the network, restarting the device, or resetting network settings.

Q: Does restarting the router fix internet issues?
A: Yes, in most cases. Restarting clears temporary errors and forces the router to establish a fresh connection with your ISP.
