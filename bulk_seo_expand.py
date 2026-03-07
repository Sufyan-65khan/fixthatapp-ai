import os
import re
from datetime import date

ROOT = r"C:\Users\sufya\fixthatapp-ai"
ARTICLES_DIR = os.path.join(ROOT, "articles")
TOOLS_DIR = os.path.join(ROOT, "tools")
BLOG_DIR = os.path.join(ROOT, "blog")
PAGES_DIR = os.path.join(ROOT, "pages")

# -----------------------------
# Ensure ads.txt line
# -----------------------------
ads_path = os.path.join(ROOT, "ads.txt")
ads_line = "google.com, pub-3140312947507954, DIRECT, f08c47fec0942fa0"
with open(ads_path, "w", encoding="utf-8") as f:
    f.write(ads_line + "\n")

# -----------------------------
# Generate 50 extra tools
# -----------------------------
extra_tools = [
    ("status-page-finder", "Status Page Finder", "Find official status pages and real-time outage signals for any service.", "service"),
    ("app-outage-map", "App Outage Map", "Build region-based outage checks with quick incident verification links.", "service"),
    ("server-response-time-checker", "Server Response Time Checker", "Measure quick response time and identify high-latency services.", "latency"),
    ("domain-health-checker", "Domain Health Checker", "Run core domain checks for DNS reachability and issue triage.", "dns"),
    ("isp-outage-helper", "ISP Outage Helper", "Check ISP-level outages and distinguish them from app-only failures.", "service"),
    ("cdn-reachability-checker", "CDN Reachability Checker", "Test CDN edge reachability and latency symptoms.", "latency"),
    ("api-health-helper", "API Health Helper", "Quickly validate API endpoint health and status behavior.", "api"),
    ("http-error-troubleshooter", "HTTP Error Troubleshooter", "Diagnose HTTP 4xx/5xx patterns with actionable next steps.", "checklist"),
    ("dns-flush-helper", "DNS Flush Helper", "Get platform-specific DNS cache flush and resolver reset guidance.", "checklist"),
    ("ipv6-connectivity-helper", "IPv6 Connectivity Helper", "Identify IPv6 route issues that break selective services.", "checklist"),
    ("proxy-detection-helper", "Proxy Detection Helper", "Check likely proxy interference with app and web traffic.", "checklist"),
    ("firewall-conflict-checker", "Firewall Conflict Checker", "Find common firewall and security rule conflicts.", "checklist"),
    ("port-blocking-helper", "Port Blocking Helper", "Troubleshoot port restrictions impacting calls, games, and apps.", "checklist"),
    ("websocket-issue-helper", "WebSocket Issue Helper", "Debug live-update and real-time socket connection failures.", "checklist"),
    ("ssl-handshake-helper", "SSL Handshake Helper", "Fix certificate and TLS handshake errors quickly.", "ssl"),
    ("app-lag-diagnoser", "App Lag Diagnoser", "Isolate app lag caused by network, device, or backend bottlenecks.", "checklist"),
    ("stuck-loading-screen-helper", "Stuck Loading Screen Helper", "Resolve endless loading screen and spinner issues.", "checklist"),
    ("crash-loop-helper", "Crash Loop Helper", "Troubleshoot repeated app crash loops with safe recovery steps.", "checklist"),
    ("account-lockout-helper", "Account Lockout Helper", "Recover locked accounts with safer identity recovery flow.", "service"),
    ("mfa-code-delay-checker", "MFA Code Delay Checker", "Fix delayed one-time code delivery and validation errors.", "checklist"),
    ("email-verification-helper", "Email Verification Helper", "Diagnose missing verification emails and sender issues.", "dns"),
    ("sms-verification-helper", "SMS Verification Helper", "Troubleshoot SMS OTP failures and delivery delays.", "checklist"),
    ("payment-gateway-helper", "Payment Gateway Helper", "Investigate gateway declines, retries, and pending states.", "checklist"),
    ("refund-status-helper", "Refund Status Helper", "Track refund timelines and identify stuck refund scenarios.", "checklist"),
    ("subscription-renewal-helper", "Subscription Renewal Helper", "Fix failed subscription renewals and billing loops.", "cancel"),
    ("in-app-purchase-helper", "In-App Purchase Helper", "Resolve in-app purchase failures across app stores.", "checklist"),
    ("stream-quality-checker", "Stream Quality Checker", "Diagnose low bitrate, stutter, and stream quality drops.", "checklist"),
    ("audio-sync-helper", "Audio Sync Helper", "Fix audio/video sync drift and delayed playback issues.", "checklist"),
    ("video-playback-helper", "Video Playback Helper", "Troubleshoot black screen, freeze, and playback interruptions.", "checklist"),
    ("meeting-connection-helper", "Meeting Connection Helper", "Fix join failures and unstable conference sessions.", "checklist"),
    ("screen-share-helper", "Screen Share Helper", "Resolve screen-share permission and rendering failures.", "checklist"),
    ("bluetooth-audio-helper", "Bluetooth Audio Helper", "Troubleshoot Bluetooth audio dropouts and pairing errors.", "checklist"),
    ("location-permission-helper", "Location Permission Helper", "Fix map and location feature failures across devices.", "perm"),
    ("camera-permission-helper", "Camera Permission Helper", "Check camera access and permission blockers.", "media"),
    ("microphone-permission-helper", "Microphone Permission Helper", "Check mic access and input capture failures.", "media"),
    ("notification-delay-helper", "Notification Delay Helper", "Diagnose delayed push notifications and background limits.", "notify"),
    ("background-sync-helper", "Background Sync Helper", "Fix background sync interruptions and queue delays.", "checklist"),
    ("data-sync-conflict-helper", "Data Sync Conflict Helper", "Resolve sync conflicts and duplicate data states.", "checklist"),
    ("backup-restore-helper", "Backup Restore Helper", "Troubleshoot restore failures and incomplete backups.", "checklist"),
    ("file-upload-failure-helper", "File Upload Failure Helper", "Fix upload failures caused by size, format, or network issues.", "checklist"),
    ("download-failure-helper", "Download Failure Helper", "Resolve stalled, blocked, or corrupted downloads.", "checklist"),
    ("cache-corruption-helper", "Cache Corruption Helper", "Detect cache corruption patterns and recover clean state.", "checklist"),
    ("cookie-session-helper", "Cookie Session Helper", "Fix login loops and broken sessions from cookie issues.", "checklist"),
    ("browser-extension-conflict-checker", "Browser Extension Conflict Checker", "Find extension conflicts that break app features.", "compat"),
    ("mobile-data-helper", "Mobile Data Helper", "Troubleshoot app failures specific to cellular data.", "checklist"),
    ("roaming-connectivity-helper", "Roaming Connectivity Helper", "Debug roaming network restrictions and app failures.", "checklist"),
    ("device-time-sync-helper", "Device Time Sync Helper", "Fix security/login failures caused by incorrect device time.", "checklist"),
    ("storage-cleanup-helper", "Storage Cleanup Helper", "Recover app stability by reducing storage pressure safely.", "storage"),
    ("battery-saver-conflict-helper", "Battery Saver Conflict Helper", "Identify power-saver settings blocking app behavior.", "battery"),
    ("app-compatibility-helper", "App Compatibility Helper", "Check compatibility issues between app version and OS/browser.", "compat"),
]

