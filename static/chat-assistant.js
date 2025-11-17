// AI Chat Assistant for AIscribe Platform

let chatMessages = [];
let isProcessing = false;
let selectedImage = null;

document.addEventListener('DOMContentLoaded', () => {
    initializeChatAssistant();
});

function initializeChatAssistant() {
    // Create chat button
    const chatButton = document.createElement('button');
    chatButton.id = 'chatAssistantBtn';
    chatButton.className = 'chat-assistant-btn';
    chatButton.innerHTML = `
        <svg viewBox="0 0 24 24" fill="none" width="28" height="28">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M8 10h.01M12 10h.01M16 10h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    `;
    chatButton.title = 'AI Assistant';
    
    // Create chat window
    const chatWindow = document.createElement('div');
    chatWindow.id = 'chatAssistantWindow';
    chatWindow.className = 'chat-assistant-window';
    chatWindow.innerHTML = `
        <div class="chat-header">
            <div class="chat-header-content">
                <div class="chat-avatar">
                    <svg viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" fill="#2563eb"/>
                        <path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01" stroke="white" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </div>
                <div class="chat-header-text">
                    <h3>AIscribe Assistant</h3>
                    <p class="chat-status">Online • Ready to help</p>
                </div>
            </div>
            <button class="chat-close-btn" onclick="closeChatAssistant()">
                <svg viewBox="0 0 24 24" fill="none" width="24" height="24">
                    <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="chat-message assistant-message">
                <div class="message-avatar">
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <circle cx="12" cy="12" r="10"/>
                    </svg>
                </div>
                <div class="message-content">
                    <p>👋 Hello! I'm your AIscribe assistant. I can help you with:</p>
                    <ul>
                        <li><strong>Platform Questions:</strong> How to use features, navigate the system</li>
                        <li><strong>Medical Questions:</strong> Clinical information, medical terminology</li>
                    </ul>
                    <p>Just ask me anything!</p>
                </div>
            </div>
        </div>
        
        <div class="chat-input-container">
            <input type="file" id="chatImageInput" accept="image/*" style="display: none;">
            <button class="chat-image-btn" onclick="selectImage()" title="Upload image">
                <svg viewBox="0 0 24 24" fill="none" width="24" height="24">
                    <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/>
                    <path d="M21 15l-5-5L5 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
            <div id="imagePreviewContainer" class="image-preview-container" style="display: none;">
                <img id="imagePreview" class="image-preview" src="" alt="Preview">
                <button class="image-remove-btn" onclick="removeImage()">×</button>
            </div>
            <textarea 
                id="chatInput" 
                class="chat-input" 
                placeholder="Ask me anything about the platform or medical questions..."
                rows="1"
            ></textarea>
            <button id="chatSendBtn" class="chat-send-btn" onclick="sendChatMessage()">
                <svg viewBox="0 0 24 24" fill="none" width="24" height="24">
                    <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
        </div>
    `;
    
    document.body.appendChild(chatButton);
    document.body.appendChild(chatWindow);
    
    // Event listeners
    chatButton.addEventListener('click', openChatAssistant);
    
    // Auto-resize textarea
    const chatInput = document.getElementById('chatInput');
    chatInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });
    
    // Send on Enter (Shift+Enter for new line)
    chatInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendChatMessage();
        }
    });
    
    // Handle image file selection
    const imageInput = document.getElementById('chatImageInput');
    imageInput.addEventListener('change', function(e) {
        handleImageSelect(e.target.files[0]);
    });
}

function selectImage() {
    document.getElementById('chatImageInput').click();
}

function handleImageSelect(file) {
    if (!file) return;
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }
    
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        alert('Image too large. Please select an image under 10MB');
        return;
    }
    
    selectedImage = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = function(e) {
        const preview = document.getElementById('imagePreview');
        const container = document.getElementById('imagePreviewContainer');
        preview.src = e.target.result;
        container.style.display = 'flex';
    };
    reader.readAsDataURL(file);
    
    // Update placeholder
    document.getElementById('chatInput').placeholder = 'Ask me about this image...';
}

function removeImage() {
    selectedImage = null;
    document.getElementById('imagePreviewContainer').style.display = 'none';
    document.getElementById('imagePreview').src = '';
    document.getElementById('chatImageInput').value = '';
    document.getElementById('chatInput').placeholder = 'Ask me anything about the platform or medical questions...';
}

