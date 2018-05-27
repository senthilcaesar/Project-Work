import re
import itertools

def removeWhitespace(string):
    return re.sub(r'\s+', '', string)

def palindrome(x):
    j = len(x)
    for i in range(0, j//2):
        if x[i] != x[j-1]:
            return False
        j -= 1
    return True

def startEnd(string, substring):
    count = 0
    l = len(string)
    for i in range(0, l):
        for j in range(i, l):
            substring.append(string[i:j+1])
    for sub in substring:
        if len(sub) > 1 and sub[0] == '1' and sub[len(sub)-1] == '1':
            count += 1
    return count    
    
def lenghtofLongsubstring(string, substring):
    longest = 0
    l = len(string)
    for i in range(0, l):
        for j in range(i, l):
            substring.append(string[i:j+1])
            
    for sub in substring:
        if palindrome(sub) == True:
            if len(sub) > longest:
                longest = len(sub)
                longest_palindrome = sub
    print(longest_palindrome, "is the longest substring which is palindrome")
    substring = []

def highestConcat(arr):
    combinations = itertools.permutations(arr)
    maximum = 0
    for tup in combinations:
        concat = ''.join(str(x) for x in tup)
        if int(concat) > maximum:
            maximum = int(concat)
            combo = tup
    return list(combo)

def RemoveAlternativeDuplicate(string):
    seen = {}
    given = string.lower()
    given = list(given)
    for i in range(0, len(given)):
        c = given[i]
        if c in seen:
            seen[c] += 1
            given[i] = "$"            
            del seen[c]
        else:
            seen[c] = 1
            
    concat = ''.join(x for x in given)
    concat = concat.replace("$", "")
    return concat

def combinations(string, size):
    lst = list(string)
    combinations = set(itertools.permutations(lst, size))
    combos = []
    for tup in combinations:
        combine = ''.join(tup)
        combos.append(combine)
        
    for combined in combos:
        if palindrome(combined) == True:
            print(combined + ' ', end="")

#----------------------------------Test---------------------------------------#    
x = 'malayalam rotator'
substring = []
string = x.lower()
string = removeWhitespace(string)
ans = palindrome(string)
if ans == True:
    print(string, "is a Palindrome")
else:
    print(string, "is not a Palindrome")

print()
lenghtofLongsubstring(string, substring)
print()
print("Combinations of size 4 of", string, "which are also palindromes:")
combinations(string, 4)

num='0010110010'
count = startEnd(num, substring)
print("\n")
print("Number of substrings in", num,"which starts and end with a 1 = ", count)
print()
arr=[9, 93, 24, 6]
output = highestConcat(arr)
print("Highest number formed by concatening elements in", arr,"=", output)
print()
given = "you got beautiful eyes"
output_string = RemoveAlternativeDuplicate(given)
print("Removed alternate characters from", given, " = ", output_string)
