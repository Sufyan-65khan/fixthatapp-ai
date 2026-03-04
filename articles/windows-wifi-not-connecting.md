# Troubleshooting Guide: Windows Wi-Fi Not Connecting

## Problem Description
Your Windows PC or laptop may fail to connect to Wi-Fi networks. You might see "Can't connect to this network", "No internet access", or the Wi-Fi option may be missing entirely from the taskbar.

## Possible Causes
1. **Wi-Fi adapter disabled**: The wireless adapter may be turned off in settings or by a physical switch.
2. **Incorrect password**: The saved Wi-Fi password may be wrong or outdated.
3. **Network driver issues**: Outdated or corrupted Wi-Fi drivers can prevent connections.
4. **IP address conflicts**: Multiple devices may have conflicting IP addresses on the network.
5. **Router issues**: The router itself may need restarting or reconfiguring.
6. **Airplane mode enabled**: Airplane mode disables all wireless connections.

## Step-by-Step Fixes

### Fix 1: Toggle Wi-Fi and Airplane Mode
- Click the Wi-Fi icon in the taskbar.
- Make sure Wi-Fi is turned On and Airplane Mode is Off.
- If Wi-Fi was on, turn it off, wait 10 seconds, and turn it back on.

### Fix 2: Forget and Reconnect to the Network
- Go to Settings > Network & Internet > Wi-Fi > Manage Known Networks.
- Find your network and click "Forget".
- Scan for networks again and reconnect by entering the password.

### Fix 3: Run the Network Troubleshooter
- Go to Settings > System > Troubleshoot > Other Troubleshooters.
- Click "Run" next to "Network and Internet".
- Follow the prompts and let Windows diagnose and fix the issue.

### Fix 4: Reset TCP/IP and DNS
- Open Command Prompt as Administrator (search "cmd", right-click, Run as Administrator).
- Type these commands one at a time, pressing Enter after each:
  - `netsh winsock reset`
  - `netsh int ip reset`
  - `ipconfig /release`
  - `ipconfig /renew`
  - `ipconfig /flushdns`
- Restart your computer.

### Fix 5: Update Wi-Fi Drivers
- Open Device Manager (right-click Start button > Device Manager).
- Expand "Network Adapters".
- Right-click your Wi-Fi adapter and select "Update Driver".
- Choose "Search automatically for drivers".
- Restart your computer after updating.

### Fix 6: Reset Network Settings
- Go to Settings > Network & Internet > Advanced Network Settings > Network Reset.
- Click "Reset Now".
- Your computer will restart and all network settings will be reset to default.
- You'll need to reconnect to all Wi-Fi networks.

## When to Contact Support
If Wi-Fi still doesn't work, the issue may be hardware-related. Contact your laptop manufacturer's support or visit a repair center to check if the Wi-Fi adapter is functioning properly.

## FAQ
Q: Why does my Windows PC say "No Internet Access" when connected to Wi-Fi?
A: This means you're connected to the router but the router doesn't have internet. Try restarting your router, or contact your internet service provider.

Q: Why is the Wi-Fi option missing from my taskbar?
A: Your Wi-Fi adapter may be disabled. Open Device Manager > Network Adapters > right-click your Wi-Fi adapter > Enable Device. Also check for a physical Wi-Fi switch on your laptop.

Q: Can I use my phone's internet on my PC?
A: Yes, enable "Hotspot" on your phone and connect your PC to it via Wi-Fi. You can also use USB tethering by connecting your phone with a USB cable.

Q: How do I find my Wi-Fi password?
A: On a device already connected, go to Settings > Network & Internet > Wi-Fi > your network > Properties > View Wi-Fi Security Key. You can also find it on the back of your router.
