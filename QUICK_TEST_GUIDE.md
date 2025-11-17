# Quick Test Guide - Get Audio Files Fast! 🎯

## 🚀 Fastest Way: Online TTS (5 Minutes)

### Option 1: TTSMaker (Recommended - No Login Required)

1. **Visit**: https://ttsmaker.com/

2. **Copy this test conversation**:
   ```
   Good morning! What brings you in today?
   [pause]
   Hi doctor, I have a fever for three days, around 102 degrees.
   [pause]
   I see. Any other symptoms?
   [pause]
   Yes, body aches and a runny nose.
   [pause]
   I'll prescribe Tylenol. Come back if symptoms persist after three days.
   [pause]
   Thank you so much, doctor.
   ```

3. **Settings**:
   - Voice: Select "English (US) - Male" or "Female"
   - Speed: Normal
   - Format: MP3

4. **Click**: "Convert to Speech" button

5. **Download**: Click "Download" to save the MP3 file

6. **Upload to AIscribe**:
   - Go to http://localhost:5000
   - Click "Browse Files" or drag & drop the MP3
   - Click "Process Audio"
   - Done! 🎉

---

## 🎬 Option 2: YouTube Medical Videos (10 Minutes)

### Best Search Terms:
- "medical OSCE patient consultation"
- "doctor patient conversation roleplay"
- "clinical skills assessment"
- "medical student patient interview"

### Good Example Channels:
- **Geeky Medics** - Medical OSCE scenarios
- **Oxford Medical Education** - Clinical skills
- **Medical School HQ** - Patient consultations

### Download YouTube Audio:

#### Method A: Online Converter (Easiest)
1. Copy YouTube video URL
2. Go to: https://ytmp3.nu/ or https://y2mate.com/
3. Paste URL
4. Select "MP3" format
5. Click "Convert" and download

#### Method B: yt-dlp (Best Quality)
```bash
# Install
pip install yt-dlp

# Download audio only
yt-dlp -x --audio-format mp3 "PASTE_YOUTUBE_URL_HERE"
```

**Example URLs to try**:
- Search: https://www.youtube.com/results?search_query=medical+osce+fever+case
- Search: https://www.youtube.com/results?search_query=doctor+patient+consultation

---

## 🎙️ Option 3: Record Yourself (15 Minutes)

### Tools:
- **Windows**: Voice Recorder (built-in)
- **Mac**: QuickTime Player
- **Online**: https://online-voice-recorder.com/

### Script to Read:

**Change your voice slightly between doctor and patient roles:**

```
[Deep voice - Doctor]
Good morning! How are you feeling today?

[Higher voice - Patient]  
Hi doctor, I'm not feeling well. I've had a high fever for three days.

[Deep voice - Doctor]
I see. Can you tell me what your temperature has been?

[Higher voice - Patient]
It's been around 102 degrees Fahrenheit. I also have body aches.

[Deep voice - Doctor]
Any other symptoms like cough or sore throat?

[Higher voice - Patient]
Just a mild cough occasionally.

[Deep voice - Doctor]
Based on your symptoms, you have a severe fever. I'll prescribe Doro 150, 
Cyprosine, and Indolo 160. Take them as directed.

[Higher voice - Patient]
Thank you, doctor.

[Deep voice - Doctor]
If symptoms persist beyond three days, come back for follow-up.
```

**Tips**:
- Speak clearly and at moderate pace
- Leave 1-2 second pauses between speakers
- Use different voice tones for doctor vs patient
- Record in a quiet environment

---

## 💻 Option 4: Generate with Python (If you have pyttsx3)

### Quick Setup:
```bash
# Install text-to-speech library
pip install pyttsx3

# Generate test audio
python generate_test_audio.py
```

This will create 3 test files in `test_audio/` folder:
- `fever_case.mp3`
- `respiratory_issue.mp3`
- `simple_consultation.mp3`

---

## 🎯 Recommended: Start with TTSMaker

**Why?**
- ✅ No installation required
- ✅ No account needed
- ✅ High quality voices
- ✅ Works immediately
- ✅ Free

