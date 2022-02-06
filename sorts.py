from time import time
import math as math
import numpy as np
import random as rand
rng = np.random.default_rng()


# ==================================================== STABLE ====================================================


def mergesort(dataset):
    """
    mergesort timing function, the bulk of the mergesort algorithm is in mergeSplit()

    :param dataset: input array
    :return: sorted array, the runtime of the sort
    """
    start_time = time()
    # the rightmost index of the initial set
    max_len = len(dataset) - 1
    mergeSplit(dataset, 0, max_len)
    end_time = time()
    return dataset, end_time - start_time


def radixLSB(dataset):
    """
    radix sort starting at the least significant bit, only utilizing 2 buckets.

    :param dataset: input array
    :return: sorted array, the runtime of the sort
    """
    temp = dataset.tolist()
    start_time = time()
    # iterate over the length of the longest value in the set
    for i in range(0, math.ceil(math.log2(max(temp)))):
        buckets = [[], []]
        # assign data to buckets based on value of bit at the current position
        for data in temp: buckets[data >> i & 1].append(data)
        # concatenate buckets in order and assign to the data set
        temp = buckets[0] + buckets[1]
    end_time = time()
    dataset = np.array(temp)
    return dataset, end_time - start_time


def radixLSD(dataset, base: int):
    """
    least-significant radix sort but using an integer base and standard arithmetic to calculate bucket count.

    :param dataset: input array
    :param base: int, indicating what base is used to create buckets and sort
    :return: sorted array, the runtime of the sort
    """
    temp = dataset.tolist()
    start_time = time()
    buckets = {}
    for i in range(0, math.ceil(math.log(max(temp), base))):
        # create buckets using arbitrary base
        for j in range(base): buckets[j] = []
        # formula used to find value of digit: floor(num) * digit mod base
        for data in temp: buckets[data // base ** i % base].append(data)
        temp.clear()
        for j in range(base): temp += buckets[j]
    end_time = time()
    dataset = np.array(temp)
    return dataset, end_time - start_time


def radixLSD2P(dataset):
    """
    least-significant radix sort, but predetermines the number of buckets to use
    best base is roughly 2^ceil(log2(max_value) / 2)

    :param dataset: input array
    :return: sorted array, the runtime of the sort
    """
    temp = dataset.tolist()
    start_time = time()
    # determine the best base to use
    power = math.ceil(math.log2(max(temp)) / 2)
    buckets = {}
    # pre-initializing values decreases runtime
    base = 2 ** power
    mask = base - 1
    # originally used i*power in the bucket assignment but having the power be the increment
    # guarantees no arithmetic during bucket calculation and thus less runtime
    for i in range(0, math.ceil(math.log(max(temp), base)) * power, power):
        for j in range(base): buckets[j] = []
        for data in temp: buckets[data >> i & mask].append(data)
        temp.clear()
        for j in buckets: temp += buckets[j]
    end_time = time()
    dataset = np.array(temp)
    return dataset, end_time - start_time


# =================================================== UNSTABLE ===================================================


def heapsort(dataset):
    """
    basic heapsort that heapifies up first then sifts down to find largest values.

    :param dataset: the full array of data
    :return: sorted array, the runtime of the sort
    """
    start_time = time()
    max_len = len(dataset)
    # heapify the set from below, O(n log n) worst case
    for i in range((max_len >> 1) - 1, -1, -1):
        heapify(dataset, i, max_len)
    # sift down, heapify can be repurposed for this
    for i in range(max_len - 1, 0, -1):
        # swap largest value with first value outside of sorting range
        swap(dataset, 0, i)
        # heapify again so that the largest value is at the top
        heapify(dataset, 0, i)
    end_time = time()
    return dataset, end_time - start_time


def quicksort(dataset):
    """
    iteratively partitions values in a array about the rightmost value, moving greater elements
    to the right and lesser elements to the left, adding ranges to a stack, then repeating for
    each range in the stack.

    :param dataset: the full array of data
    :return: sorted array, the runtime of the sort
    """
    start_time = time()
    left, right = 0, len(dataset) - 1
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
    end_time = time()
    return dataset, end_time - start_time


# =================================================== HELPERS ===================================================


def mergeSplit(dataset: np.array, left, right):
    """
    the bulk of the mergesort. splits the input array into sub-arrays and recursively sorts each
    of those sub-arrays before merging them.

    :param dataset:
    :param left:
    :param right:
    :return:
    """
    # operations are only done if the set being processed contains at least two elements
    if right - left > 0:
        # split the range in two by determine its midpoint, then run the mergesort on the subsets
        mid = left + (right - left) // 2
        mergeSplit(dataset, left, mid)
        mergeSplit(dataset, mid + 1, right)
        l_track = left
        r_track = mid + 1
        # temporary stack to track sorted elements
        temp = []
        while l_track < mid + 1 and r_track < right + 1:
            # get the smallest from each side of the array until one of the sides is completely sorted
            # this goes to the top of the stack
            if dataset[l_track] < dataset[r_track]:
                temp.append(dataset[l_track])
                l_track += 1
            else:
                temp.append(dataset[r_track])
                r_track += 1
        # append the rest of the remaining side of the array to the stack
        while l_track < mid + 1:
            temp.append(dataset[l_track])
            l_track += 1
        while r_track < right + 1:
            temp.append(dataset[r_track])
            r_track += 1
        # pop elements sequentially from the stack, smallest to largest
        for i in range(left, right + 1):
            dataset[i] = temp.pop(0)


def heapify(dataset, node, bound):
    """
    heapifies the input array, such that in a tree array where child nodes are 2 * node + 1 and 2 * node + 2
    any arbitrary parent will be greater than its children.
    this process is recursive, but recursion depth should not be an issue as the recursion depth is
    log2 of the size, and a 2^1000 size dataset is decidedly impractical.

    :param dataset: the input array
    :param node: the current
    :param bound:
    :return: None
    """
    left = node * 2 + 1
    right = node * 2 + 2
    largest = node
    if left < bound and dataset[left] > dataset[node]:
        largest = left
    if right < bound and dataset[right] > dataset[largest]:
        largest = right
    if largest != node:
        swap(dataset, node, largest)
        heapify(dataset, largest, bound)


def peek(stack):
    """
    helper function to peek at the top of a array, returning None if empty.

    :param stack: a array to be processed as a stack
    :return: the value at the top of the stack
    :rtype: generic or None
    """
    return stack[-1] if stack else None


def swap(dataset, i, j):
    """
    helper function to swap values at two indices in a array.

    :param dataset: the input array
    :param i: index 1
    :param j: index 2
    """
    dataset[i], dataset[j] = dataset[j], dataset[i]


# =========================================== DATA, FILE I/O, TESTING ===========================================


def genData(file, size, power=31):
    """
    generates random integer data within a certain range and puts it in a file.

    :param file: string - the relative path of the output file
    :param size: the amount of data to be generated
    :param power: 2^power is the max bound of randomly generated data
    :return: None
    """
    open(file, 'w').close()
    f = open(file, "a")
    for i in range(size):
        j = int(rng.random() * float(2 ** power - 1))
        f.write(str(j) + "\n")
    f.close()


def genDataArray(size, power=31):
    """
    generates random integer data within a certain range and returns it as a array.

    :param size: the amount of data to be generated
    :param power: 2^power is the max bound of randomly generated data
    :return: the randomly generated array
    """
    temp = []
    for i in range(size):
        temp.append(int(rand.random() * 2 ** power))
    return_array = np.array(temp)
    return return_array


def writeData(file, dataset):
    """
    writes data from a array onto a file, one line per element

    :param file: string - the relative path of the output file
    :param dataset: the array to be read from
    :return: None
    """
    open(file, 'w').close()
    f = open(file, "a")
    for i in dataset:
        f.write(str(i) + "\n")
    print(f'Results written to {f.name}')
    f.close()


def testSort(sort, title, dataset, write=None, opt=None, nl=True):
    """
    simple test for individual sorts.

    :param sort: a sorting function
    :param title: the name of the sort
    :param dataset: the input array
    :param write: an output file to write to - optional, no write if None, default None
    :param opt: parameter for sorts with a second field - optional, default None
    :param nl: whether a newline should be printed after the sort, default True
    :return:
    """

    print(f'Starting {title} on array of length {len(dataset)}')
    output, runtime = sort(dataset) if opt is None else sort(dataset, opt)
    print(f'{title.capitalize()} completed in {runtime} {"seconds" if runtime > 1 else "second"}'
          f', {validate(output)} discrepancies found with sorted list')
    if write is not None:  writeData(write, output)
    if nl: print()


def testSortIterative(sort, title, size, iterations, opt=None, nl=True):
    """
    simple test for individual sorts.

    :param sort: a sorting function
    :param title: the name of the sort
    :param opt: parameter for sorts with a second field - optional, default None
    :param nl: whether a newline should be printed after the sort, default True
    :return:
    """

    print(
        f'Starting {title}{"s" if iterations > 1 else ""} on {iterations} array{"s" if iterations > 1 else ""} of length {size}')
    total = 0
    total_errors = 0
    for i in range(iterations):
        dataset = genDataArray(size)
        dataset, runtime = sort(dataset) if opt is None else sort(dataset, opt)
        total += runtime
        total_errors += validate(dataset, False)
    avg = total / iterations
    avg_errors = total_errors / iterations
    print(f'{iterations} {title}{"s" if iterations > 1 else ""} completed in an average of {avg} '
          f'{"seconds" if avg > 1 else "second"}, with an average of {avg_errors if avg_errors != 0 else 0} '
          f'unsorted {"entries" if avg_errors > 1 or avg_errors == 0 else "entry"}')
    if nl: print()


def validate(dataset, verbose=True):
    """
    helper function to find the number of discrepancies in a supposedly sorted array.
    prints discrepancies for each position.

    :param verbose: whether each discrepancy ought to be printed or not
    :param dataset: input array
    :return: the number of discrepancies found, 0 if none
    :rtype: int
    """
    last = 0
    errors = 0
    for i in range(len(dataset)):
        if dataset[i] < dataset[last]:
            if verbose: print(f'discrepancy: element {i}: {dataset[i]} < element {last}: {dataset[last]}')
            errors += 1
        last = i
    return errors
