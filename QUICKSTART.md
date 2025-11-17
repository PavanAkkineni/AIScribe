# AIscribe - Quick Start Guide

## 🚀 Getting Started

### Step 1: Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Verify API Keys

The API keys are pre-configured in `config.py`:
- **AssemblyAI API Key**: For speech-to-text with speaker diarization
- **OpenRouter API Key**: For AI summarization models

### Step 3: Start the Application

Run the Flask server:

```bash
python app.py
```

You should see:
```
🚀 AIscribe Application Starting
🌐 Starting Flask server on http://localhost:5000
```

### Step 4: Open in Browser

Navigate to:
```
http://localhost:5000
```

## 📝 Using AIscribe

### Option 1: Record Audio

1. Click **"Start Recording"** button
2. Allow microphone access when prompted
3. Have a mock doctor-patient conversation
4. Click **"Stop Recording"** when done
5. Click **"Process Audio"** button

### Option 2: Upload Audio File

1. Click **"Browse Files"** or drag & drop an audio file
2. Supported formats: WAV, MP3, MP4, M4A, FLAC, OGG, WEBM
3. Click **"Process Audio"** button

## 🔍 What Happens Next?

The application will:

1. **Transcribe** the audio with speaker labels (Doctor/Patient)
2. **Generate Clinical Summary** with:
   - Chief Complaint
   - History of Present Illness
   - Assessment/Plan
3. **Generate Medical Decision Making** with:
   - ICD-10-CM Coding
   - CPT Coding
   - MDM Level Analysis

## 📊 Viewing Results

Results are displayed in three sections:

### 1. Conversation Transcript
Speaker-labeled dialogue:
```
doctor: Hi, good morning
patient: Good morning, how are you?
...
```

### 2. Clinical Summary
Structured medical note with three key sections

### 3. Medical Decision Making
Detailed coding analysis with ICD-10 and CPT codes

## 🤖 AI Models

The system uses two models with automatic fallback:

1. **Primary**: Meta Llama 3.3 70B Instruct
2. **Fallback**: DeepSeek R1 Distill Llama 70B

If the primary model hits rate limits, it automatically switches to the fallback model.

## 📋 Processing Logs

Watch the **Processing Logs** section for real-time updates:
- 🔵 Info: General progress updates
- 🟢 Success: Completed steps
- 🔴 Error: Issues encountered
- 🟡 Warning: Important notices

## 💾 Saved Results

All results are automatically saved to `uploads/` directory as JSON files with timestamps for future reference.

## ⚠️ Troubleshooting

### Microphone not working
- Check browser permissions
- Use Chrome/Edge for best compatibility
- Try uploading a file instead

### Rate limit errors
- The system will automatically try the fallback model
- Check the logs for which model was used
- Wait a few minutes if both models are rate-limited

### Upload fails
- Check file format (must be audio)
- Ensure file size < 100MB
- Try a different audio format

## 🎯 Tips for Best Results

1. **Clear Audio**: Ensure good audio quality with minimal background noise
2. **Distinct Speakers**: Have clear separation between doctor and patient voices
3. **Medical Context**: Include relevant medical terminology for accurate coding
4. **Complete Conversations**: Include chief complaint, symptoms, and treatment plan

## 🔒 Security Note

For production use:
- Move API keys to environment variables
- Add authentication to the web interface
- Use HTTPS
- Implement user access controls

---

**Need help?** Check the logs for detailed error messages or review the README.md for more information.



