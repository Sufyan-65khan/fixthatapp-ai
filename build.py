"""Build script to convert markdown articles to HTML pages."""
import os
import re
import html

ARTICLES_DIR = "articles"
PAGES_DIR = "pages"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - FixThatApp</title>
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{meta_keywords}">
    <link rel="canonical" href="https://www.fixthatapp.com/pages/{slug}.html">
    <meta property="og:title" content="{title} - FixThatApp">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.fixthatapp.com/pages/{slug}.html">
    <meta property="og:site_name" content="FixThatApp">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{title} - FixThatApp">
    <meta name="twitter:description" content="{meta_description}">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔧</text></svg>">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3140312947507954"
     crossorigin="anonymous"></script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "TechArticle",
      "headline": "{title}",
      "description": "{meta_description}",
      "dateModified": "2026-03-05",
      "author": {{
        "@type": "Organization",
        "name": "FixThatApp",
        "url": "https://www.fixthatapp.com"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "FixThatApp",
        "url": "https://www.fixthatapp.com"
      }},
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "https://www.fixthatapp.com/pages/{slug}.html"
      }}
    }}
    </script>
    {faq_schema}
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.7;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        header a {{ color: white; text-decoration: none; font-size: 1.3rem; font-weight: bold; }}
        .header-search {{
            position: relative;
            max-width: 260px;
        }}
        .header-search input {{
            width: 100%;
            padding: 0.45rem 0.8rem 0.45rem 2.2rem;
            border: none;
            border-radius: 50px;
            font-size: 0.85rem;
            outline: none;
            background: rgba(255,255,255,0.2);
            color: white;
        }}
        .header-search input::placeholder {{ color: rgba(255,255,255,0.7); }}
        .header-search input:focus {{ background: rgba(255,255,255,0.3); }}
        .header-search-icon {{
            position: absolute;
            left: 0.7rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 0.85rem;
            pointer-events: none;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        .breadcrumb {{
            font-size: 0.85rem;
            color: #888;
            margin-bottom: 1rem;
        }}
        .breadcrumb a {{ color: #667eea; text-decoration: none; }}
        .breadcrumb a:hover {{ text-decoration: underline; }}
        .article {{
            background: white;
            border-radius: 12px;
            padding: 2.5rem 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .article h1 {{ font-size: 1.8rem; color: #1a1a2e; margin-bottom: 0.5rem; }}
        .article .updated {{ font-size: 0.8rem; color: #999; margin-bottom: 1.5rem; }}
        .article h2 {{ font-size: 1.3rem; color: #1a1a2e; margin: 2rem 0 0.75rem; padding-bottom: 0.3rem; border-bottom: 2px solid #f0f0f0; }}
        .article h3 {{ font-size: 1.1rem; color: #444; margin: 1.5rem 0 0.5rem; }}
        .article p {{ margin-bottom: 0.85rem; color: #444; }}
        .article ol, .article ul {{ margin: 0.5rem 0 1rem 1.5rem; color: #444; }}
        .article li {{ margin-bottom: 0.4rem; }}
        .article strong {{ color: #333; }}
        .article code {{ background: #f0f0f5; padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.9em; }}
        .faq {{ background: #f8f9ff; border-radius: 8px; padding: 1.25rem; margin-bottom: 0.75rem; }}
        .faq p {{ margin-bottom: 0.25rem; }}
        .faq .q {{ font-weight: 600; color: #333; }}
        .faq .a {{ color: #555; }}
        footer {{
            text-align: center;
            padding: 2rem 1rem;
            color: #999;
            font-size: 0.85rem;
            border-top: 1px solid #eee;
        }}
        footer a {{ color: #667eea; text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
        @media (max-width: 600px) {{
            .article {{ padding: 1.5rem 1rem; }}
            .article h1 {{ font-size: 1.4rem; }}
            .header-search {{ display: none; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="../index.html">FixThatApp</a>
        <div class="header-search">
            <span class="header-search-icon">&#128269;</span>
            <input type="text" placeholder="Search guides..." onfocus="window.location='../index.html?q='+this.value" >
        </div>
    </header>
    <div class="container">
        <nav class="breadcrumb">
            <a href="../index.html">Home</a> &rsaquo; {breadcrumb_title}
        </nav>
        <div class="article">
            {content}
        </div>
    </div>
    <footer>&copy; 2026 FixThatApp. All rights reserved. | <a href="../privacy-policy.html">Privacy Policy</a> | <a href="../index.html">All Guides</a></footer>
</body>
</html>
"""


def md_to_html(text):
    """Convert markdown to HTML with proper h3 support."""
    lines = text.strip().split('\n')
    html_parts = []
    title = ""
    in_faq = False
    faq_pairs = []  # Collect Q&A for FAQPage schema
    current_q = None
    current_a = None
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            if in_faq:
                if current_q and current_a:
                    faq_pairs.append((current_q, current_a))
                    current_q = None
                    current_a = None
                in_faq = False
                html_parts.append('</div>')
            i += 1
            continue

        # Title (h1)
        if line.startswith('# ') and not line.startswith('## '):
            title = line[2:].strip()
            html_parts.append(f'<h1>{html.escape(title)}</h1>')
            html_parts.append('<p class="updated">Last updated: March 5, 2026</p>')
            i += 1
            continue

        # Section headers (h2)
        if line.startswith('## '):
            html_parts.append(f'<h2>{html.escape(line[3:].strip())}</h2>')
            i += 1
            continue

        # Sub-headers (h3) - THIS WAS THE BUG
        if line.startswith('### '):
            html_parts.append(f'<h3>{html.escape(line[4:].strip())}</h3>')
            i += 1
            continue

        # FAQ Q&A
        if line.startswith('Q:') or line.startswith('Q '):
            current_q = line[2:].strip() if line.startswith('Q:') else line[2:].strip()
            html_parts.append(f'<div class="faq"><p class="q">{html.escape(line)}</p>')
            in_faq = True
            i += 1
            continue

        if line.startswith('A:') or line.startswith('A '):
            current_a = line[2:].strip() if line.startswith('A:') else line[2:].strip()
            html_parts.append(f'<p class="a">{html.escape(line)}</p>')
            i += 1
            while i < len(lines) and lines[i].strip().startswith('- '):
                bullet_text = lines[i].strip()[2:]
                current_a += ' ' + bullet_text
                html_parts.append(f'<p class="a">&nbsp;&nbsp;{html.escape(lines[i].strip())}</p>')
                i += 1
            if in_faq:
                if current_q and current_a:
                    faq_pairs.append((current_q, current_a))
                    current_q = None
                    current_a = None
                html_parts.append('</div>')
                in_faq = False
            continue

        # Numbered list items
        if re.match(r'^\d+\.', line):
            content = re.sub(r'^\d+\.\s*', '', line)
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            # Handle inline code
            content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)
            html_parts.append(f'<p>{content}</p>')
            i += 1
            continue

        # Bullet points
        if line.startswith('- '):
            content = line[2:]
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)
            html_parts.append(f'<p>&bull; {content}</p>')
            i += 1
            continue

        # Regular paragraph
        line_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        line_html = re.sub(r'`(.+?)`', r'<code>\1</code>', line_html)
        html_parts.append(f'<p>{line_html}</p>')
        i += 1

    if in_faq:
        if current_q and current_a:
            faq_pairs.append((current_q, current_a))
        html_parts.append('</div>')

    if not title:
        title = "Troubleshooting Guide"

    return title, '\n            '.join(html_parts), faq_pairs


def build_faq_schema(faq_pairs):
    """Generate FAQPage JSON-LD schema from Q&A pairs."""
    if not faq_pairs:
        return ""
    items = []
    for q, a in faq_pairs:
        q_escaped = html.escape(q).replace('"', '&quot;')
        a_escaped = html.escape(a).replace('"', '&quot;')
        items.append(f'''    {{
          "@type": "Question",
          "name": "{q_escaped}",
          "acceptedAnswer": {{
            "@type": "Answer",
            "text": "{a_escaped}"
          }}
        }}''')
    joined = ",\n".join(items)
    return f'''<script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
    {joined}
      ]
    }}
    </script>'''


os.makedirs(PAGES_DIR, exist_ok=True)

for filename in os.listdir(ARTICLES_DIR):
    if not filename.endswith('.md'):
        continue

    filepath = os.path.join(ARTICLES_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    title, html_content, faq_pairs = md_to_html(content)

    slug = filename.replace('.md', '')

    # Extract first paragraph for meta description — escape for HTML attributes
    lines = content.strip().split('\n')
    desc_line = ""
    for l in lines:
        l = l.strip()
        if l and not l.startswith('#') and not l.startswith('Title') and not l.lower().startswith('problem') and not l.lower().startswith('possible') and len(l) > 40:
            desc_line = l.replace('**', '').replace('*', '')[:155]
            break
    if not desc_line:
        desc_line = f"Troubleshooting guide for {title}. Step-by-step fixes, common causes, and FAQ."
    # Escape for use in HTML attribute values
    meta_description = html.escape(desc_line, quote=True)

    keywords = title.lower().replace('troubleshooting guide:', '').replace('troubleshooting', '').strip()
    meta_keywords = html.escape(f"{keywords}, fix, troubleshooting, how to fix, not working, error, solution", quote=True)

    # Clean title for breadcrumb (remove "Troubleshooting Guide:" prefix)
    breadcrumb_title = title.replace('Troubleshooting Guide: ', '').replace('Troubleshooting Guide:', '')

    faq_schema = build_faq_schema(faq_pairs)

    page_html = TEMPLATE.format(
        title=html.escape(title, quote=True),
        content=html_content,
        meta_description=meta_description,
        meta_keywords=meta_keywords,
        slug=slug,
        breadcrumb_title=html.escape(breadcrumb_title),
        faq_schema=faq_schema
    )

    out_filename = filename.replace('.md', '.html')
    out_path = os.path.join(PAGES_DIR, out_filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page_html)

    print(f"Built: {out_filename}")

print(f"\nDone! {len(os.listdir(PAGES_DIR))} pages generated.")
