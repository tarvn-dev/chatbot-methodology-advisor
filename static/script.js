const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

let isTyping = false;

// Add message to chat
function addMessage(content, isUser = false, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = `message-content ${isError ? 'error-message' : ''}`;
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show typing indicator
function showTyping() {
    if (isTyping) return;
    isTyping = true;
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typing-indicator';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content typing-indicator';
    contentDiv.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
    
    typingDiv.appendChild(contentDiv);
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove typing indicator
function hideTyping() {
    const typing = document.getElementById('typing-indicator');
    if (typing) {
        typing.remove();
    }
    isTyping = false;
}

// Validate message
function validateMessage(message) {
    if (!message.trim()) {
        return 'Please enter a message';
    }
    if (message.length > 1000) {
        return 'Message too long. Please keep under 1000 characters.';
    }
    return null;
}

// Send message to backend
async function sendMessage() {
    const message = messageInput.value.trim();
    
    // Validate input
    const validationError = validateMessage(message);
    if (validationError) {
        addMessage(validationError, false, true);
        return;
    }
    
    // Add user message
    addMessage(message, true);
    messageInput.value = '';
    
    // Disable input
    sendButton.disabled = true;
    messageInput.disabled = true;
    showTyping();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
            timeout: 35000
        });
        
        const data = await response.json();
        hideTyping();
        
        if (data.status === 'success') {
            addMessage(data.response);
        } else {
            addMessage(data.error || 'Something went wrong. Please try again.', false, true);
        }
    } catch (error) {
        hideTyping();
        
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            addMessage('Connection error. Please check your internet and try again.', false, true);
        } else {
            addMessage('Request failed. Please try again.', false, true);
        }
    }
    
    // Re-enable input
    sendButton.disabled = false;
    messageInput.disabled = false;
    messageInput.focus();
}

// Reset conversation
async function resetConversation() {
    try {
        await fetch('/reset', { method: 'POST' });
        chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-content">
                    Hello! I'm here to help you choose the best project management methodology. 
                    Tell me about your project - team size, timeline, complexity, etc.
                </div>
            </div>
        `;
        messageInput.focus();
    } catch (error) {
        addMessage('Failed to reset conversation. Please refresh the page.', false, true);
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'r') {
        e.preventDefault();
        resetConversation();
    }
});

// Auto-resize input and character counter
messageInput.addEventListener('input', (e) => {
    const length = e.target.value.length;
    if (length > 900) {
        e.target.style.borderColor = '#ff6b6b';
    } else {
        e.target.style.borderColor = '#ddd';
    }
});

// Focus input on load
messageInput.focus();