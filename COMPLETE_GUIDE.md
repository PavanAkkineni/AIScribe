# AIscribe - Complete User Guide

## 🎯 What is AIscribe?

AIscribe is a comprehensive medical transcription and summarization system that:
1. **Records** or accepts audio files of doctor-patient conversations
2. **Transcribes** the audio with automatic speaker identification (Doctor vs Patient)
3. **Generates** professional medical summaries including:
   - Chief Complaint
   - History of Present Illness
   - Assessment/Plan
4. **Creates** Medical Decision Making (MDM) summaries with:
   - ICD-10-CM coding suggestions
   - CPT coding suggestions
   - MDM level analysis

All processing is done using cloud-hosted AI models with automatic fallback for reliability.

---

## 🚀 Getting Started (3 Steps)

### Step 1: Install Dependencies (One-time setup)

Open a terminal/command prompt in the AIscribe directory and run:

**Windows:**
```bash
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
pip3 install -r requirements.txt
```

### Step 2: Start the Application

**Windows:**
- Double-click `start.bat`, OR
- Run: `python app.py`

**Mac/Linux:**
- Make executable: `chmod +x start.sh`
- Run: `./start.sh`, OR
- Run: `python3 app.py`

You should see:
```
============================================
    AIscribe Application Starting
============================================
🌐 Starting Flask server on http://localhost:5000
```

### Step 3: Open in Browser

Navigate to: **http://localhost:5000**

---

## 📱 Using the Web Interface

### Option A: Record Audio

1. Click the **"⏺ Start Recording"** button
2. **Allow microphone access** when your browser asks
3. Have a doctor-patient conversation (or simulate one)
4. Click **"⏹ Stop Recording"** when finished
5. You'll see an audio player preview
6. Click **"🚀 Process Audio"** button

### Option B: Upload Audio File

1. Click **"Browse Files"** or drag & drop an audio file
2. Supported formats: WAV, MP3, MP4, M4A, FLAC, OGG, WEBM
3. Maximum file size: 100 MB
4. Click **"🚀 Process Audio"** button

---

## 📊 Understanding the Results

### 1. Processing Logs

Watch the logs section for real-time updates:

```
[14:30:15] 📤 Uploading audio file...
[14:30:18] 🎙️ Transcription with speaker diarization completed
[14:30:45] 🏥 Clinical summary generated
[14:31:02] 📋 Medical Decision Making summary generated
[14:31:03] ✅ Processing completed successfully!
```

**Log Colors:**
- 🔵 Blue = Information
- 🟢 Green = Success
- 🟡 Yellow = Warning
- 🔴 Red = Error

### 2. Conversation Transcript

Shows the complete conversation with speaker labels:

```
doctor: Good morning! How are you today?
patient: I'm not feeling well. I have a fever.
doctor: How long have you had the fever?
patient: About three days.
...
```

### 3. Clinical Summary

**Chief Complaint:**
Brief statement of why the patient came in (1-2 sentences)

**History of Present Illness:**
Detailed description of:
- Symptom timeline
- Severity and characteristics
- Associated symptoms
- Clinical observations

**Assessment/Plan:**
- Diagnosis
- Medications prescribed with dosages
- Treatment recommendations
- Follow-up instructions

### 4. Medical Decision Making (MDM)

**ICD-10-CM Coding:**
- Diagnostic codes with descriptions
- Justification for each code

**CPT Coding:**
- Procedure codes for billing
- Level of service (99211-99215)
- Justification based on visit complexity

**MDM Analysis:**
- Number of diagnoses/management options
- Complexity of data reviewed
- Risk level assessment
- Overall MDM level (Straightforward/Low/Moderate/High)

**Consistency Check:**
- Verification that codes match documentation

---

## 🤖 AI Models & Fallback System

AIscribe uses two AI models with automatic failover:

### Primary Model
**Meta Llama 3.3 70B Instruct**
- High-quality medical text generation
- Excellent understanding of clinical context
- Free tier via OpenRouter

