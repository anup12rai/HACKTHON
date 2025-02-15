function updateTime() {
    const now = new Date();
    document.getElementById('dateWeather').innerText = now.toLocaleString();
}
setInterval(updateTime, 1000);
updateTime();

// Toggle function
function toggle(id) {
    const toggleOn = document.getElementById(`toggle-on-${id}`);
    const toggleOff = document.getElementById(`toggle-off-${id}`);
    let valueToSend;

    if (toggleOn.style.display === 'inline') {
        toggleOn.style.display = 'none';
        toggleOff.style.display = 'inline';
        if (id === 'bed') {
            valueToSend = '0'; // Send 0 when bed light is toggled off
        } else if (id === 'kitchen') {
            valueToSend = '00'; // Send 00 when kitchen light is toggled off
        } else if (id === 'fan') {
            valueToSend = '000'; // Send 000 when fan is toggled off
        }
    } else {
        toggleOn.style.display = 'inline';
        toggleOff.style.display = 'none';
        if (id === 'bed') {
            valueToSend = '1'; // Send 1 when bed light is toggled on
        } else if (id === 'kitchen') {
            valueToSend = '11'; // Send 11 when kitchen light is toggled on
        } else if (id === 'fan') {
            valueToSend = '111'; // Send 111 when fan is toggled on
        }
    }

    // Set the value to the message input and send it
    const messageInput = document.getElementById('messageInput');
    messageInput.value = valueToSend;
    document.getElementById('sendButton').click();
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
    const voiceButton = document.getElementById('voiceButton');
    const result = document.getElementById('response');

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

    // WebSocket
    const socket = new WebSocket("ws://localhost:8765");

    // Speech Recognition Setup
    let recognition;
    let isRecognitionActive = false;
    
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        recognition.continuous = true; // Keep listening continuously

        recognition.onstart = () => {
            console.log("Speech recognition started. Speak now...");
            isRecognitionActive = true;
            voiceButton.classList.add('active');
        };
// changing here 
recognition.onresult = (event) => {
    const speechResult = event.results[event.resultIndex][0].transcript;
    console.log("Recognized speech:", speechResult);
    messageInput.value += speechResult + ' '; // Append recognized speech to input
    sendButton.click();
};
//end here
        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
            if (event.error === 'not-allowed') {
                result.textContent = "";//error msg hya raha but tost banayera
                
            }
            isRecognitionActive = false;
            voiceButton.classList.remove('active');
        };

        recognition.onend = () => {
            console.log("Speech recognition ended.");
            voiceButton.classList.remove('active');
            if (isRecognitionActive) {
                // Auto-restart listening if still active
                recognition.start();
            }
        };
    }

    voiceButton.onclick = () => {
        if (!recognition) {
            result.textContent = "Speech recognition not supported in your browser.";
            return;
        }
        
        if (!isRecognitionActive) {
            try {
                recognition.start();
                isRecognitionActive = true;
            } catch (error) {
                console.error("Error starting recognition:", error);
            }
        } else {
            isRecognitionActive = false;
            recognition.stop();
        }
    };
});