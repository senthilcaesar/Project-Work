from collections import OrderedDict

value = 'aaxbbbcxcccddeffvffggr'
non_repeat = OrderedDict()
value = list(value)

for c in value:
    if c in non_repeat:
        non_repeat[c] +=1
    else:
        non_repeat[c] = 1

for key in non_repeat:
    if non_repeat[key] == 1:
        first_non_repeat = key
        break
    
print("First non repeating character = ", first_non_repeat)