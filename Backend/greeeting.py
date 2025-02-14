import random 
from TextToSpeech import TextToSpeech
from timeee import function
def greeting():
    greetings_list = [
        "Hello, I am Nexo.",
        "Hi, my name is Nexo.",
        "How can I assist you today, sir?",
        "Sir, what can I do for you?",
        "Greetings! Ready to help you.",
        "Hey there! How may I assist?",
        "At your service, sir!",
        "Hello! Need any help?",
        "Hi! What can I do for you?",
        "Welcome! How can I assist?",
        "Good to see you! Need any help?",
        "I'm here, ready to assist!",
        "Sir, awaiting your command.",
        "How’s your day going? Need assistance?",
        "Your assistant is online! What’s next?",
        "Nexo is active! What can I do for you?",
    ]
    return random.choice(greetings_list) 
def mainn():
    for i in range(0,1):
        TextToSpeech(greeting())
        function()

mainn()