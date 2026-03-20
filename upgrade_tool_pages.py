#!/usr/bin/env python3
"""
upgrade_tool_pages.py
Replaces the generic 3-bullet tip section on every tool page with
unique, tool-specific supporting content (300-400 words each).
"""

import os
import re

TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")

# Map: folder name -> (badge_label, what_it_does, how_to_use_steps, faq_pairs, blog_slug)
TOOL_CONTENT = {
    "gst-calculator": (
        "Finance",
        "The GST Calculator handles both directions of Goods and Services Tax arithmetic. Enter a net (pre-tax) price and a GST rate to get the tax-inclusive total. Or enter a gross (tax-inclusive) price to extract the GST component and the original net price. The formula for adding GST is <code>Gross = Net × (1 + Rate/100)</code>. To remove GST from an inclusive price, divide by <code>(1 + Rate/100)</code> — never subtract the percentage directly, which is the most common mistake.",
        [
            "Enter the price in field A (net price if adding GST, gross price if removing GST).",
            "Enter the GST rate in field B — common rates are 5%, 12%, 18%, and 28% for India; 10% for Australia; 15% for New Zealand.",
            "Click Run. The result shows the GST amount and the final inclusive or exclusive price.",
            "For Indian users: choose the correct slab (5% for packaged food, 18% for most services, 28% for luxury goods).",
        ],
        [
            ("What is the difference between GST-inclusive and GST-exclusive?",
             "GST-exclusive (net) price is the base price before tax. GST-inclusive (gross) price already contains the tax. On an invoice, you add GST to the net price. When a customer asks for the pre-tax price of an inclusive amount, you divide by (1 + rate)."),
            ("Why can't I just subtract 10% from the gross to get the net?",
             "Because GST is calculated on the net price, not the gross. On a $110 inclusive price at 10% GST, the net is $100 — not $110 − $11 = $99. The correct formula is $110 ÷ 1.10 = $100."),
            ("Does India have a single GST rate?",
             "No. India uses a multi-slab GST system: 0% (fresh produce, essentials), 5% (packaged food, small restaurants), 12% (processed food, computers), 18% (most manufactured goods, services), and 28% (luxury goods, tobacco, automobiles)."),
        ],
        "gst-calculator-guide.html",
    ),

    "percentage-calculator": (
        "Utility",
        "The Percentage Calculator solves six common percentage problems without requiring you to remember formulas. It calculates what percentage one number is of another (e.g. 45 is what % of 180?), finds a percentage of a given number (e.g. 15% of 340), calculates percentage increase or decrease between two values, reverses a percentage change to find the original value, and computes the percentage difference between two numbers. Percentages are fundamental to finance, statistics, academic scoring, and everyday decisions — this tool removes the mental arithmetic barrier.",
        [
            "Select the calculation type using the tabs or mode selector.",
            "Enter value A (typically the part or the new value) and value B (the whole or the original value).",
            "Click Run. The result shows the answer along with the formula used.",
            "For percentage change: A is the new value, B is the old value. A positive result means increase; negative means decrease.",
        ],
        [
            ("What is the difference between percentage change and percentage difference?",
             "Percentage change measures how a value changed over time (old→new) and has a direction (increase or decrease). Percentage difference compares two values with no time component and uses their average as the base — it is always positive."),
            ("Why does a 50% increase followed by a 50% decrease not return to the original?",
             "Because each percentage applies to a different base. Start with 100: +50% gives 150, then −50% of 150 gives 75. The net result is a 25% loss from the original. Percentage movements are multiplicative, not additive."),
            ("How do I find the original price before a discount?",
             "If an item costs $63 after a 30% discount, the original price is $63 ÷ (1 − 0.30) = $90. Use the 'reverse percentage' mode in this calculator."),
        ],
        "percentage-calculator-guide.html",
    ),

    "compound-interest-calculator": (
        "Finance",
        "The Compound Interest Calculator projects how an investment grows when interest is calculated on both the original principal and the accumulated interest from prior periods. Unlike simple interest (which only earns on the principal), compound interest produces exponential growth over time. The formula is <code>A = P × (1 + r/n)^(n×t)</code> where P is the principal, r is the annual rate, n is the compounding frequency per year, and t is the time in years. This calculator is essential for retirement planning, savings projections, and understanding loan costs.",
        [
            "Enter the principal (initial investment or loan balance) in field A.",
            "Enter the annual interest rate as a percentage (e.g. enter 8 for 8%) in field B.",
            "The calculator defaults to a 10-year projection with annual compounding — adjust these in the settings.",
            "Compare different compounding frequencies (monthly vs annually) to see how frequency affects total return.",
        ],
        [
            ("How does compounding frequency affect the final amount?",
             "More frequent compounding produces slightly higher returns. At 8% annual rate on $10,000 for 10 years: annual compounding gives $21,589; monthly gives $22,196; daily gives $22,253. The rate matters far more than frequency."),
            ("What is the Rule of 72?",
             "Divide 72 by the annual interest rate to estimate the years needed to double your investment. At 8% annual return, 72 ÷ 8 = 9 years. At 6%, it doubles in roughly 12 years."),
            ("Does this calculator work for loan balances?",
             "Yes. A credit card balance at 20% annual interest compounded monthly will nearly triple in 6 years without payments. The same math that grows investments works against you on high-interest debt."),
        ],
        "compound-interest-calculator-guide.html",
    ),

    "discount-calculator": (
        "Finance",
        "The Discount Calculator solves three retail and pricing scenarios: finding the sale price when you know the original price and discount percentage; finding what discount percentage was applied when you know both prices; and working backwards to find the original price from a discounted price and discount rate. It also handles stacked discounts — where a 20% member discount is applied on top of a 30% sale — which cannot be added together (a 20% then 30% stack equals 44% combined, not 50%).",
        [
            "Enter the original price in field A.",
            "Enter the discount percentage in field B (e.g. enter 25 for 25% off).",
            "Click Run to see the sale price and the amount saved.",
            "To find the original price from a sale price: enter the sale price in A and the known discount % in B, then use reverse mode.",
        ],
        [
            ("Why can't I add two discounts together?",
             "Stacked discounts apply sequentially, each to a different base. A 30% sale then a 20% member discount on $100: first gives $70, then 20% off $70 gives $56. The combined discount is 44%, not 50%."),
            ("Is a percentage-off coupon always better than a fixed-amount coupon?",
             "It depends on the price. A 20% off coupon beats a $20 off coupon when the item costs more than $100. Below $100, $20 off wins. At exactly $100, they are equal."),
            ("How do I find the original price if I only know the sale price?",
             "Use Original = Sale Price ÷ (1 − Discount/100). If an item is $63 after 30% off: $63 ÷ 0.70 = $90 original price."),
        ],
        "discount-calculator-guide.html",
    ),

    "tax-calculator": (
        "Finance",
        "The Tax Calculator estimates income tax liability under a progressive (slab-based) tax system. In a progressive system, different portions of income are taxed at different rates — being in a '30% bracket' does not mean paying 30% of your entire income. Only the slice above that threshold is taxed at 30%. This calculator shows your tax by slab, total tax, effective tax rate, and estimated monthly take-home pay. For Indian users, it supports comparison between the Old Regime (with deductions) and the New Regime (lower rates, fewer deductions).",
        [
            "Enter your annual gross income in field A.",
            "Enter your total eligible deductions in field B (Section 80C investments, HRA, standard deduction, etc.).",
            "Click Run to see taxable income, tax by slab, total tax, and effective rate.",
            "For India: the standard deduction under the new regime is ₹75,000. Add 4% health and education cess on top of the calculated tax.",
        ],
        [
            ("What is the difference between marginal rate and effective tax rate?",
             "Marginal rate is the rate on your highest income slice. Effective rate is total tax ÷ total income. On ₹16 lakh income in India under the new regime, the marginal rate may be 20% but the effective rate could be 8–10%."),
            ("Old regime or new regime — which is better?",
             "If your total deductions (80C + HRA + 80D + NPS + standard deduction) exceed roughly ₹3–4 lakh, the old regime typically wins. Below that threshold, the new regime's lower rates usually produce less tax."),
            ("Does the calculator account for surcharge?",
             "Surcharge applies in India on income above ₹50 lakh (10% surcharge) and above ₹1 crore (15%). Add this manually on top of the base tax calculation for high incomes."),
        ],
        "tax-calculator-guide.html",
    ),

    "sip-calculator": (
        "Finance",
        "The SIP (Systematic Investment Plan) Calculator projects the future value of regular monthly investments into a mutual fund at an assumed annual return rate. Unlike a lump sum investment, SIP spreads purchases across time — automatically buying more units when prices are low and fewer when prices are high. This rupee-cost averaging reduces the impact of market volatility. The formula used is the future value of an annuity: <code>FV = P × ((1+r)^n − 1) / r × (1+r)</code> where P is monthly investment, r is monthly rate, and n is total months.",
        [
            "Enter your monthly SIP amount in field A (e.g. 5000 for ₹5,000 per month).",
            "Enter the expected annual return rate in field B (historical large-cap equity funds in India: 10–14%).",
            "Click Run. The result shows total invested, estimated returns, and maturity value.",
            "For a step-up SIP (where monthly amount increases each year), multiply the result by an appropriate factor for your increment rate.",
        ],
        [
            ("How is SIP different from a lump sum investment?",
             "A lump sum invests everything at once — if the market drops the next day, you lose value. SIP spreads investment over time, so you buy at multiple price points. In volatile or declining markets, SIP typically outperforms lump sum for retail investors."),
            ("What return rate should I use?",
             "For Indian equity mutual funds, 10–12% per year is a historically grounded assumption for large-cap funds over 10+ year horizons. Mid-cap/small-cap funds have higher historical returns but also higher volatility. Never assume past returns guarantee future performance."),
            ("What is XIRR and why is it different from the calculator's return?",
             "XIRR (Extended IRR) accounts for the exact timing of each investment. The SIP calculator uses an assumed flat rate. Your actual XIRR depends on real NAV history. Use XIRR in Excel or your mutual fund app to measure real past returns."),
        ],
        "sip-calculator-guide.html",
    ),

    "loan-interest-calculator": (
        "Finance",
        "The Loan Interest Calculator computes the monthly EMI (Equated Monthly Instalment), total amount repaid, and total interest charged over the life of an amortizing loan. The EMI formula is <code>EMI = P × r × (1+r)^n / ((1+r)^n − 1)</code> where P is the principal, r is the monthly interest rate (annual rate ÷ 12 ÷ 100), and n is the number of monthly payments. Each payment covers that month's interest (on the remaining balance) plus a portion of principal — so early payments are mostly interest, while late payments are mostly principal.",
        [
            "Enter the loan amount (principal) in field A.",
            "Enter the annual interest rate as a percentage in field B (e.g. 8.5 for 8.5%).",
            "Click Run to see the monthly EMI. Multiply by the loan term in months for total amount repaid.",
            "To find total interest: subtract the principal from the total amount repaid.",
        ],
        [
            ("What is amortization?",
             "Amortization means each fixed payment covers the interest accrued that month plus reduces the principal. Because the principal decreases, the interest portion shrinks each month and the principal portion grows — even though the EMI amount stays constant."),
            ("Does making extra payments save interest?",
             "Yes — significantly. Even $100/month extra on a 20-year mortgage at 7% saves approximately $23,000 in total interest and cuts the loan by 2.5 years."),
            ("What is the difference between flat rate and reducing balance interest?",
             "Flat rate calculates interest on the original principal throughout the loan. Reducing balance calculates interest on the remaining balance. A 7% flat rate is equivalent to roughly 12–13% on a reducing balance basis for a 3-year loan."),
        ],
        "loan-interest-calculator-guide.html",
    ),

    "loan-emi-calculator": (
        "Finance",
        "The Loan EMI Calculator finds the fixed monthly payment for any amortizing loan given the principal, annual interest rate, and loan tenure. EMI stands for Equated Monthly Instalment — it stays the same every month but the split between interest and principal changes. Early in the loan, most of the EMI goes toward interest. Over time, as the outstanding balance falls, more of each payment reduces the principal. Use this to compare loan offers, evaluate the impact of tenure changes, or check whether a loan fits your monthly budget.",
        [
            "Enter the loan principal in field A (e.g. 500000 for ₹5 lakh).",
            "Enter the annual interest rate in field B as a number (e.g. 10.5 for 10.5% per year).",
            "Click Run to see the monthly EMI.",
            "To compare tenures: note the EMI, then change the tenure setting and run again — longer tenure means lower EMI but more total interest.",
        ],
        [
            ("How does tenure affect EMI and total interest?",
             "A ₹10 lakh loan at 10%: 5-year tenure gives EMI ₹21,247, total interest ₹2.7 lakh. 10-year tenure gives EMI ₹13,215, total interest ₹5.9 lakh. Longer tenure = lower EMI but 2× the total interest paid."),
            ("Can I reduce my EMI after taking a loan?",
             "Yes, through balance transfer to a lower-rate lender, partial prepayment (which reduces outstanding principal and lowers future EMI), or requesting a tenure extension from your lender."),
            ("What is a prepayment penalty?",
             "Some fixed-rate loans charge a fee (typically 2–3%) if you repay before the scheduled end date. Check your loan agreement before making large prepayments."),
        ],
        None,
    ),

    "profit-margin-calculator": (
        "Finance",
        "The Profit Margin Calculator computes gross profit margin, markup percentage, and selling price from cost and revenue inputs. Margin and markup are frequently confused: margin is profit as a percentage of the selling price; markup is profit as a percentage of cost. A 50% markup on a $100 cost gives a $150 selling price — but that is only a 33.3% margin. To set a price that achieves a specific margin, use: <code>Price = Cost ÷ (1 − Margin%)</code>. Knowing your margin is essential for pricing decisions, supplier negotiations, and financial planning.",
        [
            "Enter your cost price in field A (what you paid to produce or acquire the item).",
            "Enter your selling price in field B (what the customer pays).",
            "Click Run to see gross profit, margin percentage, and markup percentage.",
            "To find the correct selling price for a target margin: enter cost in A and target margin % in B, then use 'reverse' mode.",
        ],
        [
            ("What is the difference between margin and markup?",
             "Margin = (Revenue − Cost) ÷ Revenue × 100. Markup = (Revenue − Cost) ÷ Cost × 100. On a $100 cost item selling for $150: margin is 33.3%, markup is 50%. Using the wrong one leads to serious pricing errors."),
            ("What is a good profit margin?",
             "It varies widely by industry. Software/SaaS: 70–85% gross margin. Retail: 25–50%. Restaurants: 60–70% gross margin but 3–9% net margin. Manufacturing: 20–40%. There is no universal benchmark."),
            ("How do I calculate the price that achieves a 40% margin?",
             "Use: Selling Price = Cost ÷ (1 − 0.40). If cost is $75: $75 ÷ 0.60 = $125 selling price, which yields a 40% gross margin."),
        ],
        "profit-margin-calculator-guide.html",
    ),

    "age-in-days-calculator": (
        "Utility",
        "The Age in Days Calculator finds your exact age in days, hours, minutes, and seconds from your date of birth. Unlike years, which hide the precision of your actual age, days give an unambiguous count. The calculation accounts for leap years (which add one extra day every four years), so two people both aged '32 years' could differ by up to 364 days. Day-based ages are used in pediatric medicine (newborns are measured in days), legal age verification (a person is a minor until the calendar date of their 18th birthday), and milestone celebrations like the 10,000-day mark.",
        [
            "Enter your date of birth in field A (format: YYYY-MM-DD, e.g. 1993-07-15).",
            "Click Run. The result shows your age in days from today.",
            "For hours and minutes: multiply days by 24 (hours) or 1,440 (minutes).",
            "To find a future milestone: note your current day count, subtract from the milestone (e.g. 10,000), and that is how many days remain.",
        ],
        [
            ("When is a person's 10,000-day milestone?",
             "10,000 days is approximately 27 years and 4–5 months. To find your exact date: add 10,000 days to your birthdate. This is a popular personal milestone to celebrate."),
            ("How do leap years affect the calculation?",
             "Leap years add one extra day (February 29) to the calendar every 4 years. Over any 4-year span, you accumulate 1,461 days instead of 1,460. The calculator accounts for this automatically."),
            ("Why is age in days used in medicine?",
             "For newborns and infants, development changes rapidly — a 7-day-old behaves very differently from a 14-day-old. Drug dosing tables for neonates are often keyed to age in days rather than weeks or months."),
        ],
        "age-in-days-calculator-guide.html",
    ),

    "date-difference-calculator": (
        "Utility",
        "The Date Difference Calculator finds the exact number of days between any two dates. It handles varying month lengths (February has 28 or 29 days), leap years, and the difference between calendar days (all days) and business days (excluding weekends). Common uses: calculating project deadlines, determining how many days until an event, computing contract durations, checking legal response periods, and tracking subscription renewals. The calendar-day count is straightforward; business-day count excludes Saturdays and Sundays.",
        [
            "Enter the first date in field A (format: YYYY-MM-DD).",
            "Enter the second date in field B (format: YYYY-MM-DD).",
            "Click Run. The result shows the difference in days.",
            "The result is always a positive number regardless of which date is earlier.",
        ],
        [
            ("Does the count include both the start and end date?",
             "By convention, this calculator counts the gap between dates (exclusive of both endpoints). January 1 to January 3 = 2 days. If you need inclusive counting (e.g. for a booking that includes check-in and check-out days), add 1 to the result."),
            ("What is the difference between calendar days and business days?",
             "Calendar days include all 7 days of the week. Business days exclude Saturdays and Sundays (and optionally public holidays). SLA deadlines, legal response periods, and project sprint planning typically use business days."),
            ("How do I calculate a deadline date from today?",
             "Enter today's date in A and your target date in B. Or add the number of calendar days to today's date — the result is your deadline date."),
        ],
        "date-difference-calculator-guide.html",
    ),

    "pomodoro-timer": (
        "Productivity",
        "The Pomodoro Timer is a focus timer based on the Pomodoro Technique — a time management method that breaks work into 25-minute focused sessions separated by 5-minute breaks. After four sessions, take a longer 15–30 minute break. The technique works by making the work interval short enough to feel manageable (reducing procrastination) while creating enough time pressure to maintain focus. The mandatory breaks prevent mental fatigue. Research on attention span consistently shows that focused work intervals with scheduled recovery outperform unbroken marathon sessions.",
        [
            "Click Start to begin a 25-minute focus session. Work on a single task without switching.",
            "When the timer rings, stop immediately and take a 5-minute break — stand up, stretch, look away from the screen.",
            "After 4 completed sessions (Pomodoros), take a 15–30 minute longer break.",
            "Track how many Pomodoros you complete per day — this is a concrete measure of focused work output.",
        ],
        [
            ("Can I change the 25-minute interval?",
             "Yes. 25 minutes is the original Pomodoro length but many people find 45–60 minute intervals work better for deep programming or creative work. The principle (timed focus + forced breaks) matters more than the exact duration."),
            ("What should I do during the 5-minute break?",
             "Physical movement is most effective: stand, stretch, walk, look out a window. Avoid social media or switching to another task — your brain needs genuine rest, not just different screen content."),
            ("What if I get interrupted during a Pomodoro?",
             "If you can defer it (colleague question, non-urgent notification), write it down and return to focus. If you must handle it immediately, the Pomodoro is voided — restart the full 25 minutes after resolving the interruption."),
        ],
        "pomodoro-timer-guide.html",
    ),

    "countdown-timer-online": (
        "Productivity",
        "The Countdown Timer counts down from any duration you set — in seconds, minutes, or hours — and alerts you when time is up. Use it for time-boxing work sessions, cooking timers, presentation practice, exam simulation, HIIT workout intervals, meeting time limits, and any situation where you want a visible countdown. Unlike a stopwatch (which counts up), a countdown creates urgency and makes the remaining time explicit, which research shows increases focus and task completion rate.",
        [
            "Enter the countdown duration in seconds in field A (e.g. 300 for 5 minutes, 1800 for 30 minutes).",
            "Click Run. The timer counts down and shows the remaining time.",
            "The browser will alert you when the countdown reaches zero.",
            "For recurring use: note the seconds you need and re-enter each session.",
        ],
        [
            ("What is the difference between a countdown timer and a stopwatch?",
             "A countdown starts from a set time and counts toward zero — creating urgency and a defined end point. A stopwatch starts at zero and counts up — useful for measuring how long something takes. Countdowns are better for time-boxing; stopwatches are better for timing activities."),
            ("Can I use this for Pomodoro sessions?",
             "Yes. Set it to 1500 seconds (25 minutes) for a Pomodoro focus session, or 300 seconds (5 minutes) for a short break. For a dedicated Pomodoro experience with automatic session tracking, use the Pomodoro Timer tool."),
            ("Does the timer work in the background?",
             "The timer continues while the tab is open, but some browsers throttle timers in background tabs to save resources. Keep the tab visible or use your device's native clock app for mission-critical timing."),
        ],
        "countdown-timer-online-guide.html",
    ),

    "timezone-meeting-planner": (
        "Productivity",
        "The Timezone Meeting Planner converts a date and time between multiple time zones simultaneously — showing what the same moment looks like in New York, London, Mumbai, Singapore, and any other city. This is essential for scheduling calls across geographies. Common pitfalls: the US and Europe switch Daylight Saving Time on different dates (about 2 weeks apart each spring and autumn), temporarily changing the gap between time zones. Countries like India, China, and Japan do not observe DST at all, so their offset from Western countries changes twice a year even though their own clocks don't.",
        [
            "Enter a date and time in field A (format: YYYY-MM-DD HH:MM, e.g. 2026-04-15 14:00).",
            "Click Run. The result shows the equivalent time in UTC, New York (ET), and India (IST).",
            "For other time zones: use the UTC offset shown and add/subtract from the UTC result.",
            "Always specify the timezone when sending meeting invites — e.g. '3pm London (UTC+1) / 10am New York (UTC-4) / 7:30pm Mumbai (UTC+5:30)'.",
        ],
        [
            ("What is UTC and why use it?",
             "UTC (Coordinated Universal Time) is the universal time standard — every timezone is defined as UTC plus or minus an offset. Using UTC in communications removes ambiguity about which local time was intended and avoids DST confusion."),
            ("How does Daylight Saving Time affect scheduling?",
             "The US switches DST on the second Sunday of March; Europe switches on the last Sunday of March. For the ~2 weeks between these dates, the US–Europe gap is 1 hour different from usual. A recurring 9am New York call will appear 1 hour off-schedule for European participants during this window."),
            ("What is the best time for a call between US and India?",
             "There is no perfect time — the gap is 10.5 hours (EST) or 9.5 hours (EDT). The least-bad overlap is 8–9am ET (6:30–7:30pm IST) — early for the US side, late-but-reasonable for India."),
        ],
        "timezone-meeting-planner-guide.html",
    ),

    "hash-generator": (
        "Developer",
        "The Hash Generator creates cryptographic hash digests for any text input using standard algorithms including MD5, SHA-1, SHA-256, and SHA-512. A hash function converts input of any length into a fixed-length string. The same input always produces the same hash (deterministic); changing even one character changes the entire hash (avalanche effect); and you cannot reverse a hash back to the original input (one-way). Common uses: verifying file integrity, storing passwords (use bcrypt/Argon2, not SHA), generating content fingerprints, and creating cache keys.",
        [
            "Enter the text you want to hash in field A.",
            "Click Run. The result shows the hash digest.",
            "To verify a download: hash the downloaded file's contents and compare to the publisher's listed hash.",
            "Important: do NOT use MD5 or SHA-1/SHA-256 for password storage — use bcrypt or Argon2 instead.",
        ],
        [
            ("What algorithm should I use?",
             "For file integrity checks: SHA-256 (widely used, strong). For checksums where speed matters: MD5 (weak cryptographically but fine for non-security uses). For passwords: bcrypt or Argon2 — never SHA-* for passwords. For digital signatures: SHA-256 or SHA-512."),
            ("Can I reverse a hash to get the original text?",
             "No — hash functions are one-way by design. However, common inputs (like simple passwords) can be found in precomputed lookup tables (rainbow tables). This is why password hashing must use bcrypt or Argon2 with a salt."),
            ("Why does changing one character completely change the hash?",
             "This is the avalanche effect — a deliberate property of cryptographic hash functions. It prevents attackers from making small changes and predicting the new hash."),
        ],
        "hash-generator-guide.html",
    ),

    "url-encoder-decoder": (
        "Developer",
        "The URL Encoder/Decoder converts text to and from percent-encoded URL format. URLs can only contain a limited set of 'safe' ASCII characters. Any other character (spaces, special symbols, non-ASCII letters, Unicode) must be percent-encoded: replaced with a % sign followed by two hexadecimal digits representing the character's byte value. For example, a space becomes %20, # becomes %23, and é becomes %C3%A9. Encoding is required for query string values, path segments with special characters, and data passed through HTTP requests.",
        [
            "Paste the URL or text you want to encode/decode in field A.",
            "Click Run. The result shows the encoded form (% signs) or the decoded human-readable form.",
            "For encoding: raw text goes in, URL-safe encoded text comes out.",
            "For decoding: a percent-encoded URL goes in, the original readable text comes out.",
        ],
        [
            ("What is the difference between encodeURI and encodeURIComponent?",
             "encodeURI encodes a full URL — it leaves : / ? # & = intact because those are structural URL characters. encodeURIComponent encodes a URL component (like a query parameter value) — it encodes everything including & = and ?. Use encodeURIComponent for query string values."),
            ("When should I encode a URL?",
             "Always encode user-provided values before appending to a URL. If a user searches for 'hello world & more', the query parameter must be ?q=hello%20world%20%26%20more or the & will break the URL structure."),
            ("What is double-encoding and why is it a problem?",
             "Double-encoding happens when you encode an already-encoded string — %20 becomes %2520 (% becomes %25). The server decodes once and gets %20 instead of a space. Always decode before re-encoding."),
        ],
        "url-encoder-decoder-guide.html",
    ),

    "jwt-decoder": (
        "Developer",
        "The JWT Decoder decodes JSON Web Tokens (JWTs) to reveal their header, payload, and signature components — without requiring the secret key. A JWT consists of three base64url-encoded sections separated by dots. The header specifies the algorithm (e.g. HS256). The payload contains claims — standard ones like <code>sub</code> (subject/user ID), <code>exp</code> (expiration Unix timestamp), <code>iat</code> (issued-at), and <code>aud</code> (audience). Decoding a JWT shows you these values; verifying a JWT also checks the signature against a secret — this tool does decoding only, which is appropriate for debugging and inspection.",
        [
            "Paste the JWT (three dot-separated base64url strings) into field A.",
            "Click Run. The result shows the decoded header (algorithm, token type) and payload (claims, expiry, subject).",
            "Check the exp claim: it is a Unix timestamp. If exp is in the past, the token has expired.",
            "Never decode tokens containing sensitive data in untrusted online tools — use this for development/debugging only.",
        ],
        [
            ("Is decoding a JWT the same as verifying it?",
             "No. Decoding reads the payload without checking the signature. Anyone can decode a JWT. Verifying checks the HMAC/RSA signature against the secret key, confirming the token was not tampered with. Always verify on the server; decode for inspection only."),
            ("What does the exp claim mean?",
             "exp is a Unix timestamp (seconds since Jan 1 1970 UTC) representing when the token expires. If the current time is greater than exp, the token is expired and should be rejected. You can check the expiry by converting exp to a date using a Unix timestamp converter."),
            ("Can I use a JWT without a secret key?",
             "The header algorithm 'none' removes signature verification — this is dangerous and should never be accepted by servers. Well-configured servers reject tokens with algorithm: none."),
        ],
        "jwt-decoder-guide.html",
    ),

    "unix-timestamp-converter": (
        "Developer",
        "The Unix Timestamp Converter translates between human-readable dates and Unix timestamps. A Unix timestamp is the number of seconds (or milliseconds) that have elapsed since the Unix epoch: January 1, 1970, 00:00:00 UTC. This format is used throughout programming, APIs, databases, and log files because it is timezone-independent, easy to compare, and simple to do arithmetic on. The current Unix time is always increasing. JavaScript uses milliseconds (multiply/divide by 1000 to convert to/from seconds); most other systems use seconds.",
        [
            "To convert a Unix timestamp to a date: enter the timestamp in field A (e.g. 1711843200) and click Run.",
            "To convert a date to Unix timestamp: enter a date string in field A (e.g. 2024-03-31) and click Run.",
            "If you get a date in 1970, your timestamp is in milliseconds — divide by 1000 first.",
            "All output is in UTC. Add your timezone offset manually for local time.",
        ],
        [
            ("Why does JavaScript use milliseconds while most systems use seconds?",
             "JavaScript's Date object uses milliseconds since epoch by default (Date.now() returns ms). Most Unix systems, APIs, and databases use seconds. Always check which unit an API expects — sending milliseconds to a seconds-based API will produce dates in 2554."),
            ("What is the Year 2038 problem?",
             "32-bit integers can store values up to 2,147,483,647. As a Unix timestamp, this corresponds to January 19, 2038, 03:14:07 UTC. Systems using 32-bit integers for timestamps will overflow on that date. Modern systems use 64-bit integers which won't overflow for billions of years."),
            ("What does timestamp 0 represent?",
             "Unix timestamp 0 is exactly January 1, 1970, 00:00:00 UTC — the Unix epoch. Negative timestamps represent dates before 1970."),
        ],
        "unix-timestamp-converter-guide.html",
    ),

    "duplicate-line-remover": (
        "Text",
        "The Duplicate Line Remover removes repeated lines from any text input, returning only unique lines. It supports case-sensitive mode (Apple ≠ apple) and case-insensitive mode (Apple = apple). Common uses: cleaning mailing lists with duplicate email addresses, deduplicating scraped data, removing repeated CSS or import statements, cleaning keyword lists before SEO upload, and deduplicating log entries before analysis. The tool can preserve the original order of first appearances or sort the output alphabetically.",
        [
            "Paste your list of lines in field A (one item per line).",
            "Click Run. The result shows only unique lines with duplicates removed.",
            "The count of removed duplicates is shown alongside the output.",
            "For email lists: use case-insensitive mode since email addresses are case-insensitive.",
        ],
        [
            ("Does it preserve the original order?",
             "Yes — duplicates are removed while keeping the first occurrence of each line in its original position. The output order matches the input order, minus the removed duplicates."),
            ("When should I use case-insensitive mode?",
             "Use case-insensitive for email addresses (User@Example.com and user@example.com go to the same inbox), product names (iPhone = iphone), and URLs (domain names are case-insensitive, though paths may not be). Use case-sensitive for code identifiers, file paths, and anything where case carries meaning."),
            ("What about whitespace differences?",
             "Lines with leading or trailing spaces are treated as different from lines without. If your data has inconsistent spacing, clean whitespace first using the Whitespace Cleaner tool before deduplicating."),
        ],
        "duplicate-line-remover-guide.html",
    ),

    "line-sorter": (
        "Text",
        "The Line Sorter orders a list of text lines alphabetically, numerically, or by length. It supports ascending (A–Z, 0–9) and descending (Z–A, 9–0) order, case-sensitive and case-insensitive sorting, and natural sort order (where '10' comes after '9' instead of before it). Common uses: sorting CSS property lists for readability, ordering import statements, alphabetizing configuration keys, sorting word lists for dictionary tools, and organizing data before deduplication.",
        [
            "Paste your lines in field A (one item per line).",
            "Click Run. The output shows lines sorted in ascending alphabetical order.",
            "For descending order or numeric sort, use the mode selector before running.",
            "For natural sort (files: file1, file2, file10 in that order): use natural sort mode.",
        ],
        [
            ("What is natural sort and when should I use it?",
             "Natural sort treats embedded numbers as numeric values. Lexicographic (alphabetic) sort orders '10' before '2' because '1' < '2'. Natural sort orders '2' before '10' because 2 < 10. Use natural sort for file names, version numbers, and any list mixing text with numbers."),
            ("Is the sort case-sensitive by default?",
             "Most sorters sort uppercase before lowercase (A–Z then a–z) in strict ASCII order. Case-insensitive sort ignores case so 'apple', 'Apple', and 'APPLE' are treated as equivalent."),
            ("Can I sort by line length?",
             "Yes — use length sort mode to order from shortest to longest line (or longest to shortest). Useful for identifying outlier entries in a list or formatting columnar text."),
        ],
        "line-sorter-guide.html",
    ),

    "whitespace-cleaner": (
        "Text",
        "The Whitespace Cleaner removes invisible whitespace problems from text: trailing spaces at end of lines (which break some file formats), non-breaking spaces (Unicode U+00A0, which look identical to regular spaces but aren't), double spaces, Windows CRLF line endings (converted to Unix LF), tab characters, and zero-width characters (U+200B, U+FEFF byte order mark). These invisible characters cause unexpected failures in databases, code parsers, CSV files, and search/comparison operations that appear to work visually but fail functionally.",
        [
            "Paste your text in field A.",
            "Click Run. The cleaned text is returned with invisible whitespace normalized.",
            "The result summary shows what was cleaned (e.g. '12 trailing spaces removed, 3 non-breaking spaces converted').",
            "For code: pay special attention to mixed tabs and spaces, which cause IndentationError in Python.",
        ],
        [
            ("What is a non-breaking space and where does it come from?",
             "A non-breaking space (U+00A0) looks identical to a regular space but is a different character. It appears when copying from PDFs, Word documents, or some web pages. Databases and code that compare strings see 'hello world' (regular space) and 'hello\u00a0world' (NBSP) as different strings."),
            ("Why does Excel's TRIM function not remove all spaces?",
             "Excel's TRIM only removes regular spaces (U+0020) and ASCII tabs. It does not remove non-breaking spaces, zero-width characters, or other Unicode whitespace. Use this tool for comprehensive cleaning before importing into Excel."),
            ("What are zero-width characters?",
             "Zero-width characters (U+200B zero-width space, U+FEFF BOM) are invisible and have zero visual width. They appear when copying from some websites or apps. They can break string matching, URL parsing, and code execution silently."),
        ],
        "whitespace-cleaner-guide.html",
    ),

    "word-frequency-counter": (
        "Text",
        "The Word Frequency Counter counts how many times each word appears in a text. It shows results ranked by frequency, helping you identify overused words, analyze writing patterns, check keyword density for SEO, and understand the vocabulary distribution of a document. Common uses: academic text analysis, SEO keyword density auditing, finding repeated words in a draft for editing, analyzing customer feedback for common themes, and studying language patterns in a corpus.",
        [
            "Paste your text in field A.",
            "Click Run. The result shows each unique word and its count, ranked by frequency.",
            "Stop words (the, a, is, of) dominate most English text — most analysis excludes them.",
            "For SEO keyword density: find the target keyword in the list and divide its count by total words.",
        ],
        [
            ("What are stop words and should I include them?",
             "Stop words are high-frequency function words (the, a, is, of, to, and) that carry little meaning. For SEO or content analysis, you typically exclude them to focus on meaningful terms. For linguistic or stylistic analysis, include them."),
            ("What is TF-IDF and how does it relate to word frequency?",
             "Term Frequency (TF) is simply the word count. TF-IDF (Term Frequency–Inverse Document Frequency) adjusts for words that appear in many documents — a word common across all pages (like 'the') gets a lower score than a word specific to one page. TF-IDF is more useful for SEO than raw frequency."),
            ("What is a healthy keyword density for SEO?",
             "Avoid keyword stuffing. Modern SEO guidance suggests 0.5–2% density for a primary keyword. A 1,000-word article mentioning a keyword 10–15 times is reasonable; 50+ times is keyword stuffing."),
        ],
        "word-frequency-counter-guide.html",
    ),

    "text-diff-checker": (
        "Text",
        "The Text Diff Checker compares two text blocks and highlights the differences — additions, deletions, and changes. It uses the Myers diff algorithm, which finds the minimum edit distance between two texts. Output is shown in a side-by-side or unified diff format. Common uses: comparing versions of a document or contract, spotting the difference between two API responses, checking what changed between two configuration files, comparing original and edited translation text, and reviewing code changes without a full git diff setup.",
        [
            "Paste the original text in field A.",
            "Paste the modified text in field B.",
            "Click Run. Added content is highlighted in green; removed content in red.",
            "For large files: the diff focuses on changed sections. Unchanged sections are collapsed.",
        ],
        [
            ("What does a unified diff look like?",
             "Lines starting with + are additions (in B but not A). Lines starting with − are deletions (in A but not B). Lines starting with a space are unchanged context. @@ −1,4 +1,5 @@ means the chunk starts at line 1 in the original (4 lines) and line 1 in the new (5 lines)."),
            ("What is the difference between line diff and word diff?",
             "Line diff highlights entire lines that changed. Word diff highlights only the specific words within a line that changed. Word diff is more precise for prose editing; line diff is standard for code."),
            ("Should I use this or git diff?",
             "Use this tool when you don't have git, for non-code comparisons (contracts, documents, translations), or for a quick visual comparison. Use git diff for tracked code changes — it preserves history and integrates with your version control workflow."),
        ],
        "text-diff-checker-guide.html",
    ),

    "sitemap-url-list-cleaner": (
        "SEO",
        "The Sitemap URL List Cleaner processes a raw list of URLs and removes duplicates, strips UTM tracking parameters (?utm_source=, ?utm_medium=, etc.), normalizes trailing slashes for consistency, and filters to a single domain. This is essential before generating or submitting a sitemap. Sitemaps with tracking parameters create thousands of 'unique' URLs from a single page, wasting crawl budget and potentially causing duplicate content issues. Google's sitemap protocol allows maximum 50,000 URLs per file — cleaning ensures you don't waste slots on junk URLs.",
        [
            "Paste your raw URL list in field A (one URL per line).",
            "Click Run. The cleaned URL list is returned with duplicates removed and tracking parameters stripped.",
            "The result shows how many URLs were removed and why.",
            "Copy the output directly into your sitemap generator or migration tool.",
        ],
        [
            ("Why do tracking parameters cause problems in sitemaps?",
             "UTM parameters (utm_source, utm_medium, utm_campaign, fbclid, gclid) don't change page content. A URL with and without UTMs serves the same page. In a sitemap, each unique URL string is treated as a separate page — leading Google to index tracked versions and split ranking signals."),
            ("What is URL normalization?",
             "Normalization ensures equivalent URLs are recognized as the same. Steps: lowercase the domain, remove default ports (:443 for https), sort query parameters consistently, apply a uniform trailing-slash rule, and decode unnecessarily encoded characters."),
            ("Should noindex pages be in the sitemap?",
             "No. Including noindex pages in your sitemap sends contradictory signals — you're telling Google to index (sitemap) and not index (noindex) the same page simultaneously. Remove all noindex, redirect destination (non-canonical), and login/admin pages from sitemaps."),
        ],
        "sitemap-url-list-cleaner-guide.html",
    ),

    "slug-generator": (
        "SEO",
        "The Slug Generator converts any title or phrase into a URL-friendly slug — lowercase letters, numbers, and hyphens only, with spaces replaced by hyphens and special characters removed. URL slugs determine the address of your blog posts, product pages, and articles. A clean, descriptive slug improves SEO (keywords in URLs are a minor ranking signal), improves click-through rate in search results, and makes links easier to share. Example: 'How to Fix WhatsApp Not Sending Messages' → 'how-to-fix-whatsapp-not-sending-messages'.",
        [
            "Paste or type your title in field A.",
            "Click Run. The result is the URL-ready slug.",
            "Copy the slug directly into your CMS (WordPress, Ghost, Shopify, etc.) URL field.",
            "If changing a slug on a live page: set up a 301 redirect from the old URL to the new one to preserve SEO value.",
        ],
        [
            ("Should I include stop words in slugs?",
             "Generally remove stop words (the, a, and, of, for) to keep slugs concise. 'how-to-fix-discord-not-connecting' is better than 'how-to-fix-the-discord-not-connecting-issue'. But test both — sometimes removing words changes the meaning."),
            ("What happens if I change a slug on a live page?",
             "The old URL breaks for anyone who has bookmarked or linked to it, and Google has to recrawl and reindex the new URL. Always set up a 301 redirect from old slug to new slug when making this change. Without a redirect, you lose all the SEO equity built up on the old URL."),
            ("Should slugs use hyphens or underscores?",
             "Hyphens. Google treats hyphens as word separators, so 'how-to-fix' is read as three words: how, to, fix. Underscores are treated as word joiners — 'how_to_fix' is one term. Use hyphens for SEO-friendly slugs."),
        ],
        "slug-generator-guide.html",
    ),

    "robots-txt-generator": (
        "SEO",
        "The Robots.txt Generator creates a robots.txt file — a plain text file placed at the root of your website that tells search engine crawlers which pages they are and aren't allowed to access. Common uses: blocking admin pages (/admin/), staging environments, duplicate parameter URLs, and private internal tools. Important: robots.txt controls crawl access, not indexing. A page blocked by robots.txt can still appear in search results if another site links to it — use noindex meta tags to prevent indexing.",
        [
            "Select the crawler to configure (use '*' for all crawlers, or specify Googlebot, Bingbot, etc.).",
            "Enter paths to disallow (e.g. /admin/, /staging/, /private/).",
            "Add your sitemap URL at the bottom.",
            "Place the generated file at yourdomain.com/robots.txt and test it in Google Search Console.",
        ],
        [
            ("Does blocking a URL in robots.txt remove it from Google?",
             "No. Blocking crawling prevents Google from reading the page's content, but Google can still know the URL exists from external links. To remove a page from search results, use a noindex meta tag AND allow crawling so Google can see the noindex instruction."),
            ("Can robots.txt block JavaScript and CSS files?",
             "You can, but you shouldn't. Google needs to render JavaScript and load CSS to understand your pages properly. Blocking Google from these resources makes your pages look broken to the crawler, potentially hurting rankings."),
            ("What is the difference between Disallow: / and Disallow: /admin/?",
             "Disallow: / blocks the entire site. Disallow: /admin/ blocks only URLs starting with /admin/. A trailing slash is important — Disallow: /admin (no slash) would block /admin but not /administration."),
        ],
        "robots-txt-generator-guide.html",
    ),

    "meta-tag-generator": (
        "SEO",
        "The Meta Tag Generator creates the HTML meta tags for your web page's head section — title tag, meta description, robots directive, Open Graph tags (for social sharing previews on Facebook/LinkedIn), and Twitter Card tags. These tags don't directly affect rankings for most keywords, but the title and description appear in search results and significantly affect click-through rate. Open Graph and Twitter Card tags determine how your page looks when shared on social media — without them, platforms auto-select an image and text that may look poor.",
        [
            "Enter your page title in field A (optimal length: 50–60 characters).",
            "Enter your meta description in field B (optimal length: 120–155 characters).",
            "Click Run. The HTML output is ready to paste into your page's <head> section.",
            "Include your target keyword naturally in both the title and description — don't stuff.",
        ],
        [
            ("How long should a meta title and description be?",
             "Title: 50–60 characters (Google truncates at ~600px width, roughly 60 chars). Description: 120–155 characters. Longer descriptions get cut off with '...' in search results. Shorter is usually better if it conveys value clearly."),
            ("What is an Open Graph image and what size should it be?",
             "og:image is the preview image shown when your page is shared on Facebook, LinkedIn, and WhatsApp. Optimal size: 1200×630 pixels (roughly 1.91:1 ratio). Minimum: 600×315 pixels. Use a JPG for photos, PNG for graphics. Image size under 8MB."),
            ("Do meta keywords still matter for SEO?",
             "No. Google has ignored the meta keywords tag since 2009. Bing gives it slight weight but warns that keyword stuffing in it can be treated as spam. Do not waste time on meta keywords — focus on title and description."),
        ],
        "meta-tag-generator-guide.html",
    ),

    "lorem-ipsum-generator": (
        "Writing",
        "The Lorem Ipsum Generator produces dummy placeholder text for design mockups, UI prototyping, and layout testing. The standard Lorem Ipsum text originates from 'de Finibus Bonorum et Malorum' by Cicero (45 BC), corrupted and randomized in the 1500s. It has been the industry standard placeholder since the advent of desktop publishing. Placeholder text allows designers and developers to evaluate typography, spacing, and layout without waiting for real content — and prevents premature focus on content meaning during visual design reviews.",
        [
            "Enter the amount of text you need in field A (number of words, sentences, or paragraphs).",
            "Click Run. The placeholder text is generated immediately.",
            "Copy the output directly into your design tool (Figma, Adobe XD, Sketch) or code editor.",
            "For realistic content-length testing: use 'paragraphs' mode to match your expected article length.",
        ],
        [
            ("Why use Lorem Ipsum instead of real text?",
             "Real text attracts attention to content during design reviews, distracting from layout decisions. Lorem Ipsum is recognizably placeholder text, so reviewers focus on spacing, typography, and hierarchy rather than editing copy."),
            ("When should I NOT use Lorem Ipsum?",
             "Avoid it in usability testing (participants should react to real content), accessibility reviews (screen reader testing needs real text), staging environments indexed by search engines (Google may index it), and when testing CJK or RTL character rendering."),
            ("Is Lorem Ipsum real Latin?",
             "It is scrambled Latin derived from Cicero. The original passage discusses ethics ('extreme pain or desire'). The Lorem Ipsum version is intentionally jumbled so it is clearly not meaningful text — but it does look like real Latin to untrained eyes."),
        ],
        "lorem-ipsum-generator-guide.html",
    ),

    "number-to-words-converter": (
        "Utility",
        "The Number to Words Converter converts numeric values to their written English equivalent — for example, 1234567 becomes 'one million two hundred thirty-four thousand five hundred sixty-seven'. This is required for writing cheques/checks (legal and banking requirement), drafting legal contracts and invoices where amounts must be stated in words, educational materials, and generating accessible content for screen readers. The converter handles both cardinal numbers (one, two, three) and ordinal numbers (first, second, third).",
        [
            "Enter the number in field A (digits only — no commas or currency symbols).",
            "Click Run. The result shows the number written out in words.",
            "For currency: the output gives the base amount in words; add 'dollars and X cents' manually.",
            "For ordinal numbers (1st, 2nd, 3rd): use ordinal mode if available.",
        ],
        [
            ("What is the difference between cardinal and ordinal numbers?",
             "Cardinal numbers count quantity: one, two, three. Ordinal numbers indicate position: first, second, third. Cheques and legal documents use cardinal ('five hundred dollars'). Rankings and sequences use ordinal ('the third clause')."),
            ("How are large numbers written?",
             "US/short scale: 1,000 = thousand; 1,000,000 = million; 1,000,000,000 = billion. UK/long scale (traditional): 1,000,000,000 = milliard (not used in modern UK). Modern UK uses the short scale. Always clarify which scale when dealing with international contracts above one million."),
            ("Why must cheques have amounts in words?",
             "Written-word amounts are harder to fraudulently alter than numerals. If there is a discrepancy between the number and the words on a cheque, banks legally use the written-word amount as authoritative."),
        ],
        "number-to-words-converter-guide.html",
    ),

    "color-code-converter": (
        "Design",
        "The Color Code Converter translates between the four main color formats used in web design and graphics: HEX (#667eea), RGB (102, 126, 234), HSL (228°, 75%, 66%), and CMYK (56%, 46%, 0%, 8%). Each format is used in different contexts — HEX in CSS and HTML, RGB in digital graphics and CSS, HSL for intuitive color adjustments (hue rotation, lightness changes), and CMYK in print production. Converting between them is a common need when matching colors across design tools.",
        [
            "Enter the color value in field A in any supported format (HEX with #, RGB as r,g,b, HSL as h,s%,l%).",
            "Click Run. The result shows the equivalent values in all other formats.",
            "For CSS: use the HEX or RGB output directly in your stylesheet.",
            "For print: use the CMYK output and give it to your print supplier.",
        ],
        [
            ("Why does converting HEX→CMYK→HEX not always give the same result?",
             "RGB and CMYK have different color gamuts. Some screen colors (especially bright blues and greens) cannot be accurately reproduced in print CMYK. The conversion goes through a standard formula but colors at the edges of the gamut may shift slightly."),
            ("When should I use HSL instead of HEX?",
             "HSL is easier to reason about: hue (0–360° color wheel position), saturation (intensity), lightness (brightness). To make a color 20% lighter, simply increase the L value by 20. This is much harder with HEX. Use HSL in CSS variables for theming."),
            ("What does the # mean in a HEX color code?",
             "The # is a CSS syntax prefix indicating what follows is a hex color value. The six hex digits are pairs for red (rr), green (gg), and blue (bb): #rrggbb. #667eea = R:102, G:126, B:234 in decimal."),
        ],
        "color-code-converter-guide.html",
    ),

    "gradient-generator": (
        "Design",
        "The Gradient Generator creates CSS gradient code — linear, radial, or conic — for use in web design. Gradients replace solid background colors with smooth transitions between two or more colors. The output is ready-to-paste CSS: for example <code>background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)</code>. Common uses: hero section backgrounds, button hover effects, card overlays on images, text gradients (with background-clip), and decorative UI elements.",
        [
            "Enter the first color in field A (HEX or CSS color name, e.g. #667eea or purple).",
            "Enter the second color in field B.",
            "Click Run. The CSS gradient code is generated, ready to paste.",
            "Copy the output into your CSS file as the value of the background or background-image property.",
        ],
        [
            ("What is the difference between linear, radial, and conic gradients?",
             "Linear gradient transitions along a straight line (e.g. left to right, top to bottom, or diagonal). Radial gradient radiates from a center point outward in a circle or ellipse. Conic gradient sweeps around a center point like a color wheel — useful for pie chart effects."),
            ("Can I have more than two colors in a gradient?",
             "Yes. Add additional color stops: linear-gradient(135deg, red 0%, yellow 50%, green 100%). Each stop specifies a color and a position (percentage or pixel value along the gradient line)."),
            ("How do I apply a gradient to text?",
             "Use: background: linear-gradient(...); -webkit-background-clip: text; -webkit-text-fill-color: transparent. This clips the gradient to the shape of the text. Browser support is excellent in modern browsers."),
        ],
        "gradient-generator-guide.html",
    ),

    "password-strength-checker": (
        "Security",
        "The Password Strength Checker evaluates how resistant a password is to brute-force and dictionary attacks. It estimates the number of possible combinations (entropy), the time to crack at typical attack speeds, and identifies specific weaknesses: common patterns like 'password123', keyboard walks like 'qwerty', dictionary words, and predictable substitutions like 3→E or 0→O. A strong password is long (12+ characters), uses all character types, and is not based on any dictionary word, name, or predictable pattern.",
        [
            "Type or paste a password in field A.",
            "Click Run. The result shows a strength rating and specific weaknesses found.",
            "Aim for at least 'Strong' — the combination of length and character variety matters most.",
            "Never type your actual live passwords into any online tool — use this for testing new candidates only.",
        ],
        [
            ("What makes a password strong?",
             "Length is the biggest factor. A random 16-character password of any characters is much stronger than a complex 8-character password. Use a combination of uppercase, lowercase, digits, and symbols. Avoid any word found in a dictionary, any part of your name or email, and any repeated pattern."),
            ("Why is 'P@ssw0rd' considered weak?",
             "Common substitutions (a→@, o→0, e→3) are known to attackers. Cracking tools try these patterns automatically. A password that was a word before substitution is still a dictionary word in terms of crack resistance."),
            ("What is a passphrase and is it stronger?",
             "A passphrase is a sequence of random words: 'correct horse battery staple'. At 4 random words, this has more entropy than most 8-character passwords and is far easier to memorize. NIST SP 800-63B recommends passphrases over complex short passwords."),
        ],
        "password-strength-checker-guide.html",
    ),

    "password-generator": (
        "Security",
        "The Password Generator creates cryptographically random passwords using your browser's secure random number generator (CSPRNG via the Web Crypto API) — not a predictable math formula. Generated passwords are never sent to any server; generation happens entirely in your browser. You can specify length and which character sets to include: uppercase letters, lowercase letters, numbers, and symbols. Longer passwords are exponentially stronger — each additional character multiplies the search space by the number of characters in the pool.",
        [
            "Set the desired password length in field A (minimum recommended: 16 characters).",
            "Click Run. A cryptographically random password is generated.",
            "Copy it immediately and store it in a password manager (1Password, Bitwarden, etc.).",
            "Never reuse generated passwords across multiple sites — each account should have its own unique password.",
        ],
        [
            ("Is a browser-based password generator safe to use?",
             "Yes, if it uses the Web Crypto API (window.crypto.getRandomValues). This is cryptographically secure randomness. This tool generates passwords client-side only — nothing is transmitted over the network."),
            ("How long should a password be?",
             "For important accounts: 16–20 characters minimum. For master password managers: 20+ characters. For throwaway accounts: 12+ characters. Time-to-crack at 10 billion guesses/second: 12 random chars ≈ centuries; 8 chars ≈ hours."),
            ("Should I use a password manager?",
             "Yes. A password manager stores unique random passwords for every site so you only need to remember one master password. Reusing passwords across sites is the leading cause of account takeovers — one breach exposes all accounts that share the password."),
        ],
        None,
    ),

    "random-password-list-generator": (
        "Security",
        "The Random Password List Generator creates multiple unique passwords at once — useful for IT teams onboarding new users, developers generating test credentials, bulk account creation, or provisioning API keys. All passwords are generated using your browser's CSPRNG (cryptographically secure random number generator) and never leave your device. Generate 5, 10, 50, or 100 passwords in one click, each guaranteed to be unique.",
        [
            "Enter the number of passwords to generate in field A.",
            "Click Run. The list of unique random passwords is shown immediately.",
            "Copy the entire list and use in your onboarding spreadsheet or provisioning system.",
            "Never email plain-text passwords to recipients — deliver them through a secure channel (password manager sharing, encrypted message).",
        ],
        [
            ("How should I deliver generated passwords to users?",
             "Never send plain-text passwords via email or Slack — these channels are not encrypted end-to-end. Use a password manager's sharing feature, a secrets manager (AWS Secrets Manager, HashiCorp Vault), or an encrypted message tool like Signal."),
            ("Can I use these for API keys or tokens?",
             "Yes — a long random password makes an excellent API key candidate. For production secrets, use your infrastructure's secret manager rather than a browser-based tool, as it provides auditing, rotation, and access control."),
            ("Are all generated passwords truly unique?",
             "With a 16+ character pool of 72+ characters, the probability of generating two identical passwords in a list of 100 is astronomically small (less than 10^−27). Each password is independently and randomly generated."),
        ],
        "random-password-list-generator-guide.html",
    ),

    "json-formatter": (
        "Developer",
        "The JSON Formatter validates and pretty-prints JSON data — converting compact or minified JSON into a human-readable indented format. It catches syntax errors (trailing commas, missing quotes, incorrect brackets) and highlights exactly where the problem is. JSON (JavaScript Object Notation) is the standard data exchange format for APIs, configuration files, and data storage. Minified JSON is hard to read; formatted JSON shows the structure clearly for debugging, documentation, and review.",
        [
            "Paste your JSON in field A (minified or messy).",
            "Click Run. Valid JSON is returned formatted with 2-space indentation.",
            "If the JSON is invalid, an error message shows the line and character position of the problem.",
            "Common errors: trailing comma after the last item, single quotes instead of double quotes, missing colon between key and value.",
        ],
        [
            ("What is the most common JSON syntax error?",
             "Trailing commas — adding a comma after the last item in an array or object: [1, 2, 3,]. Valid in JavaScript but invalid in strict JSON. Other common errors: using single quotes instead of double quotes for strings, and undefined/NaN values (not valid JSON)."),
            ("What is the difference between JSON and JavaScript objects?",
             "JSON is a text format derived from JavaScript object syntax but with stricter rules: all keys must be double-quoted strings, no functions or undefined values, no trailing commas. JavaScript object literals are more permissive."),
            ("Can I minify JSON to reduce file size?",
             "Yes — removing whitespace reduces JSON size by 20–30%. Use minified JSON in HTTP responses and API payloads to reduce bandwidth. Use formatted JSON in configuration files that humans need to read and edit."),
        ],
        None,
    ),

    "markdown-to-html-converter": (
        "Developer",
        "The Markdown to HTML Converter transforms Markdown-formatted text into equivalent HTML. Markdown uses simple symbols to indicate formatting: ## for h2 headings, **text** for bold, *text* for italic, - for bullet list items, and [text](url) for links. The converter handles standard CommonMark syntax and optionally GitHub Flavored Markdown (GFM) extensions: tables, task list checkboxes (- [ ]), and strikethrough (~~text~~). Use this when you write in Markdown but need HTML output for a CMS, email campaign, or static HTML file.",
        [
            "Paste or type your Markdown in field A.",
            "Click Run. The HTML output is shown in the result.",
            "Copy the HTML and paste into your CMS rich text editor (HTML mode) or .html file.",
            "The live preview shows how the output renders in a browser.",
        ],
        [
            ("What is the difference between CommonMark and GitHub Flavored Markdown?",
             "CommonMark is a strict specification for standard Markdown. GitHub Flavored Markdown (GFM) extends it with tables (using | pipe syntax), task list checkboxes (- [ ] and - [x]), strikethrough (~~text~~), and auto-linking of URLs. Most modern Markdown tools support GFM."),
            ("Why does my single line break not create a new paragraph?",
             "In Markdown, a single newline is not a paragraph break — you need a blank line between paragraphs. To create a line break within a paragraph (HTML <br>), end the line with two or more spaces before pressing Enter."),
            ("Can I mix HTML inside Markdown?",
             "Yes — most Markdown parsers pass raw HTML through unchanged. You can use <div>, <table>, <span> etc. directly inside a Markdown document. This is useful for elements that Markdown doesn't support natively."),
        ],
        "markdown-to-html-converter-guide.html",
    ),

    "css-minifier": (
        "Developer",
        "The CSS Minifier removes unnecessary whitespace, comments, and redundant characters from CSS files to reduce their size for production. Smaller CSS files load faster, especially important for mobile users on slow connections. Minification typically reduces CSS file size by 30–50%. The minified output is functionally identical to the original — all styles are preserved. Use expanded, readable CSS in development; deploy minified CSS in production.",
        [
            "Paste your CSS in field A.",
            "Click Run. The minified CSS is returned — all comments removed, whitespace compressed.",
            "Copy the output and save as your production CSS file (e.g. styles.min.css).",
            "Keep the original unminified file for editing — never edit minified CSS directly.",
        ],
        [
            ("What is the difference between minification and compression?",
             "Minification removes whitespace and comments from the source code — the result is still readable (barely). Compression (gzip/brotli) is a binary encoding applied by the web server at transfer time. Both can be used together: minify first, then serve with gzip compression."),
            ("Does minification change how the CSS works?",
             "No — the browser interprets minified CSS identically to formatted CSS. Shorthand property merging (e.g. combining margin-top, margin-right etc. into margin: shorthand) is a more aggressive optimization that some minifiers perform."),
            ("Should I minify CSS during development?",
             "No. Minified CSS is impossible to debug because line numbers and readable property names are lost. Use formatted CSS in development with source maps; minify only for production builds."),
        ],
        None,
    ),

    "js-minifier": (
        "Developer",
        "The JavaScript Minifier removes whitespace, comments, and shortens variable names in JavaScript code to reduce file size for production deployment. Large JavaScript files are a primary cause of slow page load times, particularly on mobile devices. Minification can reduce JS file size by 40–70%. The minified output is functionally identical — variable renaming is done in a way that preserves all behavior. Keep original source files for editing and debugging.",
        [
            "Paste your JavaScript in field A.",
            "Click Run. The minified JavaScript is returned.",
            "Save the output as filename.min.js for use in your production HTML.",
            "Always keep the original .js file — you cannot recover readable code from minified output.",
        ],
        [
            ("What is the difference between minification and uglification?",
             "Minification removes whitespace and comments. Uglification (uglifyJS) also renames variables to single letters (a, b, c) to further reduce size. Both produce functionally identical code. Modern bundlers like webpack and esbuild do both automatically."),
            ("Do I need to manually minify JS if I use webpack or Vite?",
             "No. Build tools like webpack, Vite, Rollup, and Parcel minify JavaScript automatically in production mode. Manual minification is only needed for standalone scripts not going through a build pipeline."),
            ("What are source maps?",
             "Source maps are separate files (.map) that map minified code back to the original source. Browser DevTools use them to show readable code during debugging while the browser actually runs minified code."),
        ],
        None,
    ),

    "html-minifier": (
        "Developer",
        "The HTML Minifier removes whitespace, comments, and optional HTML tags from HTML files to reduce their size. HTML minification is less impactful than CSS or JS minification (HTML is typically smaller) but still useful for high-traffic pages where every byte counts. Removing HTML comments is particularly useful for removing development notes before production deployment.",
        [
            "Paste your HTML in field A.",
            "Click Run. Comments are stripped and whitespace is compressed.",
            "The output is functionally identical HTML — all elements and attributes preserved.",
            "Verify the output renders correctly in a browser before deploying.",
        ],
        [
            ("Is HTML minification worth doing?",
             "The impact is smaller than CSS/JS minification because gzip compression already handles repetitive HTML structure very efficiently. HTML minification provides 5–20% size reduction; gzip handles 60–80%. Both together are ideal for very high-traffic sites."),
            ("Will minification break my HTML?",
             "Standard minification (whitespace removal) is safe. Aggressive minification that removes optional closing tags (</li>, </tr>) can occasionally break rendering in edge cases. Test the output after minification."),
            ("Should I remove HTML comments?",
             "Yes, in production. Comments add bytes and can expose implementation details to users who view source. Always remove TODO comments and code documentation from production HTML."),
        ],
        None,
    ),

    "base64-encoder-decoder": (
        "Developer",
        "The Base64 Encoder/Decoder converts binary data to and from Base64 text encoding. Base64 represents binary bytes using 64 printable ASCII characters (A–Z, a–z, 0–9, +, /), making binary data safe to transmit through text-based protocols like email (MIME), JSON, and URLs. Common uses: embedding small images directly in CSS or HTML as data URIs, transmitting binary API payloads in JSON, encoding authentication credentials in HTTP Basic Auth headers, and storing binary data in text fields.",
        [
            "To encode: paste plain text or a data string in field A, click Run — the Base64 encoded output is shown.",
            "To decode: paste a Base64 string in field A, click Run — the original text is shown.",
            "Base64 encoded strings always consist of letters, numbers, +, /, and = padding characters.",
            "Note: Base64 is encoding, not encryption. It provides no security — anyone can decode it.",
        ],
        [
            ("Is Base64 a form of encryption?",
             "No. Base64 is a reversible encoding scheme, not encryption. It does not require a key and anyone can decode it instantly. Do not use it to 'hide' sensitive information."),
            ("Why does Base64 output end with = signs?",
             "= is padding. Base64 encodes every 3 bytes of input as 4 characters. If the input isn't a multiple of 3 bytes, = signs pad the output to make it a multiple of 4 characters. One = means 1 padding byte; == means 2."),
            ("What is the difference between standard Base64 and URL-safe Base64?",
             "Standard Base64 uses + and / which are special characters in URLs. URL-safe Base64 replaces + with - and / with _ so the encoded string can be safely included in a URL or filename. JWT tokens use URL-safe Base64."),
        ],
        None,
    ),

    "html-entity-encoder-decoder": (
        "Developer",
        "The HTML Entity Encoder/Decoder converts special characters to and from their HTML entity equivalents. Characters like <, >, &, and \" have special meaning in HTML and must be escaped as &lt;, &gt;, &amp;, and &quot; when they appear as content rather than markup. Failure to encode user-provided content before inserting it into HTML is the most common cause of Cross-Site Scripting (XSS) vulnerabilities. The decoder converts entity-encoded text back to readable form.",
        [
            "To encode: paste text containing <, >, &, or quotes in field A, click Run — the HTML-safe entity version is returned.",
            "To decode: paste HTML-encoded text (with &lt;, &gt; etc.) in field A, click Run — the readable text is returned.",
            "Always encode user-provided content before rendering it in HTML to prevent XSS.",
            "The encoder handles both named entities (&amp;) and numeric entities (&#38;).",
        ],
        [
            ("What is XSS and how does HTML encoding prevent it?",
             "Cross-Site Scripting (XSS) occurs when user-provided input containing <script> tags or event handlers is inserted into a page without encoding. The browser executes the injected script. HTML encoding turns < into &lt; — the browser renders it as a literal < character, not as the start of a tag."),
            ("What is the difference between HTML encoding and URL encoding?",
             "HTML encoding escapes characters for safe use inside HTML content (&lt; for <). URL encoding (percent-encoding) escapes characters for safe use inside URLs (%3C for <). They are different schemes used in different contexts."),
            ("Do I need to encode every special character?",
             "At minimum: always encode <, >, &, and double quotes in HTML content. In attribute values, also encode single quotes. Template engines (Jinja2, Handlebars, Twig) do this automatically — use their auto-escaping features rather than manual encoding."),
        ],
        None,
    ),

    "csv-to-json-converter": (
        "Developer",
        "The CSV to JSON Converter transforms comma-separated value data into JSON format. CSV (Comma-Separated Values) is the most common data export format from spreadsheets, databases, and analytics tools. JSON is the standard format for APIs, NoSQL databases, and modern web applications. The converter uses the first row as the key names (headers) and each subsequent row as a JSON object. The output is an array of objects, ready for import into MongoDB, use in a JavaScript application, or storage in a JSON field.",
        [
            "Paste your CSV data in field A (first row must be the header row with column names).",
            "Click Run. The result is a JSON array of objects, one per CSV row.",
            "Each key in the JSON objects corresponds to a column header from the CSV.",
            "If values contain commas, they must be wrapped in double quotes in the CSV.",
        ],
        [
            ("What happens if a CSV value contains a comma?",
             "Values containing commas must be enclosed in double quotes in CSV: name,description becomes 'Apple','A fruit, red or green'. Most spreadsheet exports handle this automatically."),
            ("Can I convert CSV with special characters or accented letters?",
             "Yes, if the CSV is UTF-8 encoded. Files exported from Excel may be in Windows-1252 encoding — if you see garbled characters, save the CSV as UTF-8 in Excel first (File → Save As → CSV UTF-8)."),
            ("How do I import the JSON output into MongoDB?",
             "Save the JSON array to a file (data.json), then use: mongoimport --db mydb --collection items --file data.json --jsonArray. The --jsonArray flag is required when the file contains an array of documents."),
        ],
        "csv-to-json-converter-guide.html",
    ),

    "json-to-csv-converter": (
        "Developer",
        "The JSON to CSV Converter transforms a JSON array of objects into CSV format — ready for opening in Excel, Google Sheets, or importing into a database. The first row of the CSV output is the header row containing all unique keys from the JSON objects. Common uses: exporting API response data for analysis in a spreadsheet, converting database query results for reporting, and preparing data for import into systems that accept CSV.",
        [
            "Paste a JSON array of objects in field A — format: [{...}, {...}, {...}].",
            "Click Run. The CSV output appears with headers in the first row.",
            "Copy the CSV and paste into a text file saved as .csv, then open in Excel or Google Sheets.",
            "If objects have different keys, missing values in some rows will be blank in the CSV.",
        ],
        [
            ("What if my JSON objects have different keys?",
             "The converter uses all unique keys across all objects as the CSV header. Objects missing a key will have a blank value in that column. This matches the behavior of most database export tools."),
            ("How do I open the CSV in Excel with correct encoding?",
             "If your data contains non-ASCII characters (accented letters, CJK): save as UTF-8 CSV, then in Excel use Data → Get Data → From Text/CSV and specify UTF-8 encoding during import. Double-clicking a UTF-8 CSV in Windows opens it in the default (Windows-1252) encoding and garbles special characters."),
            ("What is the difference between CSV and TSV?",
             "CSV uses commas as delimiters; TSV (Tab-Separated Values) uses tabs. TSV is preferred when data values frequently contain commas (e.g. addresses, descriptions). Both are supported by Excel and most import tools."),
        ],
        "json-to-csv-converter-guide.html",
    ),

    "regex-tester": (
        "Developer",
        "The Regex Tester lets you test regular expression patterns against a text string and see which parts match, what groups are captured, and how many matches were found. Regular expressions are patterns used to search, extract, and transform text in programming. They are used for form validation (email, phone number formats), data extraction (parsing log files, URLs, dates), search-and-replace operations, and text processing pipelines. Testing a regex interactively before embedding it in code saves debugging time.",
        [
            "Enter your regex pattern in field A (without surrounding / slashes).",
            "Enter the test string in field B.",
            "Click Run. The result shows all matches found, captured groups, and the match index.",
            "Add flags after the pattern if needed: i for case-insensitive, g for all matches, m for multiline.",
        ],
        [
            ("What is the difference between greedy and lazy matching?",
             "Greedy (default): .* matches as many characters as possible. Lazy: .*? matches as few as possible. For 'a<b>c<d>' — the greedy <.*> matches the entire <b>c<d>; the lazy <.*?> matches only <b>."),
            ("How do I match a literal period, plus, or other special characters?",
             "Escape them with a backslash: \\. matches a literal period; \\+ matches a literal plus; \\( matches a literal parenthesis. In a character class [], most special characters lose their special meaning."),
            ("What is a capture group?",
             "Parentheses (group) define a capture group: the content matched by the group is available separately from the full match. For example, (\\d{4})-(\\d{2})-(\\d{2}) matches 2024-03-15 and captures '2024', '03', and '15' as groups 1, 2, and 3."),
        ],
        None,
    ),

    "qr-code-generator": (
        "Utility",
        "The QR Code Generator creates scannable QR codes from any text, URL, phone number, or other data. QR codes (Quick Response codes) are two-dimensional barcodes that any smartphone camera can scan instantly. Common uses: linking printed materials to websites, sharing Wi-Fi credentials, adding contact information (vCard), creating payment links, and tracking marketing campaigns with unique URLs per printed piece.",
        [
            "Enter the URL or text you want to encode in field A.",
            "Click Run. The QR code image is generated instantly.",
            "Download or screenshot the QR code for use in print, presentations, or digital content.",
            "Test the QR code by scanning it with your phone before distributing — ensure the link is correct.",
        ],
        [
            ("What is the maximum amount of data a QR code can store?",
             "A QR code can store up to 4,296 alphanumeric characters or 7,089 numeric characters. For URLs: keep them as short as possible. Long URLs make denser QR codes that are harder to scan in poor light or at small sizes."),
            ("How small can a QR code be printed?",
             "Minimum recommended print size: 1 cm × 1 cm (0.4 inch). At this size, a modern smartphone camera can scan it from about 20 cm away. For business cards: 2 cm × 2 cm minimum. Always test print at the intended size before bulk printing."),
            ("Can I customise a QR code with a logo or colors?",
             "QR codes have built-in error correction (up to 30% of the code can be obscured and still scan). This allows embedding a small logo in the center. Custom colors are also possible — but ensure sufficient contrast between the dark modules and light background."),
        ],
        None,
    ),

    "word-counter": (
        "Writing",
        "The Word Counter counts words, characters (with and without spaces), sentences, and paragraphs in any text. It also estimates reading time based on an average adult reading speed of 200–250 words per minute. Word counts are used to meet academic submission requirements (essays, dissertations), check article length for SEO targets, comply with platform limits (LinkedIn posts, grant applications), and track writing progress.",
        [
            "Paste or type your text in field A.",
            "Click Run. The result shows word count, character count, sentence count, and estimated reading time.",
            "Character count with spaces is used for Twitter-style limits; without spaces for some academic requirements.",
            "Reading time is estimated at 230 words per minute (average adult reading speed for online content).",
        ],
        [
            ("What is a word for counting purposes?",
             "A word is typically any sequence of characters separated by whitespace. Hyphenated compounds like 'well-known' are usually counted as one word by most tools. Numbers, abbreviations, and contractions (don't, can't) each count as one word."),
            ("What is the standard word count for different content types?",
             "Blog post: 1,000–2,500 words. Long-form SEO article: 2,000–4,000 words. Twitter/X post: 280 characters. LinkedIn post: 150–300 words optimal (max 3,000). Academic essay: varies by requirement. Novel chapter: 2,000–5,000 words typically."),
            ("How is reading time estimated?",
             "Reading time = word count ÷ average reading speed. Adults read online content at 200–250 words per minute (slower than print due to screen fatigue). A 1,000-word article takes approximately 4–5 minutes to read."),
        ],
        None,
    ),

    "bmi-calculator": (
        "Health",
        "The BMI (Body Mass Index) Calculator computes BMI from height and weight using the formula BMI = weight(kg) ÷ height(m)². BMI is a population-level screening tool used to categorize weight status: underweight (<18.5), normal weight (18.5–24.9), overweight (25–29.9), and obese (≥30). It is a simple initial indicator, not a diagnostic tool — BMI does not measure body fat percentage, muscle mass, or fat distribution. Athletes and people with high muscle mass often have elevated BMI despite being healthy.",
        [
            "Enter your weight in kg in field A.",
            "Enter your height in meters in field B (e.g. 1.75 for 175 cm).",
            "Click Run. Your BMI and weight category are shown.",
            "For pounds and feet: convert first — 1 lb = 0.454 kg; 1 inch = 0.0254 m.",
        ],
        [
            ("What are the BMI categories?",
             "Underweight: below 18.5. Normal weight: 18.5–24.9. Overweight: 25–29.9. Obese class I: 30–34.9. Obese class II: 35–39.9. Obese class III (severe): 40 and above. Different thresholds apply for Asian populations (overweight begins at 23)."),
            ("Is BMI accurate for athletes?",
             "No. BMI cannot distinguish muscle from fat. A muscular athlete with low body fat may have a BMI of 28 (overweight category) because muscle is denser than fat. For athletes, body fat percentage (via DEXA scan or skinfold measurement) is more accurate."),
            ("Is BMI accurate for children?",
             "Children use a different calculation: BMI-for-age percentile, which compares BMI to other children of the same age and sex. An adult BMI calculator should not be used for children under 18."),
        ],
        None,
    ),

    "currency-converter": (
        "Finance",
        "The Currency Converter provides indicative exchange rate conversions between major world currencies. Enter an amount in one currency to see the approximate equivalent in another. Note that this tool provides reference rates — actual rates used in bank transfers, credit card transactions, and currency exchanges include a spread (margin) that varies by provider and transaction type. Always check your bank or exchange provider's actual rate before a financial transaction.",
        [
            "Enter the amount to convert in field A.",
            "Select or enter the source and target currency codes in field B (e.g. USD, EUR, GBP, INR).",
            "Click Run. The converted amount is shown at the current indicative rate.",
            "For large transactions: always verify with your bank or exchange provider — the actual rate will differ.",
        ],
        [
            ("Why does my bank's rate differ from the calculator?",
             "Banks and exchange services add a spread (their profit margin) to the mid-market rate. The mid-market rate is the midpoint between buy and sell rates. Banks typically offer rates 1–3% away from mid-market; specialized FX services (Wise, Revolut) offer rates much closer to mid-market."),
            ("What is a mid-market rate?",
             "The mid-market rate (interbank rate) is the midpoint between the highest buying price and the lowest selling price in the global currency markets at any moment. This is the 'true' exchange rate — the reference point shown by Google and financial data providers."),
            ("How often do exchange rates change?",
             "Major currency pairs change continuously during trading hours — rates fluctuate second by second in liquid markets. Rates for minor currencies or exotic pairs may be less liquid and change less frequently."),
        ],
        None,
    ),

    "age-calculator": (
        "Utility",
        "The Age Calculator finds the precise age in years, months, and days from a date of birth to today (or a custom target date). It accounts for varying month lengths and leap years. Common uses: verifying legal age thresholds (18, 21, 65), calculating age for medical forms, checking eligibility criteria with age cutoffs, and determining age for insurance or pension calculations.",
        [
            "Enter your date of birth in field A (format: YYYY-MM-DD).",
            "Click Run. Your age is shown in years, months, and remaining days.",
            "To calculate age at a specific date (not today): enter that date in field B.",
            "The result is exact — it accounts for leap years and varying month lengths.",
        ],
        [
            ("Why do I get different results from different age calculators?",
             "The main source of difference is how the calculator handles months. March 31 to April 30 is 30 days but only 1 month. Some calculators count calendar months; others count 30-day periods. This calculator uses calendar months (counting to the same day number in the next month)."),
            ("What does 'age in completed years' mean?",
             "Legal and medical age is typically expressed in completed (whole) years. A person is legally 17 until the exact calendar date of their 18th birthday — even if they are only hours away."),
            ("How is age calculated across a leap day?",
             "If you were born on February 29, your birthday in non-leap years is typically treated as either February 28 or March 1, depending on jurisdiction. This calculator uses February 28 as the non-leap birthday."),
        ],
        None,
    ),

    "tip-calculator": (
        "Finance",
        "The Tip Calculator computes the tip amount and total bill given a subtotal and tip percentage, with an option to split the total evenly between multiple people. Tipping customs vary significantly by country: in the US, 15–20% is standard for restaurant service; in the UK, 10–12.5% is typical; in Japan and Australia, tipping is not customary. This calculator handles all these scenarios including bill splits.",
        [
            "Enter the bill subtotal (before tax) in field A.",
            "Enter the tip percentage in field B (e.g. 18 for 18%).",
            "Click Run. The result shows the tip amount, total, and per-person amount.",
            "For bill splits: divide the total by the number of people at your table.",
        ],
        [
            ("Should I tip on the pre-tax or post-tax amount?",
             "Standard etiquette in the US is to tip on the pre-tax subtotal. The difference on a $50 meal is small (tip on $50 vs $54 including tax), but calculating on the subtotal is the traditional convention."),
            ("What is a standard tip percentage?",
             "US restaurants: 15% minimal, 18% standard, 20%+ for excellent service. Bars: $1–2 per drink. Hotel housekeeping: $2–5 per night. Rideshare: 15–20%. In the UK: 10–12.5%, often included as a service charge. Australia and Japan: tipping is not customary."),
            ("Is a service charge the same as a tip?",
             "No. A service charge is a mandatory fee added by the restaurant — it may or may not go to the staff, depending on the establishment's policy. A gratuity/tip is optional and typically goes directly to the server. If a service charge is already included, an additional tip is at your discretion."),
        ],
        None,
    ),

    "unit-converter": (
        "Utility",
        "The Unit Converter converts between measurement units across common categories: length (meters, feet, inches, miles, km), weight/mass (kg, pounds, ounces, grams), temperature (Celsius, Fahrenheit, Kelvin), volume (liters, gallons, cups, fluid ounces), area (square meters, acres, square feet), and speed (km/h, mph, m/s). The most common conversion needs — Celsius to Fahrenheit, kg to pounds, km to miles — are handled instantly.",
        [
            "Enter the value to convert in field A.",
            "Enter or select the source and target units in field B.",
            "Click Run. The converted value is shown.",
            "Common quick conversions: 1 kg = 2.205 lbs; 1 mile = 1.609 km; °F = (°C × 9/5) + 32.",
        ],
        [
            ("How do I convert Celsius to Fahrenheit?",
             "Formula: °F = (°C × 9/5) + 32. For a quick mental estimate: double the Celsius and add 30. 20°C = 68°F exactly; estimate: 20 × 2 + 30 = 70°F (close enough for everyday use)."),
            ("How many cups in a liter?",
             "1 liter = 4.227 US cups. 1 US cup = 236.6 ml. Note: UK/imperial cups (284 ml) and metric cups used in Australia/Canada (250 ml) differ from US cups. Recipe conversions depend on which cup standard is used."),
            ("What is the difference between mass and weight?",
             "Mass (kg, grams, pounds) is the amount of matter in an object — constant regardless of location. Weight is the gravitational force on that mass — lower on the Moon, higher on Jupiter. In everyday use the terms are used interchangeably."),
        ],
        None,
    ),

    "online-calculator": (
        "Utility",
        "The Online Calculator performs standard arithmetic operations — addition, subtraction, multiplication, division — along with percentage calculations. It works entirely in your browser with no installation required, making it available on any device with internet access. Use it for quick arithmetic when you don't have a physical calculator or want to verify a calculation.",
        [
            "Enter the first number in field A.",
            "Enter the second number in field B.",
            "Click Run for basic arithmetic. The result is shown immediately.",
            "For percentages: enter the percentage value and the base — the percentage amount is calculated.",
        ],
        [
            ("What order of operations does this calculator use?",
             "Standard mathematical order of operations (BODMAS/PEMDAS): brackets first, then exponents, then multiplication and division left-to-right, then addition and subtraction left-to-right."),
            ("How do I calculate a percentage increase?",
             "Percentage increase = ((New Value − Old Value) ÷ Old Value) × 100. For a dedicated percentage tool with more calculation modes, use the Percentage Calculator."),
            ("What is the maximum number this calculator can handle?",
             "JavaScript numbers use 64-bit floating point (IEEE 754), which handles numbers up to approximately 1.8 × 10^308. For integers, precision is exact up to 2^53 (about 9 quadrillion). Beyond this, results may be rounded."),
        ],
        None,
    ),

    "weather-checker": (
        "Utility",
        "The Weather Checker provides current weather conditions and a short forecast for any city. Enter a location and get the current temperature, weather condition, humidity, and wind speed. This is a quick reference tool for checking weather before planning outdoor activities, travel decisions, or understanding current conditions in a remote location.",
        [
            "Enter the city name in field A (e.g. London, Mumbai, New York).",
            "Click Run. Current weather conditions are displayed.",
            "For more detailed forecasts and hourly breakdowns, use a dedicated weather service.",
            "If the city name is ambiguous, add the country code (e.g. London, UK vs London, Ontario, CA).",
        ],
        [
            ("Why does this differ from my local weather app?",
             "Weather data comes from different sources and observation stations. Hyperlocal conditions (your specific neighbourhood vs the airport observation station) can differ by several degrees in temperature and vary in precipitation."),
            ("What is humidity and what percentage is comfortable?",
             "Relative humidity is the amount of water vapour in the air as a percentage of the maximum it can hold at that temperature. 30–60% is generally comfortable indoors. Above 60% feels humid and sticky; below 30% causes dry skin and static."),
            ("What does 'feels like' temperature mean?",
             "Feels-like (apparent temperature) accounts for how temperature interacts with humidity and wind. High humidity makes hot temperatures feel hotter (heat index). Wind chill makes cold temperatures feel colder. Feels-like is often more relevant to comfort than the actual air temperature."),
        ],
        None,
    ),

    "website-down-checker": (
        "Troubleshooting",
        "The Website Down Checker tests whether a website is accessible from an external server — determining if the site is down for everyone or just for you. If a website works for others but not for you, the issue is local: DNS cache, ISP routing, browser cache, firewall, or VPN. If the site is down for everyone, the problem is on the server side: hosting outage, expired domain, misconfigured DNS, DDoS attack, or certificate error.",
        [
            "Enter the full URL in field A (include https://, e.g. https://example.com).",
            "Click Run. The result shows whether the site returns a successful response from an external check.",
            "If it's 'up' from the checker but you can't access it: clear your DNS cache and try a different browser.",
            "If it's 'down' from the checker too: the problem is with the server or hosting.",
        ],
        [
            ("The site shows 'up' but I still can't access it — why?",
             "Common causes: (1) Your ISP blocks the domain. (2) Your DNS cache has a stale record — flush it with ipconfig /flushdns (Windows) or sudo dscacheutil -flushcache (Mac). (3) Your browser cache is serving an old error page — try Ctrl+Shift+R. (4) Your VPN routes traffic differently."),
            ("What does a 200 response vs 403 vs 500 mean?",
             "200: page loaded successfully. 301/302: redirect (usually fine). 403: server reachable but access denied. 404: page not found (server working, page missing). 500: server-side error. 503: server overloaded or in maintenance."),
            ("How long does a typical hosting outage last?",
             "Minor outages (maintenance, brief overload): 5–30 minutes. Major outages (hardware failure, DDoS): 1–24 hours. Check the hosting provider's status page (status.provider.com) for incident updates and estimated resolution time."),
        ],
        None,
    ),

    "dns-checker": (
        "Troubleshooting",
        "The DNS Checker looks up DNS records for a domain — A records (IPv4 address), AAAA records (IPv6), CNAME records (aliases), MX records (mail server), NS records (nameservers), and TXT records (SPF, DKIM, domain verification). Use it to verify DNS propagation after changing records, check if a domain resolves correctly, troubleshoot email delivery problems (missing SPF/DKIM), and confirm nameserver configuration.",
        [
            "Enter the domain name in field A (e.g. example.com — no https://).",
            "Click Run. The DNS records are looked up and displayed.",
            "After changing DNS records, allow 24–48 hours for full propagation (though most propagate within minutes).",
            "If you just changed your A record but DNS still shows the old IP: your DNS cache has the old value. Wait for TTL expiry or flush your local DNS cache.",
        ],
        [
            ("What is DNS propagation and how long does it take?",
             "DNS propagation is the time it takes for your updated DNS records to spread to resolvers worldwide. It depends on the TTL (Time-to-Live) set on the old record. With a 3600-second (1-hour) TTL, most resolvers update within an hour. Low TTLs (300 seconds) propagate in minutes."),
            ("What DNS records do I need for email to work?",
             "MX records tell other mail servers where to deliver email for your domain. SPF (TXT record) authorizes which servers can send email on your behalf. DKIM (TXT record with public key) cryptographically signs outgoing email. DMARC (TXT record) defines policy for failed SPF/DKIM checks. All four are required for reliable email delivery."),
            ("What is the difference between A and CNAME records?",
             "An A record maps a hostname directly to an IPv4 address. A CNAME record maps a hostname to another hostname (an alias). You cannot use a CNAME for the root domain (example.com) — only for subdomains (www.example.com)."),
        ],
        None,
    ),

    "ssl-certificate-checker": (
        "Troubleshooting",
        "The SSL Certificate Checker verifies the SSL/TLS certificate for any domain — checking whether it is valid, who issued it, when it expires, and whether the domain name matches the certificate. An expired or mismatched SSL certificate causes browsers to show security warnings that prevent most visitors from accessing the site. Common causes of certificate errors: expired certificate, wrong domain in certificate (www vs non-www), self-signed certificate used in production, and certificate chain issues.",
        [
            "Enter the domain name in field A (e.g. example.com).",
            "Click Run. The certificate details are shown: issuer, expiry date, validity, and domain coverage.",
            "If the certificate is expiring soon: renew at least 30 days before expiry to avoid lapses.",
            "Let's Encrypt certificates are free and expire every 90 days — automate renewal with Certbot.",
        ],
        [
            ("Why does my site show a certificate warning even after renewal?",
             "Common causes: (1) Browser has cached the old certificate — try Ctrl+Shift+R or a different browser. (2) The certificate chain is incomplete — intermediate certificates not installed alongside the domain certificate. (3) The old certificate is still served (web server config not updated after renewal)."),
            ("What is the difference between DV, OV, and EV certificates?",
             "DV (Domain Validation): cheapest, issued in minutes, verifies domain ownership only. OV (Organization Validation): verifies the organization's legal identity. EV (Extended Validation): most rigorous vetting; previously showed green bar in browsers but visual distinction was removed in 2019. DV is appropriate for most websites."),
            ("How do I know when my SSL certificate expires?",
             "This checker shows the expiry date. You can also check in your browser: click the padlock → Certificate → Valid until. Set a calendar reminder 60 days before expiry, or configure your hosting's auto-renewal feature."),
        ],
        None,
    ),

    "internet-speed-checker": (
        "Troubleshooting",
        "The Internet Speed Checker measures your current download speed, upload speed, and ping (latency) by performing a speed test from your browser. Results tell you whether your internet connection is performing as expected for your plan, diagnosing whether slow video streaming, downloads, or video calls are caused by your connection or the service itself. Compare results at different times of day — peak hours (evenings) often show slower speeds than off-peak.",
        [
            "Click Run to start the speed test. The test downloads and uploads a small data sample.",
            "Wait for the test to complete (10–30 seconds). Results show download Mbps, upload Mbps, and ping ms.",
            "For accurate results: test while connected directly via Ethernet (not Wi-Fi). Close other tabs and apps using internet.",
            "Run the test multiple times at different hours — single tests can vary significantly.",
        ],
        [
            ("What download speed do I need for streaming?",
             "Netflix: 3 Mbps (SD), 5 Mbps (HD), 25 Mbps (4K UHD). YouTube 4K: 20+ Mbps. Video calls (Zoom HD): 1.5–3 Mbps down and up. If multiple people stream simultaneously, multiply accordingly."),
            ("What is ping and why does it matter?",
             "Ping (latency) is the round-trip time for a packet to travel to a server and back, measured in milliseconds (ms). Lower is better: under 20ms is excellent, 20–100ms is good, 100–300ms is acceptable for most uses, above 300ms causes noticeable lag. High ping significantly impacts online gaming and video calls."),
            ("Why is my speed test faster than my real-world experience?",
             "Speed tests measure the connection to a nearby test server under ideal conditions. Real-world speeds depend on the destination server's capacity, routing between your ISP and that server, Wi-Fi signal strength, and device capability. Your ISP's advertised speed is 'up to' that value."),
        ],
        None,
    ),
}

