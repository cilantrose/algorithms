from sorts import radixLSB, radixLSD, radixLSD2P, quicksort, heapsort, genData, toList, writeData, genDataList, validate
from time import time


def main():
    # genData("sample.txt", 1000000)
    # data = toList("sample.txt")
    data = genDataList(1000)
    print(f'Starting sort with {len(data)} elements')
    start_time = time()
    # output = radixLSB(data)
    output = radixLSD2P(data, 16)
    # output = quicksort(data, 0, len(data) - 1)
    end_time = time()
    print(f'Radix sort of length {len(output)} completed in {end_time - start_time} {"seconds" if end_time - start_time > 1 else "second"}')
    print(f'{validate(output)} discrepancies found')
    start_time = time()
    data = genDataList(1000)
    print(f'Starting sort with {len(data)} elements')
    output = quicksort(data, 0, len(data) - 1)
    end_time = time()
    print(f'Quicksort of length {len(output)} completed in {end_time - start_time} {"seconds" if end_time - start_time > 1 else "second"}')
    print(f'{validate(output)} discrepancies found')
    data = genDataList(1000)
    start_time = time()
    print(f'Starting sort with {len(data)} elements')
    output = heapsort(data)
    end_time = time()
    print(f'Heapsort of length {len(output)} completed in {end_time - start_time} {"seconds" if end_time - start_time > 1 else "second"}')
    print(f'{validate(output)} discrepancies found')
    writeData("out.txt", data)
    return


main()
