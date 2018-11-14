N = 7

import itertools
some = ["".join(seq) for seq in itertools.product("-+", repeat=N-1)]
a = list(range(1, N+1))

for value in some:
    output = a[0]
    for i in range(0, len(value)):      
        if value[i] == '-':
            output -= a[i+1]
        else:
            output += a[i+1] 
    if output == 0:
        print(output, value)
