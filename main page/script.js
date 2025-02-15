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

    socket.onopen = () => {
        console.log("Connected to WebSocket server.");
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const responseText = data.response;
        console.log("AI response:", responseText);

        const resultBox = document.getElementById("response");
        resultBox.textContent = responseText;
        speakText(responseText);
    };

    function speakText(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            utterance.volume = 1;
            utterance.rate = 1;
            utterance.pitch = 1;
            speechSynthesis.speak(utterance);
        } else {
            console.log("Sorry, your browser does not support speech synthesis.");
        }
    }

    voiceButton.onclick = () => {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;

            recognition.onstart = () => {
                console.log("Speech recognition started. Speak now...");
            };

            recognition.onresult = (event) => {
                const speechResult = event.results[0][0].transcript;
                console.log("Recognized speech:", speechResult);
                messageInput.value = speechResult;

                sendButton.click();
            };

            recognition.onerror = (event) => {
                console.error("Speech recognition error:", event.error);
                result.textContent = "Error in recognizing speech. Please try again.";
            };

            recognition.onend = () => {
                console.log("Speech recognition ended.");
            };

            recognition.start();
        } else {
            console.log("Sorry, your browser does not support speech recognition.");
            result.textContent = "Your browser does not support speech recognition.";
        }
    };
});