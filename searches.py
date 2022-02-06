import numpy as np


# ==================================================== SEARCH ====================================================


def binarySearch(dataset, key):
    """
    searches a sorted list by continually splitting the search range based on whether values on the
    left or right side of the search range are greater than the value being searched for.

    :param dataset: a sorted array
    :param key: the value to be searched for
    :return:
    """
    index = None
    left, right = 0, (len(dataset) - 1)
    mid = (right + left) // 2
    iterations = 0
    while right - left > 0:
        iterations += 1
        if dataset[mid] > key:
            right = left + (right - left) // 2
        else:
            left = left + (right - left) // 2 + 1
        mid = (right + left) // 2
        if dataset[mid] == key:
            index = mid
    return index, iterations


# =========================================== DATA, FILE I/O, TESTING ===========================================


def testSearch(search, title, dataset, key, v=False, nl=True):
    """"""

    print(f'Starting {title} on array of length {len(dataset)}')
    output, iterations = search(dataset, key)
    ver = np.where(dataset == key)
    print(f'{title.capitalize()} '
          f'{f"found {key} at index {output} in {iterations} steps" if output is not None else f"did not find {key} in the dataset"}')
    if v: print(f' - Dataset contains {key} at index {ver[0][0]}' if len(ver[0]) == 1
          else f' - Dataset contains {key} at indices {ver[0]}' if len(ver[0]) != 0
          else f' - Dataset does not contain {key}')
    if nl: print()

    return
