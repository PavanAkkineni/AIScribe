# 🗂️ Railway Persistent Storage Setup

This guide will help you set up persistent file storage on Railway so your audio files and recordings don't disappear on restarts.

## Why You Need This

By default, Railway uses **ephemeral storage** which means:
- ❌ Files are deleted on restart/redeploy
- ❌ Recording history is lost
- ❌ No permanent storage

With **Railway Volumes**, you get:
- ✅ Files persist across restarts
- ✅ Recording history preserved
- ✅ Permanent storage
- 💰 ~$0.25/GB/month

---

## 📋 Step-by-Step Setup

### Step 1: Create a Volume in Railway

1. **Go to your Railway project**: https://railway.app
2. **Click on your service** (AIscribe)
3. **Go to "Settings" tab**
4. **Scroll down to "Volumes" section**
5. **Click "+ New Volume"**

### Step 2: Configure Volume Settings

Fill in the following:

**Mount Path:**
```
/app/uploads
```

**Volume Name:** (optional, Railway auto-generates)
```
aiscribe-uploads
```

**Initial Size:** (start small, auto-scales)
```
1 GB
```

Click **"Add Volume"**

### Step 3: Add Environment Variable

1. **Go to "Variables" tab**
2. **Click "+ New Variable"**
3. Add:
   ```
   UPLOAD_FOLDER=/app/uploads
   ```
4. Click **"Add"**

### Step 4: Redeploy

Railway will automatically redeploy with the new volume mounted.

---

## ✅ Verification

After deployment, test:

1. **Upload an audio file** through your app
2. **Check Railway logs** for:
   ```
   💾 Saving file to: /app/uploads/PATIENT_ID/timestamp_file.mp3
   ✓ File saved successfully
   ```
3. **Trigger a redeploy** (Settings → Redeploy)
4. **Check if files still exist** after redeploy

---

## 📊 Volume Pricing

| Storage Used | Monthly Cost |
|--------------|--------------|
| 1 GB | $0.25 |
| 5 GB | $1.25 |
| 10 GB | $2.50 |
| 25 GB | $6.25 |

**Note:** Railway charges only for what you use, prorated by the hour.

---

## 🔍 How It Works

### Before (Ephemeral Storage):
```
Railway Container
├── /app/
│   ├── uploads/ (temporary, deleted on restart)
│   │   └── patient_files/
│   ├── app.py
│   └── ...
```

### After (Persistent Volume):
```
Railway Container
├── /app/
│   ├── uploads/ → mounted to persistent volume
│   │   └── patient_files/ (permanent!)
│   ├── app.py
│   └── ...

Persistent Volume (survives restarts)
└── patient_files/
    ├── P123/
    │   ├── audio.mp3
    │   └── results.json
    └── P456/
        └── ...
```

---

## 🛠️ Troubleshooting

### Volume Not Mounting?

**Check:**
1. Mount path is exactly `/app/uploads` (case-sensitive)
2. Environment variable `UPLOAD_FOLDER=/app/uploads` is set
3. Railway has redeployed after adding volume

**View logs:**
```bash
# Check if folder is created
ls -la /app/uploads

# Check volume mount
df -h | grep uploads
```

### Files Still Disappearing?

**Verify:**
1. Volume is in "Active" state in Railway dashboard
2. Environment variable is correct (no typos)
3. Application is using the right path:
   ```python
   print(f"Upload folder: {UPLOAD_FOLDER}")
   ```

### Out of Space?

**Expand volume:**
1. Go to Settings → Volumes
2. Click on your volume
3. Increase size
4. Railway will auto-scale without downtime

---

## 🎯 Alternative: Use S3 for Cheaper Storage

If you need lots of storage (>50GB), AWS S3 is cheaper:

### AWS S3 Pricing:
- $0.023/GB/month (~10x cheaper than Railway)
- Better for large-scale deployments
- Requires code changes

### Quick S3 Setup:

1. **Install boto3:**
   ```bash
   pip install boto3
   ```

2. **Add to requirements.txt:**
   ```
   boto3==1.34.0
   ```

3. **Add environment variables:**
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_S3_BUCKET=aiscribe-uploads
   AWS_REGION=us-east-1
   ```

4. **Would need code changes** to upload to S3 instead of disk

---

## 📝 Backup Strategy (Optional)

For critical data, consider:

1. **Automated backups** of Railway volume
2. **Sync to S3** periodically
3. **Database for metadata** (file paths, patient info)
4. **Separate storage** for different data types:
   - Audio files → Railway Volume or S3
   - Transcriptions → Database
   - Emails → Database

---

## 🚀 Production Recommendations

For production deployment:

### Small Scale (<10GB storage)
✅ **Use Railway Volume**
- Simple setup
- No code changes
- Built-in backups

### Medium Scale (10-50GB)
✅ **Railway Volume** or **Cloudinary**
- Railway: More control
- Cloudinary: Better for media

### Large Scale (>50GB)
✅ **AWS S3** or **Google Cloud Storage**
- Much cheaper per GB
- Industry standard
- Better performance at scale

---

## 📊 Summary

| Feature | Ephemeral | Railway Volume | AWS S3 |
|---------|-----------|----------------|--------|
| **Setup Time** | 0 min | 5 min | 30 min |
| **Persistence** | ❌ No | ✅ Yes | ✅ Yes |
| **Cost** | Free | $0.25/GB | $0.023/GB |
| **Code Changes** | None | None | Required |
| **Best For** | Testing | Production | Scale |

---

## ✅ Your Action Items

1. [ ] Create Railway Volume
2. [ ] Set mount path: `/app/uploads`
3. [ ] Add environment variable: `UPLOAD_FOLDER=/app/uploads`
4. [ ] Wait for automatic redeploy
5. [ ] Test file upload
6. [ ] Verify files persist after redeploy

---

## 🎉 Done!

Once set up, your files will persist across:
- ✅ Restarts
- ✅ Redeployments
- ✅ Container crashes
- ✅ Code updates

Your recording history will be safe and permanent! 🔒

---

Need help? Check Railway docs: https://docs.railway.app/reference/volumes

