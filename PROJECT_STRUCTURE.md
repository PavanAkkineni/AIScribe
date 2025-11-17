# AIscribe Project Structure

```
AIscribe/
│
├── app.py                          # Main Flask application with API endpoints
├── config.py                       # Configuration file with API keys and settings
├── logger_config.py                # Logging configuration with color-coded output
├── transcription_service.py        # AssemblyAI transcription with speaker diarization
├── ai_summarization_service.py     # OpenRouter AI summarization with fallback
├── test_setup.py                   # Setup verification script
│
├── requirements.txt                # Python dependencies
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
├── PROJECT_STRUCTURE.md            # This file
├── .gitignore                      # Git ignore rules
│
├── start.bat                       # Windows startup script
├── start.sh                        # Linux/Mac startup script
│
├── templates/
│   └── index.html                  # Web interface HTML
│
├── static/
│   ├── style.css                   # Stylesheet for web interface
│   └── app.js                      # Frontend JavaScript (recording, upload, processing)
│
├── uploads/                        # Audio files and processing results (auto-generated)
│   ├── [timestamp]_[filename]      # Uploaded/recorded audio files
│   └── [timestamp]_results.json    # Processing results
│
└── *.log                          # Application logs (auto-generated)
```

## File Descriptions

### Core Application Files

- **app.py**: Flask web server with REST API endpoints
  - `/` - Main web interface
  - `/api/process-audio` - Process audio with transcription and summarization
  - `/api/health` - Health check endpoint
  - `/api/results/<filename>` - Retrieve saved results

- **config.py**: Central configuration
  - API keys for AssemblyAI and OpenRouter
  - Model configurations (primary and fallback)
  - Upload folder settings and file type restrictions

### Service Modules

- **transcription_service.py**: AssemblyAI integration
  - Audio file transcription
  - Speaker diarization (Doctor vs Patient)
  - Dialogue formattin
  - Confidence scoring

- **ai_summarization_service.py**: AI summarization
  - Clinical summary generation (Chief Complaint, HPI, Assessment/Plan)
  - Medical Decision Making analysis (ICD-10, CPT, MDM level)
  - Automatic model fallback on rate limits
  - Response parsing and structuring

- **logger_config.py**: Logging system
  - Color-coded console output
  - File logging with timestamps
  - Multiple log levels (INFO, WARNING, ERROR, SUCCESS)

### Frontend Files

- **templates/index.html**: Web interface structure
  - Audio recording controls
  - File upload with drag & drop
  - Real-time processing logs
  - Results display sections

- **static/style.css**: Modern UI styling
  - Responsive design
  - Gradient backgrounds
  - Card-based layout
  - Animation effects

- **static/app.js**: Frontend logic
  - MediaRecorder API for audio recording
  - File upload handling
  - AJAX requests to backend
  - Dynamic results rendering

### Utility Files

- **test_setup.py**: Verification script
  - Check all dependencies
  - Verify API key configuration
  - Test service initialization
  - Create required directories

- **start.bat / start.sh**: Startup scripts
  - Check Python installation
  - Install dependencies if needed
  - Launch Flask server

## Data Flow

```
1. User Input (Recording/Upload)
   ↓
2. Frontend (app.js) → POST /api/process-audio
   ↓
3. Flask Backend (app.py)
   ↓
4. TranscriptionService → AssemblyAI API
   ├─ Audio transcription
   └─ Speaker diarization
   ↓
5. AISummarizationService → OpenRouter API
   ├─ Clinical Summary (Llama 3.3 70B / fallback)
   └─ MDM Summary (DeepSeek Distill Llama 70B / fallback)
   ↓
6. Results saved to JSON
   ↓
7. Response sent to Frontend
   ↓
8. Display formatted results
```

## API Integration

### AssemblyAI
- Endpoint: AssemblyAI REST API
- Purpose: Speech-to-text with speaker diarization
- Features: 
  - Real-time transcription status
  - Speaker identification
  - Confidence scores

### OpenRouter
- Endpoint: https://openrouter.ai/api/v1
- Purpose: AI model inference
- Models:
  - Primary: `meta-llama/llama-3.3-70b-instruct:free`
  - Fallback: `deepseek/deepseek-r1-distill-llama-70b:free`

## Configuration

Key configurations in `config.py`:

```python
ASSEMBLYAI_API_KEY = "your_key_here"
OPENROUTER_API_KEY = "your_key_here"
PRIMARY_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
FALLBACK_MODEL = "deepseek/deepseek-r1-distill-llama-70b:free"
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4', 'm4a', 'flac', 'ogg', 'webm'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
```

## Logging

Logs are written to:
- **Console**: Color-coded real-time output
- **File**: `aiscribe_YYYYMMDD.log` (daily rotation)

Log levels:
- 🔵 INFO: General information
- 🟢 SUCCESS: Successful operations
- 🟡 WARNING: Non-critical issues
- 🔴 ERROR: Critical errors

## Security Considerations

⚠️ **Important**: 
- API keys are currently in `config.py`
- For production, use environment variables
- Add authentication to web interface
- Use HTTPS in production
- Implement rate limiting
- Sanitize user inputs
- Secure file uploads

## Extending AIscribe

### Adding New AI Models
1. Add model identifier to `config.py`
2. Update `ai_summarization_service.py` fallback chain
3. Test model compatibility

### Customizing Summaries
1. Modify prompts in `ai_summarization_service.py`
2. Adjust parsing logic for new formats
3. Update frontend display in `index.html`

### Adding New Features
1. Create new service modules
2. Add API endpoints in `app.py`
3. Update frontend UI and logic
4. Document changes

## Troubleshooting

See logs for detailed error messages:
- Application logs: `aiscribe_YYYYMMDD.log`
- Browser console: F12 Developer Tools
- Server console: Terminal output

Run setup test:
```bash
python test_setup.py
```



