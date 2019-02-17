import queue
import time

def timer(func):
    def f(*args, **kwargs):
        before = time.time()
        rv = func(*args, **kwargs)
        after = time.time()
        print("The function {} has exectution Time = {}".format(func.__name__, after - before))
        return rv
    return f

@timer
def naiiveMatch(text, pattern):
    Q = queue.Queue()
    n = len(text)
    m = len(pattern)
    for s in range(n-m+1):
        for i in range(m):
            if pattern[i] != text[s+i]:
                break
        else:
            Q.put(s)
    return Q

            
@timer
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

@timer
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
    q1 = KMP(stringify, "hello")
    q2 = naiiveMatch(stringify, "hello")
