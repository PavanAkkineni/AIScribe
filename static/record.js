// Recording Interface JavaScript

let mediaRecorder = null;
let audioChunks = [];
let recordedBlob = null;
let isRecording = false;
let recordingStartTime = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupRecordingInterface();
    updateDateTime();
});

function setupRecordingInterface() {
    const micButton = document.getElementById('micButton');
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submitBtn');

    if (micButton) {
        micButton.addEventListener('click', toggleRecording);
    }

    if (fileInput) {
        fileInput.addEventListener('change', handleFileUpload);
    }

    if (submitBtn) {
        submitBtn.addEventListener('click', submitRecording);
    }

    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            const tabId = btn.dataset.tab + '-tab';
            document.getElementById(tabId).classList.add('active');
        });
    });
}

function updateDateTime() {
    const dateElement = document.getElementById('recordingDate');
    if (dateElement) {
        const now = new Date();
        dateElement.textContent = now.toLocaleString('en-US', {
            month: 'numeric',
            day: 'numeric',
            year: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
    }
}

async function toggleRecording() {
    if (!isRecording) {
        await startRecording();
    } else {
        stopRecording();
    }
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
            
            // Show audio preview
            const audioPlayer = document.getElementById('audioPlayer');
            const audioPreview = document.getElementById('audioPreview');
            const audioUrl = URL.createObjectURL(recordedBlob);
            audioPlayer.src = audioUrl;
            audioPreview.style.display = 'flex';
            
            // Show submit button
            document.getElementById('submitBtn').style.display = 'block';
            
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
            
            // Update status
            document.getElementById('recordingStatus').textContent = 'Recording saved! Click submit to process.';
        };
        
        mediaRecorder.start();
        isRecording = true;
        recordingStartTime = Date.now();
        
        // Update UI
        const micButton = document.getElementById('micButton');
        micButton.classList.add('recording');
        document.getElementById('recordingStatus').textContent = '🔴 Recording in progress... Click to stop';
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Error: Unable to access microphone. Please check permissions.');
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        isRecording = false;
        
        // Update UI
        const micButton = document.getElementById('micButton');
        micButton.classList.remove('recording');
        
        // Calculate duration
        if (recordingStartTime) {
            const duration = Math.round((Date.now() - recordingStartTime) / 1000 / 60);
            document.getElementById('durationBadge').textContent = `${duration} mins`;
        }
    }
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    // Validate file
    const validTypes = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/mp4', 'audio/m4a', 
                       'audio/flac', 'audio/ogg', 'audio/webm'];
    const validExtensions = ['.wav', '.mp3', '.mp4', '.m4a', '.flac', '.ogg', '.webm'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
        alert('Invalid file type. Please upload an audio file.');
        return;
    }
    
    // Validate size (100MB max)
    const maxSize = 100 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('File too large. Maximum size is 100MB.');
        return;
    }
    
    recordedBlob = file;
    
    // Show preview
    const audioPlayer = document.getElementById('audioPlayer');
    const audioPreview = document.getElementById('audioPreview');
    const audioUrl = URL.createObjectURL(file);
    audioPlayer.src = audioUrl;
    audioPreview.style.display = 'flex';
    
    // Show submit button
    document.getElementById('submitBtn').style.display = 'block';
    document.getElementById('recordingStatus').textContent = `File uploaded: ${file.name}. Click submit to process.`;
}

async function submitRecording() {
    if (!recordedBlob) {
        alert('No recording to submit!');
        return;
    }

    // Prompt for patient email
    const patientEmail = prompt('📧 Enter patient email to send visit summary (optional):');
    
    // Hide recording section, show processing
    document.getElementById('recordingSection').style.display = 'none';
    document.getElementById('processingSection').style.display = 'block';

    try {
        // Get recording type from URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const recordingType = urlParams.get('type') || 'conversation';
        
        // Prepare form data
        const formData = new FormData();
        
        if (recordedBlob instanceof Blob && !(recordedBlob instanceof File)) {
            formData.append('audio', recordedBlob, 'recording.webm');
        } else {
            formData.append('audio', recordedBlob);
        }
        
        formData.append('patient_id', patientId);
        formData.append('recording_type', recordingType);
        
        if (patientEmail && patientEmail.trim()) {
            formData.append('patient_email', patientEmail.trim());
        }

        // Update processing step
        document.getElementById('processingStep').textContent = 'Uploading audio...';

        // Send to backend
        const response = await fetch('/api/process-audio', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (!result.success) {
            throw new Error(result.error || 'Processing failed');
        }

        // Update processing steps
        document.getElementById('processingStep').textContent = 'Transcription complete!';
        await sleep(500);
        document.getElementById('processingStep').textContent = 'Generating clinical summary...';
        await sleep(500);
        document.getElementById('processingStep').textContent = 'Generating MDM summary...';
        await sleep(500);

        // Display results
        displayResults(result);

    } catch (error) {
        console.error('Processing error:', error);
        alert(`Error processing recording: ${error.message}`);
        
        // Show recording section again
        document.getElementById('recordingSection').style.display = 'flex';
        document.getElementById('processingSection').style.display = 'none';
    }
}

function displayResults(result) {
    // Hide processing, show results
    document.getElementById('processingSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';

    // Populate conversation transcript
    document.getElementById('transcriptContent').textContent = result.conversation_text || 'N/A';

    // Populate clinical summary
    const clinical = result.clinical_summary;
    document.getElementById('chiefComplaint').textContent = clinical.chief_complaint || 'N/A';
    document.getElementById('historyPresentIllness').textContent = clinical.history_of_present_illness || 'N/A';
    document.getElementById('assessmentPlan').textContent = clinical.assessment_plan || 'N/A';

    // Populate MDM
    const mdm = result.mdm_summary;
    document.getElementById('mdmContent').textContent = mdm.mdm_summary || 'N/A';

    // Update duration
    if (result.transcription && result.transcription.duration) {
        const mins = Math.round(result.transcription.duration / 60);
        document.getElementById('durationBadge').textContent = `${mins} mins`;
    }

    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function saveAndReturn() {
    // Navigate back to recordings list
    window.location.href = '/';
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

