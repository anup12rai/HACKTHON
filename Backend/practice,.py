import time
from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_elon_musk_net_worth():
    query = "Elon Musk current net worth"
    search_results = search(query, num_results=5)  # Limit search to top 5 results

    for result in search_results:
        time.sleep(2)  # Add a 2-second delay between requests to avoid being blocked
        try:
            response = requests.get(result)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for specific tags or classes that might contain the net worth info
            # You need to inspect the webpage and adjust the tag/class as needed
            # Example: Searching for text or a tag with a specific class
            net_worth_tag = soup.find('div', {'class': 'net-worth'})  # Update this to the correct tag/class

            if net_worth_tag:
                return f"Elon Musk's current net worth: {net_worth_tag.text.strip()}"
            
        except requests.exceptions.RequestException as e:
            print(f"Error while scraping {result}: {e}")
    
    return "Could not find Elon Musk's net worth information."

print(get_elon_musk_net_worth())
