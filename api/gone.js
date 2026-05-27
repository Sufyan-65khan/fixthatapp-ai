export default function handler(req, res) {
  res.statusCode = 410;
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.end(`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="robots" content="noindex,nofollow">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>410 Gone | FixThatApp</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f7fa;color:#333;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;padding:1rem}
    .card{background:#fff;max-width:540px;padding:2rem 2.5rem;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.08);text-align:center}
    h1{font-size:1.5rem;margin:0 0 .75rem;color:#1a1a2e}
    p{line-height:1.6;color:#555;margin:.5rem 0}
    a{color:#667eea;text-decoration:none;font-weight:600}
    a:hover{text-decoration:underline}
  </style>
</head>
<body>
  <div class="card">
    <h1>This page has been removed</h1>
    <p>The guide you were looking for is no longer available. We removed it during a site cleanup.</p>
    <p><a href="/">Browse current troubleshooting guides</a></p>
  </div>
</body>
</html>`);
}