function openChatAssistant() {
    const chatWindow = document.getElementById('chatAssistantWindow');
    const chatButton = document.getElementById('chatAssistantBtn');
    
    chatWindow.classList.add('open');
    chatButton.style.display = 'none';
    
    // Focus input
    setTimeout(() => {
        document.getElementById('chatInput').focus();
    }, 300);
}

function closeChatAssistant() {
    const chatWindow = document.getElementById('chatAssistantWindow');
    const chatButton = document.getElementById('chatAssistantBtn');
    
    chatWindow.classList.remove('open');
    chatButton.style.display = 'flex';
}

async function sendChatMessage() {
    if (isProcessing) return;
    
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message && !selectedImage) return;
    
    // Add user message to chat
    if (selectedImage) {
        addImageMessageToChat('user', message || 'What is in this image?', selectedImage);
    } else {
        addMessageToChat('user', message);
    }
    
    // Clear input
    input.value = '';
    input.style.height = 'auto';
    
    // Show typing indicator
    isProcessing = true;
    addTypingIndicator();
    
    try {
        let response, data;
        
        if (selectedImage) {
            // Send image + text with FormData
            const formData = new FormData();
            formData.append('image', selectedImage);
            formData.append('message', message || 'What is in this image?');
            
            response = await fetch('/api/chat-assistant', {
                method: 'POST',
                body: formData
            });
            
            // Clear selected image after sending
            removeImage();
        } else {
            // Send text-only with JSON
            response = await fetch('/api/chat-assistant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });
        }
        
        data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.success) {
            // Add assistant response with category badge
            addMessageToChat('assistant', data.response, data.category, data.model_used);
        } else {
            addMessageToChat('assistant', `Sorry, I encountered an error: ${data.error || 'Unknown error'}`, 'error');
        }
        
    } catch (error) {
        removeTypingIndicator();
        console.error('Chat error:', error);
        addMessageToChat('assistant', 'Sorry, I\'m having trouble connecting. Please try again.', 'error');
    } finally {
        isProcessing = false;
    }
}

function addMessageToChat(type, content, category = null, model = null) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}-message`;
    
    if (type === 'user') {
        messageDiv.innerHTML = `
            <div class="message-content user-content">
                <p>${escapeHtml(content)}</p>
            </div>
            <div class="message-avatar user-avatar">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="white"/>
                </svg>
            </div>
        `;
    } else {
        let categoryBadge = '';
        if (category === 'platform') {
            categoryBadge = '<span class="category-badge platform-badge">📱 Platform Assistance</span>';
        } else if (category === 'medical') {
            categoryBadge = '<span class="category-badge medical-badge">🏥 Medical Assistance</span>';
        } else if (category === 'vision') {
            categoryBadge = '<span class="category-badge vision-badge">🖼️ Vision AI</span>';
        }
        
        let modelInfo = '';
        if (model) {
            modelInfo = `<span class="model-info">Powered by ${model}</span>`;
        }
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="12" cy="12" r="10"/>
                </svg>
            </div>
            <div class="message-content">
                ${categoryBadge}
                <p>${formatMessage(content)}</p>
                ${modelInfo}
            </div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    chatMessages.push({ type, content, category, model });
}

function addImageMessageToChat(type, content, imageFile) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}-message`;
    
    // Create image preview URL
    const reader = new FileReader();
    reader.onload = function(e) {
        const imageUrl = e.target.result;
        
        messageDiv.innerHTML = `
            <div class="message-content user-content">
                <img src="${imageUrl}" class="chat-image" alt="Uploaded image">
                <p>${escapeHtml(content)}</p>
            </div>
            <div class="message-avatar user-avatar">
                <svg viewBox="0 0 24 24" fill="currentColor">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="white"/>
                </svg>
            </div>
        `;
    };
    reader.readAsDataURL(imageFile);
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typingIndicator';
    typingDiv.className = 'chat-message assistant-message typing-indicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <svg viewBox="0 0 24 24" fill="currentColor">
                <circle cx="12" cy="12" r="10"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function formatMessage(text) {
    // Convert markdown-like formatting
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    text = text.replace(/\n/g, '<br>');
    
    // Convert bullet points
    text = text.replace(/^- (.*)/gm, '• $1');
    
    return text;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

