# Troubleshooting Guide: Discord Mic Not Working

## Problem Description
Your microphone may not work in Discord voice channels or calls. Other users can't hear you, even though your mic works fine in other applications. The mic icon may show you as muted or the green ring around your avatar may not appear when you speak.

## Possible Causes
1. **Wrong input device selected**: Discord may be using a different microphone than the one you want.
2. **Microphone permissions**: Discord may not have permission to access your microphone.
3. **Voice settings misconfigured**: Input sensitivity or voice activity settings may be wrong.
4. **Audio driver issues**: Outdated or corrupted audio drivers can cause mic problems.
5. **Discord audio subsystem**: The audio subsystem may not be compatible with your setup.

## Step-by-Step Fixes

### Fix 1: Check Microphone Permissions
- On Windows: Settings > Privacy > Microphone > Make sure "Allow apps to access your microphone" is On and Discord is enabled.
- On Mac: System Preferences > Security & Privacy > Privacy > Microphone > Check Discord.
- On mobile: Settings > Apps > Discord > Permissions > Enable Microphone.

### Fix 2: Select the Correct Input Device
- Open Discord > User Settings (gear icon) > Voice & Video.
- Under "Input Device", select your microphone from the dropdown.
- Don't use "Default" — choose the specific device instead.
- Click "Let's Check" to test your microphone.

### Fix 3: Reset Voice Settings
- Go to Discord > User Settings > Voice & Video.
- Scroll to the bottom and click "Reset Voice Settings".
- Confirm the reset and test your mic again.

### Fix 4: Adjust Input Sensitivity
- Go to User Settings > Voice & Video.
- Turn off "Automatically determine input sensitivity".
- Manually drag the sensitivity slider to the left so it picks up your voice.
- Speak into your mic and watch the indicator to make sure it detects sound.

### Fix 5: Change Audio Subsystem
- Go to User Settings > Voice & Video.
- Scroll down to "Audio Subsystem".
- Switch from "Standard" to "Legacy" (or vice versa).
- Discord will restart — test your mic after it reopens.

### Fix 6: Update Audio Drivers
- On Windows: Open Device Manager > Audio inputs and outputs > Right-click your mic > Update driver.
- You can also visit your computer manufacturer's website to download the latest audio drivers.
- Restart your computer after updating.

## When to Contact Support
If your mic still doesn't work after trying all steps, contact Discord support at support.discord.com. Include your system info by going to User Settings > Voice & Video and noting the "Debug Logging" information.

## FAQ
Q: Why can people hear me in other apps but not Discord?
A: Discord may be using a different input device. Go to Voice & Video settings and manually select the correct microphone.

Q: How do I know if my mic is being detected by Discord?
A: Go to User Settings > Voice & Video and use the "Let's Check" feature. Speak into your mic — if the bar moves, Discord is detecting your voice.

Q: Why does my mic work in DMs but not in servers?
A: Check if you're server-muted by a moderator. Also, some servers have voice channel permissions that may restrict your microphone usage.

Q: Can I use my phone as a mic for Discord on PC?
A: Yes, there are apps like WO Mic that let you use your phone's microphone on your PC. Set it up and select it as the input device in Discord settings.
