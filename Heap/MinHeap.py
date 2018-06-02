def buildHeap(x):
    heap_size = len(x)
    for i in range(heap_size//2-1, -1, -1):
        heapify(x, i, heap_size)

def heapify(x, i, heap_size):
    left = 2*i+1
    right = 2*i+2
    
    if left < heap_size and x[left] > x[i]:
        largest = left
    else:
        largest = i
    if right < heap_size and x[right] > x[largest]:
        largest = right
        
    if i != largest:
        tmp = x[i]
        x[i] = x[largest]
        x[largest] = tmp
        heapify(x, largest, heap_size)

def pop(x):
    n = len(x) - 1
    tmp = x[0]
    x[0] = x[n]
    x[n] = tmp
    print(tmp, "replaced by", x[0], "| size of heap = ", n+1)
    removed = x[-1]
    del x[-1]
    print("Removed idx = ", n, "| Removed Element = ", removed)
    if(n != 0):
        print("Root = ", x[0], "       | size of heap = ", n)
        heapify(x, 0, n)
        print("After Heapify root = ", x[0])
        print(" ")
    else:
        print(" ")
        print("Size of heap =", n)
        print("Heap is empty")
    
    return tmp

x = [16, 10, 14, 2, 3, 5]
buildHeap(x)
n = len(x)
''' Perform Heap sort in place '''
for i in range(n-1, -1, -1):
     x[i], x[0] = x[0], x[i]
     heapify(x, 0, i)
     
print ("Sorted array is")
for i in range(n):
    print ("%d" %x[i]),
