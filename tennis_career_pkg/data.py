import pandas as pd
import requests
import json
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

def parse_js_matches(js_text):
    """Converts raw JS match data into a DataFrame."""
    start = js_text.index("var morematchmx")
    bracket = js_text.index("[", start)
    data, _ = json.JSONDecoder().raw_decode(js_text[bracket:])

    df = pd.DataFrame(data)
    df = df[[0, 1, 4, 11, 16]].copy()
    df.columns = ["Date", "Tournament", "Win/Lose",
                  "Opponent", "OpponentAgeRaw"]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
    return df

def calculate_opponent_age(df, is_female):
    """Calculate opponent ages for female or male match data."""
    if is_female:
        dob = pd.to_datetime(df["OpponentAgeRaw"],
                             format="%Y%m%d", errors="coerce")
        return (df["Date"] - dob).dt.days / 365.25
    return pd.to_numeric(df["OpponentAgeRaw"], errors="coerce")

def add_ages(df, player_dob, is_female):
    """Calculate player age and age difference."""
    df = df.copy()
    df["Age"] = (df["Date"] - pd.Timestamp(player_dob)).dt.days / 365.25
    df["OppAge"] = calculate_opponent_age(df, is_female)
    df["AgeDiff"] = df["Age"] - df["OppAge"]
    return df