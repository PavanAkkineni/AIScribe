# AIscribe Architecture

## System Overview

AIscribe is a full-stack medical transcription and summarization system that processes doctor-patient conversations and generates structured medical documentation with coding suggestions.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          WEB BROWSER                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    Frontend (index.html)                       │  │
│  │  ┌────────────────┐  ┌──────────────┐  ┌──────────────────┐  │  │
│  │  │  MediaRecorder │  │ File Upload  │  │  Results Display │  │  │
│  │  │  (app.js)      │  │  (Drag/Drop) │  │  (Dynamic HTML)  │  │  │
│  │  └────────────────┘  └──────────────┘  └──────────────────┘  │  │
│  │                 │              │                 ▲             │  │
│  └─────────────────┼──────────────┼─────────────────┼─────────────┘  │
│                    │              │                 │                │
└────────────────────┼──────────────┼─────────────────┼────────────────┘
                     │              │                 │
                     ▼              ▼                 │
        ┌────────────────────────────────────────────┼────────────────┐
        │                 Flask Backend (app.py)     │                │
        │  ┌──────────────────────────────────────────────────────┐  │
        │  │         POST /api/process-audio                       │  │
        │  │  • Receive audio file                                 │  │
        │  │  • Save to uploads/                                   │  │
        │  │  • Orchestrate processing pipeline                    │  │
        │  │  • Return results as JSON                             │  │
        │  └──────────────────────────────────────────────────────┘  │
        │                    │                          ▲             │
        │                    ▼                          │             │
        │  ┌──────────────────────────────────────────────────────┐  │
        │  │           TranscriptionService                        │  │
        │  │         (transcription_service.py)                    │  │
        │  │  • Upload audio to AssemblyAI                         │  │
        │  │  • Wait for transcription completion                  │  │
        │  │  • Extract speaker-labeled utterances                 │  │
        │  │  • Format dialogue (Doctor/Patient)                   │  │
        │  └──────────────────────────────────────────────────────┘  │
        │                    │                                        │
        │                    ▼                                        │
        │  ┌──────────────────────────────────────────────────────┐  │
        │  │        AISummarizationService                         │  │
        │  │      (ai_summarization_service.py)                    │  │
        │  │                                                        │  │
        │  │  ┌──────────────────────────────────────────────┐    │  │
        │  │  │  generate_clinical_summary()                 │    │  │
        │  │  │  • Create prompt with conversation            │    │  │
        │  │  │  • Call OpenRouter API                        │    │  │
        │  │  │  • Extract: Chief Complaint, HPI, A/P         │    │  │
        │  │  │  • Return structured summary                  │    │  │
        │  │  └──────────────────────────────────────────────┘    │  │
        │  │                                                        │  │
        │  │  ┌──────────────────────────────────────────────┐    │  │
        │  │  │  generate_medical_decision_making()          │    │  │
        │  │  │  • Create MDM prompt                          │    │  │
        │  │  │  • Call OpenRouter API                        │    │  │
        │  │  │  • Extract: ICD-10, CPT, MDM Analysis         │    │  │
        │  │  │  • Return coding recommendations              │    │  │
        │  │  └──────────────────────────────────────────────┘    │  │
        │  │                                                        │  │
        │  │  ┌──────────────────────────────────────────────┐    │  │
        │  │  │  _call_ai_with_fallback()                    │    │  │
        │  │  │  • Try Primary Model (Llama 3.3 70B)         │    │  │
        │  │  │  • On failure → Fallback Model (DeepSeek)    │    │  │
        │  │  │  • Return response with model info            │    │  │
        │  │  └──────────────────────────────────────────────┘    │  │
        │  └──────────────────────────────────────────────────────┘  │
        │                                                              │
        │  ┌──────────────────────────────────────────────────────┐  │
        │  │           LoggerConfig (logger_config.py)             │  │
        │  │  • Color-coded console output                         │  │
        │  │  • File logging with timestamps                       │  │
        │  │  • Multi-level logging (INFO/WARNING/ERROR)           │  │
        │  └──────────────────────────────────────────────────────┘  │
        └──────────────────────────────────────────────────────────────┘
                     │                          │
                     ▼                          ▼
        ┌────────────────────┐    ┌──────────────────────────┐
        │   AssemblyAI API   │    │   OpenRouter API         │
        │  ┌──────────────┐  │    │  ┌────────────────────┐  │
        │  │ Transcription│  │    │  │ Primary Model:     │  │
        │  │ + Speaker    │  │    │  │ Llama 3.3 70B     │  │
        │  │   Diarization│  │    │  └────────────────────┘  │
        │  └──────────────┘  │    │  ┌────────────────────┐  │
        │                    │    │  │ Fallback Model:    │  │
        │                    │    │  │ DeepSeek Distill   │  │
        │                    │    │  └────────────────────┘  │
        └────────────────────┘    └──────────────────────────┘
