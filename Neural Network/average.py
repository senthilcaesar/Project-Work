import cv2
img = cv2.imread("../data/images/tile3_25.pgm", 0)
filename = 'crater.txt'
avg_file = 'avg.txt'
new_file = 'crater_coord_write.txt'

i = 0
w = 30
h = 30
coord = []
new_coord = []

for line in open(filename):
    line = line.split()
    x = int(line[0])
    y = int(line[1])
    tup = (x, y)
    coord.append(tup)

n = 0
avg_x = 0
avg_y = 0
result = 0
for i in range(len(coord)):
    for j in range(len(coord)):
            k = 0
           
            x_val = abs(coord[j][0] - coord[k][0])
            y_val = abs(coord[j][1] - coord[k][1])
            if  x_val < 25 and y_val < 25:
                #print k, j, len(coord), coord
                avg_x += coord[j][0]
                avg_y += coord[j][1]
                n += 1
            else:
                l1 = str(coord[j][0])
                l2 = str(coord[j][1])
                line = l1 + ' ' + l2
                with open(new_file, "a") as myfile:
                    myfile.write(line + '\n')
     
           
    # write average to file    
    print avg_x/n, avg_y/n, n
    averaged = str(avg_x/n) + ' ' + str(avg_y/n)
    n = 0
    avg_x = 0
    avg_y = 0
    with open(avg_file, "a") as avgfile:
        avgfile.write(averaged + '\n')
    
    # update the coordinates   
    coord = []        
    for line in open(new_file):
        line = line.split()
        x1 = int(line[0])
        y1 = int(line[1])
        tup = (x1, y1)
        coord.append(tup)

    # Before wrting the new coordinates empty the file content
    open(new_file, 'w').close() 

    if len(coord) < 1: break

