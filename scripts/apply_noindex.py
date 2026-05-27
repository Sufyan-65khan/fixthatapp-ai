"""Apply noindex meta and strip AdSense from non-indexable utility pages.

One-shot Week 1 cleanup script. Not part of the build pipeline.
"""
import os
import re

FILES = [
    "tools/index.html",
    "tools/color-code-converter/index.html",
    "tools/error-message-explainer/index.html",
    "tools/gradient-generator/index.html",
    "tools/hash-generator/index.html",
    "tools/json-formatter/index.html",
    "tools/jwt-decoder/index.html",
    "tools/password-generator/index.html",
    "tools/regex-tester/index.html",
    "seo-troubleshooting-guides.html",
    "seo-page-not-indexed.html",
    "seo-crawled-not-indexed.html",
    "seo-ranking-dropped.html",
    "privacy-policy.html",
    "terms.html",
    "cookie-policy.html",
    "all-guides.html",
]

NOINDEX_TAG = '<meta name="robots" content="noindex,follow">'

# Matches the multi-line consent + AdSense pair (Pattern A), tolerating whitespace.
PATTERN_A = re.compile(
    r'\s*<script>\s*\(function\(\)\s*\{\s*try\s*\{\s*var\s+consent\s*=\s*localStorage\.getItem\([\'"]fta_cookie_consent[\'"]\);.*?\}\)\(\);\s*</script>\s*<script\s+async\s+src=[\'"]https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*></script>',
    re.DOTALL,
)

# Matches the compact one-liner pair (Pattern B).
PATTERN_B = re.compile(
    r'\s*<script>\(function\(\)\{try\{var c=localStorage\.getItem\([\'"]fta_cookie_consent[\'"]\);.*?\}\)\(\);</script>\s*<script\s+async\s+src=[\'"]https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*></script>',
    re.DOTALL,
)

# Stray inline references inside the cookie-banner script block.
PATTERN_INLINE_ADS = re.compile(
    r'\s*window\.adsbygoogle\s*=\s*window\.adsbygoogle\s*\|\|\s*\[\];\s*window\.adsbygoogle\.requestNonPersonalizedAds\s*=\s*1;',
)

VIEWPORT_RE = re.compile(r'(<meta\s+name=["\']viewport["\'][^>]*>)', re.IGNORECASE)
ROBOTS_RE = re.compile(r'<meta\s+name=["\']robots["\'][^>]*>', re.IGNORECASE)


def process(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html
    actions = []

    if PATTERN_A.search(html):
        html = PATTERN_A.sub("", html)
        actions.append("stripped_ads_A")
    if PATTERN_B.search(html):
        html = PATTERN_B.sub("", html)
        actions.append("stripped_ads_B")
    if PATTERN_INLINE_ADS.search(html):
        html = PATTERN_INLINE_ADS.sub("", html)
        actions.append("stripped_inline_ads")

    if ROBOTS_RE.search(html):
        html = ROBOTS_RE.sub(NOINDEX_TAG, html)
        actions.append("replaced_robots")
    else:
        m = VIEWPORT_RE.search(html)
        if m:
            html = html[: m.end()] + "\n    " + NOINDEX_TAG + html[m.end():]
            actions.append("inserted_robots")
        else:
            actions.append("WARN_NO_VIEWPORT")

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    return ",".join(actions) if actions else "no_change"


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for rel in FILES:
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            print(f"MISSING {rel}")
            continue
        print(f"{rel}: {process(p)}")
