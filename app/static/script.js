let currentConversationId = null;
let isLoading = false;

document.addEventListener('DOMContentLoaded', () => {
    // Создание нового диалога
    document.getElementById('new-conversation').addEventListener('click', async () => {
        if (isLoading) return;
        
        const response = await fetch('/api/conversations', {
            method: 'POST'
        });
        const conv = await response.json();
        
        const li = document.createElement('li');
        li.textContent = conv.title;
        li.dataset.id = conv.id;
        document.getElementById('conversation-list').appendChild(li);
        
        // Загружаем новый диалог
        loadConversation(conv.id);
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
});

async function loadConversation(conversationId) {
    currentConversationId = conversationId;
    isLoading = true;
    
    // Подсветка активного диалога
    document.querySelectorAll('#conversation-list li').forEach(li => {
        li.classList.toggle('active', parseInt(li.dataset.id) === conversationId);
    });
    
    // Загрузка сообщений
    const response = await fetch(`/api/conversations/${conversationId}/messages`);
    const messages = await response.json();
    
    const messagesContainer = document.getElementById('messages');
    messagesContainer.innerHTML = '';
    
    messages.forEach(msg => {
        addMessageToChat(msg.role, msg.content);
    });
    
    isLoading = false;
}

async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message || !currentConversationId || isLoading) return;
    
    addMessageToChat('user', message);
    input.value = '';
    
    // Показываем индикатор загрузки
    showLoadingIndicator();
    
    try {
        const response = await fetch(`/api/conversations/${currentConversationId}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const assistantMessage = await response.json();
        // Убираем индикатор и показываем ответ
        hideLoadingIndicator();
        addMessageToChat(assistantMessage.role, assistantMessage.content, assistantMessage.formatted_content);
    } catch (error) {
        hideLoadingIndicator();
        addMessageToChat('assistant', `Error: ${error.message}`);
    }
}

function addMessageToChat(role, content, formattedContent = null) {
    const messagesContainer = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${role}-message`);
    
    if (formattedContent) {
        // Создаем DOM-элемент и вставляем как HTML
        const temp = document.createElement('div');
        temp.innerHTML = formattedContent;
        
        // Чистим и форматируем текст
        let cleanContent = '';
        temp.childNodes.forEach(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                cleanContent += node.textContent;
            } else if (node.nodeName === 'UL' || node.nodeName === 'OL') {
                node.querySelectorAll('li').forEach(li => {
                    cleanContent += `• ${li.textContent}\n`;
                });
            } else {
                cleanContent += node.textContent + '\n\n';
            }
        });
        
        messageDiv.textContent = cleanContent.trim();
    } else {
        messageDiv.textContent = content;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showLoadingIndicator() {
    const messagesContainer = document.getElementById('messages');
    
    // Удаляем старый индикатор, если есть
    const oldIndicator = document.querySelector('.assistant-typing');
    if (oldIndicator) oldIndicator.remove();
    
    // Создаем новый индикатор
    const indicator = document.createElement('div');
    indicator.className = 'assistant-typing';
    indicator.innerHTML = `
        <span>Лама думает </span>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    
    messagesContainer.appendChild(indicator);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function hideLoadingIndicator() {
    const indicator = document.querySelector('.assistant-typing');
    if (indicator) indicator.remove();
}