import pandas as pd
import requests
import re

def format_player_name(name):
    """Formats name from user to be used for URL download link."""
    name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name) 
    return ''.join(word.capitalize() for word in name.split())


def download_data(name):
    """Downloads career data for given player."""
    player = format_player_name(name) #formating name input
    url = f"https://www.tennisabstract.com/jsmatches/{player}Career.js"
    response = requests.get(url, timeout=15)
	#Getting data from url
    if response.status_code == 404:
        raise ValueError(f"No career file found for '{name}'.")
    response.raise_for_status()
    return response.text