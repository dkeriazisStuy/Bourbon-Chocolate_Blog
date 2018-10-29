import string

# A bonus for a character matching its corresponding pattern character
MATCH_BONUS = 1

# Bonus for characters at the beginning of words
# (A word is defined as a group of text matching the following regex: /\w+/)
WORD_BONUS = 2
WORD_CHARS = string.ascii_letters + string.digits + '_'


def gap_bonus(n):
    """A bonus for shortened gaps between two matched characters"""
    return 20 / n


def immediacy_bonus(n):
    """A bonus for how early in the text the first match is found"""
    return 2 / (n + 1)


def smart_case(text, pattern):
    """Return """
    for p in pattern:
        if p not in string.ascii_lowercase:
            return text, pattern
    return text.lower(), pattern.lower()


def score(text, pattern):
    """Returns the score for a match of `pattern` on `text`"""
    num = 0
    if pattern == '' or text == '':
        return 0

    text, pattern = smart_case(text, pattern)
    pattern_index = 0
    pattern_char = pattern[0]
    last_index = None
    for i, c in enumerate(text):
        if c != pattern_char:  # Loop until c == pattern_char
            continue

        # Match bonus
        num += MATCH_BONUS

        # Word bonus
        if i == 0 or text[i-1] not in WORD_CHARS:
            num += WORD_BONUS

        # Gap bonus
        if last_index is not None:
            num += gap_bonus(i - last_index)

        # Immediacy bonus
        if last_index is None:
            num += immediacy_bonus(i)

        # Increment pattern
        last_index = i
        pattern_index += 1
        if pattern_index >= len(pattern):
            pattern_char = None
        else:
            pattern_char = pattern[pattern_index]

    if pattern_char is None:
        return num
    else:
        return 0

