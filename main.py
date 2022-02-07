import searches
import sorts as sorts
import searches as search


if __name__ == '__main__':
    # sorts.testSortIterative(sorts.radixLSD2P, "radix sort", 10000, 100)
    # sorts.testSortIterative(sorts.heapsort, "heapsort", 10000, 100)
    # sorts.testSortIterative(sorts.quicksort, "quicksort", 10000, 100)
    a = sorts.genDataArray(10000, 9)
    sorts.testSort(sorts.mergesort, "mergesort", a, "out.txt")
    searches.testSearch(search.exponentialSearchRange, "exponential search", a, 511)
