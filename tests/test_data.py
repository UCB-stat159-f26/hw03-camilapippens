from tennis_career_pkg.data import (format_player_name,
									parse_js_matches,
								    calculate_opponent_age,
									add_ages)
import pandas as pd
import pytest
from pathlib import Path

def test_format_player_name():
    assert format_player_name("serena williams") == "SerenaWilliams"
    assert format_player_name("Serena Williams") == "SerenaWilliams"
    assert format_player_name("SErenaWilliams") == "SerenaWilliams"
    assert format_player_name("Rafael Nadal") == "RafaelNadal"

mockup = Path(__file__).parent/"mockup"

def test_parse_female_matches():
    js_text = (mockup/"female_player.js").read_text()
    matches = parse_js_matches(js_text)
    assert len(matches) == 3
    assert matches.iloc[0]["Opponent"] == "Anne Miller"

def test_parse_male_matches():
	js_text = (mockup/"male_player.js").read_text()
	matches = parse_js_matches(js_text)
	assert len(matches) == 3
	assert matches.iloc[0]["Opponent"] == "Guillermo Platel"

def test_female_opponent_age():
    raw = (mockup/"female_player.js").read_text()
    df = parse_js_matches(raw)
    ages = calculate_opponent_age(df, is_female=True)
    expected = (
        pd.Timestamp("1995-10-30") -
        pd.Timestamp("1977-01-19")
    ).days / 365.25
    assert ages.iloc[0] == pytest.approx(expected)

def test_male_opponent_age():
	raw = (mockup/"male_player.js").read_text()
	df = parse_js_matches(raw)
	ages = calculate_opponent_age(df, is_female=False)
	assert ages.iloc[0] == pytest.approx(22.264202601)

def test_player_ages():
    raw = (mockup / "female_player.js").read_text()
    matches = parse_js_matches(raw)
    result = add_ages(matches, "1981-09-26", True)
    assert "Age" in result.columns
    assert "OppAge" in result.columns
    assert "AgeDiff" in result.columns
    assert result.iloc[0]["Age"] < 15