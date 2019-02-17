import queue
import time

def naiiveMatch(text, pattern):
    Q = queue.Queue()
    n = len(text)
    m = len(pattern)
    for s in range(n-m+1):
        matches = True
        for i in range(m):
            if pattern[i] != text[s+i]:
                matches = False
                break
        if matches:
            Q.put(s)
    return Q

            

def preprocess(pattern):
    # Longest Prexif that is also a suffix
    m = len(pattern)
    i, j = 0, 1 # initialize values for i and j
    suffix_table = [0]*m # create an empty suffic table all values initially to zero
    while j < m:
        if pattern[i] != pattern[j] and i == 0:
            j += 1
        elif pattern[i] == pattern[j]:
            suffix_table[j] = i+1
            j+=1
            i+=1
        else:
            j+=1
            i = suffix_table[i-1]
    return suffix_table

def KMP(text, pattern):
    suffix_table = preprocess(pattern)
    n = len(text)
    m = len(pattern)
    q = 0
    myQ = queue.Queue()
    for i,letter in enumerate(text):
        while q > 0 and pattern[q] != letter:
            q = suffix_table[q-1]
        if pattern[q] == letter:
            q += 1
        if q == m:
            myQ.put(i-m+1)
            q = suffix_table[q-1]
    return myQ


with open("testDocument.txt", 'r') as testFile:
    stringify = testFile.read()
    # word = stringify.split(' ')
    # print(len(word))
    t0 = time.time()
    q1 = KMP(stringify, "the")
    t1 = time.time()
    print("Execution time is {}".format(t1 - t0))
