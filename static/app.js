// AIscribe Frontend JavaScript

let mediaRecorder = null;
let audioChunks = [];
let recordedBlob = null;
let uploadedFile = null;

// DOM Elements
const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const recordingStatus = document.getElementById('recordingStatus');
const audioPreview = document.getElementById('audioPreview');
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadStatus = document.getElementById('uploadStatus');
const processBtn = document.getElementById('processBtn');
const logsSection = document.getElementById('logsSection');
const logsContent = document.getElementById('logsContent');
const resultsSection = document.getElementById('resultsSection');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupRecording();
    setupUpload();
    setupProcessing();
});

// ============ Recording Setup ============

function setupRecording() {
    recordBtn.addEventListener('click', startRecording);
    stopBtn.addEventListener('click', stopRecording);
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = () => {
            recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
            uploadedFile = null; // Clear uploaded file if recording
            
            // Show audio preview
            const audioUrl = URL.createObjectURL(recordedBlob);
            audioPreview.innerHTML = `
                <audio controls>
                    <source src="${audioUrl}" type="audio/webm">
                </audio>
            `;
            
            showStatus(recordingStatus, 'Recording saved! Ready to process.', 'success');
            processBtn.disabled = false;
            
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        
        recordBtn.disabled = true;
        stopBtn.disabled = false;
        recordBtn.classList.add('recording-active');
        
        showStatus(recordingStatus, '🔴 Recording in progress...', 'warning');
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
        showStatus(recordingStatus, 'Error: Unable to access microphone. Please check permissions.', 'error');
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        recordBtn.disabled = false;
        stopBtn.disabled = true;
        recordBtn.classList.remove('recording-active');
    }
}

// ============ Upload Setup ============

function setupUpload() {
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect({ target: fileInput });
        }
    });
    
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    // Validate file type
    const validTypes = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/mp4', 'audio/m4a', 
                       'audio/flac', 'audio/ogg', 'audio/webm'];
    const validExtensions = ['.wav', '.mp3', '.mp4', '.m4a', '.flac', '.ogg', '.webm'];
    
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
        showStatus(uploadStatus, 'Invalid file type. Please upload an audio file.', 'error');
        return;
    }
    
    // Validate file size (100MB max)
    const maxSize = 100 * 1024 * 1024;
    if (file.size > maxSize) {
        showStatus(uploadStatus, 'File too large. Maximum size is 100MB.', 'error');
        return;
    }
    
    uploadedFile = file;
    recordedBlob = null; // Clear recorded audio if file uploaded
    audioPreview.innerHTML = ''; // Clear recording preview
    
    showStatus(uploadStatus, `✓ File selected: ${file.name} (${formatFileSize(file.size)})`, 'success');
    processBtn.disabled = false;
}

// ============ Processing Setup ============

function setupProcessing() {
    processBtn.addEventListener('click', processAudio);
}

async function processAudio() {
    // Clear previous results
    logsContent.innerHTML = '';
    logsSection.style.display = 'block';
    resultsSection.style.display = 'none';
    
    processBtn.disabled = true;
    processBtn.textContent = '⏳ Processing...';
    
    addLog('🚀 Starting audio processing...', 'info');
    
    try {
        // Prepare form data
        const formData = new FormData();
        
        if (recordedBlob) {
            formData.append('audio', recordedBlob, 'recording.webm');
            addLog('📤 Uploading recorded audio...', 'info');
        } else if (uploadedFile) {
            formData.append('audio', uploadedFile);
            addLog(`📤 Uploading file: ${uploadedFile.name}...`, 'info');
        } else {
            addLog('❌ No audio file to process!', 'error');
            processBtn.disabled = false;
            processBtn.textContent = '🚀 Process Audio';
            return;
        }
        
        // Send to backend
        addLog('🔄 Sending to server for processing...', 'info');
        
        const response = await fetch('/api/process-audio', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Processing failed');
        }
        
        // Show processing logs
        addLog('✓ Audio uploaded successfully', 'success');
        addLog('🎙️ Transcription with speaker diarization completed', 'success');
        addLog('🏥 Clinical summary generated', 'success');
        addLog('📋 Medical Decision Making summary generated', 'success');
        addLog('✅ Processing completed successfully!', 'success');
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Processing error:', error);
        addLog(`❌ Error: ${error.message}`, 'error');
        showStatus(recordingStatus, `Processing failed: ${error.message}`, 'error');
    } finally {
        processBtn.disabled = false;
        processBtn.textContent = '🚀 Process Audio';
    }
}

function displayResults(result) {
    resultsSection.style.display = 'block';
    
    // Conversation transcript
    const conversationDiv = document.getElementById('conversationText');
    conversationDiv.textContent = result.conversation_text || 'No conversation text available';
    
    // Clinical summary
    const clinical = result.clinical_summary;
    document.getElementById('chiefComplaint').textContent = clinical.chief_complaint || 'N/A';
    document.getElementById('historyPresentIllness').textContent = clinical.history_of_present_illness || 'N/A';
    document.getElementById('assessmentPlan').textContent = clinical.assessment_plan || 'N/A';
    
    // MDM summary
    const mdm = result.mdm_summary;
    document.getElementById('mdmSummary').textContent = mdm.mdm_summary || 'N/A';
    
    // Model information
    document.getElementById('clinicalModel').textContent = clinical.model_used || 'Unknown';
    document.getElementById('mdmModel').textContent = mdm.model_used || 'Unknown';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ============ Utility Functions ============

function showStatus(element, message, type) {
    element.textContent = message;
    element.className = `status-message ${type}`;
    element.style.display = 'block';
}

function addLog(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    logEntry.textContent = `[${timestamp}] ${message}`;
    logsContent.appendChild(logEntry);
    logsContent.scrollTop = logsContent.scrollHeight;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}



