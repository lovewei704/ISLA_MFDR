# -*- coding: utf-8 -*-
# The whole class using camera(1) (The camera in the robot body)
# variable iii from main.py is a record of robot image (iii.jpg)
from __future__ import division
## sudo pip install future
import cv2
## sudo apt-get install libopencv-dev python-opencv 
import numpy as np
## sudo apt-get install python-numpy python-scipy python-matplotlib ipython
import Image
## sudo apt-get install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev
## sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
## sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
## sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib
import os
##Built-in

# Create a VideoCapture object
cap = cv2.VideoCapture(1)

# threshold image and then process and return result #
def thresholding_inv(image,Blur):
        equalizeHist = cv2.equalizeHist(image) # using CV.equalizeHistogram
        bin = cv2.medianBlur(equalizeHist, Blur) # using CV.medianBlur filter
        ret, bin = cv2.threshold(equalizeHist, cv2.THRESH_OTSU, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU) # using CV.threshold by OTSU
        
        return bin
def thresholding(image):
    bin = cv2.medianBlur(image, 3) # using CV.medianBlur filter
    ret, bin = cv2.threshold(image, cv2.THRESH_OTSU, 255, cv2.THRESH_BINARY) # using CV.threshold by OTSU

    return bin
# End threshold image #

# 定義img旋轉rotate函數
def rotate(image, angle, center=None, scale=1.0):
    # 獲取映像尺寸
    (h, w) = image.shape[:2]

    # 若未指定旋轉中心，則將映像中心設為旋轉中心
    if center is None:
        center = (w / 2, h / 2)

    # 執行旋轉
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h),borderValue=255 )
    # 返迴旋轉後的映像
    return rotated
# End rotate #

# this function is for robot walking and keep straight by the color block on the wall
def WallColor(RedOrGreen,iii): # Get wall color rectangle R or G , R=Red G=Green
    if RedOrGreen!="R" and RedOrGreen!="G": # If not R or G , just return nothing
        return "null"

    while(1):

        # Capture Video from Camera
        _, frame = cap.read()
        _, frame = cap.read()
        _, frame = cap.read()
        _, frame = cap.read()
        _, frame = cap.read()
        _, frame = cap.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range of green color in HSV 
        lower_green = np.array([35,50,100])
        upper_green = np.array([60,255,255])

        # Define range of red color in HSV 
        lower_red = np.array([-10,100,100])
        upper_red = np.array([10,255,255])

        # Save image by HSV
        cv2.imwrite("pic/"+str(iii)+'.bmp',hsv)
        cv2.imwrite('Wall.bmp',hsv)

        # Start croping wall image into three pieces
        cropimg=Image.open('Wall.bmp')
        iii=iii+1
        cropimg.crop( (100,0,247,480) ).save("pic/"+str(iii)+'.bmp')# Crop left part of image (x-bar=0~247)
        cropimg.crop( (100,0,247,480) ).save('left.bmp') # Save image
        iii=iii+1
        cropimg.crop( (247,0,394,480) ).save("pic/"+str(iii)+'.bmp')# Crop middle part of image (x-bar=247~394)
        cropimg.crop( (247,0,394,480) ).save('mid.bmp') # Save image
        iii=iii+1
        cropimg.crop( (394,0,540,480) ).save("pic/"+str(iii)+'.bmp')# Crop right part of image (x-bar=394~540)
        cropimg.crop( (394,0,540,480) ).save('right.bmp') # Save image
        iii=iii+1
        
        # Read all three part of wall image
        rim=cv2.imread('right.bmp') 
        mim=cv2.imread('mid.bmp')
        lim=cv2.imread('left.bmp')
        
        if RedOrGreen=="G": # If command is green block
            # Using define range of green color in HSV to delimit lower and upper bond
            lower=lower_green
            upper=upper_green
        elif RedOrGreen=="R": # If command is red block
            # Using define range of red color in HSV to delimit lower and upper bond
            lower=lower_red
            upper=upper_red

        # Processing right image and count the sum of color point
        mask_RG = cv2.inRange(rim, lower, upper) # Using CV.inRange to get mask of image (just like color point)
        res_RG = cv2.bitwise_and(rim,rim, mask= mask_RG) # Using CV.bitwise to delete all pixel which isn't in the range of mask_RG 
        cv2.imwrite("pic/"+str(iii)+'.bmp',res_RG) # Save image
        cv2.imwrite('rmask.bmp',res_RG) # Save image
        iii=iii+1
        rcount=mask_RG.sum() # Get the sum of color point in right part of image

        # Processing middle image and count the sum of color point
        mask_RG = cv2.inRange(mim, lower, upper) # Using CV.inRange to get mask of image (just like color point)
        res_RG = cv2.bitwise_and(mim,mim, mask= mask_RG) # Using CV.bitwise to delete all pixel which isn't in the range of mask_RG 
        cv2.imwrite("pic/"+str(iii)+'.bmp',res_RG) # Save image
        cv2.imwrite('mmask.bmp',res_RG) # Save image
        iii=iii+1
        mcount=mask_RG.sum() # Get the sum of color point in middle part of image

        # Processing left image and count the sum of color point
        mask_RG = cv2.inRange(lim, lower, upper) # Using CV.inRange to get mask of image (just like color point)
        res_RG = cv2.bitwise_and(lim,lim, mask= mask_RG) # Using CV.bitwise to delete all pixel which isn't in the range of mask_RG 
        cv2.imwrite("pic/"+str(iii)+'.bmp',res_RG) # Save image
        cv2.imwrite('lmask.bmp',res_RG) # Save image
        iii=iii+1
        lcount=mask_RG.sum() # Get the sum of color point in left part of image

        # The sum of mask in the image is from 0~78336000 
        #count_green=mask_green.sum() #0~78336000 
        #count_red=mask_red.sum() #0~78336000
        
        return lcount/1000,mcount/1000,rcount/1000,iii # return the color point of three part image
