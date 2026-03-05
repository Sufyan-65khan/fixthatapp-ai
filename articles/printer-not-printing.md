# Troubleshooting Guide: Printer Not Printing

## Problem Description
Your printer may refuse to print, show "Offline" status, print blank pages, get stuck in a print queue, or display error messages. This can happen with USB-connected, Wi-Fi, or network printers.

## Possible Causes
1. **Printer offline**: The printer may have lost connection to your computer.
2. **Print queue stuck**: Previous print jobs may be blocking new ones.
3. **Ink or toner empty**: Cartridges may be low or empty.
4. **Paper jam**: Paper stuck inside the printer prevents printing.
5. **Driver issues**: Outdated or corrupted printer drivers.
6. **Wrong printer selected**: Your computer may be sending to a different printer.

## Step-by-Step Fixes

### Fix 1: Check Printer Status
- Make sure the printer is turned on and has paper loaded.
- Check for any error lights or messages on the printer's display.
- Ensure the printer is connected (USB cable plugged in or connected to Wi-Fi).

### Fix 2: Set as Default Printer
- On Windows: Settings > Bluetooth & Devices > Printers & Scanners > Select your printer > Set as Default.
- On Mac: System Preferences > Printers & Scanners > Right-click your printer > Set as Default.

### Fix 3: Clear Print Queue
- On Windows: Settings > Printers & Scanners > Select printer > Open Print Queue > Cancel All Documents.
- On Mac: System Preferences > Printers & Scanners > Open Print Queue > select jobs > Delete.

### Fix 4: Restart Print Spooler (Windows)
- Press Win+R, type `services.msc`, press Enter.
- Find "Print Spooler" service.
- Right-click > Stop. Wait 10 seconds. Right-click > Start.
- Try printing again.

### Fix 5: Check Ink/Toner Levels
- Most printers have a utility to check ink levels.
- On Windows: Settings > Printers > select printer > Print Preferences.
- Replace empty cartridges.

### Fix 6: Update or Reinstall Printer Driver
- On Windows: Device Manager > Print Queues > right-click printer > Update Driver.
- Or visit the printer manufacturer's website to download the latest driver.
- Uninstall and reinstall the printer if updating doesn't work.

## When to Contact Support
If the printer still won't print after all fixes, contact the printer manufacturer (HP, Canon, Epson, Brother, etc.) for hardware support.

## FAQ
Q: Why does my printer say "Offline"?
A: The printer lost its connection. For Wi-Fi printers, check the Wi-Fi connection. For USB printers, check the cable. Restart both the printer and computer.

Q: Why is my printer printing blank pages?
A: The ink cartridges may be empty or clogged. Run the printer's head cleaning utility and check ink levels.

Q: Can I print from my phone?
A: Yes, most modern printers support AirPrint (iPhone) or Google Cloud Print / Mopria (Android). Make sure the printer and phone are on the same Wi-Fi.

Q: Why does my printer print very slowly?
A: Check if you're printing in high quality mode, which is slower. Switch to draft or normal quality. Also check ink levels — low ink can slow printing.