# --- HTML content block template ------------------------------------------ #

def build_guide_html(what_it_does, steps, faqs, blog_slug):
    """Build the replacement HTML for the .tip div."""
    steps_html = "".join(
        f"<li>{s}</li>" for s in steps
    )
    faqs_html = "".join(
        f"<div class='faq-item'><h3 class='faq-q'>{q}</h3><p class='faq-a'>{a}</p></div>"
        for q, a in faqs
    )
    blog_link = ""
    if blog_slug:
        blog_link = (
            f"<div class='guide-cta'>"
            f"<a href='../../blog/{blog_slug}'>Read the full guide &rarr;</a>"
            f"</div>"
        )
    return f"""<div class="tool-guide">
    <div class="guide-section">
        <h2>How This Tool Works</h2>
        <p>{what_it_does}</p>
    </div>
    <div class="guide-section">
        <h2>How to Use</h2>
        <ol class="guide-steps">{steps_html}</ol>
    </div>
    <div class="guide-section">
        <h2>Common Questions</h2>
        <div class="faq-list">{faqs_html}</div>
    </div>
    {blog_link}
</div>"""


GUIDE_CSS = """
    .tool-guide{background:#fff;border-radius:12px;padding:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.08);margin-top:1rem}
    .guide-section{margin-bottom:1.5rem}
    .guide-section h2{font-size:1.05rem;color:#1a1a2e;margin-bottom:.6rem;padding-bottom:.3rem;border-bottom:2px solid #f0f0f5}
    .guide-section p{color:#444;font-size:.92rem;line-height:1.65;margin-bottom:.5rem}
    .guide-steps{margin-left:1.2rem;color:#444;font-size:.92rem}
    .guide-steps li{margin-bottom:.4rem;line-height:1.6}
    .faq-item{margin-bottom:1rem;padding-bottom:1rem;border-bottom:1px solid #f0f0f5}
    .faq-item:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}
    .faq-q{font-size:.95rem;color:#1a1a2e;font-weight:600;margin-bottom:.3rem}
    .faq-a{font-size:.88rem;color:#555;line-height:1.6}
    .guide-cta{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:8px;padding:.85rem 1.2rem;margin-top:1rem}
    .guide-cta a{color:#fff;text-decoration:none;font-weight:600;font-size:.9rem}
    .guide-cta a:hover{text-decoration:underline}
"""

