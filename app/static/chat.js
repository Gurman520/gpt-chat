let currentConversationId = null;
let isLoading = false;
let currentUser = null;

// Функция для авторизованных запросов
async function makeAuthRequest(url, options = {}) {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/';
        return;
    }

    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers
    };

    return fetch(url, {
        ...options,
        headers
    });
}

// Инициализация чата после загрузки страницы
document.addEventListener('DOMContentLoaded', async () => {
    // Проверяем авторизацию
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/';
        return;
    }

    try {
        // Получаем информацию о пользователе
        const userResponse = await makeAuthRequest('/api/auth/verify');
        if (!userResponse.ok) throw new Error('Not authorized');
        
        currentUser = await userResponse.json();
        document.getElementById('username-display').textContent = currentUser.username;
        
        // Загружаем чаты пользователя
        await loadUserConversations();
        
        // Назначаем обработчики
        setupEventListeners();
    } catch (error) {
        console.error('Auth check failed:', error);
        window.location.href = '/';
    }
});

function setupEventListeners() {
    // Создание нового диалога
    document.getElementById('new-conversation').addEventListener('click', async () => {
        if (isLoading) return;
        
        try {
            const response = await makeAuthRequest('/api/conversations', {
                method: 'POST'
            });

            if (!response.ok) throw new Error('Failed to create conversation');

            const conv = await response.json();
            const li = document.createElement('li');
            li.textContent = conv.title;
            li.dataset.id = conv.id;
            document.getElementById('conversation-list').appendChild(li);

            // Сразу загружаем и активируем новый диалог
            await loadConversation(conv.id);
        } catch (error) {
            console.error('Error creating conversation:', error);
            alert('Failed to create conversation');
        }
    });
    
    // Загрузка диалога при клике
    document.getElementById('conversation-list').addEventListener('click', (e) => {
        if (e.target.tagName === 'LI' && !isLoading) {
            loadConversation(parseInt(e.target.dataset.id));
        }
    });
    
    // Отправка сообщения
    document.getElementById('send-button').addEventListener('click', sendMessage);
    document.getElementById('message-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !isLoading) {
            sendMessage();
        }
    });
}

async function loadUserConversations() {
    try {
        const response = await makeAuthRequest('/api/conversations');
        if (!response.ok) throw new Error('Failed to load conversations');
        
        const conversations = await response.json();
        const list = document.getElementById('conversation-list');
        list.innerHTML = '';
        
        conversations.forEach(conv => {
            const li = document.createElement('li');
            li.textContent = conv.title;
            li.dataset.id = conv.id;
            list.appendChild(li);
        });
        
        if (conversations.length > 0) {
            loadConversation(conversations[0].id);
        }
    } catch (error) {
        console.error('Error loading conversations:', error);
    }
}

async function loadConversation(conversationId) {
    currentConversationId = conversationId;
    isLoading = true;
    hasActiveConversation = true;
    
    // Активируем поле ввода
    document.getElementById('message-input').disabled = false;
    document.getElementById('send-button').disabled = !hasActiveConversation;
    
    // Подсветка активного диалога
    document.querySelectorAll('#conversation-list li').forEach(li => {
        li.classList.toggle('active', parseInt(li.dataset.id) === conversationId);
    });
    
    try {
        const response = await makeAuthRequest(`/api/conversations/${conversationId}/messages`);
        if (!response.ok) throw new Error('Failed to load messages');
        
        const messages = await response.json();
        const messagesContainer = document.getElementById('messages');
        messagesContainer.innerHTML = '';
        
        messages.forEach(msg => {
            addMessageToChat(msg.role, msg.content, msg.formatted_content);
        });
    } catch (error) {
        console.error('Error loading messages:', error);
        hasActiveConversation = false;
        document.getElementById('message-input').disabled = true;
        document.getElementById('send-button').disabled = true;
    } finally {
        isLoading = false;
    }
}

async function sendMessage() {
    if (!hasActiveConversation) return;
    
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message || isLoading) return;
    
    addMessageToChat('user', message);
    input.value = '';
    showLoadingIndicator();
    
    try {
        const response = await makeAuthRequest(
            `/api/conversations/${currentConversationId}/messages`, 
            {
                method: 'POST',
                body: JSON.stringify({ message })
            }
        );
        
        if (!response.ok) throw new Error('Failed to send message');
        
        const assistantMessage = await response.json();
        hideLoadingIndicator();
        addMessageToChat(
            assistantMessage.role, 
            assistantMessage.content, 
            assistantMessage.formatted_content
        );
    } catch (error) {
        hideLoadingIndicator();
        addMessageToChat('assistant', `Error: ${error.message}`);
        console.error('Error sending message:', error);
    }
}

function addMessageToChat(role, content, formattedContent = null) {
    const messagesContainer = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${role}-message`);
    
    messageDiv.innerHTML = formattedContent || content;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showLoadingIndicator() {
    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML += `
        <div class="assistant-typing">
            <span>Лама думает </span>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideLoadingIndicator() {
    const indicator = document.querySelector('.assistant-typing');
    if (indicator) indicator.remove();
}

// Выход из системы
window.logout = function() {
    localStorage.removeItem('access_token');
    window.location.href = '/';
};


