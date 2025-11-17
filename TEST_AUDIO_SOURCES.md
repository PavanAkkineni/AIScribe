# Test Audio Sources for AIscribe

## 🎯 Where to Get Doctor-Patient Audio Clips

### Option 1: Free Medical Audio Resources

#### 1. **MedEdPORTAL (iCollaborative)**
- **URL**: https://www.mededportal.org/
- **Content**: Educational medical simulations and patient encounters
- **Format**: Various audio/video formats
- **License**: Educational use
- **Note**: May require free registration

#### 2. **YouTube Medical Education Channels**
Download using tools like `yt-dlp`:
- **Channels to search**:
  - "Medical simulation patient encounter"
  - "OSCE practice consultation"
  - "Medical student patient interview practice"
  - "Clinical skills assessment"
- **Tools**: Use `yt-dlp` or online YouTube to MP3 converters
- **Command**: `yt-dlp -x --audio-format mp3 [YouTube_URL]`

#### 3. **Freesound.org**
- **URL**: https://freesound.org/
- **Search terms**: "doctor patient", "medical consultation", "hospital"
- **Format**: WAV, MP3
- **License**: Creative Commons (check individual licenses)

#### 4. **Internet Archive**
- **URL**: https://archive.org/
- **Search**: "medical education patient interview"
- **Content**: Historical medical recordings, educational content
- **Format**: Various formats

---

## Option 2: Create Your Own Test Audio

### Method 1: Text-to-Speech (Easiest!)

Use free online TTS services to create test conversations:

#### **Google Text-to-Speech**
- **URL**: https://cloud.google.com/text-to-speech
- Free tier available
- Multiple voices (use different voices for doctor/patient)

#### **Microsoft Azure Speech**
- **URL**: https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/
- Free tier: 5 million characters/month
- Neural voices available

#### **TTSMaker (Free, No Login)**
- **URL**: https://ttsmaker.com/
- No registration required
- Multiple languages and voices
- Can download MP3 directly

#### **Natural Readers**
- **URL**: https://www.naturalreaders.com/online/
- Free version available
- Good voice quality

### Method 2: Record Yourself

**Tools**:
- **Windows**: Voice Recorder (built-in) or Audacity
- **Mac**: QuickTime Player or Audacity
- **Online**: https://online-voice-recorder.com/

**Script to Read**:
```
[Doctor voice]
Good morning! How are you feeling today?

[Patient voice]
Hi doctor, I'm not feeling well. I've had a high fever for the past three days.

[Doctor voice]
I see. Can you tell me what your temperature has been?

[Patient voice]
It's been around 102 to 103 degrees Fahrenheit. I also have body aches.

[Doctor voice]
Any other symptoms like cough or sore throat?

[Patient voice]
Just a mild cough occasionally.

[Doctor voice]
Based on your symptoms, you have a severe fever. I'll prescribe Doro 150, 
Cyprosine, Indolo-160, and Citrogen. Take them as directed.

[Patient voice]
Thank you, doctor.

[Doctor voice]
If symptoms persist beyond three days, please come back for follow-up.
```

---

## Option 3: Use Sample Medical Scripts with TTS

I've created sample scripts below that you can convert to audio:

### Test Script 1: Simple Fever Case
```
Doctor: Good morning! What brings you in today?
Patient: I have a fever that started three days ago.
Doctor: How high is your fever?
Patient: It's been around 102 degrees.
Doctor: Any other symptoms?
Patient: Yes, body aches and a runny nose.
Doctor: I'll prescribe some medication. Take Tylenol for the fever.
Patient: Thank you, doctor.
```

### Test Script 2: Respiratory Issue
```
Doctor: Hello, what seems to be the problem?
Patient: I've been having trouble breathing and a persistent cough.
Doctor: How long has this been going on?
Patient: About a week now.
Doctor: Is the cough producing mucus?
Patient: Yes, yellow mucus.
Doctor: This sounds like bronchitis. I'll prescribe an antibiotic and an inhaler.
Patient: Should I do anything else?
Doctor: Yes, get plenty of rest and drink lots of fluids.
Patient: Okay, thank you.
```

### Test Script 3: Follow-up Visit
```
Doctor: Welcome back. How have you been feeling?
Patient: Much better! The medication really helped.
Doctor: Good to hear. Any remaining symptoms?
Patient: No, the cough is completely gone.
Doctor: Excellent. You can stop the medication now.
Patient: Thank you so much, doctor.
```

---

## 🛠️ Quick Setup: Create Test Audio with TTSMaker

### Step-by-Step Guide:

1. **Go to**: https://ttsmaker.com/

2. **For Doctor's Lines**:
   - Paste doctor's dialogue
   - Select voice: "English (US) - Male" (e.g., David, Matthew)
   - Click "Convert to Speech"
   - Download as MP3

