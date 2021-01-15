import imutils
import cv2

import matplotlib.pyplot as plt

def Image_Pre_Processing(image):
    
    im1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    deltax = int(250/8.8)
    deltay = int(250/8.5)
    cells = []

    resized = imutils.resize(im1, width=300)
    ratio = im1.shape[0] / float(resized.shape[0])

    im2 = resized.copy()
    im2 = 255 - im2
    
    thresh = cv2.adaptiveThreshold(im2, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, -6)

    cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    reject_num = 0

    for c in cnts:
        area = cv2.contourArea(c)
        if(area > 30000): #mudar threshld
            d = c
            break
        else:

            reject_num += 1
            
    
    if(reject_num == len(cnts)):
        return False, None, None
    
    #maxarea = argmax(c)
    

    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    #for debug only, no other use in this project
    
    #M = cv2.moments(c)

    #if M["m00"] !=0:
    #    cX = int((M["m10"] / M["m00"]) * ratio) - 25
    #    cY = int((M["m01"] / M["m00"]) * ratio) - 25
    #else:
        # set values as what you need in the situation
    #    cX, cY = 0, 0

    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    d = d.astype("float")
    d *= ratio
    d = d.astype("int")

    x,y,w,h = cv2.boundingRect(d)
    x += 40
    y += 40
    w -= 80
    h -= 80

    ROI = cv2.adaptiveThreshold(imutils.resize(im1[y:y+h, x:x+w], width = 250),
                255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 5)
    #ROI = cv2.adaptiveThreshold(imutils.resize(im1, width = 250),
    #            255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 5)
    #fig, axis = plt.subplots(9, 9)
    
    for j in range(0,9):
        for k in range(0,9):
            cells.append(ROI[max((k*deltay - 2), 0):((k+1)*deltay - 2), j*deltax:(j+1)*deltax])
            cells[j*9+k] = cv2.resize(cells[j*9+k], (32,32))
            #axis[k, j].imshow(cells[j*9+k].squeeze(), cmap="gray")
    #plt.show(block=True)
    
    return True, ROI, cells
    
    
def process_frame(image):
    im1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    deltax = int(250/8.8)
    deltay = int(250/8.5)
    cells = []

    resized = imutils.resize(im1, width=300)
    ratio = im1.shape[0] / float(resized.shape[0])

    im2 = resized.copy()
    im2 = 255 - im2
    
    thresh = cv2.adaptiveThreshold(im2, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, -6)

    cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    reject_num = 0

    for c in cnts:
        area = cv2.contourArea(c)
        if(area > 30000): #mudar threshld
            d = c
            break
        else:
            reject_num += 1
    
    if(reject_num == len(cnts)):
        return image
    
    d = d.astype("float")
    d *= ratio
    d = d.astype("int")

    x,y,w,h = cv2.boundingRect(d)
    x += 40
    y += 40
    w -= 80
    h -= 80

    ROI = cv2.rectangle(image.copy(), (x, y), (x + w, y + h), (255,0,0), 2)
    
    return ROI