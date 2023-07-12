import cv2
import numpy as np
import math


filepath = "C:/Users/datis/Downloads/spiderman.jpg"
filepath2 = "C:/Users/datis/Downloads/spiderman1.jpg"

bmp = cv2.imread(filepath)

bmp = cv2.cvtColor(bmp, cv2.COLOR_BGR2GRAY)

width = len(bmp[0]) - (len(bmp[0])%2)
height = len(bmp) - (len(bmp)%2)




if(height > width):
    factor = math.ceil(height/200)
else:
    factor = math.ceil(width/200)

cv2.waitKey(0)

_, bmp = cv2.threshold(bmp, 127, 255, cv2.THRESH_BINARY)

newwidth = int(width/factor)
newheight = int(height/factor)

newwidth, newheight = newheight, newwidth


empty = np.zeros((newwidth, newheight))


for j in range(0, newheight-3):
    for i in range(0, newwidth-3):
        
        empty[i][j] = (bmp[i*factor][j*factor] + bmp[(i*factor)+1][j*factor] + bmp[i*factor][(j*factor)+1] + bmp[(i*factor)+1][(j*factor)+1])/4


cv2.imshow("frame", empty)

cv2.imwrite(filepath2, empty)

file = open("output.gcode", 'a')

line = []

for i in range(0, len(empty)):
    for j in range(0, len(empty[0])):
        string = ""
        if(empty[i][j] == 0):
            string += "G0 X" + str((j+40)) + " Y" + str((200-i)) + " Z0\n"
            string += "G4 P100\n"
            string += "G0 X" + str((j+40)) + " Y" + str((200-i)) + " Z5\n"
        line.append(string)

file.write("G28\nM220 S500\n")
for i in line:
    file.write(i)

file.close()

cv2.waitKey(0)


