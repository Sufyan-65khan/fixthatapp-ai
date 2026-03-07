"""Generate sitemap.xml from all HTML pages, tools, and blog posts."""
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

# Core compliance and SEO pages
for path, changefreq, priority in [
    ("about.html", "monthly", "0.4"),
    ("all-guides.html", "daily", "0.9"),
    ("privacy-policy.html", "monthly", "0.3"),
    ("cookie-policy.html", "monthly", "0.3"),
    ("terms.html", "monthly", "0.3"),
    ("contact.html", "monthly", "0.4"),
    ("seo-troubleshooting-guides.html", "weekly", "0.7"),
    ("seo-page-not-indexed.html", "monthly", "0.6"),
    ("seo-crawled-not-indexed.html", "monthly", "0.6"),
    ("seo-ranking-dropped.html", "monthly", "0.6"),
]:
    urls.append(f"""  <url>
    <loc>{DOMAIN}/{path}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

# Tools index
urls.append(f"""  <url>
    <loc>{DOMAIN}/tools/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>""")

# Individual tools
tools_dir = "tools"
for tool_name in sorted(os.listdir(tools_dir)):
    tool_path = os.path.join(tools_dir, tool_name)
    if os.path.isdir(tool_path) and os.path.exists(os.path.join(tool_path, "index.html")):
        urls.append(f"""  <url>
    <loc>{DOMAIN}/tools/{tool_name}/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.85</priority>
  </url>""")

# Blog index
urls.append(f"""  <url>
    <loc>{DOMAIN}/blog/</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

# Blog posts
blog_dir = "blog"
for filename in sorted(os.listdir(blog_dir)):
    if filename.endswith('.html') and filename != 'index.html':
        urls.append(f"""  <url>
    <loc>{DOMAIN}/blog/{filename}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
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
