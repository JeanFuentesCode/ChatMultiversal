const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// URL de tu backend (cámbiala cuando subas el backend a Render/Railway)
const API_URL = 'https://chatmultiversal.onrender.com/chat';

// Función para agregar mensajes al DOM
function addMessage(sender, text, isUser) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');
    msgDiv.classList.add(isUser ? 'user' : 'bot');
    
    // Si es un bot, le asignamos el dataset para pintarle el nombre del color correcto
    if (!isUser) {
        msgDiv.setAttribute('data-bot', sender);
    }

    let innerHTML = '';
    // Solo mostramos el nombre si es un bot
    if (!isUser) {
        innerHTML += `<span class="sender-name">${sender}</span>`;
    }
    
    // Reemplazamos los saltos de línea de la IA por etiquetas <br> de HTML
    const formattedText = text.replace(/\n/g, '<br>');
    innerHTML += `<p>${formattedText}</p>`;
    
    msgDiv.innerHTML = innerHTML;
    chatBox.appendChild(msgDiv);
    
    // Auto-scroll al fondo
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Indicador de "Escribiendo..."
function showTyping(show) {
    let indicator = document.getElementById('typing-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.classList.add('message', 'typing-indicator');
        indicator.textContent = 'Los bots están escribiendo...';
        chatBox.appendChild(indicator);
    }
    indicator.style.display = show ? 'block' : 'none';
    if (show) chatBox.scrollTop = chatBox.scrollHeight;
}

// Función principal para enviar el mensaje
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Bloquear el input mientras carga
    userInput.value = '';
    userInput.disabled = true;
    sendBtn.disabled = true;

    // Mostrar mensaje del usuario
    addMessage('Jean', text, true);
    
    // Mostrar que están pensando (tardan unos 5-10 seg)
    showTyping(true);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        });

        if (!response.ok) throw new Error('Error en el servidor');

        const data = await response.json();
        showTyping(false);

        // Iterar sobre las respuestas del array de los 3 bots
        if (data.responses && Array.isArray(data.responses)) {
            // Un pequeño delay entre mensajes para que parezca que responden uno tras otro
            data.responses.forEach((bot, index) => {
                setTimeout(() => {
                    addMessage(bot.name, bot.text, false);
                }, index * 800); // 800ms de diferencia entre cada mensaje
            });
        }

    } catch (error) {
        showTyping(false);
        addMessage('Sistema', 'Error de conexión con el servidor. Verifica que Uvicorn esté corriendo.', false);
        console.error(error);
    } finally {
        // Desbloquear el input
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Eventos de click y tecla Enter
sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function showTyping(show) {
    let indicator = document.getElementById('typing-indicator');
    if (show) {
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.id = 'typing-indicator';
            indicator.classList.add('message', 'bot', 'typing');
            indicator.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
            chatBox.appendChild(indicator);
        }
        indicator.style.display = 'flex';
        chatBox.scrollTop = chatBox.scrollHeight;
    } else if (indicator) {
        indicator.style.display = 'none';
    }
}

// REGISTRO DE PWA PARA QUE SALGA EL BOTÓN DE INSTALAR
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
            .then(reg => console.log('SW activo', reg))
            .catch(err => console.log('SW falló', err));
    });
}