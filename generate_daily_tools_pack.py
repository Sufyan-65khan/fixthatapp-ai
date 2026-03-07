import os

ROOT = r"C:\Users\sufya\fixthatapp-ai"
TOOLS_DIR = os.path.join(ROOT, "tools")

TOOLS = [
    {
        "slug": "online-calculator",
        "title": "Online Calculator",
        "desc": "Fast calculator for daily math operations with percentage and memory-friendly workflow.",
        "tag": "Daily",
        "icon": "Calc",
        "input_html": """
            <div class=\"row\"><input id=\"expr\" placeholder=\"e.g. (125*4)+18%\" /><button class=\"btn\" onclick=\"calc()\">Calculate</button><button class=\"btn secondary\" onclick=\"clearAll()\">Clear</button></div>
            <div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function calc(){
                const v=(document.getElementById('expr').value||'').trim();
                if(!v){show('Enter a calculation expression.');return;}
                try{
                    const safe=v.replace(/[^0-9+\-*/().% ]/g,'');
                    const normalized=safe.replace(/(\d+(?:\.\d+)?)%/g,'($1/100)');
                    const out=Function('return ('+normalized+')')();
                    show('<strong>Result:</strong> '+out);
                }catch(e){show('Invalid expression.');}
            }
            function clearAll(){document.getElementById('expr').value='';hide();}
        """
    },
    {
        "slug": "unit-converter",
        "title": "Unit Converter",
        "desc": "Convert length, weight, temperature, and speed units instantly.",
        "tag": "Converter",
        "icon": "Unit",
        "input_html": """
            <div class=\"row\"><input id=\"num\" placeholder=\"Value\" /><select id=\"type\"><option value=\"length\">Length</option><option value=\"weight\">Weight</option><option value=\"temp\">Temperature</option><option value=\"speed\">Speed</option></select></div>
            <div class=\"row\"><select id=\"from\"></select><select id=\"to\"></select><button class=\"btn\" onclick=\"convert()\">Convert</button></div>
            <div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            const maps={
              length:{m:1,km:1000,cm:0.01,mm:0.001,mi:1609.344,ft:0.3048,in:0.0254},
              weight:{kg:1,g:0.001,lb:0.45359237,oz:0.0283495231},
              speed:{'m/s':1,'km/h':0.277777778,'mph':0.44704,'kn':0.514444},
            };
            const temp=['c','f','k'];
            function fill(){
              const t=document.getElementById('type').value;const f=document.getElementById('from');const to=document.getElementById('to');f.innerHTML='';to.innerHTML='';
              const vals=t==='temp'?temp:Object.keys(maps[t]);
              vals.forEach(v=>{f.innerHTML+=`<option value=\"${v}\">${v}</option>`;to.innerHTML+=`<option value=\"${v}\">${v}</option>`});
              to.selectedIndex=vals.length>1?1:0;
            }
            function t2c(v,u){if(u==='c')return v;if(u==='f')return (v-32)*5/9;return v-273.15}
            function c2t(v,u){if(u==='c')return v;if(u==='f')return v*9/5+32;return v+273.15}
            function convert(){
              const n=parseFloat(document.getElementById('num').value); if(Number.isNaN(n)){show('Enter a valid number.');return;}
              const t=document.getElementById('type').value,fr=document.getElementById('from').value,to=document.getElementById('to').value;
              let out;
              if(t==='temp'){out=c2t(t2c(n,fr),to);} else {out=n*maps[t][fr]/maps[t][to];}
              show(`<strong>${n} ${fr}</strong> = <strong>${out.toFixed(6).replace(/\\.?0+$/,'')} ${to}</strong>`);
            }
            document.getElementById('type').addEventListener('change',fill);fill();
        """
    },
    {
        "slug": "currency-converter",
        "title": "Currency Converter",
        "desc": "Live currency conversion using daily exchange rates for major world currencies.",
        "tag": "Finance",
        "icon": "FX",
        "input_html": """
            <div class=\"row\"><input id=\"amt\" placeholder=\"Amount\" value=\"1\" /><select id=\"from\"></select><select id=\"to\"></select><button class=\"btn\" onclick=\"convertFx()\">Convert</button></div>
            <div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            const cc=['USD','EUR','GBP','INR','JPY','AUD','CAD','SGD','AED','CNY'];
            const f=document.getElementById('from'),t=document.getElementById('to');
            cc.forEach(c=>{f.innerHTML+=`<option>${c}</option>`;t.innerHTML+=`<option>${c}</option>`});
            f.value='USD';t.value='INR';
            async function convertFx(){
              const amt=parseFloat(document.getElementById('amt').value); if(Number.isNaN(amt)){show('Enter a valid amount.');return;}
              const from=f.value,to=t.value;
              try{
                const r=await fetch(`https://open.er-api.com/v6/latest/${from}`).then(x=>x.json());
                if(!r.rates||!r.rates[to]){show('Rate unavailable right now.');return;}
                const out=amt*r.rates[to];
                show(`<strong>${amt} ${from}</strong> = <strong>${out.toFixed(4)} ${to}</strong><br><small>Rates source: open.er-api.com</small>`);
              }catch(e){show('Unable to fetch exchange rates now.');}
            }
        """
    },
    {
        "slug": "bmi-calculator",
        "title": "BMI Calculator",
        "desc": "Body Mass Index calculator with health category output.",
        "tag": "Health",
        "icon": "BMI",
        "input_html": """
            <div class=\"row\"><input id=\"w\" placeholder=\"Weight (kg)\" /><input id=\"h\" placeholder=\"Height (cm)\" /><button class=\"btn\" onclick=\"bmi()\">Calculate BMI</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function bmi(){
              const w=parseFloat(document.getElementById('w').value), h=parseFloat(document.getElementById('h').value);
              if(Number.isNaN(w)||Number.isNaN(h)||h<=0){show('Enter valid weight and height.');return;}
              const v=w/((h/100)*(h/100));
              let cat='Obese'; if(v<18.5)cat='Underweight'; else if(v<25)cat='Normal'; else if(v<30)cat='Overweight';
              show(`<strong>BMI:</strong> ${v.toFixed(2)} (${cat})`);
            }
        """
    },
    {
        "slug": "age-calculator",
        "title": "Age Calculator",
        "desc": "Calculate exact age in years, months, and days from date of birth.",
        "tag": "Daily",
        "icon": "Age",
        "input_html": """
            <div class=\"row\"><input id=\"dob\" type=\"date\" /><button class=\"btn\" onclick=\"ageCalc()\">Calculate Age</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function ageCalc(){
              const dob=document.getElementById('dob').value; if(!dob){show('Select date of birth.');return;}
              const b=new Date(dob), t=new Date();
              let y=t.getFullYear()-b.getFullYear(), m=t.getMonth()-b.getMonth(), d=t.getDate()-b.getDate();
              if(d<0){m--; d+=new Date(t.getFullYear(),t.getMonth(),0).getDate();}
              if(m<0){y--; m+=12;}
              show(`<strong>${y}</strong> years, <strong>${m}</strong> months, <strong>${d}</strong> days`);
            }
        """
    },
    {
        "slug": "loan-emi-calculator",
        "title": "Loan EMI Calculator",
        "desc": "Compute monthly EMI for loans using principal, interest rate, and tenure.",
        "tag": "Finance",
        "icon": "EMI",
        "input_html": """
            <div class=\"row\"><input id=\"p\" placeholder=\"Principal\" /><input id=\"r\" placeholder=\"Annual Interest %\" /><input id=\"n\" placeholder=\"Tenure (months)\" /><button class=\"btn\" onclick=\"emi()\">Calculate EMI</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function emi(){
              const P=parseFloat(p.value), annual=parseFloat(r.value), n=parseInt(document.getElementById('n').value,10);
              if(Number.isNaN(P)||Number.isNaN(annual)||Number.isNaN(n)||n<=0){show('Enter valid loan details.');return;}
              const R=(annual/12)/100;
              const e=(P*R*Math.pow(1+R,n))/(Math.pow(1+R,n)-1);
              const total=e*n, interest=total-P;
              show(`<strong>EMI:</strong> ${e.toFixed(2)}<br><strong>Total Interest:</strong> ${interest.toFixed(2)}<br><strong>Total Payment:</strong> ${total.toFixed(2)}`);
            }
        """
    },
    {
        "slug": "tip-calculator",
        "title": "Tip Calculator",
        "desc": "Calculate tip and split bill amount quickly for restaurants and services.",
        "tag": "Daily",
        "icon": "Tip",
        "input_html": """
            <div class=\"row\"><input id=\"bill\" placeholder=\"Bill amount\" /><input id=\"tip\" placeholder=\"Tip %\" value=\"10\" /><input id=\"people\" placeholder=\"People\" value=\"1\" /><button class=\"btn\" onclick=\"tipCalc()\">Calculate</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function tipCalc(){
              const b=parseFloat(bill.value), t=parseFloat(tip.value), p=Math.max(1,parseInt(people.value||'1',10));
              if(Number.isNaN(b)||Number.isNaN(t)){show('Enter valid bill and tip.');return;}
              const tipAmt=b*t/100, total=b+tipAmt;
              show(`<strong>Tip:</strong> ${tipAmt.toFixed(2)}<br><strong>Total:</strong> ${total.toFixed(2)}<br><strong>Per person:</strong> ${(total/p).toFixed(2)}`);
            }
        """
    },
    {
        "slug": "qr-code-generator",
        "title": "QR Code Generator",
        "desc": "Create downloadable QR codes for links, text, phone numbers, and more.",
        "tag": "Utility",
        "icon": "QR",
        "input_html": """
            <div class=\"row\"><input id=\"qtext\" placeholder=\"Enter text or URL\" /><button class=\"btn\" onclick=\"makeQr()\">Generate QR</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function makeQr(){
              const v=(qtext.value||'').trim(); if(!v){show('Enter text or URL.');return;}
              const src='https://api.qrserver.com/v1/create-qr-code/?size=240x240&data='+encodeURIComponent(v);
              show(`<img src=\"${src}\" alt=\"QR code\" width=\"240\" height=\"240\" style=\"border-radius:8px;background:#fff;padding:8px\"/><br><a href=\"${src}\" target=\"_blank\" rel=\"noopener\">Open / Download QR</a>`);
            }
        """
    },
    {
        "slug": "weather-checker",
        "title": "Weather Checker",
        "desc": "Check current weather and temperature for any city worldwide.",
        "tag": "Weather",
        "icon": "Wx",
        "input_html": """
            <div class=\"row\"><input id=\"city\" placeholder=\"Enter city (e.g. New York)\" /><button class=\"btn\" onclick=\"weather()\">Get Weather</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            async function weather(){
              const c=(city.value||'').trim(); if(!c){show('Enter a city name.');return;}
              try{
                const g=await fetch('https://geocoding-api.open-meteo.com/v1/search?name='+encodeURIComponent(c)+'&count=1').then(r=>r.json());
                if(!g.results||!g.results.length){show('City not found.');return;}
                const x=g.results[0];
                const w=await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${x.latitude}&longitude=${x.longitude}&current=temperature_2m,weather_code,wind_speed_10m`).then(r=>r.json());
                const cur=w.current||{};
                show(`<strong>${x.name}, ${x.country||''}</strong><br>Temperature: ${cur.temperature_2m}°C<br>Wind: ${cur.wind_speed_10m} km/h<br><small>Data source: Open-Meteo</small>`);
              }catch(e){show('Weather lookup failed right now.');}
            }
        """
    },
    {
        "slug": "time-zone-converter",
        "title": "Time Zone Converter",
        "desc": "Convert date and time between major global time zones instantly.",
        "tag": "Time",
        "icon": "TZ",
        "input_html": """
            <div class=\"row\"><input id=\"dt\" type=\"datetime-local\" /><select id=\"from\"></select><select id=\"to\"></select><button class=\"btn\" onclick=\"tz()\">Convert</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            const zones=['UTC','America/New_York','Europe/London','Europe/Berlin','Asia/Kolkata','Asia/Dubai','Asia/Singapore','Asia/Tokyo','Australia/Sydney'];
            zones.forEach(z=>{from.innerHTML+=`<option value=\"${z}\">${z}</option>`;to.innerHTML+=`<option value=\"${z}\">${z}</option>`});
            from.value='UTC';to.value='Asia/Kolkata';
            function tz(){
              const v=dt.value; if(!v){show('Pick date and time.');return;}
              const d=new Date(v);
              const fmt=(z)=>new Intl.DateTimeFormat('en-US',{dateStyle:'full',timeStyle:'long',timeZone:z}).format(d);
              show(`<strong>${from.value}:</strong> ${fmt(from.value)}<br><strong>${to.value}:</strong> ${fmt(to.value)}`);
            }
        """
    },
    {
        "slug": "word-counter",
        "title": "Word Counter",
        "desc": "Count words, characters, sentences, and reading time for any text.",
        "tag": "Writing",
        "icon": "Txt",
        "input_html": """
            <div class=\"row\"><textarea id=\"txt\" placeholder=\"Paste text here...\"></textarea></div><div class=\"row\"><button class=\"btn\" onclick=\"countText()\">Analyze Text</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function countText(){
              const t=(txt.value||'').trim();
              if(!t){show('Paste text to analyze.');return;}
              const words=t.split(/\\s+/).filter(Boolean).length;
              const chars=t.length;
              const charsNo=t.replace(/\\s/g,'').length;
              const sent=(t.match(/[.!?]+/g)||[]).length||1;
              const mins=Math.max(1,Math.ceil(words/200));
              show(`<strong>Words:</strong> ${words}<br><strong>Characters:</strong> ${chars}<br><strong>Characters (no spaces):</strong> ${charsNo}<br><strong>Sentences:</strong> ${sent}<br><strong>Estimated reading time:</strong> ${mins} min`);
            }
        """
    },
    {
        "slug": "image-resizer",
        "title": "Image Resizer",
        "desc": "Resize images in-browser and download optimized versions quickly.",
        "tag": "Image",
        "icon": "Img",
        "input_html": """
            <div class=\"row\"><input id=\"imgFile\" type=\"file\" accept=\"image/*\" /><input id=\"w\" placeholder=\"Width\" /><input id=\"h\" placeholder=\"Height\" /><button class=\"btn\" onclick=\"resizeImg()\">Resize</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function resizeImg(){
              const f=imgFile.files&&imgFile.files[0]; if(!f){show('Choose an image first.');return;}
              const W=parseInt(document.getElementById('w').value,10), H=parseInt(document.getElementById('h').value,10);
              if(!W||!H){show('Enter output width and height.');return;}
              const reader=new FileReader();
              reader.onload=()=>{
                const im=new Image(); im.onload=()=>{
                  const c=document.createElement('canvas'); c.width=W; c.height=H;
                  const ctx=c.getContext('2d'); ctx.drawImage(im,0,0,W,H);
                  const out=c.toDataURL('image/jpeg',0.9);
                  show(`<img src=\"${out}\" style=\"max-width:100%;border-radius:8px\"/><br><a href=\"${out}\" download=\"resized.jpg\">Download resized image</a>`);
                }; im.src=reader.result;
              };
              reader.readAsDataURL(f);
            }
        """
    },
    {
        "slug": "base64-encoder-decoder",
        "title": "Base64 Encoder Decoder",
        "desc": "Encode and decode Base64 text directly in your browser.",
        "tag": "Developer",
        "icon": "B64",
        "input_html": """
            <div class=\"row\"><textarea id=\"txt\" placeholder=\"Enter text or Base64...\"></textarea></div><div class=\"row\"><button class=\"btn\" onclick=\"enc()\">Encode</button><button class=\"btn\" onclick=\"dec()\">Decode</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function enc(){try{show('<strong>Encoded:</strong><br><code>'+btoa(unescape(encodeURIComponent(txt.value||'')))+'</code>');}catch(e){show('Unable to encode input.');}}
            function dec(){try{show('<strong>Decoded:</strong><br><code>'+escapeHtml(decodeURIComponent(escape(atob(txt.value||''))))+'</code>');}catch(e){show('Invalid Base64 input.');}}
        """
    },
    {
        "slug": "uuid-generator",
        "title": "UUID Generator",
        "desc": "Generate v4 UUIDs instantly for apps, APIs, and databases.",
        "tag": "Developer",
        "icon": "UUID",
        "input_html": """
            <div class=\"row\"><input id=\"count\" placeholder=\"Count\" value=\"5\" /><button class=\"btn\" onclick=\"gen()\">Generate UUIDs</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function u(){return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,c=>{const r=Math.random()*16|0,v=c=='x'?r:(r&0x3|0x8);return v.toString(16);});}
            function gen(){
              const n=Math.min(100,Math.max(1,parseInt(count.value||'5',10)||5));
              let out=''; for(let i=0;i<n;i++) out+=u()+'<br>';
              show(out);
            }
        """
    },
    {
        "slug": "random-number-picker",
        "title": "Random Number Picker",
        "desc": "Generate random numbers in custom ranges for giveaways and decisions.",
        "tag": "Utility",
        "icon": "Rnd",
        "input_html": """
            <div class=\"row\"><input id=\"min\" placeholder=\"Min\" value=\"1\" /><input id=\"max\" placeholder=\"Max\" value=\"100\" /><input id=\"count\" placeholder=\"Count\" value=\"1\" /><button class=\"btn\" onclick=\"pick()\">Pick</button></div><div id=\"result\" class=\"result\"></div>
        """,
        "script": """
            function pick(){
              const minV=parseInt(min.value,10), maxV=parseInt(max.value,10), c=Math.min(100,Math.max(1,parseInt(count.value||'1',10)));
              if(Number.isNaN(minV)||Number.isNaN(maxV)||maxV<minV){show('Invalid range.');return;}
              const arr=[]; for(let i=0;i<c;i++) arr.push(Math.floor(Math.random()*(maxV-minV+1))+minV);
              show('<strong>Result:</strong> '+arr.join(', '));
            }
        """
    }
]

