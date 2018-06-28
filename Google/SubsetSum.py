''' BackTracking Recursive Algorithm '''

nsets = 0
def backtrack(total, arr, num):
    i = 0
    global nsets
    l = len(arr)
    if(l == 0): return True
    total = total
    sub_arr = arr[i:l]
    add_sub_arr = sum(sub_arr)
        
    i += 1
    right_total = total
    right_sub_arr = sub_arr[i:l]
    countr = add_sub_arr - sub_arr[i-1]
    #print("Right = ", right_total, countr)
    if(right_total == num and countr == 0): nsets += 1
    
    left_total = total + sub_arr[i-1]
    left_sub_arr = sub_arr[i:l]
    countl = add_sub_arr - sub_arr[i-1]
    #print("Left = ", left_total, countl)
    if(left_total == num and countl == 0): nsets += 1
    
    backtrack(left_total, left_sub_arr, num)
    backtrack(right_total, right_sub_arr, num)
    
    return nsets

arr = [2, 4, 6, 10, 5, 1, 3]
num = 10
nsets = backtrack(0, arr, num)
print("No of subsets with sum equal to", num, " = ", nsets)
