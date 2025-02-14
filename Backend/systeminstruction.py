from dotenv import dotenv_values
from datetime import datetime

# Load environment variables from .env file
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

def calculate_age(user_dob):
    # Parse the date of birth string into a datetime object
    dob_date = datetime.strptime(user_dob, "%Y-%m-%d")

    # Get the current date and time
    current_date = datetime.now()

    # Calculate the age in years
    age_years = current_date.year - dob_date.year

    # Check if the birthday hasn't occurred yet this year
    if (current_date.month, current_date.day) < (dob_date.month, dob_date.day):
        age_years -= 1

    return age_years

# Dates of birth for Aniruddha and Rezina
dob_aniruddha = "2005-10-30"
dob_rezina = "2006-04-19"


# Calculate the ages
age_aniruddha = calculate_age(dob_aniruddha)
age_rezina = calculate_age(dob_rezina)

# User details and preferences
user_details = {
    #"name": ""jarvic",
    #"email": ""jarvic",
}
hardware_control = {
    "turn on": {
        "LED": {
            "LED1": "on",
            "LED2": "on"
        },
        "light": {
            "light1": "on",
            "light2": "on"
        },
        "fan": {
            "fan1": "on",
            "fan2": "on"
        },
        "ceiling_fan": {
            "ceiling_fan1": "on",
            "ceiling_fan2": "on"
        }
    },
    "turn off": {
        "LED": {
            "LED1": "off",
            "LED2": "off"
        },
        "light": {
            "light1": "off",
            "light2": "off"
        },
        "fan": {
            "fan1": "off",
            "fan2": "off"
        },
        "ceiling_fan": {
            "ceiling_fan1": "off",
            "ceiling_fan2": "off"
        }
    }
}

real_detail = "when aniruddha,rezina,family ask for somthing to buy or somethings what in the data then say can i search for you then it give realtimedetails according to data from {user_details}"
    


# System configuration message
System = f"""
Hello, I am jaris, and you are a very accurate and advanced AI chatbot named {Assistantname} with real-time, up-to-date information from the internet.

{Username}'s details are here: {user_details}. {real_detail}. you can controll the hardwalso details here:{hardware_control}. when i say boring or tired then you recomended the song for me or jokes for me ok

*** Instructions: ***
- Do not tell time unless explicitly asked.
- Keep your responses concise and relevant to the question.
- Always respond in English, even if the question is in another language.
- Avoid providing notes or context about your training data. Focus solely on answering the question.
"""