PAGE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{title} - Free Online Tool | FixThatApp</title>
  <meta name=\"description\" content=\"{desc}\" />
  <meta name=\"keywords\" content=\"{title_l}, online tool, free tool, fixthatapp\" />
  <link rel=\"canonical\" href=\"https://www.fixthatapp.com/tools/{slug}/\" />
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
    :root{{--bg:#f5f7fa;--card:#fff;--text:#333;--muted:#777;--accent:#667eea;--border:#e0e0e0;--input-bg:#f8f9ff}}
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh;display:flex;flex-direction:column}}
    header{{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:1rem 1.5rem;display:flex;align-items:center;justify-content:space-between}}
    header a{{color:#fff;text-decoration:none;font-size:1.2rem;font-weight:700}}
    .container{{max-width:930px;margin:0 auto;padding:1.5rem 1rem;flex:1;width:100%}}
    .breadcrumb{{font-size:.85rem;color:var(--muted);margin-bottom:1rem}}
    .breadcrumb a{{color:var(--accent);text-decoration:none}}
    .card{{background:var(--card);border-radius:12px;padding:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.08);margin-bottom:1rem}}
    .badge{{display:inline-block;font-size:.72rem;background:var(--input-bg);color:var(--accent);padding:.2rem .6rem;border-radius:999px;font-weight:600;margin-bottom:.5rem}}
    h1{{font-size:1.55rem;margin-bottom:.35rem}}
    .subtitle{{color:var(--muted);margin-bottom:1rem}}
    .row{{display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.5rem}}
    input,select,textarea{{flex:1;min-width:180px;padding:.72rem .9rem;border:2px solid var(--border);border-radius:8px;font-size:.95rem;background:var(--input-bg);color:var(--text)}}
    textarea{{min-height:140px;resize:vertical}}
    .btn{{padding:.72rem 1rem;background:var(--accent);color:#fff;border:none;border-radius:8px;font-weight:600;cursor:pointer}}
    .btn.secondary{{background:#fff;color:var(--accent);border:2px solid var(--accent)}}
    .result{{margin-top:.6rem;background:var(--input-bg);border-radius:8px;padding:1rem;display:none;overflow:auto}}
    .result.show{{display:block}}
    .tip{{background:#fff;border-radius:12px;padding:1.1rem;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
    .tip h2{{font-size:1.05rem;margin-bottom:.5rem}}
    .tip ul{{margin-left:1.2rem;color:#444}}
    .tip li{{margin-bottom:.35rem}}
    footer{{text-align:center;padding:1.5rem;color:#999;font-size:.82rem;border-top:1px solid var(--border)}}
    footer a{{color:var(--accent);text-decoration:none}}
    .cookie-banner{{position:fixed;left:1rem;right:1rem;bottom:1rem;background:#1a1a2e;color:#fff;padding:.85rem 1rem;border-radius:10px;display:none;align-items:center;justify-content:space-between;gap:.8rem;z-index:2000;box-shadow:0 8px 24px rgba(0,0,0,.25);font-size:.85rem}}
    .cookie-banner a{{color:#9ec2ff}}
    .cookie-actions{{display:flex;gap:.5rem;flex-shrink:0}}
    .cookie-btn{{border:1px solid #667eea;background:transparent;color:#fff;padding:.35rem .65rem;border-radius:6px;cursor:pointer;font-size:.8rem}}
    .cookie-btn.primary{{background:#667eea}}
    @media(max-width:700px){{.row{{flex-direction:column}}.btn{{width:100%}}}}
  </style>
</head>
<body>
  <header><a href=\"../../index.html\">FixThatApp</a><a href=\"../\">All Tools</a></header>
  <div class=\"container\">
    <nav class=\"breadcrumb\"><a href=\"../../index.html\">Home</a> &rsaquo; <a href=\"../index.html\">Tools</a> &rsaquo; {title}</nav>
    <div class=\"card\">
      <span class=\"badge\">{tag}</span>
      <h1>{title}</h1>
      <p class=\"subtitle\">{desc}</p>
      {input_html}
    </div>
    <div class=\"tip\">
      <h2>Quick Usage Tips</h2>
      <ul>
        <li>Use realistic values to get accurate outputs.</li>
        <li>Retry from another browser if a request-based tool fails.</li>
        <li>For critical decisions, verify results with official sources.</li>
      </ul>
    </div>
  </div>
  <footer>&copy; 2026 FixThatApp | <a href=\"../../about.html\">About</a> | <a href=\"../../privacy-policy.html\">Privacy Policy</a> | <a href=\"../../cookie-policy.html\">Cookie Policy</a> | <a href=\"../../contact.html\">Contact</a></footer>
  <div class=\"cookie-banner\" id=\"cookieBanner\">
    <span>We use cookies for ads and core site functions. <a href=\"../../cookie-policy.html\">Cookie Policy</a></span>
    <div class=\"cookie-actions\">
      <button class=\"cookie-btn\" id=\"cookieReject\">Reject</button>
      <button class=\"cookie-btn primary\" id=\"cookieAccept\">Accept</button>
    </div>
  </div>
  <script>
    function escapeHtml(str){{return String(str||'').replace(/[&<>\"']/g,m=>({{'&':'&amp;','<':'&lt;','>':'&gt;','\\"':'&quot;',"'":'&#39;'}}[m]));}}
    function show(html){{const e=document.getElementById('result');e.innerHTML=html;e.classList.add('show');}}
    function hide(){{const e=document.getElementById('result');e.classList.remove('show');e.innerHTML='';}}
    {script}
    (function() {{
      var key='fta_cookie_consent';
      var banner=document.getElementById('cookieBanner');
      var acceptBtn=document.getElementById('cookieAccept');
      var rejectBtn=document.getElementById('cookieReject');
      if (!banner || !acceptBtn || !rejectBtn) return;
      var saved=null; try{{saved=localStorage.getItem(key);}}catch(e){{}}
      if(!saved) banner.style.display='flex';
      acceptBtn.addEventListener('click',function(){{try{{localStorage.setItem(key,'accepted');}}catch(e){{}} banner.style.display='none';}});
      rejectBtn.addEventListener('click',function(){{try{{localStorage.setItem(key,'rejected');}}catch(e){{}} window.adsbygoogle=window.adsbygoogle||[]; window.adsbygoogle.requestNonPersonalizedAds=1; banner.style.display='none';}});
    }})();
  </script>
</body>
</html>
"""

for t in TOOLS:
    d = os.path.join(TOOLS_DIR, t["slug"])
    os.makedirs(d, exist_ok=True)
    out = PAGE.format(
        title=t["title"],
        desc=t["desc"],
        title_l=t["title"].lower(),
        slug=t["slug"],
        tag=t["tag"],
        input_html=t["input_html"],
        script=t["script"],
    )
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)

# Update tools index section
idx = os.path.join(TOOLS_DIR, "index.html")
with open(idx, "r", encoding="utf-8") as f:
    content = f.read()

if "Most Used Daily Tools" not in content:
    cards = []
    for t in TOOLS:
        cards.append(f'''            <a class="card" href="{t["slug"]}/">\n                <div class="card-icon">{t["icon"]}</div>\n                <h2>{t["title"]}</h2>\n                <p>{t["desc"]}</p>\n                <span class="tag">{t["tag"]}</span>\n            </a>''')
    section = "\n\n        <h2 class=\"section-title\">Most Used Daily Tools</h2>\n        <div class=\"grid\">\n" + "\n".join(cards) + "\n        </div>\n"
    content = content.replace('<h2 class="section-title">Developer Tools</h2>', section + '\n        <h2 class="section-title">Developer Tools</h2>', 1)
    with open(idx, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Generated {len(TOOLS)} daily-use tools and updated tools index.")
