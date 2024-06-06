'''
Utils files for handlers
'''

# std imports

# 3rd party imports

# local imports

SCORE_MIN_VALUE = 0
SCORE_MAX_VALUE = 100


def sentiment_color(score: int) -> str:
    '''
    Args:
        score (int): It represents a scale value between 0 and 100.
    Returns:
        str: The color representing the perception of the score according to the defined ranges.
    '''
    # Guard Clause for score out of score ranges
    if score < SCORE_MIN_VALUE or SCORE_MAX_VALUE < score:
        error = f'''
        Score {
            score
        } is out of range (Should be between {
            SCORE_MIN_VALUE
        } and {
            SCORE_MAX_VALUE
        }).
        '''
        raise ValueError(error)

    # Ranges flow control
    red_max_score = (SCORE_MAX_VALUE - SCORE_MIN_VALUE) // 2  # 50
    yellow_max_score = SCORE_MAX_VALUE - red_max_score // 2  # 75

    if score <= red_max_score:
        return 'red'
    elif score <= yellow_max_score:
        return 'yellow'
    return 'green'