**Steps**:
1. Go to https://ttsmaker.com/ (2 minutes)
2. Paste conversation text (30 seconds)
3. Generate and download MP3 (1 minute)
4. Upload to AIscribe (30 seconds)
5. Test the pipeline (1 minute)

**Total time: 5 minutes!**

---

## 📋 3 Ready-to-Use Test Scripts

### Test 1: Simple Fever (30 seconds)
```
Good morning doctor.
Hello, what brings you in today?
I have a fever for three days, around 102 degrees.
I see. Any other symptoms?
Yes, body aches and runny nose.
I'll prescribe Tylenol. Come back if it persists.
Thank you, doctor.
```

### Test 2: Respiratory Issue (45 seconds)
```
Hello doctor, I need help.
What seems to be the problem?
I have trouble breathing and a bad cough for a week.
Is it a dry cough or producing mucus?
It's producing yellow mucus, and I have a low fever.
Let me listen to your lungs. I hear wheezing. This is likely bronchitis.
What should I do?
I'll prescribe an antibiotic and inhaler. Get plenty of rest.
Thank you so much.
```

### Test 3: Headache (30 seconds)
```
I've had a bad headache for two days.
Can you describe the pain?
It's throbbing on both sides of my head.
Any nausea or light sensitivity?
A little nausea, yes.
This sounds like a tension headache. Take ibuprofen and rest.
Should I be worried?
No, but come back if it gets worse.
Okay, thank you.
```

---

## 🎤 Voice Tips for Better Results

### For Doctor Voice:
- Lower, steady tone
- Speak with authority
- Clear pronunciation of medical terms

### For Patient Voice:
- Slightly higher pitch
- Conversational tone
- Show emotion (concern, relief)

### General Tips:
- **Pace**: Not too fast, not too slow
- **Pauses**: 1-2 seconds between speakers
- **Clarity**: Enunciate medical terms
- **Volume**: Consistent throughout

---

## ⚡ Super Quick Test (2 Minutes)

**Don't want to generate audio? Use AIscribe's recording feature!**

1. Open: http://localhost:5000
2. Click: "Start Recording"
3. Read aloud:
   ```
   Doctor: Hi, what brings you in?
   Patient: I have a fever, 102 degrees.
   Doctor: I'll prescribe Tylenol.
   ```
4. Click: "Stop Recording"
5. Click: "Process Audio"
6. Done! ✅

---

## 📦 Sample Files Available

If you prefer, I can provide links to:
1. Sample medical audio clips (public domain)
2. Educational OSCE recordings
3. Clinical simulation audio

---

## 🔗 Quick Links

| Service | URL | Free? | Quality |
|---------|-----|-------|---------|
| TTSMaker | https://ttsmaker.com/ | ✅ Yes | ⭐⭐⭐⭐⭐ |
| Natural Readers | https://www.naturalreaders.com/online/ | ✅ Yes | ⭐⭐⭐⭐ |
| YouTube to MP3 | https://ytmp3.nu/ | ✅ Yes | ⭐⭐⭐⭐ |
| Online Recorder | https://online-voice-recorder.com/ | ✅ Yes | ⭐⭐⭐ |
| Freesound | https://freesound.org/ | ✅ Yes | ⭐⭐⭐ |

---

## ✅ Checklist

- [ ] Choose a method (TTSMaker recommended)
- [ ] Generate or download audio file
- [ ] Save as MP3 format
- [ ] Open AIscribe (http://localhost:5000)
- [ ] Upload audio file
- [ ] Click "Process Audio"
- [ ] View results!

---

## 🆘 Need Help?

**Audio not processing?**
- Check file format (must be audio file)
- Ensure file size < 100MB
- Try converting to MP3

**Speaker not identified correctly?**
- Use more distinct voices
- Add longer pauses between speakers
- Ensure clear audio quality

**Want better quality?**
- See TEST_AUDIO_SOURCES.md for advanced options
- Use professional TTS services
- Record with better microphone

---

**Ready to test? Start with TTSMaker - it's the fastest way!** 🚀

Visit: https://ttsmaker.com/ and paste one of the test scripts above!



