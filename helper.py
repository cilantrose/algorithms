from random import random


def genData(file, size):
    open(file, 'w').close()
    f = open(file, "a")
    for i in range(size):
        j = int(random() * float(2 ** 31 - 1))
        f.write(str(j) + "\n")
    f.close()


def genDataList(size):
    return_list = []
    for i in range(size):
        return_list.append(int(random() * float(2 ** 31 - 1)))
    return return_list


def toList(file):
    dataset = []
    f = open(file, "r")
    for line in f:
        dataset.append(int(line.strip()))
    f.close()
    return dataset


def writeData(file, dataset):
    open(file, 'w').close()
    f = open(file, "a")
    for i in dataset:
        f.write(str(i) + "\n")
    f.close()
