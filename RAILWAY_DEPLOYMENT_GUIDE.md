# 🚂 Deploy AIScribe to Railway

This guide will walk you through deploying your AIScribe application to Railway.

## Prerequisites

- [x] GitHub account with your code at https://github.com/PavanAkkineni/AIScribe.git
- [x] Railway account (https://railway.app)
- [x] Your API keys ready (from your `.env` file)

---

## Step 1: Create a Railway Account

1. Go to https://railway.app
2. Click **"Login"** or **"Start a New Project"**
3. Sign up with your GitHub account (recommended)
4. Authorize Railway to access your GitHub repositories

---

## Step 2: Create a New Project

1. Click **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `PavanAkkineni/AIScribe`
4. Railway will automatically detect it's a Python project

---

## Step 3: Configure Environment Variables

This is the **MOST IMPORTANT** step!

### How to Add Environment Variables in Railway:

1. In your Railway project dashboard, click on your service
2. Go to the **"Variables"** tab
3. Click **"+ New Variable"** for each one below

### Required Environment Variables:

Add these **11 variables** (copy values from your local `.env` file):

#### API Keys:
```
ASSEMBLYAI_API_KEY=your_assemblyai_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_API_KEY_BACKUP=your_backup_openrouter_key_here
OPENAI_API_KEY=your_openai_key_here
```

#### Email Configuration:
```
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
EMAIL_FROM_NAME=AIscribe Medical Team
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_IMAP_PORT=993
```

### Optional Variables:
```
PYTHON_VERSION=3.11.0
SECRET_KEY=your_random_secret_key_here
```

### For Persistent File Storage (Recommended):
```
UPLOAD_FOLDER=/app/uploads
```

> **Note:** You'll also need to create a Railway Volume (see Step 3.5 below)

### ⚠️ Important Notes:
- Copy **exact values** from your `.env` file (no extra spaces)
- For Gmail, use an **App Password**, not your regular password
- Generate Gmail App Password: https://myaccount.google.com/apppasswords

---

## Step 3.5: Storage Information (Optional)

By default, Railway provides **ephemeral storage** (~8GB):
- ✅ Files upload and process correctly
- ✅ Included free with your plan
- ⚠️ Files deleted on container restart/redeploy
- ✅ **Perfect for most use cases**

### Do You Need Persistent Storage?

**You DON'T need it if:**
- Just testing/demo
- Audio is processed immediately
- Results sent via email
- Okay with files being temporary

**You MIGHT need it if:**
- Building recording archive
- Need file history long-term
- Compliance requires permanent storage

### If You Need Persistent Storage:

**Volumes option might not be visible on all Railway plans.** Alternatives:

1. **Check Railway Settings** → Look for "Volumes" section
2. **Upgrade Plan** → Volumes might be on paid tiers
3. **Use Cloud Storage** → See `RAILWAY_VOLUME_SETUP.md` for S3/Cloudinary options

**For now, proceed without volumes - your app works great with ephemeral storage!**

---

## Step 4: Configure Build Settings (If Needed)

Railway usually auto-detects Python projects, but if needed:

### Build Command:
```bash
pip install -r requirements.txt
```

### Start Command:
```bash
gunicorn app:app
```

### Python Version:
Railway will use Python 3.11 (specified in environment variable)

---

## Step 5: Deploy!

1. After adding all environment variables, Railway will **automatically deploy**
2. Watch the build logs in the **"Deployments"** tab
3. Deployment usually takes 2-5 minutes

You'll see:
- ✅ Installing dependencies
- ✅ Starting application
- ✅ Deployment successful

---

## Step 6: Access Your Application

1. Once deployed, go to the **"Settings"** tab
2. Click **"Generate Domain"** under the "Domains" section
3. Railway will create a public URL like: `https://your-app.up.railway.app`
4. Click the URL to access your deployed application

---

## Step 7: Test Your Application

Visit your Railway URL and test:
- ✅ Homepage loads
- ✅ User signup/login works
- ✅ Audio transcription works
- ✅ AI summarization works (with 4-tier fallback)
- ✅ Email features work

---

## Railway Features

### Free Tier:
- $5 free credit per month
- ~500 hours of runtime
- Perfect for development and testing

### Paid Plan ($5/month):
- $5 credit + pay-as-you-go
- Better performance
- No sleep mode

### Monitoring:
- **Logs**: Real-time application logs
- **Metrics**: CPU, Memory, Network usage
- **Deployments**: View all deployment history

---

## Updating Your Application

When you make changes to your code:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```

2. **Railway Auto-Deploys**:
   - Railway detects the push automatically
   - Rebuilds and redeploys your application
   - Takes 2-5 minutes

You can also manually trigger deployments from the Railway dashboard.

---

## Environment Variables Management

### To View/Edit Variables:
1. Go to your Railway project
2. Click on your service
3. Go to **"Variables"** tab
4. Edit any variable and save
5. Railway will automatically redeploy

### To Add New Variables:
1. Click **"+ New Variable"**
2. Enter **Variable Name** and **Value**
3. Click **"Add"**
4. Application will restart automatically

---

## Troubleshooting

### Build Failed?
- Check the **"Deployments"** logs for errors
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

### Application Not Starting?
- Check environment variables are set correctly
- Review the deployment logs
- Make sure all required variables are added

### API Keys Not Working?
- Verify you copied them exactly (no extra spaces)
- Check variable names match exactly
- Redeploy after fixing: Click "Redeploy" button

### Email Features Not Working?
- Make sure you're using Gmail **App Password**, not regular password
- Verify SMTP/IMAP settings are correct
- Check Gmail allows less secure apps (if needed)

---

## Custom Domain (Optional)

To use your own domain:

1. Go to **"Settings"** → **"Domains"**
2. Click **"Custom Domain"**
3. Enter your domain name
4. Add the CNAME record to your DNS provider
5. Wait for DNS propagation (can take up to 48 hours)
6. SSL certificate is automatically provided

---

## Environment Variable Checklist

Before deploying, verify you've added all these variables:

### Required:
- [ ] `ASSEMBLYAI_API_KEY`
- [ ] `OPENROUTER_API_KEY`
- [ ] `OPENROUTER_API_KEY_BACKUP`
- [ ] `OPENAI_API_KEY`
- [ ] `EMAIL_USERNAME`
- [ ] `EMAIL_PASSWORD`
- [ ] `EMAIL_FROM_NAME`
- [ ] `EMAIL_SMTP_SERVER`
- [ ] `EMAIL_SMTP_PORT`
- [ ] `EMAIL_IMAP_SERVER`
- [ ] `EMAIL_IMAP_PORT`

### Optional but Recommended:
- [ ] `PYTHON_VERSION` (3.11.0)
- [ ] `SECRET_KEY` (random secure key)
- [ ] `UPLOAD_FOLDER` (/app/uploads) + Railway Volume

### Persistent Storage Setup:
- [ ] Created Railway Volume
- [ ] Mount path set to `/app/uploads`
- [ ] Added `UPLOAD_FOLDER=/app/uploads` variable

---

## Comparison: Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| Free Tier | $5/month credit | 750 hours/month |
| Auto-sleep | No (on free tier) | Yes (after 15 min) |
| Build Speed | Fast ⚡ | Medium |
| GitHub Integration | Excellent | Excellent |
| Environment Variables | Easy to manage | Easy to manage |
| Custom Domains | Free | Free |
| Best For | Active apps | Low-traffic apps |

---

## Security Best Practices

✅ **Already Implemented**:
- Environment variables for all secrets
- `.env` file not in version control
- `.gitignore` protecting sensitive files

✅ **Recommended**:
- Use strong `SECRET_KEY` for Flask sessions
- Regularly rotate API keys
- Monitor application logs for suspicious activity
- Enable 2FA on your Railway account

---

## Need Help?

- **Railway Documentation**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Your Repository**: https://github.com/PavanAkkineni/AIScribe

---

## Common Railway Commands (CLI - Optional)

Install Railway CLI:
```bash
npm i -g @railway/cli
```

Login:
```bash
railway login
```

Link project:
```bash
railway link
```

View logs:
```bash
railway logs
```

Set environment variable:
```bash
railway variables set KEY=VALUE
```

---

🎉 **Congratulations!** Your AIScribe application is now live on Railway!

## Quick Summary

1. ✅ Create Railway account & link GitHub
2. ✅ Select your repository
3. ✅ Add **11 environment variables** from `.env`
4. ✅ Railway auto-deploys
5. ✅ Generate domain & access your app
6. ✅ Test all features

Your app will be live at: `https://your-app.up.railway.app`

