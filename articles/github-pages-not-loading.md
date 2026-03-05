# Troubleshooting Guide: GitHub Pages Not Loading

## Problem Description
Your GitHub Pages website may fail to load, show a 404 error, display a blank page, or not update when you push new code. Custom domains may also stop working.

## Possible Causes
1. **Build failed**: Jekyll or other static site generators may have build errors.
2. **Wrong branch configured**: GitHub Pages may be pointing to the wrong branch.
3. **Missing index.html**: The root directory must have an index.html file.
4. **Custom domain DNS issues**: DNS records may be misconfigured.
5. **Repository settings**: Pages may not be enabled or is set to private.

## Step-by-Step Fixes

### Fix 1: Check GitHub Pages Settings
- Go to your repository > Settings > Pages.
- Verify the correct branch and folder are selected.
- Make sure the source is set to "Deploy from a branch".

### Fix 2: Check Build Status
- Go to your repository > Actions tab.
- Look for the "pages build and deployment" workflow.
- If it failed, click on it to see the error details.

### Fix 3: Verify index.html Exists
- Make sure you have an index.html file in the root of your selected branch/folder.
- The file name must be exactly "index.html" (lowercase).
- Check that the file isn't empty.

### Fix 4: Check Custom Domain
- Verify your CNAME file contains the correct domain.
- Check DNS records point to GitHub's servers (185.199.108-111.153).
- Wait up to 30 minutes for DNS changes to propagate.
- Enable "Enforce HTTPS" in Pages settings.

### Fix 5: Clear Browser Cache
- Hard refresh with Ctrl+Shift+R.
- Try viewing your site in an incognito window.
- GitHub Pages can cache old versions for up to 10 minutes.

### Fix 6: Redeploy
- Make a minor change to any file and push a new commit.
- This triggers a new build and deployment.
- Check the Actions tab to monitor the deployment.

## When to Contact Support
If your site still doesn't load, contact GitHub support at support.github.com or check githubstatus.com for outages.

## FAQ
Q: How long does GitHub Pages take to deploy?
A: Usually 1-5 minutes. First deployments or those with many files may take longer.

Q: Is GitHub Pages free?
A: Yes, for public repositories. GitHub Pro users can also use Pages with private repositories.

Q: Can I use a custom domain with GitHub Pages?
A: Yes, add a CNAME file to your repository and configure DNS records with your domain registrar.

Q: Why does my site show an old version?
A: GitHub Pages caches content. Wait 10 minutes, clear your browser cache, or check the Actions tab to make sure the latest deployment succeeded.