tool_template = """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{title} - Free Online Tool | FixThatApp</title>
  <meta name=\"description\" content=\"{desc}\">
  <meta name=\"keywords\" content=\"{slug_words}, troubleshooting tool, fixthatapp\">
  <link rel=\"canonical\" href=\"https://www.fixthatapp.com/tools/{slug}/\">
  <script>
  (function() {{
    try {{
      var consent = localStorage.getItem('fta_cookie_consent');
      if (consent === 'rejected') {{
        window.adsbygoogle = window.adsbygoogle || [];
        window.adsbygoogle.requestNonPersonalizedAds = 1;
      }}
    }} catch (e) {{}}
  }})();
  </script>
  <script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3140312947507954\" crossorigin=\"anonymous\"></script>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fa;color:#333;line-height:1.6;min-height:100vh;display:flex;flex-direction:column}}
    header{{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:1rem 1.5rem;display:flex;justify-content:space-between;align-items:center}}
    header a{{color:#fff;text-decoration:none;font-size:1.2rem;font-weight:700}}
    .container{{max-width:920px;margin:0 auto;padding:1.5rem 1rem;flex:1;width:100%}}
    .breadcrumb{{font-size:.85rem;color:#777;margin-bottom:1rem}}
    .breadcrumb a{{color:#667eea;text-decoration:none}}
    .card{{background:#fff;border-radius:12px;padding:1.4rem;box-shadow:0 2px 8px rgba(0,0,0,.08);margin-bottom:1rem}}
    h1{{font-size:1.55rem;margin-bottom:.4rem}}
    .subtitle{{color:#666;margin-bottom:1rem}}
    .row{{display:flex;gap:.5rem;flex-wrap:wrap}}
    input{{flex:1;min-width:240px;padding:.7rem .9rem;border:2px solid #e0e0e0;border-radius:8px;font-size:.95rem;background:#f8f9ff;color:#333}}
    .btn{{padding:.7rem 1rem;background:#667eea;color:#fff;border:none;border-radius:8px;cursor:pointer;font-weight:600}}
    .btn.secondary{{background:#fff;color:#667eea;border:2px solid #667eea}}
    .result{{margin-top:1rem;background:#f8f9ff;border-radius:8px;padding:1rem;display:none}}
    .result.show{{display:block}}
    .result a{{color:#667eea;text-decoration:none;display:inline-block;margin-right:.8rem;margin-top:.25rem}}
    .tips{{background:#fff;border-radius:12px;padding:1.1rem;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
    .tips h2{{font-size:1.05rem;margin-bottom:.6rem}}
    .tips ul{{margin-left:1.2rem;color:#444}}
    .tips li{{margin-bottom:.4rem}}
    footer{{text-align:center;padding:1.5rem;color:#999;font-size:.82rem;border-top:1px solid #e0e0e0}}
    footer a{{color:#667eea;text-decoration:none}}
  </style>
</head>
<body>
  <header>
    <a href=\"../../index.html\">FixThatApp</a>
    <a href=\"../\">All Tools</a>
  </header>
  <div class=\"container\">
    <nav class=\"breadcrumb\"><a href=\"../../index.html\">Home</a> &rsaquo; <a href=\"../index.html\">Tools</a> &rsaquo; {title}</nav>
    <div class=\"card\">
      <h1>{title}</h1>
      <p class=\"subtitle\">{desc}</p>
      <div class=\"row\">
        <input id=\"toolInput\" placeholder=\"e.g. ChatGPT, Netflix, example.com\" />
        <button class=\"btn\" onclick=\"runTool()\">Run Check</button>
        <button class=\"btn secondary\" onclick=\"resetTool()\">Reset</button>
      </div>
      <div id=\"result\" class=\"result\"></div>
    </div>
    <div class=\"tips\">
      <h2>Quick Triage Pattern</h2>
      <ul>
        <li>Validate scope first (only you vs everyone).</li>
        <li>Check service status and incident reports.</li>
        <li>Test on another device/network before deep config changes.</li>
        <li>Collect timestamp + exact error for support escalation.</li>
      </ul>
    </div>
  </div>
  <footer>&copy; 2026 FixThatApp | <a href=\"../../about.html\">About</a> | <a href=\"../../privacy-policy.html\">Privacy Policy</a> | <a href=\"../../cookie-policy.html\">Cookie Policy</a> | <a href=\"../../contact.html\">Contact</a></footer>
  <script>
  const MODE = '{mode}';
  function esc(s){{return String(s||'').replace(/[&<>\"']/g,m=>({{'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;',"'":'&#39;'}}[m]));}}
  function show(html){{const e=document.getElementById('result');e.innerHTML=html;e.classList.add('show');}}
  async function runTool(){{
    const raw=(document.getElementById('toolInput').value||'').trim();
    if(!raw && !['notify','media','perm','compat','storage','battery','checklist'].includes(MODE)){{show('<p>Enter a value first.</p>');return;}}
    if(['service','cancel','website'].includes(MODE)){{
      const q=encodeURIComponent(raw);
      show('<p><strong>Checks for:</strong> '+esc(raw)+'</p>'+
        '<a target="_blank" rel="noopener" href="https://downdetector.com/search/?q='+q+'">DownDetector Search</a>'+
        '<a target="_blank" rel="noopener" href="https://www.google.com/search?q='+q+'+status+page">Status Page Search</a>'+
        '<a target="_blank" rel="noopener" href="https://www.google.com/search?q='+q+'+not+working">Latest Reports</a>');
      return;
    }}
    if(MODE==='dns'){{
      const d=raw.replace(/^https?:\/\//,'').split('/')[0];
      try{{
        const r=await fetch('https://dns.google/resolve?name='+encodeURIComponent(d)+'&type=A').then(x=>x.json());
        const a=(r.Answer||[]).map(x=>x.data).join(', ')||'No A record';
        show('<p><strong>Domain:</strong> '+esc(d)+'</p><p><strong>A Records:</strong> '+esc(a)+'</p><a target="_blank" rel="noopener" href="https://dnschecker.org/#A/'+encodeURIComponent(d)+'">Propagation Check</a>');
      }}catch(e){{show('<p>DNS lookup failed in browser. Retry or use external resolver.</p>')}}
      return;
    }}
    if(MODE==='latency'){{
      const t=raw.startsWith('http')?raw:'https://www.google.com/favicon.ico';
      const vals=[];for(let i=0;i<5;i++){{const s=performance.now();try{{await fetch(t+(t.includes('?')?'&':'?')+'t='+Date.now()+i,{{mode:'no-cors',cache:'no-store'}})}}catch(e){{}}vals.push(Math.round(performance.now()-s));}}
      const avg=Math.round(vals.reduce((a,b)=>a+b,0)/vals.length);show('<p><strong>Latency samples (ms):</strong> '+vals.join(', ')+'</p><p><strong>Average:</strong> '+avg+' ms</p>');return;
    }}
    if(MODE==='api'){{
      const u=raw.startsWith('http')?raw:'https://'+raw;const s=performance.now();
      try{{const r=await fetch(u,{{cache:'no-store'}});show('<p><strong>Status:</strong> '+r.status+' '+esc(r.statusText)+'</p><p><strong>Response time:</strong> '+Math.round(performance.now()-s)+' ms</p>')}}catch(e){{show('<p>Request failed (possibly CORS or unreachable endpoint).</p>')}}
      return;
    }}
    if(MODE==='ssl'){{
      const d=raw.replace(/^https?:\/\//,'').split('/')[0];
      show('<p><strong>SSL checks for:</strong> '+esc(d)+'</p><a target="_blank" rel="noopener" href="https://www.ssllabs.com/ssltest/analyze.html?d='+encodeURIComponent(d)+'">SSL Labs</a><a target="_blank" rel="noopener" href="https://www.google.com/search?q='+encodeURIComponent(d)+'+certificate+invalid">Certificate Errors</a>');
      return;
    }}
    if(MODE==='speed'){{
      const s=performance.now();
      try{{await fetch('https://proof.ovh.net/files/10Mb.dat?'+Date.now(),{{mode:'no-cors',cache:'no-store'}});const sec=(performance.now()-s)/1000;const mbps=((10*8)/Math.max(sec,0.3)).toFixed(2);show('<p><strong>Estimated speed:</strong> '+mbps+' Mbps</p><p><strong>Test time:</strong> '+sec.toFixed(2)+'s</p>')}}catch(e){{show('<p>Speed test failed. Retry on stable network.</p>')}}
      return;
    }}
    if(MODE==='notify'){{show('<p><strong>Notifications:</strong> '+(('Notification' in window)?Notification.permission:'unsupported')+'</p>');return;}}
    if(MODE==='media'){{if(!(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia)){{show('<p>Media API unsupported.</p>');return;}}try{{const st=await navigator.mediaDevices.getUserMedia({{audio:true,video:true}});st.getTracks().forEach(t=>t.stop());show('<p>Camera and microphone look available.</p>')}}catch(e){{show('<p>Permission denied or device busy.</p>')}}return;}}
    if(MODE==='perm'){{show('<p><strong>Geolocation:</strong> '+(('geolocation' in navigator)?'supported':'unsupported')+'</p><p><strong>Notifications:</strong> '+(('Notification' in window)?Notification.permission:'unsupported')+'</p>');return;}}
    if(MODE==='compat'){{show('<p><strong>Fetch:</strong> '+(!!window.fetch)+'</p><p><strong>Service Worker:</strong> '+('serviceWorker' in navigator)+'</p><p><strong>WebRTC:</strong> '+(!!(navigator.mediaDevices&&navigator.mediaDevices.getUserMedia))+'</p>');return;}}
    if(MODE==='storage'){{if(!(navigator.storage&&navigator.storage.estimate)){{show('<p>Storage API unsupported.</p>');return;}}const q=await navigator.storage.estimate();show('<p><strong>Usage:</strong> '+(q.usage/(1024*1024)).toFixed(2)+' MB</p><p><strong>Quota:</strong> '+(q.quota/(1024*1024)).toFixed(2)+' MB</p>');return;}}
    if(MODE==='battery'){{if(!navigator.getBattery){{show('<p>Battery API unsupported.</p>');return;}}const b=await navigator.getBattery();show('<p><strong>Battery:</strong> '+Math.round(b.level*100)+'%</p><p><strong>Charging:</strong> '+(b.charging?'Yes':'No')+'</p>');return;}}
    show('<p>Follow the checklist above for this helper.</p>');
  }}
  function resetTool(){{document.getElementById('toolInput').value='';const e=document.getElementById('result');e.classList.remove('show');e.innerHTML='';}}
  </script>
</body>
</html>
"""

