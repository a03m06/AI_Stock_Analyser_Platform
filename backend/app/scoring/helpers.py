def higher_is_better(value, benchmark, weight):

    if value is None:
        return 0

    score = (value / benchmark) * weight

    return round(
        min(score, weight),
        2
    )


def lower_is_better(value, benchmark, weight):

    if value is None:
        return 0

    ratio = benchmark / max(value, 0.01)

    score = ratio * weight

    return round(
        min(score, weight),
        2
    )