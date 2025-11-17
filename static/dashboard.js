// Dashboard JavaScript for Recordings

let recordings = [];

// Load recordings on page load
document.addEventListener('DOMContentLoaded', () => {
    loadRecordings();
    setupEventListeners();
});

function setupEventListeners() {
    const startBtn = document.getElementById('startBtn');
    if (startBtn) {
        startBtn.addEventListener('click', showPatientIdModal);
    }

    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            sortRecordings(sortSelect.value);
        });
    }

    // Search functionality
    const searchInput = document.getElementById('patientSearchInput');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.trim();
            filterPatients(searchTerm);
            
            // Show/hide clear button
            if (clearSearchBtn) {
                clearSearchBtn.style.display = searchTerm ? 'flex' : 'none';
            }
        });

        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const searchTerm = e.target.value.trim();
                filterPatients(searchTerm);
            }
        });
    }

    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            searchInput.value = '';
            clearSearchBtn.style.display = 'none';
            filterPatients('');
            searchInput.focus();
        });
    }
}

function showPatientIdModal() {
    // Create modal
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-header">
                <h2 class="modal-title">New Recording</h2>
                <button class="modal-close" onclick="closeModal()">×</button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <input type="text" id="patientIdInput" placeholder="Insert patient name or initials" autofocus>
                </div>
                <div class="form-group recording-type-group">
                    <label class="recording-type-label">Recording Type:</label>
                    <div class="radio-group">
                        <label class="radio-option">
                            <input type="radio" name="recordingType" value="conversation" checked>
                            <span class="radio-label">
                                <strong>💬 Full Conversation</strong>
                                <small>Doctor-patient dialogue with speaker identification</small>
                            </span>
                        </label>
                        <label class="radio-option">
                            <input type="radio" name="recordingType" value="summary">
                            <span class="radio-label">
                                <strong>📝 Summary Notes</strong>
                                <small>Doctor's notes/summary recording (no diarization)</small>
                            </span>
                        </label>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button class="btn-modal-primary" onclick="startRecordingSession()">
                    OK
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Focus on input
    setTimeout(() => {
        document.getElementById('patientIdInput').focus();
    }, 100);
    
    // Handle Enter key
    document.getElementById('patientIdInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            startRecordingSession();
        }
    });
    
    // Close on overlay click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

function closeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.remove();
    }
}

function togglePatientGroup(index) {
    const patientGroup = document.querySelector(`[data-patient-index="${index}"]`);
    if (patientGroup) {
        if (patientGroup.classList.contains('collapsed')) {
            patientGroup.classList.remove('collapsed');
            patientGroup.classList.add('expanded');
        } else {
            patientGroup.classList.remove('expanded');
            patientGroup.classList.add('collapsed');
        }
    }
}

function startRecordingSession() {
    const patientId = document.getElementById('patientIdInput').value.trim();
    
    if (!patientId) {
        alert('Please enter a patient name or ID');
        return;
    }
    
    // Get selected recording type
    const recordingType = document.querySelector('input[name="recordingType"]:checked').value;
    
    // Redirect to recording interface with patient ID and recording type
    window.location.href = `/record/${encodeURIComponent(patientId)}?type=${recordingType}`;
}

async function loadRecordings() {
    const listContainer = document.getElementById('recordingsList');
    
    try {
        const response = await fetch('/api/recordings');
        const data = await response.json();
        
        if (data.success) {
            recordings = data.recordings;
            renderRecordings(recordings);
        } else {
            listContainer.innerHTML = '<div class="empty-message">No recordings found. Click START to begin!</div>';
        }
    } catch (error) {
        console.error('Error loading recordings:', error);
        listContainer.innerHTML = '<div class="empty-message">Error loading recordings. Please try again.</div>';
    }
}

function renderRecordings(recordingsList) {
    const listContainer = document.getElementById('recordingsList');
    
    if (!recordingsList || recordingsList.length === 0) {
        listContainer.innerHTML = '<div class="empty-message">No recordings found. Click START to begin!</div>';
        return;
    }

    // Group recordings by patient (folder structure)
    const groupedRecordings = groupByPatient(recordingsList);
    
    let html = '';
    let index = 0;
    for (const [patientId, items] of Object.entries(groupedRecordings)) {
        html += `
            <div class="patient-group collapsed" data-patient-index="${index}" data-patient-id="${patientId}">
                <div class="patient-group-header">
                    <div class="patient-group-icon">📁</div>
                    <div class="patient-group-info" onclick="togglePatientGroup(${index})">
                        <h3 class="patient-group-name">${patientId}</h3>
                        <p class="patient-group-count">${items.length} recording${items.length > 1 ? 's' : ''}</p>
                    </div>
                    <button class="summary-icon-btn" onclick="event.stopPropagation(); openPatientSummary('${patientId}')" title="Patient Health Summary">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                    <button class="email-icon-btn" onclick="event.stopPropagation(); openEmailTrail('${patientId}')" title="Email Patient">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </button>
                    <div class="patient-group-toggle" onclick="togglePatientGroup(${index})">▼</div>
                </div>
                <div class="patient-recordings">
                    ${items.map(recording => renderRecordingItem(recording)).join('')}
                </div>
            </div>
        `;
        index++;
    }
    
    listContainer.innerHTML = html;
}

