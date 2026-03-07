import os

ROOT = r"C:\Users\sufya\fixthatapp-ai"
BLOG = os.path.join(ROOT, "blog")

posts = [
    ("online-calculator", "online-calculator-guide", "Online Calculator Guide: Faster Daily Math Without App Installs", "Daily"),
    ("unit-converter", "unit-converter-guide", "Unit Converter Guide: Convert Length, Weight, Temp, and Speed Correctly", "Converter"),
    ("currency-converter", "currency-converter-guide", "Currency Converter Guide: Check Real-Time Exchange Estimates", "Finance"),
    ("bmi-calculator", "bmi-calculator-guide", "BMI Calculator Guide: Understand Your BMI Category in Seconds", "Health"),
    ("age-calculator", "age-calculator-guide", "Age Calculator Guide: Exact Years, Months, and Days", "Daily"),
    ("loan-emi-calculator", "loan-emi-calculator-guide", "Loan EMI Calculator Guide: Estimate Monthly Payments Clearly", "Finance"),
    ("tip-calculator", "tip-calculator-guide", "Tip Calculator Guide: Split Bills and Tips Instantly", "Daily"),
    ("qr-code-generator", "qr-code-generator-guide", "QR Code Generator Guide: Create Scan-Ready Codes Quickly", "Utility"),
    ("weather-checker", "weather-checker-guide", "Weather Checker Guide: Get Quick City Forecasts", "Weather"),
    ("time-zone-converter", "time-zone-converter-guide", "Time Zone Converter Guide: Schedule Across Countries", "Time"),
    ("word-counter", "word-counter-guide", "Word Counter Guide: Track Writing Length and Reading Time", "Writing"),
    ("image-resizer", "image-resizer-guide", "Image Resizer Guide: Resize Images Without Extra Software", "Image"),
    ("base64-encoder-decoder", "base64-encoder-decoder-guide", "Base64 Encoder Decoder Guide: Encode and Decode Text Safely", "Developer"),
    ("uuid-generator", "uuid-generator-guide", "UUID Generator Guide: Create Unique IDs for Apps and APIs", "Developer"),
    ("random-number-picker", "random-number-picker-guide", "Random Number Picker Guide: Fair Picks for Giveaways", "Utility"),
]

page_tpl = """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{title} | FixThatApp</title>
  <meta name=\"description\" content=\"Learn how to use {tool_name} effectively with practical examples and troubleshooting tips.\">
  <link rel=\"canonical\" href=\"https://www.fixthatapp.com/blog/{slug}.html\">
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
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fa;color:#333;line-height:1.7}}
    header{{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:1rem 1.5rem;display:flex;justify-content:space-between;align-items:center}}
    header a{{color:#fff;text-decoration:none;font-size:1.2rem;font-weight:700}}
    .container{{max-width:820px;margin:0 auto;padding:2rem 1rem}}
    .article{{background:#fff;border-radius:12px;padding:2rem;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
    h1{{font-size:1.6rem;margin-bottom:.4rem}}
    .muted{{font-size:.82rem;color:#888;margin-bottom:1rem}}
    h2{{font-size:1.15rem;margin:1.4rem 0 .6rem}}
    p{{margin-bottom:.85rem;color:#444}}
    ul,ol{{margin:.4rem 0 1rem 1.4rem;color:#444}}
    a{{color:#667eea;text-decoration:none}}
    .cta{{background:#eef2ff;border-left:4px solid #667eea;border-radius:8px;padding:1rem 1.2rem;margin:1rem 0}}
    footer{{text-align:center;padding:2rem 1rem;color:#999;font-size:.84rem;border-top:1px solid #e0e0e0}}
    footer a{{color:#667eea;text-decoration:none}}
  </style>
</head>
<body>
  <header><a href=\"../index.html\">FixThatApp</a><a href=\"./\">Blog</a></header>
  <div class=\"container\">
    <article class=\"article\">
      <h1>{title}</h1>
      <div class=\"muted\">Published March 7, 2026</div>
      <p>{tool_name} is one of the most searched day-to-day utility intents because users need fast answers without installing software. This guide helps you use it correctly and avoid common mistakes.</p>
      <h2>When to Use This Tool</h2>
      <ul>
        <li>You need quick results in browser.</li>
        <li>You want a no-signup workflow.</li>
        <li>You need cross-device access.</li>
      </ul>
      <h2>How to Use It</h2>
      <ol>
        <li>Open the tool page.</li>
        <li>Enter the required values.</li>
        <li>Run the action and verify the output.</li>
      </ol>
      <div class=\"cta\">Open tool: <a href=\"../tools/{tool_slug}/\">{tool_name}</a></div>
      <h2>Common Issues</h2>
      <p>If results look incorrect, check input format, unit assumptions, and decimal separators. Retry with fresh values and compare with a secondary source for critical use cases.</p>
      <h2>Related Resources</h2>
      <ul>
        <li><a href=\"../tools/\">All Tools</a></li>
        <li><a href=\"../all-guides.html\">All Troubleshooting Guides</a></li>
      </ul>
    </article>
  </div>
  <footer>&copy; 2026 FixThatApp | <a href=\"../privacy-policy.html\">Privacy Policy</a> | <a href=\"../cookie-policy.html\">Cookie Policy</a> | <a href=\"../tools/\">Tools</a></footer>
</body>
</html>
"""

for tool_slug, slug, title, tag in posts:
    tool_name = tool_slug.replace('-', ' ').title().replace('Emi', 'EMI').replace('Bmi', 'BMI').replace('Uuid', 'UUID').replace('Qr', 'QR').replace('Base64', 'Base64')
    path = os.path.join(BLOG, slug + ".html")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(page_tpl.format(title=title, tool_name=tool_name, tool_slug=tool_slug, slug=slug))

idx = os.path.join(BLOG, "index.html")
with open(idx, "r", encoding="utf-8") as f:
    content = f.read()

if "online-calculator-guide.html" not in content:
    cards = []
    for tool_slug, slug, title, tag in posts:
        cards.append(f'''            <a class="post" href="{slug}.html">\n                <span class="tag">{tag}</span>\n                <h2>{title}</h2>\n                <p>Practical usage guide with quick steps, mistakes to avoid, and direct links to the tool.</p>\n                <div class="meta">March 7, 2026</div>\n            </a>''')
    content = content.replace('<div class="post-list">', '<div class="post-list">\n' + '\n'.join(cards), 1)
    with open(idx, "w", encoding="utf-8") as f:
        f.write(content)

print("Generated daily-tools blog pack and updated blog index.")
