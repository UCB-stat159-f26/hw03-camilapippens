from tennis_career_pkg.data import format_player_name

def test_format_player_name():
    assert format_player_name("serena williams") == "SerenaWilliams"
    assert format_player_name("Serena Williams") == "SerenaWilliams"
    assert format_player_name("SErenaWilliams") == "SerenaWilliams"
    assert format_player_name("Rafael Nadal") == "RafaelNadal"