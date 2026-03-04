"""Build script to convert markdown articles to HTML pages."""
import os
import re

ARTICLES_DIR = "articles"
PAGES_DIR = "pages"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - FixThatApp</title>
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
            padding: 1.5rem 1rem;
        }}
        header a {{ color: white; text-decoration: none; font-size: 1.5rem; font-weight: bold; }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        .back {{ display: inline-block; margin-bottom: 1.5rem; color: #667eea; text-decoration: none; font-weight: 500; }}
        .back:hover {{ text-decoration: underline; }}
        .article {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .article h1 {{ font-size: 1.8rem; color: #1a1a2e; margin-bottom: 1.5rem; }}
        .article h2 {{ font-size: 1.3rem; color: #333; margin: 1.5rem 0 0.75rem; padding-bottom: 0.3rem; border-bottom: 2px solid #f0f0f0; }}
        .article p {{ margin-bottom: 1rem; color: #444; }}
        .article ol, .article ul {{ margin: 0.5rem 0 1rem 1.5rem; color: #444; }}
        .article li {{ margin-bottom: 0.5rem; }}
        .article strong {{ color: #333; }}
        .faq {{ background: #f8f9ff; border-radius: 8px; padding: 1.25rem; margin-bottom: 0.75rem; }}
        .faq p {{ margin-bottom: 0.25rem; }}
        .faq .q {{ font-weight: 600; color: #333; }}
        .faq .a {{ color: #555; }}
        footer {{
            text-align: center;
            padding: 2rem 1rem;
            color: #999;
            font-size: 0.85rem;
        }}
        footer a {{ color: #667eea; text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <header><a href="../index.html">FixThatApp</a></header>
    <div class="container">
        <a class="back" href="../index.html">&larr; Back to all guides</a>
        <div class="article">
            {content}
        </div>
    </div>
    <footer>&copy; 2026 FixThatApp. All rights reserved. | <a href="../privacy-policy.html">Privacy Policy</a></footer>
</body>
</html>
"""

def md_to_html(text):
    """Simple markdown to HTML converter."""
    lines = text.strip().split('\n')
    html_parts = []
    title = ""
    in_faq = False
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            if in_faq:
                in_faq = False
                html_parts.append('</div>')
            i += 1
            continue

        # Extract title
        if line.startswith('# '):
            title = line[2:].strip()
            html_parts.append(f'<h1>{title}</h1>')
            i += 1
            continue

        if line.lower().startswith('title:'):
            title = line.split(':', 1)[1].strip()
            html_parts.append(f'<h1>{title}</h1>')
            i += 1
            continue

        if line.lower() == 'title':
            # Next line is the title
            i += 1
            if i < len(lines):
                title = lines[i].strip()
                html_parts.append(f'<h1>{title}</h1>')
            i += 1
            continue

        # Section headers
        if line.startswith('## '):
            html_parts.append(f'<h2>{line[3:].strip()}</h2>')
            i += 1
            continue

        # Detect section headers without markdown syntax
        section_keywords = ['Problem Description', 'Possible Causes', 'Step-by-step fixes',
                           'Step-by-step Fixes', 'When to Contact Support', 'When to contact support',
                           'FAQ', 'User Guide', 'Note']
        is_section = False
        for kw in section_keywords:
            if line.lower().replace(':', '').strip() == kw.lower() or \
               re.match(r'^\d+\.\s*' + re.escape(kw), line, re.IGNORECASE):
                clean = re.sub(r'^\d+\.\s*', '', line).rstrip(':')
                html_parts.append(f'<h2>{clean}</h2>')
                is_section = True
                break
        if is_section:
            i += 1
            continue

        # FAQ Q&A
        if line.startswith('Q:') or line.startswith('Q '):
            html_parts.append(f'<div class="faq"><p class="q">{line}</p>')
            in_faq = True
            i += 1
            continue

        if line.startswith('A:') or line.startswith('A '):
            html_parts.append(f'<p class="a">{line}</p>')
            # Collect continuation lines
            i += 1
            while i < len(lines) and lines[i].strip().startswith('- '):
                html_parts.append(f'<p class="a">&nbsp;&nbsp;{lines[i].strip()}</p>')
                i += 1
            if in_faq:
                html_parts.append('</div>')
                in_faq = False
            continue

        # Numbered list items
        if re.match(r'^\d+\.', line):
            content = re.sub(r'^\d+\.\s*', '', line)
            # Bold text
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            html_parts.append(f'<p>{content}</p>')
            i += 1
            continue

        # Bullet points
        if line.startswith('- '):
            content = line[2:]
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            html_parts.append(f'<p>&bull; {content}</p>')
            i += 1
            continue

        # Regular paragraph
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        html_parts.append(f'<p>{line}</p>')
        i += 1

    if in_faq:
        html_parts.append('</div>')

    if not title:
        title = "Troubleshooting Guide"

    return title, '\n            '.join(html_parts)


os.makedirs(PAGES_DIR, exist_ok=True)

for filename in os.listdir(ARTICLES_DIR):
    if not filename.endswith('.md'):
        continue

    filepath = os.path.join(ARTICLES_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    title, html_content = md_to_html(content)
    page_html = TEMPLATE.format(title=title, content=html_content)

    out_filename = filename.replace('.md', '.html')
    out_path = os.path.join(PAGES_DIR, out_filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page_html)

    print(f"Built: {out_filename}")

print(f"\nDone! {len(os.listdir(PAGES_DIR))} pages generated.")