### Fallback Model
**DeepSeek R1 Distill Llama 70B**
- Automatically used if primary model fails
- Ensures reliability and uptime
- Free tier via OpenRouter

**How Fallback Works:**
1. System tries primary model first
2. If rate limit or error occurs → automatically switches to fallback
3. Logs show which model was used
4. No user intervention required

---

## 💡 Tips for Best Results

### Audio Quality
✅ **DO:**
- Use a quiet environment
- Speak clearly at moderate pace
- Use external microphone if possible
- Keep speaker-to-mic distance consistent

❌ **DON'T:**
- Record in noisy environments
- Speak too fast or mumble
- Allow speakers to talk over each other
- Use poor quality built-in mics

### Conversation Structure
✅ **DO:**
- Start with greetings
- Clearly state chief complaint
- Discuss symptoms in detail
- Include physical exam findings
- State diagnosis explicitly
- Mention specific medications and dosages
- Include follow-up instructions

❌ **DON'T:**
- Skip important details
- Use vague descriptions ("some medicine")
- Omit follow-up plans
- Rush through the conversation

### Medical Terminology
✅ **DO:**
- Use proper medical terms when appropriate
- Spell out medication names clearly
- Include vital signs if taken
- Mention specific tests or procedures

❌ **DON'T:**
- Use excessive slang
- Be too informal
- Skip medication details

---

## 🔍 Troubleshooting

### Problem: Microphone Not Working

**Solutions:**
1. Check browser permissions (Chrome/Edge recommended)
2. Allow microphone access when prompted
3. Try a different browser
4. Use upload option instead

### Problem: Upload Fails

**Check:**
- File format (must be audio)
- File size (< 100 MB)
- File is not corrupted

**Solutions:**
- Convert file to MP3 or WAV
- Compress large files
- Try a different file

### Problem: "Rate Limit" Error

**What it means:**
Too many requests to AI model in short time

**Solutions:**
- Wait 1-2 minutes and try again
- System will automatically try fallback model
- Check logs to see which model was used

### Problem: Poor Transcription Quality

**Causes:**
- Low audio quality
- Heavy background noise
- Multiple speakers talking simultaneously
- Unclear speech

**Solutions:**
- Re-record in quieter environment
- Speak more clearly
- Ensure speakers take turns
- Upload higher quality audio file

### Problem: Inaccurate Medical Coding

**Causes:**
- Incomplete medical information in conversation
- Vague symptom descriptions
- Missing diagnosis statement

**Solutions:**
- Include more specific medical details
- State diagnosis clearly
- Mention relevant test results
- Specify medications with dosages

---

## 📁 File Management

### Where Files Are Stored

All processed files are saved in the `uploads/` directory:

```
uploads/
├── 20241114_143015_recording.webm        # Audio file
├── 20241114_143015_results.json          # Complete results
├── 20241114_150230_patient_audio.mp3     # Another audio
└── 20241114_150230_results.json          # Its results
```

### Results JSON Structure

Each `_results.json` file contains:
```json
{
  "timestamp": "2024-11-14T14:30:15",
  "filename": "recording.webm",
  "transcription": { ... },
  "conversation_text": "doctor: Hello...",
  "clinical_summary": {
    "chief_complaint": "...",
    "history_of_present_illness": "...",
    "assessment_plan": "..."
  },
  "mdm_summary": {
    "mdm_summary": "Step 1: ICD-10-CM..."
  }
}
```

### Accessing Saved Results

1. Go to `uploads/` folder
2. Open any `_results.json` file
3. View in any text editor or JSON viewer

---

## 🔒 Security & Privacy

### ⚠️ Important Notes

**Current Setup (Development):**
- API keys are in `config.py` file
- No user authentication
- HTTP (not HTTPS)
- Suitable for testing and development ONLY

**For Production Use:**
- Move API keys to environment variables
- Implement user authentication
- Use HTTPS/SSL encryption
- Add access controls
- Follow HIPAA compliance if handling real patient data
- Encrypt stored data
- Implement audit logging

### API Keys

**Location:** `config.py`