# End WallColor #


# This function is for robot checking if elevator has arrived the correct floor which it want to go
def CheckFloorColor():
        while(1):
                # Capture Video from Camera
                _, frame = cap.read()
                _, frame = cap.read()
                _, frame = cap.read()
                _, frame = cap.read()
                _, frame = cap.read()
                _, frame = cap.read()

                # Convert BGR to HSV
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # define range of green color in HSV 
                lower_green = np.array([35,50,100])
                upper_green = np.array([60,255,255])

                # define range of red color in HSV 
                lower_red = np.array([-10,100,100])
                upper_red = np.array([10,255,255])

                cv2.imwrite('countFloor.bmp',hsv) # Save HSV image

                # Processing image and count the sum of green color point
                mask_G = cv2.inRange(hsv, lower_green, upper_green) # Using CV.inRange to get mask of image (just like color point)
                res_G = cv2.bitwise_and(hsv,hsv, mask= mask_G)  # Using CV.bitwise to delete all pixel which isn't in the range of mask_RG
                cv2.imwrite('Gmask.bmp',res_G) # Save image
                gcount=mask_G.sum()# Get the sum of color point in left part of image
                # Processing image and count the sum of red color point
                mask_R = cv2.inRange(hsv, lower_red, upper_red) # Using CV.inRange to get mask of image (just like color point)
                res_R = cv2.bitwise_and(hsv,hsv, mask= mask_R)  # Using CV.bitwise to delete all pixel which isn't in the range of mask_RG
                cv2.imwrite('Rmask.bmp',res_R) # Save image
                rcount=mask_R.sum()# Get the sum of color point in left part of image

                # Check if it's target floor (4 floor = green , 7 floor = red)
                TargetFloor=0
                if gcount>1000000: # If is 4 floor
                        TargetFloor=4
                elif rcount>1000000: # If is 7 floor
                        TargetFloor=7
                print rcount,gcount
                return TargetFloor # Return which floor robot arrived
# End CheckFloorColor #


