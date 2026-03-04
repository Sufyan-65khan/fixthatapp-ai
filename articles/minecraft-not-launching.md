# Troubleshooting Guide: Minecraft Not Launching

## Problem Description
Minecraft may fail to launch, crashing on startup, showing a black screen, freezing on the loading screen, or displaying Java errors. This affects both Minecraft Java Edition and Bedrock Edition.

## Possible Causes
1. **Outdated Java**: Minecraft Java Edition requires an up-to-date Java installation.
2. **Graphics driver issues**: Outdated or incompatible GPU drivers can prevent launching.
3. **Corrupted game files**: Damaged installation or mod files can cause crashes.
4. **Insufficient system resources**: Low RAM or disk space can prevent Minecraft from loading.
5. **Conflicting mods**: Incompatible mods or mod loaders can crash the game.
6. **Antivirus interference**: Security software may block Minecraft files.

## Step-by-Step Fixes

### Fix 1: Update Java (Java Edition)
- Visit java.com and download the latest version.
- Install it and restart your computer.
- Minecraft Launcher usually includes its own Java, but system Java should be updated too.

### Fix 2: Update Graphics Drivers
- Visit your GPU manufacturer's website (NVIDIA, AMD, or Intel).
- Download and install the latest drivers for your graphics card.
- Restart your computer after updating.

### Fix 3: Allocate More RAM
- Open Minecraft Launcher > Installations > Edit your profile.
- Click "More Options" and find the JVM Arguments field.
- Change `-Xmx2G` to `-Xmx4G` to allocate 4 GB of RAM.
- Save and try launching again.

### Fix 4: Remove Mods
- Navigate to your Minecraft folder: Press Win+R, type `%appdata%\.minecraft`.
- Move the "mods" folder to your desktop as a backup.
- Try launching vanilla Minecraft without mods.
- If it works, add mods back one at a time to find the problematic one.

### Fix 5: Delete and Reinstall
- Uninstall Minecraft from your system.
- Delete the .minecraft folder (back up your saves first from %appdata%\.minecraft\saves).
- Reinstall from minecraft.net.
- Restore your saves folder after reinstalling.

### Fix 6: Run as Administrator
- Right-click the Minecraft Launcher.
- Select "Run as Administrator".
- This gives Minecraft the permissions it needs to access files and hardware.

## When to Contact Support
If Minecraft still won't launch, visit help.minecraft.net for support. Include your system specifications, error messages, and crash logs from the .minecraft/crash-reports folder.

## FAQ
Q: Why does Minecraft show a black screen on launch?
A: This is usually a graphics driver issue. Update your GPU drivers and try launching again. You can also try running in windowed mode.

Q: Can I play Minecraft with integrated graphics?
A: Yes, but you may need to lower graphics settings significantly. Allocate more RAM and reduce render distance to improve performance.

Q: Why does Minecraft crash only with mods?
A: Mods may be incompatible with your Minecraft version or with each other. Check that all mods are for the correct version and remove recently added mods.

Q: How do I find my Minecraft crash logs?
A: Go to %appdata%\.minecraft\crash-reports. The latest crash report will contain information about what caused the crash.
