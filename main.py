import cv2
import numpy as np
import math


filepath = "C:/Users/datis/Downloads/consider.jpg"
filepath2 = "C:/Users/datis/Downloads/output.jpg"

bmp = cv2.imread(filepath)


bmp = cv2.cvtColor(bmp, cv2.COLOR_BGR2GRAY)

_, bmp = cv2.threshold(bmp, 127, 255, cv2.THRESH_BINARY)


width = len(bmp[0]) - (len(bmp[0])%2)
height = len(bmp) - (len(bmp)%2)


if(height > width):
    factor = math.ceil(height/200)
else:
    factor = math.ceil(width/200)

cv2.waitKey(0)


newwidth = int(width/factor)
newheight = int(height/factor)

newwidth, newheight = newheight, newwidth


empty = np.zeros((newwidth, newheight))


for j in range(0, newheight-3):
    for i in range(0, newwidth-3):
        
        empty[i][j] = ((bmp[i*factor][j*factor] + bmp[(i*factor)+1][j*factor] + bmp[i*factor][(j*factor)+1] + bmp[(i*factor)+1][(j*factor)+1])/4)


file = open("output.gcode", 'a')



cv2.imwrite(filepath2, empty)


cv2.imshow('frame', empty)
cv2.waitKey(0)

line = []


for i in range(0, len(empty)):
    for j in range(0, len(empty[0])):
        string = ""
        if(empty[i][j] == 0):
            string += "G0 X" + str((j+40)) + " Y" + str((200-i)) + "\n"
            string += "G0 X" + str((j+40)) + " Y" + str((200-i)) + " Z3\n"
        else:
            string += "G0 Z6\n"
            
        line.append(string)

file.write("G28\nM220 S500\n")
for i in line:
    file.write(i)

file.close()

cv2.waitKey(0)


