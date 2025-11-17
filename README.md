# AIscribe - Medical Transcription & Summarization Software

A comprehensive medical transcription system that records doctor-patient conversations, classifies speakers, and generates medical summaries with ICD-10/CPT coding.

## ✨ Features

- 🎙️ **Audio Recording**: Record conversations directly in the browser using MediaRecorder API
- 📁 **File Upload**: Upload pre-recorded audio files (drag & drop supported)
- 🗣️ **Speaker Diarization**: Automatically classify doctor and patient dialogues using AssemblyAI
- 📝 **Medical Summaries**: Generate comprehensive medical notes with AI
- 🏥 **Medical Coding**: Automatic ICD-10-CM and CPT coding suggestions
- 🔄 **Fallback Models**: Automatic failover between AI models for reliability
- 📊 **Detailed Logging**: Track every step of the process with color-coded logs
- 💾 **Result Persistence**: All results saved as JSON for future reference
- 🎨 **Modern UI**: Beautiful, responsive web interface

## 🚀 Quick Start

### 1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the application:
```bash
python app.py
```

### 3. Open your browser:
```
http://localhost:5000
```

### 4. Start using AIscribe!
- Record a conversation OR upload an audio file
- Click "Process Audio"
- View your medical summaries and coding

📖 **For detailed instructions, see [QUICKSTART.md](QUICKSTART.md)**

## Technology Stack

- **Backend**: Python Flask
- **Speech-to-Text**: AssemblyAI (with speaker diarization)
- **AI Models**: 
  - Meta Llama 3.3 70B (primary)
  - DeepSeek R1 Distill Llama 70B (fallback)
- **Frontend**: HTML5, CSS3, JavaScript (MediaRecorder API)

## Usage

1. **Record Audio**: Click "Start Recording" to record a conversation
2. **Upload Audio**: Or upload a pre-recorded audio file
3. **Process**: The system will:
   - Transcribe the audio with speaker labels
   - Generate clinical summary
   - Generate medical decision-making summary with coding
4. **Review**: View the results with detailed logging

## API Models

The system uses OpenRouter API with automatic fallback:
- Primary: `meta-llama/llama-3.3-70b-instruct:free`
- Fallback: `deepseek/deepseek-r1-distill-llama-70b:free`

## Security Note

For production use, move API keys to environment variables and never commit them to version control.

