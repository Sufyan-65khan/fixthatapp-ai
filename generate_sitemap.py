"""Generate sitemap.xml from all HTML pages."""
import os
from datetime import date

DOMAIN = "https://www.fixthatapp.com"
TODAY = date.today().isoformat()

urls = []

# Homepage
urls.append(f"""  <url>
    <loc>{DOMAIN}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""")

# Privacy policy
urls.append(f"""  <url>
    <loc>{DOMAIN}/privacy-policy.html</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>""")

# All article pages
pages_dir = "pages"
for filename in sorted(os.listdir(pages_dir)):
    if filename.endswith('.html'):
        urls.append(f"""  <url>
    <loc>{DOMAIN}/pages/{filename}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"Sitemap generated with {len(urls)} URLs.")
