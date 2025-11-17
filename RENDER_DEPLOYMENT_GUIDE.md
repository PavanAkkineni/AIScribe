# 🚀 Deploy AIScribe to Render

This guide will walk you through deploying your AIScribe application to Render.

## Prerequisites

- [x] GitHub account with your code pushed to https://github.com/PavanAkkineni/AIScribe.git
- [x] Render account (free tier available at https://render.com)
- [x] Your API keys ready (from your `.env` file)

---

## Step 1: Create a Render Account

1. Go to https://render.com
2. Click **"Get Started"** or **"Sign Up"**
3. Sign up with your GitHub account (recommended for easy deployment)
4. Authorize Render to access your GitHub repositories

---

## Step 2: Create a New Web Service

1. Once logged in, click **"New +"** button in the top right
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - If not already connected, click **"Connect GitHub"**
   - Find and select your repository: `PavanAkkineni/AIScribe`
   - Click **"Connect"**

---

## Step 3: Configure Your Web Service

Fill in the following settings:

### Basic Settings:
- **Name**: `aiscribe-api` (or any name you prefer)
- **Region**: Choose closest to your location (e.g., `Oregon (US West)`)
- **Branch**: `main`
- **Root Directory**: Leave empty (blank)
- **Runtime**: `Python 3`

### Build & Deploy Settings:
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```

- **Start Command**: 
  ```
  gunicorn app:app
  ```

### Instance Type:
- Select **"Free"** (or upgrade to a paid plan for better performance)

---

## Step 4: Add Environment Variables

This is the **MOST IMPORTANT** step! Scroll down to the **"Environment Variables"** section and add the following:

Click **"Add Environment Variable"** for each one:

### Required API Keys:

1. **Variable Name**: `ASSEMBLYAI_API_KEY`
   - **Value**: `your_assemblyai_api_key_here`
   - Get your key from: https://www.assemblyai.com/

2. **Variable Name**: `OPENROUTER_API_KEY`
   - **Value**: `your_openrouter_api_key_here`
   - Get your key from: https://openrouter.ai/keys

3. **Variable Name**: `OPENROUTER_API_KEY_BACKUP`
   - **Value**: `your_backup_openrouter_api_key_here`
   - (Optional but recommended for redundancy)

4. **Variable Name**: `OPENAI_API_KEY`
   - **Value**: `your_openai_api_key_here`
   - Get your key from: https://platform.openai.com/api-keys

> **💡 Important:** Use your actual API key values from your local `.env` file. Never commit these keys to version control!

### Optional (But Recommended):

5. **Variable Name**: `PYTHON_VERSION`
   - **Value**: `3.11.0`

6. **Variable Name**: `SECRET_KEY`
   - **Value**: Generate a secure random key (you can use: https://randomkeygen.com/)

---

## Step 5: Deploy!

1. Click **"Create Web Service"** button at the bottom
2. Render will now:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start your Flask application with Gunicorn
3. Wait for the deployment to complete (usually 2-5 minutes)

You'll see logs showing the build progress.

---

## Step 6: Access Your Deployed Application

Once deployment is complete:

1. You'll see a green **"Live"** status
2. Your app URL will be shown at the top (e.g., `https://aiscribe-api.onrender.com`)
3. Click the URL to access your deployed AIScribe application!

---

## Step 7: Test Your Application

Visit your Render URL and test:
- ✅ Homepage loads
- ✅ User signup/login works
- ✅ Audio transcription works
- ✅ AI summarization works
- ✅ All 4 fallback models are available

---

## Important Notes

### Free Tier Limitations:
- ⚠️ **Free tier sleeps after 15 minutes of inactivity**
- First request after sleep will take 30-60 seconds to wake up
- 750 hours/month free (enough for continuous running)

### Upgrade Benefits ($7/month):
- ✅ No sleeping - always available
- ✅ Better performance
- ✅ More memory and CPU

### Keeping Free Tier Active:
If you want to keep the free tier active 24/7, you can:
1. Use a service like **UptimeRobot** (free) to ping your app every 5 minutes
2. Set it to ping: `https://your-app.onrender.com/health` (if you add a health endpoint)

---

## Troubleshooting

### Build Failed?
- Check the logs in Render dashboard
- Ensure `requirements.txt` is correct
- Verify Python version compatibility

### Application Not Starting?
- Check environment variables are set correctly
- Review the deployment logs
- Make sure all required API keys are added

### API Keys Not Working?
- Verify you copied them exactly (no extra spaces)
- Check the variable names match exactly
- Redeploy after fixing: **Manual Deploy → Clear build cache & deploy**

---

## Monitoring Your Application

Render provides:
- 📊 **Metrics**: CPU, Memory usage
- 📝 **Logs**: Real-time application logs
- 🔔 **Alerts**: Email notifications for issues

Access these from your Render dashboard.

---

## Updating Your Application

When you make changes to your code:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```

2. **Render Auto-Deploys**:
   - Render automatically detects the push
   - Rebuilds and redeploys your application
   - Takes 2-5 minutes

You can also manually trigger deployments from the Render dashboard.

---

## Custom Domain (Optional)

To use your own domain:

1. Go to your service settings in Render
2. Click **"Custom Domain"**
3. Follow the instructions to add your domain
4. Update DNS records as shown
5. SSL certificate is automatically provided (free)

---

## Security Best Practices

✅ **Already Implemented**:
- Environment variables for API keys
- `.env` file not in version control
- `.gitignore` protecting sensitive files

✅ **Recommended Additions**:
- Change the Flask `SECRET_KEY` to a strong random value
- Set up monitoring and alerts
- Regularly update dependencies
- Enable HTTPS only (Render does this by default)

---

## Need Help?

- **Render Documentation**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Your Repository**: https://github.com/PavanAkkineni/AIScribe

---

## Summary Checklist

- [ ] Created Render account
- [ ] Connected GitHub repository
- [ ] Configured web service settings
- [ ] Added all environment variables (4 API keys)
- [ ] Clicked "Create Web Service"
- [ ] Waited for deployment to complete
- [ ] Tested the live URL
- [ ] Application is working correctly

---

🎉 **Congratulations!** Your AIScribe application is now live on Render!

