import pandas as pd


def format_player_name(name):
    """Formats name from user to be used for URL download link."""
    name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name) 
    return ''.join(word.capitalize() for word in name.split())
