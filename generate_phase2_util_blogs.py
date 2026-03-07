import os

ROOT = r"C:\Users\sufya\fixthatapp-ai"
BLOG = os.path.join(ROOT, "blog")

TOOLS = [
"percentage-calculator","discount-calculator","tax-calculator","gst-calculator","profit-margin-calculator","loan-interest-calculator","sip-calculator","compound-interest-calculator","age-in-days-calculator","date-difference-calculator","countdown-timer-online","pomodoro-timer","timezone-meeting-planner","unix-timestamp-converter","json-to-csv-converter","csv-to-json-converter","markdown-to-html-converter","html-to-markdown-converter","url-encoder-decoder","html-entity-encoder-decoder","jwt-decoder","hash-generator","password-strength-checker","lorem-ipsum-generator","slug-generator","meta-tag-generator","robots-txt-generator","sitemap-url-list-cleaner","text-diff-checker","duplicate-line-remover","line-sorter","whitespace-cleaner","number-to-words-converter","random-password-list-generator","color-code-converter","gradient-generator","css-minifier","js-minifier","html-minifier","word-frequency-counter"
]

TPL = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>__TITLE__ Guide | FixThatApp</title>
  <meta name="description" content="Learn how to use __TITLE__ with practical examples and troubleshooting tips.">
  <link rel="canonical" href="https://www.fixthatapp.com/blog/__SLUG__.html">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3140312947507954" crossorigin="anonymous"></script>
  <style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fa;color:#333;line-height:1.7}header{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:1rem 1.5rem;display:flex;justify-content:space-between;align-items:center}header a{color:#fff;text-decoration:none;font-size:1.2rem;font-weight:700}.container{max-width:820px;margin:0 auto;padding:2rem 1rem}.article{background:#fff;border-radius:12px;padding:2rem;box-shadow:0 2px 8px rgba(0,0,0,.08)}h1{font-size:1.6rem;margin-bottom:.4rem}.muted{font-size:.82rem;color:#888;margin-bottom:1rem}h2{font-size:1.15rem;margin:1.4rem 0 .6rem}p{margin-bottom:.85rem;color:#444}ul,ol{margin:.4rem 0 1rem 1.4rem;color:#444}.cta{background:#eef2ff;border-left:4px solid #667eea;border-radius:8px;padding:1rem 1.2rem;margin:1rem 0}a{color:#667eea;text-decoration:none}footer{text-align:center;padding:2rem 1rem;color:#999;font-size:.84rem;border-top:1px solid #e0e0e0}</style>
</head>
<body>
  <header><a href="../index.html">FixThatApp</a><a href="./">Blog</a></header>
  <div class="container"><article class="article">
    <h1>__TITLE__ Guide</h1><div class="muted">Published March 7, 2026</div>
    <p>__TITLE__ is a high-frequency utility intent in day-to-day workflows. This quick guide helps you use it effectively and avoid common mistakes.</p>
    <h2>Best Use Cases</h2>
    <ul><li>Fast browser-based execution with no app install.</li><li>Quick validation and reference checks.</li><li>Repeat tasks in daily work, study, or business operations.</li></ul>
    <h2>How to Use</h2>
    <ol><li>Open the tool page.</li><li>Enter clean input values.</li><li>Run and verify output.</li></ol>
    <div class="cta">Open tool: <a href="../tools/__TOOL__/">__TITLE__</a></div>
    <h2>Troubleshooting</h2>
    <p>If output seems wrong, check formatting (decimals, units, separators), retry with simplified input, and validate with a secondary trusted source when needed.</p>
    <h2>Related</h2>
    <ul><li><a href="../tools/">All Tools</a></li><li><a href="../all-guides.html">All Guides Directory</a></li></ul>
  </article></div>
  <footer>&copy; 2026 FixThatApp | <a href="../privacy-policy.html">Privacy Policy</a> | <a href="../cookie-policy.html">Cookie Policy</a> | <a href="../tools/">Tools</a></footer>
</body>
</html>
'''

cards = []
for tool in TOOLS:
    slug = tool + "-guide"
    title = tool.replace('-', ' ').title().replace('Gst','GST').replace('Sip','SIP').replace('Jwt','JWT').replace('Txt','TXT').replace('Url','URL').replace('Json','JSON').replace('Csv','CSV').replace('Html','HTML').replace('Css','CSS').replace('Js','JS')
    path = os.path.join(BLOG, slug + ".html")
    if not os.path.exists(path):
        page = TPL.replace('__TITLE__', title).replace('__SLUG__', slug).replace('__TOOL__', tool)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(page)
    cards.append(f'''            <a class="post" href="{slug}.html">\n                <span class="tag">Utility</span>\n                <h2>{title} Guide</h2>\n                <p>Practical usage guide with direct tool access and troubleshooting steps.</p>\n                <div class="meta">March 7, 2026</div>\n            </a>''')

idx = os.path.join(BLOG, 'index.html')
with open(idx, 'r', encoding='utf-8') as f:
    content = f.read()
if 'percentage-calculator-guide.html' not in content:
    content = content.replace('<div class="post-list">', '<div class="post-list">\n' + '\n'.join(cards), 1)
    with open(idx, 'w', encoding='utf-8') as f:
        f.write(content)

print('Generated phase-2 utility blog pages and updated blog index.')
