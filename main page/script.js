function updateTime() {
    const now = new Date();
    document.getElementById('dateWeather').innerText = now.toLocaleString();
}
setInterval(updateTime, 1000);
updateTime();

function sendMessage() {
    const msg = document.getElementById('message').value;
    if (msg) {
        document.getElementById('speechBox').innerText = msg;
    }
}

// Toggle function
function toggle(id) {
    const toggleOn = document.getElementById(`toggle-on-${id}`);
    const toggleOff = document.getElementById(`toggle-off-${id}`);

    if (toggleOn.style.display === 'inline') {
        toggleOn.style.display = 'none';
        toggleOff.style.display = 'inline';
    } else {
        toggleOn.style.display = 'inline';
        toggleOff.style.display = 'none';
    }
}

// Weather function
function processWeatherData(response) {
    const weatherInfo = document.getElementById('weatherInfo');
    const currentConditions = response.currentConditions;
    weatherInfo.innerText = `Temperature: ${currentConditions.temp}°F \n Condition: ${currentConditions.conditions}`;
}

fetch("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/kathmandu?unitGroup=us&key=W33RTSCK5XCBJK2XKTBAMETW5&contentType=json", {
    method: 'GET'
}).then(response => {
    if (!response.ok) {
        throw response; // Check the HTTP response code and if it isn't ok then throw the response as an error
    }
    return response.json(); // Parse the result as JSON
}).then(response => {
    // Response now contains parsed JSON ready for use
    processWeatherData(response);
}).catch((errorResponse) => {
    if (errorResponse.text) { // Additional error information
        errorResponse.text().then(errorMessage => {
            console.error(errorMessage); // Log the error message
        });
    } else {
        console.error('An unknown error occurred'); // No additional error information
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages');
    const typingIndicator = document.getElementById('typing');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');

    let isTyping = false;

    function addMessage(text, sender) {
        const messageElement = document.createElement('p');
        messageElement.classList.add('message', sender);
        messageElement.textContent = text;
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            messageInput.value = '';
            simulateBotResponse();
        }
    }

    function simulateBotResponse() {
        isTyping = true;
        typingIndicator.style.display = 'block';
        setTimeout(() => {
            isTyping = false;
            typingIndicator.style.display = 'none';
            addMessage('This is a bot response.', 'bot');
        }, 1000);
    }

    sendButton.addEventListener('click', sendMessage);

    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});

// websocket

const socket = new WebSocket("ws://localhost:8765");

socket.onmessage = function(event) {
    document.getElementById("response").innerText = event.data;
};

function sendMessage() {
    let message = document.getElementById("message-input").value;
    socket.send(message);
}