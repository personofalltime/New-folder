import cv2
import numpy as np
import math

def increase_brightness(img, value=180):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

filepath = "C:/Users/datis/Downloads/spiderman.jpg"
filepath2 = "C:/Users/datis/Downloads/output.jpg"

bmp = cv2.imread(filepath)

bmp = increase_brightness(bmp)

bmp = cv2.cvtColor(bmp, cv2.COLOR_BGR2GRAY)

width = len(bmp[0]) - (len(bmp[0])%2)
height = len(bmp) - (len(bmp)%2)

bmp = cv2.bitwise_not(bmp)


if(height > width):
    factor = math.ceil(height/200)
else:
    factor = math.ceil(width/200)

cv2.waitKey(0)

bmp = cv2.Canny(bmp, 0, 255)


yes, hierarchy = cv2.findContours(bmp, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print(len(yes))

bmp = cv2.drawContours(bmp, yes, -1, (255,255,255), 3)


newwidth = int(width/factor)
newheight = int(height/factor)

newwidth, newheight = newheight, newwidth


empty = np.zeros((newwidth, newheight))


for j in range(0, newheight-3):
    for i in range(0, newwidth-3):
        
        empty[i][j] = math.floor((bmp[i*factor][j*factor] + bmp[(i*factor)+1][j*factor] + bmp[i*factor][(j*factor)+1] + bmp[(i*factor)+1][(j*factor)+1])/4)


file = open("output.gcode", 'a')


cv2.imwrite(filepath2, empty)
_, empty = cv2.threshold(empty, 60, 255, cv2.THRESH_BINARY)


cv2.imshow('frame', empty)
cv2.waitKey(0)

line = []



for i in range(0, len(empty)):
    for j in range(0, len(empty[0])):
        string = ""
        if(empty[i][j] >= 1):
            string += "G0 X" + str((j+40)) + " Y" + str((200-i)) + " Z0\n"
        else:
            string += "G0 Z5\n"
        line.append(string)

file.write("G28\nM220 S500\n")
for i in line:
    file.write(i)

file.close()

cv2.waitKey(0)


