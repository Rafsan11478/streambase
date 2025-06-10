# StreamBase - Vercel Deployment Guide

## Prerequisites
- Vercel account (https://vercel.com)
- GitHub repository for your project

## Step 1: Prepare for Vercel Deployment

1. Create a `vercel.json` file in your project root:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

2. Create a `requirements.txt` file:
```
Flask==2.3.3
Werkzeug==2.3.7
gunicorn==21.2.0
```

## Step 2: GitHub Repository Setup

1. Push your project to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/streambase.git
git push -u origin main
```

## Step 3: Deploy to Vercel

1. Go to https://vercel.com and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect it's a Python project
5. Click "Deploy"

## Step 4: Environment Variables (Optional)

In Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add `SESSION_SECRET` with a secure random string

## Step 5: Custom Domain (Optional)

1. In project settings, go to "Domains"
2. Add your custom domain
3. Follow DNS configuration instructions

## Updating Accounts - GitHub Workflow

### Method 1: Direct File Edit (Recommended)
1. Go to your GitHub repository
2. Navigate to `data/services.json`
3. Click the edit (pencil) icon
4. Update your services and accounts
5. Commit changes
6. Vercel will automatically redeploy

### Method 2: Admin Panel + Manual Sync
1. Use the admin panel to update accounts locally
2. Copy the generated environment code
3. Update your GitHub repository with new `data/services.json`
4. Push changes to trigger redeploy

### Method 3: GitHub API (Advanced)
You can use the GitHub API to programmatically update the services.json file:

```bash
# Get current file
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
     https://api.github.com/repos/YOUR_USERNAME/streambase/contents/data/services.json

# Update file (you'll need the SHA from the previous response)
curl -X PUT \
     -H "Authorization: token YOUR_GITHUB_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Update accounts",
       "content": "BASE64_ENCODED_CONTENT",
       "sha": "CURRENT_FILE_SHA"
     }' \
     https://api.github.com/repos/YOUR_USERNAME/streambase/contents/data/services.json
```

## Automatic Redeployment
- Vercel automatically redeploys when you push to your main branch
- Changes typically go live within 30-60 seconds
- You can monitor deployments in the Vercel dashboard

## File Structure for Vercel
```
streambase/
├── main.py              # Entry point
├── app.py               # Flask application
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
├── data/
│   ├── services.json    # Your services data
│   └── settings.json    # App settings
├── static/              # CSS, JS, images
├── templates/           # HTML templates
└── DEPLOYMENT.md        # This guide
```

## Tips for Frequent Updates

1. **Bookmark your repo**: Keep your GitHub repository bookmarked for quick access
2. **Use GitHub mobile app**: Edit files directly from your phone
3. **Create a simple script**: Make a local script that updates the JSON and pushes to GitHub
4. **Use GitHub Actions**: Set up automated workflows for regular updates

## Troubleshooting

### Build Fails
- Check `requirements.txt` has correct dependencies
- Ensure `main.py` exists and imports properly
- Check Vercel build logs for specific errors

### Static Files Not Loading
- Verify files are in the `static/` directory
- Check file paths in templates use `url_for('static', filename='...')`

### Data Not Persisting
- Remember: Vercel is serverless, data resets on each deployment
- All persistent data must be in your GitHub repository
- Update `data/services.json` in your repo, not through the admin panel

## Security Notes
- Never commit sensitive API keys to GitHub
- Use Vercel environment variables for secrets
- The admin email check provides basic protection
- Consider adding rate limiting for production use

Your StreamBase website will be available at: `https://your-project-name.vercel.app`