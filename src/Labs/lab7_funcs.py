'''
No description needed at this point. Fill in the functions below
according to the description provided.

These functions must be solved RECURSIVELY. If your solution does
not use recursion, you risk receiving a zero on the lab submission.

'''

from typing import Any, Union

# --------------------------------------------------------------
# 1) Count occurrences
# --------------------------------------------------------------

def count(items: list[Any], target: Any):

    '''
    This function emulates the list method 'count'. Assume items
    is a list, and target is some object. Return the number of
    times that target appears in items.

    YOU MUST USE RECURSION!

    '''

    def run(index: int) -> int:
        return (1 + run(index + 1) if items[index] == target else run(index + 1)) if index < len(items) else 0

    return run(0)


# --------------------------------------------------------------
# 2) Sum of integers
# --------------------------------------------------------------

def integer_sum(items: list[Union[str, int, bool]]) -> int:

    '''
    This function calculates and returns the sum of the integer
    values in the list 'items'.

    Be careful - items may contain things other than integers!

    For example, if the input is [ 1, 3, 'hello', 5.66 ], you
    should return 4 (1 + 3).

    Hint: You can check if an object is an integer by performing
    the following comparison: type(obj) == int

    YOU MUST USE RECURSION!

    '''

    if len(items) < 1:
        return 0

    val = 0
    if type(items[0]) == int:
        val = items[0]

    items.pop(0)
    return val + integer_sum(items)



# --------------------------------------------------------------
# 3) Exponentiation
# --------------------------------------------------------------

def pow_rec(base: int, exponent: int) -> int:

    '''
    Assume that base and exponent are integers >= 0.

    Calculate and return base to the power of exponent using
    repeated multiplications.

    YOU MUST USE RECURSION!

    '''
    if exponent < 0:
        return 0
    return base * pow_rec(base, exponent-1) if exponent >= 1 else 1



# --------------------------------------------------------------
# 4) Palindrome checker
# --------------------------------------------------------------

def is_palindrome(text: str) -> bool:

    '''
    A recursion classic.

    Assume that 'text' is a string. Return True if text is a
    palindrome, and False otherwise.

    A string is a palindrome if it reads the same forwards and
    backwards. For example, 'racecar' is a palindrome.

    YOU MUST USE RECURSION!

    '''

    if len(text) <= 1:
        return True
    return is_palindrome(text[1:-1]) if text[0] == text[-1] else False


# --------------------------------------------------------------
# 5) Nested list reverser
# --------------------------------------------------------------

def nested_reverse(items: Any) -> Any:

    '''
    Assume that items is a list, that may contain nested lists
    as elements. This function will perform a reverse operation,
    but with a twist - nested sublists must be reveresed as well.

    For example, if the input is [ 1, 2, [5, 4, 3, [9, 0], 3] ]
    then you should return [ [ 3, [0, 9], 3, 4, 5], 2, 1 ]

    Hint: You can check if an object is a list by performing the
    following comparison: type(obj) == list

    YOU MUST USE RECURSION!

    '''

    if len(items) < 1:
        return []
    if len(items) < 2:
        return items

    last = items[-1:]
    rest = nested_reverse(items[:-1])

    return (last if type(last[0]) != list else [nested_reverse(last[0])]) + rest