TIP_PATTERN = re.compile(
    r'<div class="tip">.*?</div>',
    re.DOTALL
)

CSS_CLOSE_PATTERN = re.compile(r'</style>', re.IGNORECASE)


def upgrade_tool(folder_name):
    index_path = os.path.join(TOOLS_DIR, folder_name, "index.html")
    if not os.path.exists(index_path):
        return False, "index.html not found"

    if folder_name not in TOOL_CONTENT:
        return False, "no content defined"

    badge, what_it_does, steps, faqs, blog_slug = TOOL_CONTENT[folder_name]

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Inject CSS before </style>
    if GUIDE_CSS not in html:
        css_replacement = GUIDE_CSS + "\n    </style>"
        html = CSS_CLOSE_PATTERN.sub(lambda m: css_replacement, html, count=1)

    # 2. Replace the generic tip div with our guide content
    guide_html = build_guide_html(what_it_does, steps, faqs, blog_slug)
    new_html = TIP_PATTERN.sub(lambda m: guide_html, html)

    if new_html == html:
        return False, "tip div not found or already replaced"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_html)

    return True, "OK"


def main():
    success, skipped, failed = [], [], []
    all_tools = sorted(os.listdir(TOOLS_DIR))

    for folder in all_tools:
        tool_path = os.path.join(TOOLS_DIR, folder)
        if not os.path.isdir(tool_path):
            continue
        ok, msg = upgrade_tool(folder)
        if ok:
            success.append(folder)
        elif msg == "no content defined":
            skipped.append(folder)
        else:
            failed.append((folder, msg))

    print(f"\nUpgraded: {len(success)} tools")
    for t in success:
        print(f"   {t}")

    print(f"\nSkipped (no content defined yet): {len(skipped)} tools")
    for t in skipped:
        print(f"   {t}")

    if failed:
        print(f"\nFailed: {len(failed)}")
        for t, m in failed:
            print(f"   {t}: {m}")


if __name__ == "__main__":
    main()
