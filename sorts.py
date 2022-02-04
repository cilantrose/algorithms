from math import log2, ceil, log


# ==================================================== STABLE ====================================================


def radixLSB(dataset: list):
    """
    radix sort starting at the least significant bit, only utilizing 2 buckets

    :param dataset: input list
    :return: sorted list
    """
    # iterate over the length of the longest value in the set
    for i in range(0, ceil(log2(max(dataset)))):
        buckets = [[], []]
        # assign data to buckets based on value of bit at the current position
        for data in dataset: buckets[data >> i & 1].append(data)
        # concatenate buckets in order and assign to the data set
        dataset = buckets[0] + buckets[1]
    return dataset


def radixLSD(dataset: list, base: int):
    """
    least-significant radix sort but using an integer base and standard arithmetic to calculate bucket count.

    :param dataset: input list
    :param base: int, indicating what base is used to create buckets and sort
    :return: sorted list
    """
    buckets = {}
    for i in range(0, ceil(log(max(dataset), base))):
        # create buckets using arbitrary base
        for j in range(base): buckets[j] = []
        # formula used to find value of digit: floor(num) * digit mod base
        for data in dataset: buckets[data // base ** i % base].append(data)
        dataset.clear()
        for j in range(base): dataset += buckets[j]
    return dataset


def radixLSD2P(dataset: list, power: int):
    """
    least-significant radix sort, but only accepting powers of 2 as a base.
    runtime is less (20-25% for 2^16) than arithmetic radix sort with same base due to usage of bitwise ops.
    best base is consistently 2^16 for large data sets.

    :param dataset: input list
    :param power: int, indicating which power of 2 used to create buckets and sort
    :return: sorted list
    """
    buckets = {}
    # pre-initializing values decreases runtime
    base = 2 ** power
    mask = base - 1
    # originally used i*power in the bucket assignment but having the power be the increment
    # guarantees no arithmetic during bucket calculation and thus less runtime
    for i in range(0, ceil(log(max(dataset), base)) * power, power):
        for j in range(base): buckets[j] = []
        for data in dataset: buckets[data >> i & mask].append(data)
        dataset.clear()
        for j in range(base): dataset += buckets[j]
    return dataset


# =================================================== UNSTABLE ===================================================


def quicksort(dataset: list, left, right):
    """
    iteratively partitions values in a list about the rightmost value, moving greater elements
    to the right and lesser elements to the left, adding ranges to a stack, then repeating for
    each range in the stack.

    :param dataset: the full list of data
    :param left: sorting range lower bound
    :param right: sorting range upper bound
    :return: the dataset - for convenience with assignment, although lists are already mutable inside functions
    """
    # initialize a stack to keep track of left/right pairs
    stack = [(left, right)]
    while len(stack) > 0:
        # get the current values from the current top of the stack
        index, pivot = left, right = peek(stack)
        # iterate over the range at the top of the stack
        for i in range(left, pivot):
            # compare values with pivot - increment least index if less than value at pivot
            if dataset[i] < dataset[pivot]:
                swap(dataset, i, index)
                index += 1
        # swapping the value at the pivot effectively moves greater values to the right of the pivot
        swap(dataset, index, pivot)
        stack.pop()
        # if there are valid ranges to the left or right of the current range, add them to the stack
        if index - 1 > left: stack.append([left, index - 1])
        if index + 1 < right: stack.append([index + 1, right])
    return dataset


def heapsort(dataset: list):
    return


# =================================================== HELPERS ===================================================


def swap(dataset, i, j):
    """
    helper function to swap values at two indices in a list

    :param dataset: the input list
    :param i: index 1
    :param j: index 2
    """
    dataset[i], dataset[j] = dataset[j], dataset[i]


def peek(stack):
    """
    helper function to peek at the top of a list, returning None if empty

    :param stack: a list to be processed as a stack
    :return: the value at the top of the stack
    :rtype: generic or None
    """
    return stack[-1] if stack else None
