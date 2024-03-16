def less_than_k(k, list_n):
    """
    Return numbers from list_n that are less than k.

    Parameters:
    k (int): Threshold number.
    list_n (list of int): List of numbers to be compared against k.

    Returns:
    list of int: Numbers from list_n that are less than k.
    """
    return [n for n in list_n if n < k]
