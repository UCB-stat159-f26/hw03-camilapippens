from html import unescape
from io import StringIO
import pandas as pd
import requests
import json
import re

PLAYER_DOBS = {
    "serenawilliams": "1981-09-26",
    "rafaelnadal": "1986-06-03"
}

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

def get_player_matches(name, birthdate=None):
    """Retrieve and clean a player's career matches."""
    raw = download_data(name)
    df = parse_js_matches(raw)
    is_female = (
        df["OpponentAgeRaw"].astype(str)
        .str.fullmatch(r"\d{8}").mean() > 0.5
    )
    player = format_player_name(name).casefold()
    dob = birthdate if birthdate is not None else PLAYER_DOBS.get(player)
    if dob is None:
        raise ValueError(f"Please provide a birthdate for {name} in format yyyy-mm-dd.")
    df = add_ages(df, dob, is_female)
    df.attrs["player"] = name
    return df