# This function is for robot pressing up/down button , by using camera(1) (The camera in the robot body)
def UpDownBtnPress(iii): 
    # Capture Video from Camera
    _, frame = cap.read()
    _, frame = cap.read()
    _, frame = cap.read()
    _, frame = cap.read()
    _, frame = cap.read()
    _, frame = cap.read()
    _, frame = cap.read()
    _, frame = cap.read()

    
    cv2.imwrite("pic/"+str(iii)+'.jpg',frame) # Save image
    iii=iii+1
    cv2.imwrite('UD.jpg',frame) # Save image
    # crop the middle part of elevator button from image (x-bar=100~540)
    im=Image.open('UD.jpg')
    im.crop( (100,0,540,480) ).save('EleUpDownBtnCutted.jpg') # crop and save image
    img=cv2.imread('EleUpDownBtnCutted.jpg',0)
    img=thresholding_inv(img,9) # using def thresholding_inv
    img=rotate(img,5)   # using def rotate
    cv2.imwrite('EleUpDownBtninv.jpg',img) # Save image
    cv2.imwrite("pic/"+str(iii)+'.jpg',img) # Save image
    iii=iii+1

    # Find contours in image by openCV and sort them all
    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])
            
    arr = []   
    for index, (c, _) in enumerate(cnts): # Bound all contours by rectengle
        (x, y, w, h) = cv2.boundingRect(c) # Bounding contours 
        try:
            # Save contours which 20>width>100 and 40>height>200 or delete
            if w > 20 and h > 40 and w < 100 and h < 200:
                if (h/w)>1.8 and (h/w)<2.2:
                    add = True
                    if add:
                        arr.append((x, y, w, h)) # If contours have to save , append on arr[] (arr[i]=(X-bar,Y-bar,width,height)
        except IndexError:
            pass

    TargetNum=-1
    # Start check all number of image by arr[]
    for arrnum in range(0,len(arr),+1):
            im=Image.open('EleUpDownBtninv.jpg') # Open thresholded image
            # Crop the image by arr and get the number picture
            im.crop( (arr[arrnum][0],arr[arrnum][1],arr[arrnum][0]+arr[arrnum][2],arr[arrnum][1]+arr[arrnum][3]) ).save('SplitPic.bmp')
            im=cv2.imread("SplitPic.bmp")
            im=thresholding(im) # Using def thresholding
            im=cv2.resize(im,(20,40)) # Resize the number picture to 20x40 pixel
            cv2.imwrite('2040pix.bmp',im) # Save image

            # Change the image into 0/1 list
            imarr=[]
            i=0
            while i < 40: # 20x40 Pixel 建立要讀取之數字陣列
                j=0
                while j < 20:
                    if im[i][j][0]==255:
                        imarr.append(0) # If point is white = 0
                    else:
                        imarr.append(1) # If point is black = 1
                    j+=1
                i+=1

            temp_path = os.getcwd() # Find the folder path by os

            for f in os.listdir(temp_path+'/temp_panel/'):  #進入temp內的資料夾
                    DBimg=cv2.imread(temp_path+'/temp_panel/'+os.path.join(f))
                    i=0
                    DBimgarr=[]     #清空DBimgArray
                    while i < 40:    #20x40 Pixel 建立DBimg陣列
                        j=0
                        while j < 20:
                            if DBimg[i][j][0]==255:
                                DBimgarr.append(0) # If point is white = 1
                            else:
                                DBimgarr.append(1) # If point is black = 1
                            j+=1
                        i+=1

                    Num=0
                    Different=0
                    while Num<800:
                        if imarr[Num]!=DBimgarr[Num]: # If database image point isn't same as robot image , Different +1
                            Different+=1
                        Num+=1
                    print Different

                    if(Different>200): # If the smallest different point>120 then it must not the button
                        SmallestNumber="None"
                    else:
                        TargetNum=arrnum
                        break

    # We've got the button location then have to tell main process if button location is in the right range to press
    if TargetNum!=-1:
        print arr[TargetNum][0]

        # Button is at middie of the image => return "MID" to main.py
        if arr[TargetNum][0]>(443-arr[TargetNum][2])/2-10 and arr[TargetNum][0]<(443-arr[TargetNum][2])/2+10:
            return "MID",iii
        # Button is at right of the image => return "LEFT" to main.py
        elif arr[TargetNum][0]<(443-arr[TargetNum][2])/2-10:
            return "LEFT",iii
        else:# Button is at left of the image => return "RIGHT" to main.py
            return "RIGHT",iii
    else:
        return "PASS",iii
# End UpDownBtnPress #




