"""Generate sitemap.xml from indexable HTML pages.

Skips any HTML containing a `noindex` meta tag. Uses each file's mtime for
`<lastmod>` so the sitemap reflects real edit history, not a build timestamp.
"""
import os
from datetime import datetime, timezone

DOMAIN = "https://www.fixthatapp.com"
ROOT = os.path.dirname(os.path.abspath(__file__))


def is_noindex(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return 'content="noindex' in f.read()
    except OSError:
        return True


def lastmod(path: str) -> str:
    ts = os.path.getmtime(path)
    return datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()


def add(urls: list, loc: str, path: str, changefreq: str, priority: str) -> None:
    if not os.path.exists(path) or is_noindex(path):
        return
    urls.append(
        f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod(path)}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
    )


urls: list[str] = []

# Homepage
home = os.path.join(ROOT, "index.html")
urls.append(
    f"""  <url>
    <loc>{DOMAIN}/</loc>
    <lastmod>{lastmod(home)}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
)

# Trust / EEAT pages (indexable only)
add(urls, f"{DOMAIN}/about.html", os.path.join(ROOT, "about.html"), "monthly", "0.6")
add(urls, f"{DOMAIN}/contact.html", os.path.join(ROOT, "contact.html"), "monthly", "0.4")

# Troubleshooting pages
pages_dir = os.path.join(ROOT, "pages")
if os.path.isdir(pages_dir):
    for filename in sorted(os.listdir(pages_dir)):
        if not filename.endswith(".html"):
            continue
        path = os.path.join(pages_dir, filename)
        add(urls, f"{DOMAIN}/pages/{filename}", path, "weekly", "0.8")

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""

with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"Sitemap generated with {len(urls)} URLs.")