new_cards = []
for slug, title, desc, mode in extra_tools:
    dir_path = os.path.join(TOOLS_DIR, slug)
    os.makedirs(dir_path, exist_ok=True)
    html = tool_template.format(
        title=title,
        desc=desc,
        slug=slug,
        slug_words=slug.replace("-", " "),
        mode=mode,
    )
    with open(os.path.join(dir_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    new_cards.append(
        f'''            <a class="card" href="{slug}/">\n                <div class="card-icon">TS</div>\n                <h2>{title}</h2>\n                <p>{desc}</p>\n                <span class="tag">Troubleshooting</span>\n            </a>'''
    )

# Insert new section into tools/index.html if not present
index_tools_path = os.path.join(TOOLS_DIR, "index.html")
with open(index_tools_path, "r", encoding="utf-8") as f:
    tools_index = f.read()

marker = "Advanced Troubleshooting Tools"
if marker not in tools_index:
    section = "\n\n        <h2 class=\"section-title\">Advanced Troubleshooting Tools</h2>\n        <div class=\"grid\">\n" + "\n".join(new_cards) + "\n        </div>\n"
    tools_index = tools_index.replace("<div class=\"cta\">", section + "\n        <div class=\"cta\">", 1)
    with open(index_tools_path, "w", encoding="utf-8") as f:
        f.write(tools_index)

# -----------------------------
# Generate 520 new article markdown files
# -----------------------------
apps = [
"Telegram","Signal","Threads","Reddit","Pinterest","Canva","Notion","Trello","Asana","ClickUp","Monday","Dropbox","Box","Slack","Zoom","Teams","Meet","Skype","Discord","Steam","Epic Games","Battle.net","EA App","Ubisoft Connect","Palworld","Genshin Impact","Honkai Star Rail","Warzone","Apex Legends","FIFA Mobile","Clash of Clans","Brawl Stars","PUBG Mobile","Mobile Legends","Roblox Studio","CapCut","InShot","Snapseed","Lightroom Mobile","VSCO","Google Docs","Google Sheets","Google Slides","Google Calendar","Google Keep","Google One","Microsoft 365","OneNote","Word","Excel","PowerPoint","Outlook","Yahoo Mail","Proton Mail","iCloud Mail","Mailchimp","Shopify Admin","WooCommerce","Etsy Seller","Amazon Seller","Paytm","PhonePe","Razorpay","Stripe Dashboard","Square","Wise","Revolut","Binance","Coinbase","Kraken","Metamask","Trust Wallet","Uber Driver","Lyft Driver","DoorDash Driver","Instacart Shopper","Swiggy","Zomato","Blinkit","Zepto","Payoneer","Upwork","Fiverr","LinkedIn","X","Facebook","Messenger","WhatsApp","Instagram","TikTok","YouTube","YouTube Music","Spotify","Apple Music","Netflix","Prime Video","Disney Plus","Hulu","Max","Crunchyroll","Sony LIV","JioCinema","Hotstar","Twitch","OBS Studio","Adobe Creative Cloud","Photoshop","Illustrator","Premiere Pro","After Effects","Figma","Framer","Webflow","GitHub","GitLab","Bitbucket","Vercel","Netlify","Cloudflare","Firebase","Supabase","MongoDB Atlas","Render","Railway","DigitalOcean","Linode","Hostinger","Bluehost","Namecheap","cPanel","WordPress","Elementor","Yoast SEO","RankMath","Google Search Console","Google Analytics","GA4","Ahrefs","SEMrush","Ubersuggest","Screaming Frog","Zapier","Make","IFTTT","Claude","Gemini","Perplexity","Copilot","Midjourney","DALL-E","Runway","Canva AI","Notion AI"
]

issue_specs = [
    ("not-loading", "Not Loading"),
    ("login-not-working", "Login Not Working"),
    ("keeps-crashing", "Keeps Crashing"),
    ("notifications-not-working", "Notifications Not Working"),
    ("verification-code-not-received", "Verification Code Not Received"),
    ("payment-failed", "Payment Failed"),
    ("sync-not-working", "Sync Not Working"),
    ("connection-timeout", "Connection Timeout"),
    ("update-stuck", "Update Stuck"),
    ("account-locked", "Account Locked"),
]

existing = {fn[:-3] for fn in os.listdir(ARTICLES_DIR) if fn.endswith('.md')}
created = 0

for app in apps:
    app_slug = re.sub(r"[^a-z0-9]+", "-", app.lower()).strip("-")
    app_name = app
    for issue_slug, issue_title in issue_specs:
        slug = f"{app_slug}-{issue_slug}"
        if slug in existing:
            continue
        title = f"Troubleshooting Guide: {app_name} {issue_title}"
        md = f"""# {title}

{app_name} {issue_title.lower()} is usually caused by account state, outdated app versions, network instability, or backend service issues. Use this guide to isolate the root cause quickly.

## Quick Fix Sequence

1. Confirm whether the issue affects only your device or multiple devices/accounts.
2. Check official status updates and live outage reports for {app_name}.
3. Update the app and device OS to the latest stable versions.
4. Sign out, restart device, and sign back in.
5. Retry on another network (Wi-Fi vs mobile data).

## Detailed Troubleshooting Steps

### Verify Service Status First

Before changing settings, confirm whether {app_name} is currently down. If there is a confirmed outage, local fixes will not resolve the problem until service recovers.

### Check Version and Compatibility

Outdated app builds can trigger {issue_title.lower()} behavior after backend protocol updates. Install the latest app version and confirm OS compatibility.

### Reset Session and Cached State

Stale sessions and corrupted cache data are common causes. Clear app cache where available, then sign in again.

### Test Network Path

Switch between Wi-Fi and mobile data. If behavior changes, troubleshoot DNS, VPN, router, or ISP path issues.

### Validate Account or Billing State

If this issue involves account access, purchases, or subscriptions, verify account standing, payment method validity, and region restrictions.

## Prevention Checklist

- Keep app and OS updated automatically.
- Enable account recovery options and multi-factor authentication.
- Avoid unstable VPN/proxy setups unless required.
- Keep enough device storage free for app updates and cache operations.

## FAQ

Q: Why did {app_name} suddenly start showing {issue_title.lower()} today?
A: Sudden behavior usually maps to outages, silent app updates, expired sessions, or local network path changes.

Q: Should I reinstall {app_name} immediately?
A: Reinstall only after status checks, update checks, and cache/session resets fail.

Q: How long should I wait before escalating to support?
A: If no outage is reported and guided checks fail within 20-30 minutes, escalate with exact error text, timestamp, device model, and app version.
"""
        path = os.path.join(ARTICLES_DIR, slug + ".md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(md)
        existing.add(slug)
        created += 1
        if created >= 520:
            break
    if created >= 520:
        break

print(f"Created {created} new markdown guide files.")

# -----------------------------
# Build all pages + sitemap
# -----------------------------
os.system(f'py -3 "{os.path.join(ROOT, "build.py")}"')
os.system(f'py -3 "{os.path.join(ROOT, "generate_sitemap.py")}"')

# -----------------------------
# Create all-guides directory page
# -----------------------------
all_guides = sorted([fn for fn in os.listdir(PAGES_DIR) if fn.endswith('.html')])
items = []
for fn in all_guides:
    label = fn.replace('.html', '').replace('-', ' ').title()
    items.append(f'<li><a href="pages/{fn}">{label}</a></li>')

all_guides_html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>All Troubleshooting Guides - FixThatApp</title>
  <meta name=\"description\" content=\"Complete index of troubleshooting guides for apps, devices, networks, payments, and account issues.\">
  <link rel=\"canonical\" href=\"https://www.fixthatapp.com/all-guides.html\">
  <script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3140312947507954\" crossorigin=\"anonymous\"></script>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fa;color:#333;line-height:1.6}}
    header{{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:1.4rem 1rem;text-align:center}}
    header a{{color:#fff;text-decoration:none;font-size:1.3rem;font-weight:700}}
    .container{{max-width:1100px;margin:0 auto;padding:1.5rem 1rem 2rem}}
    .card{{background:#fff;border-radius:12px;padding:1.2rem;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
    h1{{font-size:1.5rem;margin-bottom:.5rem}}
    p{{color:#555;margin-bottom:1rem}}
    ul{{columns:3;column-gap:1.4rem;list-style:none}}
    li{{margin-bottom:.35rem}}
    a{{color:#667eea;text-decoration:none}}
    @media(max-width:900px){{ul{{columns:2}}}}
    @media(max-width:640px){{ul{{columns:1}}}}
  </style>
</head>
<body>
  <header><a href=\"index.html\">FixThatApp</a></header>
  <div class=\"container\">
    <div class=\"card\">
      <h1>All Troubleshooting Guides</h1>
      <p>Browsable index of all guides currently available on FixThatApp.</p>
      <ul>
        {''.join(items)}
      </ul>
    </div>
  </div>
</body>
</html>
"""
with open(os.path.join(ROOT, "all-guides.html"), "w", encoding="utf-8") as f:
    f.write(all_guides_html)

# Refresh sitemap again to include all-guides.html if script catches static core pages list not automatic
os.system(f'py -3 "{os.path.join(ROOT, "generate_sitemap.py")}"')

print(f"Total pages currently: {len(all_guides)}")
