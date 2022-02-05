import sorts as sorts


if __name__ == '__main__':
    data = sorts.genDataArray(100000)
    sorts.testSort(sorts.radixLSD2P, "variable base radix sort", data)
    sorts.testSortIterative(sorts.heapSort, "heapsort", 1000, 1000)
    sorts.testSortIterative(sorts.quickSort, "quicksort", 1000, 1000)
