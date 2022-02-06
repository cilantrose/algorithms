import sorts as sorts


if __name__ == '__main__':
    # sorts.testSortIterative(sorts.radixLSD2P, "radix sort", 10000, 100)
    # sorts.testSortIterative(sorts.heapsort, "heapsort", 10000, 100)
    # sorts.testSortIterative(sorts.quicksort, "quicksort", 10000, 100)
    sorts.testSort(sorts.mergesort, "mergesort", sorts.genDataArray(10000))