3. **For Patient's Lines**:
   - Paste patient's dialogue
   - Select voice: "English (US) - Female" (e.g., Aria, Jenny)
   - Click "Convert to Speech"
   - Download as MP3

4. **Combine Audio** (Optional):
   - Use Audacity (free) to combine both files
   - Or upload them separately and combine in your app

5. **Alternative - All at Once**:
   - Paste entire conversation in one go
   - Use different voice tags if available
   - Let AIscribe's speaker diarization separate them

---

## 🎬 YouTube Videos to Download

Search YouTube for these and download audio:

1. **"Medical OSCE examination"**
   - Example: https://www.youtube.com/results?search_query=medical+osce+patient+consultation

2. **"Clinical skills patient interview"**
   - Example: https://www.youtube.com/results?search_query=clinical+skills+patient+interview

3. **"Medical student patient encounter practice"**
   - Example: https://www.youtube.com/results?search_query=medical+student+patient+encounter

### Download YouTube Audio:

**Using yt-dlp (Recommended)**:
```bash
# Install
pip install yt-dlp

# Download as MP3
yt-dlp -x --audio-format mp3 "YOUTUBE_URL"
```

**Using Online Tools**:
- https://ytmp3.nu/
- https://y2mate.com/
- https://320ytmp3.com/

---

## 📦 Ready-Made Test Audio

### Create Your Own Test Files Now:

I'll create a Python script to generate test audio using pyttsx3 (offline TTS):

```python
# Save as generate_test_audio.py
import pyttsx3
import time

engine = pyttsx3.init()

# Set properties
engine.setProperty('rate', 150)  # Speed

# Get voices
voices = engine.getProperty('voices')

# Create doctor voice (male)
engine.setProperty('voice', voices[0].id)

# Doctor-Patient conversation
conversation = [
    ("Doctor", "Good morning! What brings you in today?"),
    ("Patient", "I have a fever that started three days ago."),
    ("Doctor", "How high is your fever?"),
    ("Patient", "It's been around 102 degrees."),
    ("Doctor", "Any other symptoms?"),
    ("Patient", "Yes, body aches and a runny nose."),
    ("Doctor", "I'll prescribe Tylenol for the fever. Come back if it persists."),
    ("Patient", "Thank you, doctor."),
]

# Save each line
for i, (speaker, text) in enumerate(conversation):
    if speaker == "Doctor":
        engine.setProperty('voice', voices[0].id)  # Male voice
    else:
        engine.setProperty('voice', voices[1].id)  # Female voice
    
    filename = f"line_{i}_{speaker}.mp3"
    engine.save_to_file(text, filename)
    print(f"Created: {filename}")

engine.runAndWait()
print("All audio files created!")
```

---

## 🔍 Recommended Quick Test

### Fastest Method (5 minutes):

1. **Visit**: https://ttsmaker.com/
2. **Copy this text**:
   ```
   Good morning doctor.
   Hello, what brings you in today?
   I have a fever for three days, around 102 degrees.
   I see. Any other symptoms?
   Yes, body aches and a runny nose.
   I'll prescribe Tylenol. Come back if symptoms persist after three days.
   Thank you so much, doctor.
   ```
3. **Select voice**: English (US) - any voice
4. **Click**: "Convert to Speech"
5. **Download**: MP3 file
6. **Upload to AIscribe**: Use the file upload feature
7. **Test**: Click "Process Audio"

---

## 📋 Legal & Ethical Considerations

### ⚠️ Important Notes:

1. **Public Domain**: Use only public domain or Creative Commons audio
2. **Educational Use**: Ensure you have rights for your intended use
3. **Real Patient Data**: NEVER use real patient conversations without proper consent and HIPAA compliance
4. **YouTube**: Check video licenses before downloading
5. **Attribution**: Credit sources when required by license

### For Production:
- Obtain proper consent from patients
- Follow HIPAA guidelines
- Implement proper data protection
- Consult legal team

---

## 🎯 Quick Test Files

I can help you create test audio files right now using Text-to-Speech. Would you like me to:

1. Create a Python script that generates test audio files?
2. Provide specific YouTube links for medical consultations?
3. Create sample scripts you can record yourself?

---

## 📞 Support

If you need help:
1. Creating test audio files
2. Converting formats
3. Troubleshooting audio quality issues

Just let me know!

---

## ✅ Recommended Workflow

1. **Start Simple**: Use TTSMaker to create a 30-second test file
2. **Upload to AIscribe**: Test the pipeline
3. **Verify Results**: Check transcription accuracy
4. **Scale Up**: Create longer, more complex scenarios
5. **Fine-tune**: Adjust based on results

---

**Ready to test? Try TTSMaker first - it's the fastest way to get started!**



