# transfer single label file into dataset(mask picture)
import cv2
import numpy as np

loc=input("Drag your label file here(special UTF-8 in path is not availiable)->")
loc=loc.replace("\\","/")
loc=loc.replace("\"","")

data = []
for line in open(loc,"r"):
    data.append(line)

w,h = data[1][1:-2].split(',')
w = int(eval(w))
h = int(eval(h))
poly = []
for points in range(len(data)):
    if points < 3:
        continue
    x1,y1 = data[points][1:-2].split(',')
    x1 = eval(x1)
    y1 = eval(y1) 
    poly.append([x1,y1])

bkg = np.zeros((h,w,3))
poly_array = np.array(poly,dtype = np.int32)
cv2.fillPoly(bkg,np.int32([poly_array]),(0,0,255))
loc_new = loc[0:-3]+"jpg"
cv2.imwrite(loc_new,bkg)