function renderRecordingItem(recording) {
    return `
        <div class="recording-item" onclick="viewRecording('${recording.id}')">
            <div class="recording-info">
                <div class="mic-icon">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                        <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                    </svg>
                </div>
                <div class="recording-details">
                    <div class="recording-name">${recording.title || 'Untitled Recording'}</div>
                    <div class="recording-meta-info">
                        <span>📅 ${recording.date || 'N/A'}</span>
                        <span>🕐 ${recording.timestamp || 'N/A'}</span>
                    </div>
                </div>
            </div>
            <div class="recording-actions">
                <div class="quick-note">Quick Note</div>
                <button class="delete-btn" onclick="deleteRecording(event, '${recording.id}')">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                    </svg>
                </button>
            </div>
        </div>
    `;
}

function groupByPatient(recordingsList) {
    const grouped = {};
    
    recordingsList.forEach(recording => {
        const patientId = recording.patient_id || 'Unknown Patient';
        if (!grouped[patientId]) {
            grouped[patientId] = [];
        }
        grouped[patientId].push(recording);
    });
    
    return grouped;
}

function groupByDate(recordingsList) {
    const grouped = {};
    
    recordingsList.forEach(recording => {
        const date = recording.date || 'Unknown Date';
        if (!grouped[date]) {
            grouped[date] = [];
        }
        grouped[date].push(recording);
    });
    
    return grouped;
}

function sortRecordings(sortBy) {
    let sorted = [...recordings];
    
    switch (sortBy) {
        case 'newest':
            sorted.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
            break;
        case 'oldest':
            sorted.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
            break;
        case 'name':
            sorted.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
            break;
    }
    
    renderRecordings(sorted);
}

function viewRecording(id) {
    window.location.href = `/recording/${id}`;
}

