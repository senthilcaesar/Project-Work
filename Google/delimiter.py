filename = 'testgood.txt'
delimiter = []
error = False

for line in open(filename):
    for c in line:
        if c == '{' or c == '(' or c == '[':
            delimiter.append(c)
        if c == '}' or c == ')' or c == ']':
            lastd = delimiter[-1]
            if c == '}' and lastd == '{' or\
               c == ')' and lastd == '(' or\
               c == ']' and lastd == '[':
                   c1 = delimiter.pop()
            else:
                error = True
                c1 = delimiter[-1]
                break

if len(delimiter) == 0 and not error:
    print("The Balance check is okay") 
if error:         
    print("Mismatched pair ", c, "and", c1)
if len(delimiter) > 0 and not error:
    print("There are missing closing delimiters")
