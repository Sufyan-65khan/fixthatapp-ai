# Troubleshooting Guide: Shopify Store Not Loading

## Problem Description
Your Shopify store may fail to load for customers, show error pages, have extremely slow loading times, or display broken layouts. This directly impacts your sales and customer experience.

## Possible Causes
1. **Shopify platform outage**: Shopify's servers may be experiencing issues.
2. **Theme issues**: A broken or incompatible theme can prevent loading.
3. **App conflicts**: Third-party Shopify apps may cause problems.
4. **Heavy images**: Large, unoptimized images slow down page loading.
5. **DNS issues**: Domain configuration problems can prevent access.
6. **Custom code errors**: JavaScript or Liquid template errors.

## Step-by-Step Fixes

### Fix 1: Check Shopify Status
- Visit status.shopify.com to check for platform issues.
- If Shopify is down, wait for them to resolve it.
- Your store data is safe during outages.

### Fix 2: Preview Without Apps
- Temporarily disable third-party apps one by one.
- Check if the store loads after each disable.
- This helps identify which app is causing the problem.

### Fix 3: Switch to Default Theme
- Go to Online Store > Themes.
- Activate a default Shopify theme (like Dawn) temporarily.
- If the store loads with the default theme, your custom theme has issues.

### Fix 4: Optimize Images
- Compress images using tools like TinyPNG before uploading.
- Use WebP format for better compression.
- Keep product images under 500KB each.

### Fix 5: Check Custom Code
- Review any custom JavaScript or Liquid code you've added.
- Check the browser console (F12 > Console) for error messages.
- Temporarily remove custom code to see if the issue resolves.

### Fix 6: Verify Domain Settings
- Go to Settings > Domains in Shopify admin.
- Make sure your domain is properly connected.
- If using a custom domain, verify DNS records are correct.

## When to Contact Support
If your store still doesn't load, contact Shopify support through the admin panel: Settings > Support. You can also visit help.shopify.com.

## FAQ
Q: Does Shopify go down often?
A: Shopify has excellent uptime (99.99%+). Major outages are very rare, but brief degradations can occur during high-traffic events like Black Friday.

Q: Will I lose sales if my Shopify store goes down?
A: During Shopify outages, orders cannot be processed. However, once the service is restored, all your store data remains intact.

Q: How can I make my Shopify store load faster?
A: Optimize images, minimize apps, use a lightweight theme, enable lazy loading for images, and minimize custom scripts.

Q: Can I host Shopify on my own server?
A: No, Shopify is a fully hosted platform. You cannot self-host a Shopify store. Consider alternatives like WooCommerce if you want self-hosting.
