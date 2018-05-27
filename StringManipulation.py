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