```

## Component Responsibilities

### Frontend Layer

#### HTML/CSS/JavaScript (templates/index.html, static/)
- **Purpose**: User interface for audio input and results display
- **Key Features**:
  - Audio recording using MediaRecorder API
  - File upload with drag-and-drop support
  - Real-time processing logs
  - Formatted display of conversation and summaries
  - Responsive design for mobile and desktop

#### JavaScript Functions (app.js)
- `startRecording()` - Initialize audio capture
- `stopRecording()` - Stop and save recording
- `handleFileSelect()` - Process uploaded files
- `processAudio()` - Send audio to backend API
- `displayResults()` - Render processed results
- `addLog()` - Update processing logs in real-time

### Backend Layer

#### Flask Application (app.py)
- **Purpose**: REST API server and request orchestration
- **Endpoints**:
  - `GET /` - Serve web interface
  - `POST /api/process-audio` - Main processing endpoint
  - `GET /api/health` - Health check
  - `GET /api/results/<filename>` - Retrieve saved results
- **Responsibilities**:
  - Request validation
  - File handling and storage
  - Service coordination
  - Response formatting
  - Error handling

#### Transcription Service (transcription_service.py)
- **Purpose**: Audio-to-text conversion with speaker identification
- **Key Methods**:
  - `transcribe_audio(file_path)` - Main transcription method
  - `_format_dialogue(transcript)` - Speaker labeling
  - `format_dialogue_text(dialogue)` - Text formatting
- **Integration**: AssemblyAI API
- **Features**:
  - Automatic speaker diarization
  - Confidence scoring
  - Doctor/Patient role assignment

#### AI Summarization Service (ai_summarization_service.py)
- **Purpose**: Generate medical documentation from conversations
- **Key Methods**:
  - `generate_clinical_summary()` - Create medical notes
  - `generate_medical_decision_making()` - Create coding analysis
  - `_call_ai_with_fallback()` - Model failover logic
  - `_call_openrouter()` - API communication
  - `_parse_clinical_summary()` - Response parsing
- **Integration**: OpenRouter API (multiple models)
- **Features**:
  - Structured prompt engineering
  - Automatic model fallback on rate limits
  - Response parsing and validation

#### Logger Configuration (logger_config.py)
- **Purpose**: Centralized logging system
- **Features**:
  - Color-coded console output
  - File-based logging with daily rotation
  - Multiple log levels
  - Timestamp formatting
- **Log Levels**:
  - DEBUG - Detailed debugging information
  - INFO - General information
  - WARNING - Warning messages
  - ERROR - Error messages
  - CRITICAL - Critical system errors

### External Services

#### AssemblyAI
- **Type**: Third-party speech-to-text API
- **Capabilities**:
  - Audio transcription
  - Speaker diarization (up to 10 speakers)
  - Real-time and batch processing
  - Multiple audio format support
- **Authentication**: API key
- **Rate Limits**: Based on plan

#### OpenRouter
- **Type**: AI model aggregation platform
- **Capabilities**:
  - Access to multiple LLM models
  - Automatic failover
  - Usage tracking
- **Models Used**:
  - **Primary**: Meta Llama 3.3 70B Instruct (free tier)
  - **Fallback**: DeepSeek R1 Distill Llama 70B (free tier)
- **Authentication**: API key
- **Rate Limits**: Per-model limits (handled automatically)

## Data Flow Sequence

```
1. User Action
   ↓
2. Frontend captures audio (record OR upload)
   ↓
