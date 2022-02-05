from math import log2, ceil, log
from random import random


# ==================================================== STABLE ====================================================


def radixLSB(dataset: list):
    """
    radix sort starting at the least significant bit, only utilizing 2 buckets.

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
    best base is roughly 2^ceil(log2(max(dataset)))

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
    :return: sorted list
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
    """
    basic heapsort that heapifies up first then sifts down to find largest values.

    :param dataset: the full list of data
    :return: sorted list
    """
    max_len = len(dataset)
    # heapify the set from below, O(n log n) worst case
    for i in range(max_len // 2 - 1, -1, -1):
        heapify(dataset, i, max_len)
    # sift down, heapify can be repurposed for this
    for i in range(max_len - 1, 0, -1):
        # swap largest value with first value outside of sorting range
        swap(dataset, 0, i)
        # heapify again so that the largest value is at the top
        heapify(dataset, 0, i)
    return dataset


# =================================================== HELPERS ===================================================


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


def validate(dataset):
    """
    helper function to find the number of discrepancies in a supposedly sorted list.
    prints discrepancies for each position.

    :param dataset: input list
    :return: the number of discrepancies found, 0 if none
    :rtype: int
    """
    last = 0
    errors = 0
    for i in range(len(dataset)):
        if dataset[i] < dataset[last]:
            print(f'discrepancy: element {i}: {dataset[i]} < element {last}: {dataset[last]}')
            errors += 1
        last = i
    return errors


def peek(stack):
    """
    helper function to peek at the top of a list, returning None if empty.

    :param stack: a list to be processed as a stack
    :return: the value at the top of the stack
    :rtype: generic or None
    """
    return stack[-1] if stack else None


def swap(dataset, i, j):
    """
    helper function to swap values at two indices in a list.

    :param dataset: the input list
    :param i: index 1
    :param j: index 2
    """
    dataset[i], dataset[j] = dataset[j], dataset[i]


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
        j = int(random() * float(2 ** power - 1))
        f.write(str(j) + "\n")
    f.close()


def genDataList(size, power=31):
    """
    generates random integer data within a certain range and returns it as a list.

    :param size: the amount of data to be generated
    :param power: 2^power is the max bound of randomly generated data
    :return: the randomly generated list
    :rtype: list[int]
    """
    return_list = []
    for i in range(size):
        return_list.append(int(random() * float(2 ** power - 1)))
    return return_list


def toList(file):
    """
    takes data from a file and puts it in a list.

    :param file: string - the relative path of the output file
    :return: the list
    :rtype: list[int]
    """
    dataset = []
    f = open(file, "r")
    for line in f:
        dataset.append(int(line.strip()))
    f.close()
    return dataset


def writeData(file, dataset):
    """
    writes data from a list onto a file, one line per element

    :param file: string - the relative path of the output file
    :param dataset: the list to be written
    :return: None
    """
    open(file, 'w').close()
    f = open(file, "a")
    for i in dataset:
        f.write(str(i) + "\n")
    f.close()
