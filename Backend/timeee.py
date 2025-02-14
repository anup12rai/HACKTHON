import datetime
import random
from TextToSpeech import TextToSpeech
def greetings():
    greetings_list = ["hi my name is nexo", "Hi sir how can i assist you", "nice to meet you sir i am nexo"]
    return random.choice(greetings_list)
def function():
    x = datetime.datetime.now()

    TextToSpeech(x.strftime("today is %B %d %A sir"))
function()    