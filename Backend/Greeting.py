import random 
from TextToSpeech import TextToSpeech
def greetings():
    greetings_list = ["hi my name is nexo", "Hi sir how cani assist you", "nice to meet you sir i am nexo"]
    return random.choice(greetings_list)
TextToSpeech(greetings())