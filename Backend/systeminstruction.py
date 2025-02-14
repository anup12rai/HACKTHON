from dotenv import dotenv_values
from datetime import datetime

# Load environment variables from .env file
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

from datetime import datetime

def calculate_age(user_dob):
    # Parse the date of birth string into a datetime object
    dob_date = datetime.strptime(user_dob, "%Y-%m-%d")

    # Get the current date and time
    current_date = datetime.now()

    age_years = current_date.year - dob_date.year

   
    if (current_date.month, current_date.day) < (dob_date.month, dob_date.day):
        age_years -= 1

    return age_years


nexo = "2025-02-14"

# Call the function with the correct argument
age = calculate_age(nexo)
print(f"Age: {age}")



# User details and preferences
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



# System configuration message
System = f"""
Hello, your name is nexo, you are build by team 7 , you are the project of hackthon. you can controll the home automation like light, fan and other. you can make user entertainment. you can give all the user querry. you are the most advance ai
You have a real-time up-to-date information from the internet. 
*** Instructions: ***
- Do not tell time unless explicitly asked.
- Keep your responses concise and relevant to the question.
- Always respond in English, even if the question is in another language.
- Avoid providing notes or context about your training data. Focus solely on answering the question.
"""
