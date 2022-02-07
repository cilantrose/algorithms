import numpy as np


# ==================================================== SEARCH ====================================================


def binarySearch(dataset, key, t=None):
    """
    searches a sorted list by continually splitting the search range based on whether values on the
    left or right side of the search range are greater than the value being searched for.
    complexity is O(log n) - this version of the search always finds the greatest index at which the key occurs.

    :param t: tuple, represents an optional range
    :param dataset: a sorted array
    :param key: the value to be searched for
    :return: the largest index at which the key is found/None if not found and the number of iterations the search took
    """
    index = None
    # initializes values to track the range of values to be searched
    if t is None: left, right = 0, (len(dataset) - 1)
    else: left, right = t
    # initialize a midpoint value
    mid = (right + left) >> 1
    iterations = 0
    # iterate over the range while the range still consists of at least 2 values
    while right - left > 0:
        iterations += 1
        # if the key is to the left of the midpoint, shrink the right side of the range
        if key < dataset[mid]:
            right = left + ((right - left) >> 1)
        # otherwise, shrink the left side of the range
        else:
            left = left + ((right - left) >> 1) + 1
        # recalculate the midpoint
        mid = (right + left) >> 1
        if dataset[mid] == key:
            index = mid
    return index, iterations


def binarySearchLeastIndex(dataset, key, t=None):
    """
    searches a sorted list by continually splitting the search range based on whether values on the
    left or right side of the search range are greater than the value being searched for.
    complexity is O(log n) - this version of the search always finds the least index at which the key occurs.

    :param t: tuple, represents an optional range
    :param dataset: a sorted array
    :param key: the value to be searched for
    :return: the largest index at which the key is found/None if not found and the number of iterations the search took
    """
    index = None
    # initializes values to track the range of values to be searched
    if t is None: left, right = 0, (len(dataset) - 1)
    else: left, right = t
    # initialize a midpoint value
    mid = (right + left) >> 1
    iterations = 0
    # iterate over the range while the range still consists of at least 2 values
    while right - left > 0:
        iterations += 1
        # if the key is to the right of the midpoint, shrink the left side of the range
        if key > dataset[mid]:
            left = left + ((right - left) >> 1) + 1
        # otherwise, shrink the left side of the range
        else:
            right = left + ((right - left) >> 1)
        # recalculate the midpoint
        mid = (right + left) >> 1
        if dataset[mid] == key:
            index = mid
    return index, iterations


def exponentialSearch(dataset, key, lower=False):
    """
    searches for a potential range in a sorted array to do a binary search in first.

    :param dataset: a sorted array
    :param key: the value to be searched for
    :param lower: whether the binary search should find the least or greatest index
    :return: the largest index at which the key is found/None if not found and the number of iterations the search took
    """
    index = None
    iterations = 0
    max_index = len(dataset) - 1
    # handle the case in which the key is not in the range
    if key > dataset[max_index]:
        return None, 1
    left = 0
    right = 1
    power = -1
    # this finds a potential range to binary search in, sets to None if a valid range is not found
    while left < max_index:
        left = int(2 ** power)
        right = 2 ** (power + 1)
        if right > max_index: right = max_index
        # if the key is between the searched ranges, it exits the loop
        if dataset[right] >= key >= dataset[left]:
            break
        # if the right side of the searched range is the max and the key is not in between, breaks, sets returns to None
        elif dataset[right] == max_index:
            left = right = None
            break
        power += 1
    # do binary search to find least or greatest index, depending on optional arg
    if left is not None:
        if lower: index, temp = binarySearchLeastIndex(dataset, key, (left, right))
        else: index, temp = binarySearch(dataset, key, (left, right))
        iterations += temp
    return index, iterations


# =================================================== HELPERS ===================================================


def binarySearchRange(dataset, key):
    """
    performs a binary search to find the range of indices at which a value occurs in a set
    :param dataset: a sorted array
    :param key: the value to be searched for
    :return: either a single index, or a range of indices
    """
    right, iterations = binarySearch(dataset, key)
    left, temp = binarySearchLeastIndex(dataset, key)
    iterations += temp
    t = None
    if left is not None:
        t = left, right
    return t, iterations


def exponentialSearchRange(dataset, key):
    """
    performs an exponential search to find the range of indices at which a value occurs in a set
    :param dataset: a sorted array
    :param key: the value to be searched for
    :return: either a single index, or a range of indices
    """
    right, iterations = exponentialSearch(dataset, key)
    left, temp = exponentialSearch(dataset, key, True)
    iterations += temp
    t = None
    if left is not None:
        t = left, right
    return t, iterations


# =========================================== DATA, FILE I/O, TESTING ===========================================


def testSearch(search, title, dataset, key, v=True, nl=True):
    """
    simple test for individual searches.

    :param search: the search function to be used
    :param title: the name of the search
    :param dataset: a sorted array
    :param key: the key to be searched for
    :param v: whether the message should print where numpy.where() finds the same key in the dataset
    :param nl: whether there should be a newline printed after the report
    :return: None
    """
    print(f'Starting {title} on array of length {len(dataset)}')
    output, iterations = search(dataset, key)
    ver = np.where(dataset == key)
    print(f'{title.capitalize()} found {key} at {processOutput(output)} in {iterations} steps' if output is not None
          else f'{title.capitalize()} did not find {key} in the dataset')
    if v: print(f' - np.where() found {key} at index {ver[0][0]}' if len(ver[0]) == 1
          else f' - np.where() found {key} at indices {ver[0][0]} to {ver[0][len(ver[0]) - 1]}' if len(ver[0]) != 0
          else f' - np.where() did not find {key} in the dataset')
    if nl: print()


def processOutput(output):
    """
    processes the output of a search algorithm depending on whether it is a single value or a range
    :param output: the output of the search algorithm
    :return: a string that reports what the search algorithm found
    """
    if type(output) == int:
        return f'index {output}'
    if type(output) == tuple:
        return f'indices {output[0]} to {output[1]}' if output[1] > output[0] else f'index {output[0]}'
