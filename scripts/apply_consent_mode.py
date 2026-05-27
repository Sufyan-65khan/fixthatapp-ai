"""Apply Google Consent Mode v2 to all indexed pages with ads.

Two passes:
1. STRIP_ADS: remove all ad-related code from contact.html (thin page, must be ad-free).
2. CONSENT_MODE: in 52 indexed pages, replace the legacy pre-consent + raw
   adsbygoogle script with a default-denied Consent Mode v2 block, and replace
   the cookie-banner script with one that loads AdSense only after Accept.

Also updates cookie-banner copy and adds CLS-safe min-height on .cookie-banner.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- File lists -------------------------------------------------------------

STRIP_ADS_FILES = ["contact.html"]

CONSENT_MODE_FILES = [
    "index.html",
    "about.html",
] + [f"pages/{name}" for name in sorted(os.listdir(os.path.join(ROOT, "pages"))) if name.endswith(".html")]

# --- Patterns ---------------------------------------------------------------

# Head ad block — multi-line (Pattern A across most files).
HEAD_ADS_A = re.compile(
    r'\s*<script>\s*\(function\(\)\s*\{\s*try\s*\{\s*var\s+consent\s*=\s*localStorage\.getItem\([\'"]fta_cookie_consent[\'"]\);.*?\}\)\(\);\s*</script>\s*<script\s+async\s+src=[\'"]https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*></script>',
    re.DOTALL,
)
# Head ad block — compact (Pattern B).
HEAD_ADS_B = re.compile(
    r'\s*<script>\(function\(\)\{try\{var c=localStorage\.getItem\([\'"]fta_cookie_consent[\'"]\);.*?\}\)\(\);</script>\s*<script\s+async\s+src=[\'"]https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*></script>',
    re.DOTALL,
)

# Cookie-banner div block.
COOKIE_BANNER_DIV = re.compile(
    r'\s*<div class="cookie-banner" id="cookieBanner">.*?</div>\s*</div>',
    re.DOTALL,
)

# Cookie-banner script — old version (sets adsbygoogle on reject, no Consent Mode).
COOKIE_BANNER_SCRIPT_OLD = re.compile(
    r'\s*<script>\s*\(function\(\)\s*\{\s*var\s+key\s*=\s*[\'"]fta_cookie_consent[\'"];.*?banner\.style\.display\s*=\s*[\'"]none[\'"];\s*\}\);\s*\}\)\(\);\s*</script>',
    re.DOTALL,
)
# Cookie-banner script — same with extra payload after (e.g. contact.html form handler).
COOKIE_BANNER_SCRIPT_WITH_FORM = re.compile(
    r'\s*<script>\s*\(function\(\)\s*\{\s*var\s+key\s*=\s*[\'"]fta_cookie_consent[\'"];.*?\}\)\(\);(.*?)</script>',
    re.DOTALL,
)

VIEWPORT_RE = re.compile(r'(<meta\s+name=["\']viewport["\'][^>]*>)', re.IGNORECASE)
ROBOTS_RE = re.compile(r'<meta\s+name=["\']robots["\'][^>]*>', re.IGNORECASE)

CONSENT_BANNER_COPY_OLD = "We use cookies for ads and core site functions."
CONSENT_BANNER_COPY_NEW = "We use cookies for site functions and, if you accept, personalized ads."

CLS_CSS_OLD = ".cookie-banner{position:fixed;left:1rem;right:1rem;bottom:1rem;background:#1a1a2e;color:#fff;padding:.85rem 1rem;border-radius:10px;display:none;align-items:center;justify-content:space-between;gap:.8rem;z-index:2000;box-shadow:0 8px 24px rgba(0,0,0,.25);font-size:.85rem}"
CLS_CSS_NEW = ".cookie-banner{position:fixed;left:1rem;right:1rem;bottom:1rem;background:#1a1a2e;color:#fff;padding:.85rem 1rem;border-radius:10px;display:none;align-items:center;justify-content:space-between;gap:.8rem;z-index:2000;box-shadow:0 8px 24px rgba(0,0,0,.25);font-size:.85rem;min-height:64px;contain:layout style}@media(max-width:600px){.cookie-banner{min-height:88px}}"

# --- New head block (Consent Mode v2) ---------------------------------------

NEW_HEAD_BLOCK = '''<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {
      'ad_storage':'denied','ad_user_data':'denied',
      'ad_personalization':'denied','analytics_storage':'denied',
      'wait_for_update': 500
    });
    (function(){
      try {
        var c = localStorage.getItem('fta_cookie_consent');
        if (c === 'accepted') {
          gtag('consent','update',{
            'ad_storage':'granted','ad_user_data':'granted',
            'ad_personalization':'granted','analytics_storage':'granted'
          });
          var s = document.createElement('script');
          s.async = true;
          s.crossOrigin = 'anonymous';
          s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3140312947507954';
          document.head.appendChild(s);
        }
      } catch (e) {}
    })();
    </script>'''

NEW_BANNER_SCRIPT = '''<script>
    (function(){
      var key = 'fta_cookie_consent';
      var banner = document.getElementById('cookieBanner');
      var acceptBtn = document.getElementById('cookieAccept');
      var rejectBtn = document.getElementById('cookieReject');
      if (!banner || !acceptBtn || !rejectBtn) return;
      var saved = null;
      try { saved = localStorage.getItem(key); } catch (e) {}
      if (!saved) banner.style.display = 'flex';
      function loadAds(){
        if (window.__ftaAdsLoaded) return;
        window.__ftaAdsLoaded = true;
        var s = document.createElement('script');
        s.async = true;
        s.crossOrigin = 'anonymous';
        s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3140312947507954';
        document.head.appendChild(s);
      }
      acceptBtn.addEventListener('click', function(){
        try { localStorage.setItem(key, 'accepted'); } catch (e) {}
        if (typeof gtag === 'function') {
          gtag('consent','update',{
            'ad_storage':'granted','ad_user_data':'granted',
            'ad_personalization':'granted','analytics_storage':'granted'
          });
        }
        loadAds();
        banner.style.display = 'none';
      });
      rejectBtn.addEventListener('click', function(){
        try { localStorage.setItem(key, 'rejected'); } catch (e) {}
        banner.style.display = 'none';
      });
    })();
    </script>'''


def strip_ads(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    actions = []

    if HEAD_ADS_A.search(html):
        html = HEAD_ADS_A.sub("", html)
        actions.append("strip_head_A")
    if HEAD_ADS_B.search(html):
        html = HEAD_ADS_B.sub("", html)
        actions.append("strip_head_B")
    if COOKIE_BANNER_DIV.search(html):
        # Keep one closing div (we removed the outer </div> too). Re-add it.
        html = COOKIE_BANNER_DIV.sub("\n    </div>", html)
        actions.append("strip_banner_div")
    if COOKIE_BANNER_SCRIPT_OLD.search(html):
        html = COOKIE_BANNER_SCRIPT_OLD.sub("", html)
        actions.append("strip_banner_script")

    # Drop the cookie-banner CSS block too (contact only needs body styles).
    html = html.replace(CLS_CSS_OLD, "")
    html = re.sub(r'\s*\.cookie-banner[^{]*\{[^}]*\}\s*\.cookie-banner a\{[^}]*\}\s*\.cookie-actions\{[^}]*\}\s*\.cookie-btn[^{]*\{[^}]*\}\s*\.cookie-btn\.primary\{[^}]*\}', '', html)

    # Add explicit robots index,follow if not present.
    if not ROBOTS_RE.search(html):
        m = VIEWPORT_RE.search(html)
        if m:
            html = html[: m.end()] + '\n    <meta name="robots" content="index,follow">' + html[m.end():]
            actions.append("add_robots_index")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return ",".join(actions) if actions else "no_change"


def apply_consent_mode(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    actions = []
    original = html

    # Replace head ads with new Consent Mode block.
    if HEAD_ADS_A.search(html):
        html = HEAD_ADS_A.sub("\n    " + NEW_HEAD_BLOCK, html)
        actions.append("head_consent_v2_A")
    elif HEAD_ADS_B.search(html):
        html = HEAD_ADS_B.sub("\n    " + NEW_HEAD_BLOCK, html)
        actions.append("head_consent_v2_B")

    # Replace cookie-banner script (preserving any trailing payload for pages
    # like contact.html that bundle form handlers — but contact is handled by
    # strip_ads, not here, so this path is for regular pages).
    if COOKIE_BANNER_SCRIPT_OLD.search(html):
        html = COOKIE_BANNER_SCRIPT_OLD.sub("\n    " + NEW_BANNER_SCRIPT, html)
        actions.append("banner_script_v2")

    # Update banner copy.
    if CONSENT_BANNER_COPY_OLD in html:
        html = html.replace(CONSENT_BANNER_COPY_OLD, CONSENT_BANNER_COPY_NEW)
        actions.append("banner_copy")

    # CLS-safe banner CSS.
    if CLS_CSS_OLD in html:
        html = html.replace(CLS_CSS_OLD, CLS_CSS_NEW)
        actions.append("cls_css")

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return ",".join(actions) if actions else "no_change"


if __name__ == "__main__":
    print("=== STRIP_ADS ===")
    for rel in STRIP_ADS_FILES:
        p = os.path.join(ROOT, rel)
        print(f"{rel}: {strip_ads(p)}")

    print("\n=== CONSENT_MODE ===")
    for rel in CONSENT_MODE_FILES:
        p = os.path.join(ROOT, rel)
        print(f"{rel}: {apply_consent_mode(p)}")
