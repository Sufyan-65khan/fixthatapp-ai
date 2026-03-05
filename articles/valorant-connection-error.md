# Troubleshooting Guide: Valorant Connection Error

## Problem Description
Valorant may show connection errors like "Valorant has encountered a connection error", Error Code VAN 1, VAN 68, or VAN 84. You might be unable to log in, experience high ping during matches, or get disconnected frequently.

## Possible Causes
1. **Riot Vanguard issues**: The anti-cheat system may need restarting.
2. **Internet connection**: Unstable network causes connection errors.
3. **Firewall blocking**: Windows Firewall or antivirus may block Valorant.
4. **Server issues**: Riot Games servers may be under maintenance.
5. **DNS problems**: Incorrect DNS settings can prevent connections.

## Step-by-Step Fixes

### Fix 1: Restart Vanguard
- Right-click the Vanguard icon in the system tray and select "Exit".
- Restart your computer (Vanguard requires a reboot).
- Launch Valorant after restarting.

### Fix 2: Check Riot Games Status
- Visit status.riotgames.com and select Valorant.
- Check if there are server issues in your region.
- If servers are down, wait for Riot to fix the problem.

### Fix 3: Allow Valorant Through Firewall
- Open Windows Firewall > Allow an App Through Firewall.
- Make sure Valorant and Riot Vanguard are both allowed.
- Add them manually if they're not in the list.

### Fix 4: Flush DNS
- Open Command Prompt as Administrator.
- Type `ipconfig /flushdns` and press Enter.
- Type `ipconfig /release` then `ipconfig /renew`.
- Restart your computer.

### Fix 5: Use Wired Connection
- Connect your PC directly to the router with ethernet.
- This reduces ping and improves connection stability.
- Close other bandwidth-heavy applications.

### Fix 6: Reinstall Valorant and Vanguard
- Uninstall Riot Vanguard first: Settings > Apps > Riot Vanguard > Uninstall.
- Then uninstall Valorant.
- Download and install Valorant fresh from playvalorant.com.
- Restart your computer before launching.

## When to Contact Support
If connection errors persist, submit a ticket at support-valorant.riotgames.com. Include your error code, region, and network diagnostics.

## FAQ
Q: What does Error VAN 1 mean?
A: VAN 1 usually means Riot Vanguard isn't running. Restart your computer to start Vanguard automatically, then launch Valorant.

Q: Why is my Valorant ping so high?
A: High ping can be caused by Wi-Fi, network congestion, or distance from servers. Use ethernet, close background apps, and select the closest server region.

Q: Can I play Valorant without Vanguard?
A: No, Riot Vanguard anti-cheat is required. It starts at boot and must be running for Valorant to launch.

Q: Does VPN help with Valorant connection issues?
A: Usually not. VPNs add latency. However, if your ISP has poor routing, a gaming VPN might help. Note that some VPNs may trigger Vanguard restrictions.
