import sorts as sorts


def main():
    data = sorts.genDataArray(1000000)
    sorts.testSort(sorts.radixLSD2P, "radix sort", data)
    data = sorts.genDataArray(1000000)
    sorts.testSort(sorts.quickSort, "quicksort", data)
    data = sorts.genDataArray(1000000)
    sorts.testSort(sorts.heapSort, "heapsort", data)
    return


main()