3. User clicks "Process Audio"
   ↓
4. JavaScript sends FormData to POST /api/process-audio
   ↓
5. Flask receives file, validates, saves to uploads/
   ↓
6. Flask → TranscriptionService.transcribe_audio()
   ↓
7. TranscriptionService → AssemblyAI API
   - Upload audio
   - Wait for processing
   - Retrieve transcript with speaker labels
   ↓
8. Format dialogue (Doctor/Patient labeling)
   ↓
9. Flask → AISummarizationService.generate_clinical_summary()
   ↓
10. AISummarizationService → OpenRouter API (Primary Model)
    - If success → return summary
    - If rate limit → try Fallback Model
   ↓
11. Parse response into structured sections
   ↓
12. Flask → AISummarizationService.generate_medical_decision_making()
   ↓
13. AISummarizationService → OpenRouter API (with fallback)
   ↓
14. Combine all results into JSON response
   ↓
15. Save results to uploads/[timestamp]_results.json
   ↓
16. Return JSON to frontend
   ↓
17. JavaScript displays results in UI
```

## Error Handling Strategy

### Frontend
- Input validation (file type, size)
- Network error handling
- User-friendly error messages
- Graceful degradation

### Backend
- Try-except blocks around critical operations
- Validation of all inputs
- Detailed error logging
- Meaningful HTTP status codes
- Partial success handling (e.g., transcription success but MDM fails)

### External API Calls
- Automatic retry with fallback models
- Timeout handling
- Rate limit detection
- Connection error recovery

## Security Considerations

### Current Implementation
- ⚠️ API keys in config.py (development only)
- File type validation
- File size limits
- CORS enabled (development)

### Production Recommendations
1. **API Keys**: Move to environment variables or secret management
2. **Authentication**: Implement user authentication (OAuth, JWT)
3. **Authorization**: Role-based access control
4. **HTTPS**: SSL/TLS encryption
5. **Input Sanitization**: Validate and sanitize all inputs
6. **Rate Limiting**: Implement per-user rate limits
7. **File Security**: Scan uploads for malware
8. **Data Privacy**: Encrypt PHI (Protected Health Information)
9. **Audit Logging**: Track all access to patient data
10. **HIPAA Compliance**: Follow healthcare regulations

## Performance Considerations

### Bottlenecks
1. **AssemblyAI Transcription**: 5-30 seconds depending on audio length
2. **AI Model Inference**: 10-30 seconds per summary
3. **Network Latency**: Variable based on connection

### Optimization Strategies
1. **Async Processing**: Consider background tasks for long operations
2. **Caching**: Cache common medical terms and templates
3. **Compression**: Compress audio before upload
4. **CDN**: Serve static assets from CDN
5. **Database**: Add database for result persistence
6. **Queue System**: Use task queue (Celery) for parallel processing

## Scalability

### Current Limitations
- Single-server deployment
- Synchronous processing
- Local file storage
- No horizontal scaling

### Scaling Recommendations
1. **Load Balancer**: Distribute requests across multiple servers
2. **Queue System**: Redis + Celery for async task processing
3. **Cloud Storage**: S3 or similar for audio files
4. **Database**: PostgreSQL for structured data
5. **Containerization**: Docker for consistent deployment
6. **Orchestration**: Kubernetes for auto-scaling
7. **Monitoring**: Prometheus + Grafana for observability

## Extension Points

### Easy Additions
- Additional AI models
- Custom prompt templates
- Export to PDF/DOCX
- Email notifications
- User accounts and history

### Advanced Features
- Real-time transcription
- Multi-language support
- Custom medical terminology
- EHR integration (FHIR)
- Voice commands
- Mobile app

## Technology Choices

### Why Flask?
- Lightweight and simple
- Easy to set up and deploy
- Good for small to medium projects
- Extensive ecosystem

### Why AssemblyAI?
- Excellent speaker diarization
- High accuracy
- Good API documentation
- Reasonable pricing

### Why OpenRouter?
- Access to multiple models
- Free tier availability
- Automatic failover
- No vendor lock-in

### Why Vanilla JavaScript?
- No build step required
- Fast development
- Small footprint
- Easy to understand



