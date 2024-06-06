'''
Utils files for data. Help with simple calculations and presentation of data
'''

# std imports

# 3rd party imports

# local imports

SCORE_MIN_VALUE = 0
SCORE_MAX_VALUE = 100
COLORS_INTERVALS = {
    'red': (SCORE_MIN_VALUE, 50),
    'yellow': (50, 75),
    'green': (75, SCORE_MAX_VALUE),
}


def check_score_in_range(score: int) -> None:
    '''
    Check if score is out of range. Raises ValueError if this condition is met.
    Args:
        score (int): It represents a scale value between 0 and 100.
    Returns:
        None
    '''
    if score < SCORE_MIN_VALUE or SCORE_MAX_VALUE < score:
        raise ValueError(f'''
            Score {
                score
            } is out of range (Should be between {
                SCORE_MIN_VALUE
            } and {
                SCORE_MAX_VALUE
            }).
        ''')


def sentiment_color(score: int) -> str:
    '''
    Find the correct color associated to a score according to a lookup table.
    Args:
        score (int): It represents a scale value between 0 and 100.
    Returns:
        str: The color representing the perception of the score according to the defined ranges.
    '''
    check_score_in_range(score)

    # Check low - high intervals for matching and return color
    for color, (low, high) in COLORS_INTERVALS.items():
        if low <= score and score <= high:
            return color


if __name__ == '__main__':
    assert sentiment_color(50) == 'red'
    assert sentiment_color(75) == 'yellow'
    assert sentiment_color(100) == 'green'
    print(f'All tests passed')