function deleteRecording(event, id) {
    event.stopPropagation(); // Prevent triggering viewRecording
    
    if (confirm('Are you sure you want to delete this recording?')) {
        fetch(`/api/recording/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadRecordings(); // Reload list
            } else {
                alert('Failed to delete recording');
            }
        })
        .catch(error => {
            console.error('Error deleting recording:', error);
            alert('Error deleting recording');
        });
    }
}

async function openEmailTrail(patientId) {
    // Create email modal
    const modal = document.createElement('div');
    modal.className = 'email-modal';
    modal.innerHTML = `
        <div class="email-modal-content">
            <div class="email-modal-header">
                <div class="email-modal-title">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <h2>Email Trail - ${patientId}</h2>
                </div>
                <div style="display: flex; gap: 12px; align-items: center;">
                    <button class="btn-refresh-inbox" onclick="refreshPatientInbox('${patientId}')">
                        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
                            <path d="M21 2v6h-6M3 12a9 9 0 0 1 15-6.7L21 8M3 22v-6h6M21 12a9 9 0 0 1-15 6.7L3 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        Refresh Inbox
                    </button>
                    <button class="email-modal-close" onclick="closeEmailModal()">×</button>
                </div>
            </div>
            <div class="email-modal-body" id="emailThreadContainer">
                <div style="text-align: center; padding: 40px; color: #64748b;">
                    Loading emails...
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close on overlay click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
    
    // Load emails for this patient
    await loadEmailsForPatient(patientId);
}

function closeEmailModal() {
    const modal = document.querySelector('.email-modal');
    if (modal) {
        modal.remove();
    }
}

function renderEmailItem(email) {
    const date = new Date(email.timestamp).toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
    
    // Determine email direction
    const isInbound = email.direction === 'inbound' || email.from !== undefined;
    const directionIcon = isInbound ? '📩' : '📤';
    const directionText = isInbound ? 'Received from' : 'Sent to';
    const emailAddress = isInbound ? (email.from || 'Unknown') : (email.to || 'Unknown');
    const sentStatus = email.sent === false ? ' <span style="color: #f59e0b;">(Not sent)</span>' : '';
    
    return `
        <div class="email-item ${isInbound ? 'email-inbound' : 'email-outbound'}">
            <div class="email-item-header">
                <div class="email-item-info">
                    <div class="email-item-subject">${directionIcon} ${email.subject}${sentStatus}</div>
                    <div class="email-item-meta">
                        <span>📧 ${directionText}: ${emailAddress}</span>
                        <span>📅 ${date}</span>
                    </div>
                </div>
            </div>
            <div class="email-item-body">
                ${email.body}
            </div>
        </div>
    `;
}

async function refreshPatientInbox(patientId) {
    const button = event.target.closest('.btn-refresh-inbox');
    const originalText = button.innerHTML;
    
    try {
        // Show loading state
        button.disabled = true;
        button.innerHTML = `<svg class="spin" viewBox="0 0 24 24" fill="none" width="18" height="18">
            <path d="M21 2v6h-6M3 12a9 9 0 0 1 15-6.7L21 8M3 22v-6h6M21 12a9 9 0 0 1-15 6.7L3 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg> Checking...`;
        
        // Fetch inbox
        const response = await fetch(`/api/patient/${encodeURIComponent(patientId)}/fetch-inbox`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show notification with details
            const message = data.total_fetched ? 
                `📬 Checked inbox: Found ${data.total_fetched} total email(s), ${data.new_emails} new` :
                `✅ Checked inbox: ${data.new_emails} new email(s)`;
            alert(message);
            
            // Reload emails to show new ones
            await loadEmailsForPatient(patientId);
        } else {
            alert(`❌ Error: ${data.error || 'Failed to fetch inbox'}`);
        }
        
    } catch (error) {
        console.error('Error refreshing inbox:', error);
        alert('❌ Error checking inbox. Please try again.');
    } finally {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

async function loadEmailsForPatient(patientId) {
    try {
        const response = await fetch(`/api/patient/${encodeURIComponent(patientId)}/emails`);
        const data = await response.json();
        
        const container = document.getElementById('emailThreadContainer');
        
        if (data.success && data.emails && data.emails.length > 0) {
            // Find patient email from sent emails
            let patientEmail = '';
            for (const email of data.emails) {
                if (email.direction === 'outbound' && email.to) {
                    patientEmail = email.to;
                    break;
                }
            }
            
            // Get latest email for reply subject
            const latestEmail = data.emails[0];
            const replySubject = latestEmail.subject.startsWith('Re:') ? 
                latestEmail.subject : 
                `Re: ${latestEmail.subject}`;
            
            container.innerHTML = `
                <div class="email-thread">
                    ${data.emails.map(email => renderEmailItem(email)).join('')}
                </div>
                
                <div class="email-compose">
                    <h3>💬 Compose Reply</h3>
                    <div class="compose-form">
                        <div class="form-row">
                            <label>To:</label>
                            <input type="email" id="composeToEmail" value="${patientEmail}" readonly>
                        </div>
                        <div class="form-row">
                            <label>Subject:</label>
                            <input type="text" id="composeSubject" value="${replySubject}">
                        </div>
                        <div class="form-row">
                            <label>Message:</label>
                            <textarea id="composeBody" rows="6" placeholder="Write your reply here..."></textarea>
                        </div>
                        <div class="form-actions">
                            <button class="btn-send-email" onclick="sendReplyEmail('${patientId}', '${patientEmail}')">
                                📤 Send Email
                            </button>
                        </div>
                    </div>
                </div>
            `;
        } else {
            container.innerHTML = `
                <div class="email-empty">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <h3>No emails yet</h3>
                    <p>Emails will appear here after recordings are processed.</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading emails:', error);
        document.getElementById('emailThreadContainer').innerHTML = `
            <div class="email-empty">
                <h3>Error loading emails</h3>
                <p>Please try again later.</p>
            </div>
        `;
    }
}

async function sendReplyEmail(patientId, patientEmail) {
    const subject = document.getElementById('composeSubject').value;
    const body = document.getElementById('composeBody').value;
    
    if (!body.trim()) {
        alert('Please enter a message');
        return;
    }
    
    const button = event.target.closest('.btn-send-email');
    const originalText = button.innerHTML;
    
    try {
        button.disabled = true;
        button.innerHTML = '📤 Sending...';
        
        const response = await fetch(`/api/patient/${encodeURIComponent(patientId)}/send-reply`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                patient_email: patientEmail,
                subject: subject,
                body: `<p>${body.replace(/\n/g, '<br>')}</p>`
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('✅ Email sent successfully!');
            // Clear compose form
            document.getElementById('composeBody').value = '';
            // Reload emails to show sent reply
            await loadEmailsForPatient(patientId);
        } else {
            alert(`❌ Failed to send email: ${data.error || 'Unknown error'}`);
        }
        
    } catch (error) {
        console.error('Error sending reply:', error);
        alert('❌ Error sending email. Please try again.');
    } finally {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

function filterPatients(searchTerm) {
    const patientGroups = document.querySelectorAll('.patient-group');
    let visibleCount = 0;
    
    if (!searchTerm) {
        // Show all patient groups
        patientGroups.forEach(group => {
            group.style.display = 'block';
            visibleCount++;
        });
    } else {
        // Filter patient groups by name
        const searchLower = searchTerm.toLowerCase();
        
        patientGroups.forEach(group => {
            const patientNameElement = group.querySelector('.patient-group-name');
            if (patientNameElement) {
                const patientName = patientNameElement.textContent.toLowerCase();
                
                if (patientName.includes(searchLower)) {
                    group.style.display = 'block';
                    // Keep collapsed - don't auto-expand
                    visibleCount++;
                } else {
                    group.style.display = 'none';
                }
            }
        });
    }
    
    // Show "no results" message if no matches
    const listContainer = document.getElementById('recordingsList');
    const existingNoResults = listContainer.querySelector('.no-results');
    
    if (visibleCount === 0 && searchTerm) {
        if (!existingNoResults) {
            const noResults = document.createElement('div');
            noResults.className = 'no-results';
            noResults.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none">
                    <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
                    <path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <h3>No patients found</h3>
                <p>No patients match "${searchTerm}". Try a different search term.</p>
            `;
            listContainer.appendChild(noResults);
        }
    } else {
        if (existingNoResults) {
            existingNoResults.remove();
        }
    }
}

async function openPatientSummary(patientId) {
    console.log(`Opening patient summary for: ${patientId}`);
    
    // Create modal overlay
    const modal = document.createElement('div');
    modal.id = 'summaryModal';
    modal.className = 'summary-modal';
    modal.innerHTML = `
        <div class="summary-modal-content">
            <div class="summary-modal-header">
                <h2>📋 Patient Health Summary - ${patientId}</h2>
                <button class="close-summary-btn" onclick="closeSummaryModal()">×</button>
            </div>
            <div class="summary-modal-body">
                <div class="loading-summary">
                    <div class="spinner"></div>
                    <p>Generating comprehensive health summary...</p>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Fetch and generate patient summary
    try {
        const response = await fetch(`/api/patient/${encodeURIComponent(patientId)}/health-summary`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        const modalBody = document.querySelector('.summary-modal-body');
        
        if (data.success) {
            modalBody.innerHTML = `
                <div class="summary-content">
                    <div class="summary-section">
                        <h3>🏥 Comprehensive Health History</h3>
                        <div class="summary-text">${formatSummaryText(data.summary)}</div>
                    </div>
                    
                    <div class="summary-meta">
                        <div class="meta-item">
                            <span class="meta-label">Total Visits:</span>
                            <span class="meta-value">${data.total_visits || 0}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Generated:</span>
                            <span class="meta-value">${new Date().toLocaleString()}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Model:</span>
                            <span class="meta-value">${data.model_used || 'AI'}</span>
                        </div>
                    </div>
                </div>
            `;
        } else {
            modalBody.innerHTML = `
                <div class="summary-error">
                    <svg viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                        <path d="M12 8v4m0 4h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    <h3>Error Generating Summary</h3>
                    <p>${data.error || 'Unable to generate patient summary. Please try again.'}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error fetching patient summary:', error);
        const modalBody = document.querySelector('.summary-modal-body');
        modalBody.innerHTML = `
            <div class="summary-error">
                <h3>Network Error</h3>
                <p>Failed to connect to the server. Please check your connection and try again.</p>
            </div>
        `;
    }
    
    // Close on overlay click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeSummaryModal();
        }
    });
}

function closeSummaryModal() {
    const modal = document.getElementById('summaryModal');
    if (modal) {
        modal.remove();
    }
}

function formatSummaryText(text) {
    // Convert newlines to <br> tags
    text = text.replace(/\n/g, '<br>');
    
    // Bold headers (text followed by colon)
    text = text.replace(/^([A-Z][^:]+:)/gm, '<strong>$1</strong>');
    
    // Convert bullet points
    text = text.replace(/^- (.*)/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    return text;
}

