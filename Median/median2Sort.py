x = [7, 8, 9, 10, 11, 12]
y = [1, 2, 3, 4 ,5, 6]

def median(x, y):
    print(x, y)
    length_x = len(x)
    length_y = len(y)
    nx = len(x)
    ny = len(y)
    if nx == 2 and ny ==2:
        return (x[1]+y[0]) // 2
    idx = length_x // 2
    idy = length_y // 2
    if nx != 2:
        if length_x % 2 != 0:
            print("m1 = ", x[idx])
            m1 = x[idx]
        else:
            print("m1 = ", x[idx-1], "+", x[idx])
            m1 = (x[idx -1] + x[idx]) // 2
    else:
        m1 = x[1]
    
    if ny != 2:
        if length_y % 2 != 0:
            print("m2 = ", y[idy])
            m2 = y[idy]
        else:
            print("m2 = ", y[idy-1], "+", y[idy])
            m2 = (y[idy -1] + y[idy]) // 2
    else:
        m2 = y[1]
        
    if m2 > m1:      
        x = x[x.index(m1):nx]
        y = y[0:y.index(m2)+1]
        return median(x, y)
    else:
        x = x[0:x.index(m1)+1]
        y = y[y.index(m2):ny]
        return median(y, x)

value = median(x,y)
print("Median of two sorted list = ", value)
