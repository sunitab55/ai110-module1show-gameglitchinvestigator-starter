from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_check_guess_returns_message():
    outcome, msg = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in msg

def test_guess_one_above_secret():
    outcome, _ = check_guess(51, 50)
    assert outcome == "Too High"

def test_guess_one_below_secret():
    outcome, _ = check_guess(49, 50)
    assert outcome == "Too Low"

def test_parse_guess_valid_integer():
    ok, val, err = parse_guess("42")
    assert ok and val == 42 and err is None

def test_parse_guess_empty_string():
    ok, _, _ = parse_guess("")
    assert not ok

def test_parse_guess_none():
    ok, _, _ = parse_guess(None)
    assert not ok

def test_parse_guess_non_numeric():
    ok, _, err = parse_guess("abc")
    assert not ok and "not a number" in err.lower()

def test_parse_guess_float_string():
    ok, val, _ = parse_guess("3.7")
    assert ok and val == 3  # truncates, not rounds

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 50)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 100)

def test_unknown_difficulty_fallback():
    assert get_range_for_difficulty("Impossible") == (1, 50)

def test_score_win_early_attempt():
    # attempt 1: 100 - 10*(1+1) = 80
    assert update_score(0, "Win", 1) == 80

def test_score_win_minimum_points():
    # Late win should award at least 10 points
    assert update_score(0, "Win", 20) >= 10

def test_score_too_high_even_attempt():
    assert update_score(50, "Too High", 2) == 55  # +5

def test_score_too_high_odd_attempt():
    assert update_score(50, "Too High", 3) == 45  # -5

def test_score_too_low():
    assert update_score(50, "Too Low", 1) == 45  # -5

def test_score_unknown_outcome_unchanged():
    assert update_score(50, "Gibberish", 1) == 50

