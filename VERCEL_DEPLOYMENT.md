# StreamBase - Vercel Deployment Instructions

## Quick Setup

### 1. Create Required Files
Add these files to your project root:

**vercel.json**
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

**requirements.txt**
```
Flask==3.1.1
Werkzeug==3.1.3
gunicorn==23.0.0
```

### 2. Push to GitHub
```bash
git init
git add .
git commit -m "StreamBase initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/streambase.git
git push -u origin main
```

### 3. Deploy to Vercel
1. Go to vercel.com and sign in with GitHub
2. Click "New Project"
3. Select your streambase repository
4. Click "Deploy"

Your site will be live at: `https://your-project-name.vercel.app`

## Updating Accounts - 3 Methods

### Method 1: GitHub Web Interface (Easiest)
1. Go to your GitHub repo
2. Click on `data/services.json`
3. Click the pencil icon to edit
4. Update your accounts
5. Commit changes
6. Vercel auto-deploys in 30 seconds

### Method 2: Local Admin Panel
1. Run admin panel locally
2. Add/edit services and accounts
3. Copy the generated environment code
4. Update GitHub repo manually
5. Push changes

### Method 3: GitHub Mobile App
1. Install GitHub mobile app
2. Navigate to your repo
3. Edit `data/services.json` directly
4. Commit from your phone
5. Instant deployment

## Account Format Examples

**Credentials:**
```
user@example.com|password123|2024-12-31|Premium
netflix@test.com|mypass||Standard
justuser|justpass
```

**Cookies:**
```
session_id=abc123; user_token=xyz789
auth_cookie=def456; preference=premium
```

## File Structure
```
streambase/
├── main.py
├── app.py
├── vercel.json
├── requirements.txt
├── data/
│   └── services.json    # Update this file to change accounts
├── static/
├── templates/
└── VERCEL_DEPLOYMENT.md
```

## Pro Tips

- **Bookmark your repo**: Quick access for account updates
- **Use GitHub mobile**: Update accounts from anywhere
- **Monitor deployments**: Check vercel.com dashboard for status
- **Custom domain**: Add in Vercel project settings
- **Environment variables**: Set SESSION_SECRET in Vercel dashboard

## Troubleshooting

**Build fails**: Check requirements.txt matches exactly
**Static files missing**: Ensure they're in static/ folder
**Admin panel changes don't persist**: Update GitHub repo, not local files
**Site not updating**: Wait 60 seconds, clear browser cache

Your StreamBase is now ready for Vercel! Update accounts anytime by editing the GitHub repository.