```python
ASSEMBLYAI_API_KEY = "your_key_here"
OPENROUTER_API_KEY = "your_key_here"
```

**Protecting Your Keys:**
1. Never commit `config.py` to public repositories
2. Use `.gitignore` (already included)
3. For production, use environment variables:

```python
import os
ASSEMBLYAI_API_KEY = os.getenv('ASSEMBLYAI_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
```

---

## 🛠️ Advanced Usage

### Verifying Setup

Run the setup verification script:

```bash
python test_setup.py
```

Expected output:
```
✓ Flask version: 3.0.0
✓ AssemblyAI installed
✓ OpenAI library installed
✓ Requests library installed
✓ AssemblyAI API key configured
✓ OpenRouter API key configured
✓ TranscriptionService initialized
✓ AISummarizationService initialized
✓ All tests passed! AIscribe is ready to use.
```

### Viewing Logs

Application logs are saved as:
- Filename: `aiscribe_YYYYMMDD.log`
- Example: `aiscribe_20241114.log`

View logs:
```bash
# Windows
type aiscribe_20241114.log

# Mac/Linux
cat aiscribe_20241114.log

# Or open in any text editor
```

### API Endpoints

For programmatic access:

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Process Audio:**
```bash
curl -X POST http://localhost:5000/api/process-audio \
  -F "audio=@path/to/audio.mp3"
```

**Get Results:**
```bash
curl http://localhost:5000/api/results/20241114_143015_results.json
```

---

## 📚 Additional Resources

- **[README.md](README.md)** - Quick overview
- **[QUICKSTART.md](QUICKSTART.md)** - Fast setup guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture details
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - File organization
- **[EXAMPLES.md](EXAMPLES.md)** - Usage examples with sample outputs

---

## ❓ FAQ

**Q: Can I use my own API keys?**
A: Yes! Edit `config.py` and replace the keys with your own.

**Q: How long does processing take?**
A: Typically 30-90 seconds depending on audio length and AI model response time.

**Q: Can I process multiple files at once?**
A: Currently no, but you can process them sequentially.

**Q: What audio formats are supported?**
A: WAV, MP3, MP4, M4A, FLAC, OGG, WEBM

**Q: Is my data stored permanently?**
A: Audio files and results are saved locally in the `uploads/` folder. Delete them manually if needed.

**Q: Can I customize the summary format?**
A: Yes! Edit the prompts in `ai_summarization_service.py`

**Q: Does it work offline?**
A: No, it requires internet connection for AssemblyAI and OpenRouter APIs.

**Q: How accurate is the transcription?**
A: AssemblyAI provides 90%+ accuracy with clear audio. Speaker diarization works best with distinct voices.

**Q: Can I use this for real patient data?**
A: Only after implementing proper security measures, HIPAA compliance, and consulting with legal/compliance teams.

---

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** - Most errors are logged with details
2. **Run test script** - `python test_setup.py`
3. **Review documentation** - QUICKSTART.md, ARCHITECTURE.md
4. **Check API status** - AssemblyAI and OpenRouter service status

---

## 🎓 Learning Resources

### Understanding Medical Coding
- [ICD-10-CM Basics](https://www.cdc.gov/nchs/icd/icd-10-cm.htm)
- [CPT Coding Guide](https://www.ama-assn.org/practice-management/cpt)

### Speech Recognition
- [AssemblyAI Documentation](https://www.assemblyai.com/docs)
- [Speaker Diarization Guide](https://www.assemblyai.com/docs/audio-intelligence/speaker-diarization)

### AI Models
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Llama Model Information](https://llama.meta.com/)

---

## ✅ Quick Reference

### Start Application
```bash
# Windows
python app.py

# Mac/Linux
python3 app.py
```

### Access Web Interface
```
http://localhost:5000
```

### Test Setup
```bash
python test_setup.py
```

### View Logs
Check file: `aiscribe_YYYYMMDD.log`

### Stop Application
Press `Ctrl+C` in terminal

---

**Congratulations! You're ready to use AIscribe!** 🎉

Start by running `python app.py` and opening http://localhost:5000 in your browser.



