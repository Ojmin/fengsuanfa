def isLeapYear(year):
    return (not (year % 4 and year % 100)) or (not year % 400)


def mod(money):
    cent = int(money * 100)
    all_cent = {25: 0, 10: 0, 5: 0, 1: 0}
    for k in all_cent:
        all_cent[k], cent = divmod(cent, k)
    return all_cent


def maxCommonDivisor(m, n):
    while True:
        remainder = m % n
        if not remainder:
            return n
        else:
            m, n = n, remainder


# 三角打印
def triangleDisplay(mystr):
    # mystr = unicode(mystr, 'utf-8')
    mystr += ' '
    result = []
    le = len(mystr)
    for i in range(1, le):
        result.append(mystr[-i: -1])
    for i in range(le):
        result.append(mystr[i: -1])
    return result


def insertSort(seq):
    for j in range(1, len(seq)):
        key = seq[j]
        print(key)
        # insert arrays[j] into the sorted seq[0...j-1]
        i = j - 1
        while i >= 0 and seq[i] > key:
            seq[i + 1] = seq[i]
            i -= 1
        seq[i + 1] = key


def selectSort(sqe):
    le = len(sqe)
    for i in range(le - 1):
        minIndex = i
        for j in range(i, le):
            print(j)
            if sqe[minIndex] > sqe[j]:
                minIndex = j
        if minIndex != i:
            sqe[i], sqe[minIndex] = sqe[minIndex], sqe[i]

    return sqe


def inserts(seq):
    for i in range(len(seq) - 1):  # xunhuancishu
        for j in range(i + 1):
            if seq[i] > seq[i + 1]:
                seq[i + 1], seq[i] = seq[i], seq[i + 1]
            else:
                pass
            i -= 1
    return seq


def mergeSort(seq):
    if len(seq) <= 1:
        return seq
    mid = len(seq) // 2
    left = mergeSort(seq[:mid])
    right = mergeSort(seq[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += (left[i:])
    result += (right[j:])
    return result


def bubbleSort(seq):
    for i in range(len(seq) - 1):
        for j in range(1, len(seq) - i):
            if seq[j] < seq[j - 1]:
                seq[j - 1], seq[j] = seq[j], seq[j - 1]
    return seq


def build_heap(seq):
    l = len(seq)
    for root in range((l - 2) // 2, -1, -1):
        re_heap(seq, l, root)


def re_heap(seq, size, root):
    larger = root
    left = root * 2 + 1
    right = left + 1
    if left < size and seq[left] > seq[larger]:
        larger = left
    if right < size and seq[right] > seq[larger]:
        larger = right
    if larger != root:
        seq[larger], seq[root] = seq[root], seq[larger]
        re_heap(seq, size, larger)


def heap_sort(seq):
    build_heap(seq)
    size = len(seq)
    for i in range(size - 1, -1, -1):
        seq[0], seq[i] = seq[i], seq[0]
        re_heap(seq, i, 0)
    return seq


def quick_sort(array):
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less_than_pivot = [x for x in array[1:] if x < pivot]
        more_than_pivot = [x for x in array[1:] if x >= pivot]
        return quick_sort(less_than_pivot) + [pivot] + quick_sort(more_than_pivot)


import random



def radixSort():
    A=[random.randint(1,99) for i in range(10)]
    for k in range(2):#2轮
        s=[[] for i in range(10)]
        for i in A:
            s[(i//(10**k)%10)].append(i)
        A=[ b for a in s for b in a]
    return A

if __name__ == '__main__':
    import math

    print(math.floor(2.5))
    print(radixSort())

