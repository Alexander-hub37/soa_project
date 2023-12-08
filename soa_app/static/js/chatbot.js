function sendMessage() {
    var userMessage = document.getElementById('user-input').value;
    if (userMessage.trim() !== '') {
        document.getElementById('user-input').value = '';  // Limpiar el input
        document.getElementById('chat-log').innerHTML += `
            <div class="message-container user-message">
                <div class="message">
                    ${userMessage}
                </div>
            </div>`;
        
        // Enviar mensaje al servidor
        fetch('/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': '{{ csrf_token }}' 
            },
            body: 'message=' + encodeURIComponent(userMessage)
        })
            .then(response => response.json())
            .then(data => {
                if (data.response) {
                    var botResponse = data.response;
                    document.getElementById('chat-log').innerHTML += `
                        <div class="message-container bot-message">
                            <div class="message">
                                ${botResponse}
                            </div>
                        </div>`;
                } else {
                    console.error('Error en la respuesta del servidor');
                }
            })
            .catch(error => {
                console.error('Error al enviar mensaje al servidor:', error);
            });
    } else {
        console.error('El mensaje del usuario no puede estar vacío.');
    }
}

function toggleChatWindow() {
    var chatWindow = document.getElementById('chat-window');
    chatWindow.style.transform = chatWindow.style.transform === 'translateY(0%)' ? 'translateY(150%)' : 'translateY(0%)';
}