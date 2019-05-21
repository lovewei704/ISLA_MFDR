# encoding: utf-8
# the whole class don't use camera while running
# variable iii from main.py is a record of robot image (iii.jpg)
import numpy as py
## sudo apt-get install python-numpy python-scipy python-matplotlib ipython
import cv2
## sudo apt-get install libopencv-dev python-opencv 
import matplotlib as mat
## sudo apt-get install python-matplotlib
import Image
## sudo apt-get install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev
## sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
## sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
## sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib
import os
##Built-in
import random
##Built-in

location="0" # Record elevator button location variable

# threshold image and then process and return result #
def thresholding_inv(image): # using CV.equalizeHistogram
    bin = cv2.medianBlur(image, 3) # using CV.medianBlur filter
    ret, bin = cv2.threshold(image, cv2.THRESH_OTSU, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU) # using CV.threshold by OTSU
        
    return bin
def thresholding(image):
    bin = cv2.medianBlur(image, 3) # using CV.medianBlur filter
    ret, bin = cv2.threshold(image, cv2.THRESH_OTSU, 255, cv2.THRESH_BINARY) # using CV.threshold by OTSU

    return bin
# End threshold image #

# Find all buttons in the image #
def ContoursBound(img):
    # Find contours in image by openCV and sort them all
    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])
    
    arr = []
    
    for index, (c, _) in enumerate(cnts): # Bound all contours by rectengle
            (x, y, w, h) = cv2.boundingRect(c) # Bounding contours
            try:
                    # Save contours which 15>width>35 and 30>height>50 or delete it
                    if w > 10 and h > 30 and w < 35 and h < 50: 
                            add = True
                            if add:
                                    arr.append((x, y, w, h)) # If contours have to save , append on arr[] (arr[i]=(X-bar,Y-bar,width,height)
            except IndexError:
                    pass
    return arr,contours
# End ContoursBound #

# 本程式用於已有資料庫的情況下，指定要從影像中抓出幾號的位置
def CheckNumber(NumberUWant,iii):
    temp_path = os.getcwd()
    # Split 2 Number from Main
    Num1=str(NumberUWant)[0:1]
    Num2=str(NumberUWant)[1:2]

    img=cv2.imread("Btn.jpg",cv2.IMREAD_GRAYSCALE) # Read Button image which robot got

    img=thresholding_inv(img)
    cv2.imwrite('INVimg.bmp',img) # Save image after thresholding
    cv2.imwrite("pic/"+str(iii)+'.bmp',img) # Record every picture
    iii=iii+1

    arr,contours=ContoursBound(img) # Find all buttons in the image 

    cv2.drawContours(img,contours,-1,(255,255,255),2) # Draw contours on image (-1=draw all contours)
    
    temp_path = os.getcwd() # Find the folder path by os

    # If target elevator floor >9 (two numbers floor)
    if(Num2!=""):
        # clean all variable
        Num1FoundCount=0
        Num2FoundCount=0
        Num1arr=[]
        Num2arr=[]

        # Start check all number of image by arr[]
        for arrnum in range(0,len(arr),+1):
            im=Image.open('INVimg.bmp') # Open thresholded image
            # Crop the image by arr and get the number picture
            im.crop( (arr[arrnum][0],arr[arrnum][1],arr[arrnum][0]+arr[arrnum][2],arr[arrnum][1]+arr[arrnum][3]) ).save('SplitPic.bmp')
            im=cv2.imread("SplitPic.bmp")
            im=thresholding(im)
            im=cv2.resize(im,(25,25)) # Resize the number picture to 25x25 pixel
        
            
            # Change the image into 0/1 list
            imarr=[]
            i=0
            while i < 25:# 5x5 Pixel 建立要讀取之數字陣列
                j=0
                while j < 25:
                    if im[i][j][0]==255: # If point is white = 0
                        imarr.append(0)
                    else: # If point is black = 1
                        imarr.append(1)
                    j+=1
                i+=1
        
        
            SmallestD=999999    #與所要讀取之數字相差最少者
            SmallestNumber='X'  #最小者的檔名
            for root in os.listdir(temp_path+'/templates'): #進入temp中
                for f in os.listdir(temp_path+'/templates/'+root):  #進入temp內的資料夾
                    DBimg=cv2.imread(temp_path+'/templates/'+os.path.join(root, f))
                    i=0
                    DBimgarr=[]     #清空DBimgArray
                    while i < 25:    #25x25 Pixel 建立DBimg陣列
                        j=0
                        while j < 25:
                            if DBimg[i][j][0]==255: # If point is white = 0
                                DBimgarr.append(0)
                            else: # If point is black = 1
                                DBimgarr.append(1)
                            j+=1
                        i+=1
        
                    Num=0
                    Different=0
                    while Num<625:
                        if imarr[Num]!=DBimgarr[Num]: # If database image point isn't same as robot image , Different +1
                            Different+=1
                        Num+=1
                        
                    # Save the smallest different points of database image number
                    if(SmallestD>Different):
                        SmallestD=Different
                        SmallestNumber=root
                        if(Different>120): # If the smallest different point>120 then it must not the number we want
                            SmallestNumber="None"
            # Start saving all Num1 array and Num2 array (cuz if there got lots of same number in the image , we should check if it is the number we want) 
            if(SmallestNumber==Num1):
                Num1arr.append( (arr[arrnum][0],arr[arrnum][1],arr[arrnum][2],arr[arrnum][3]) )
                Num1FoundCount=Num1FoundCount+1
            if(SmallestNumber==Num2):
                Num2arr.append( (arr[arrnum][0],arr[arrnum][1],arr[arrnum][2],arr[arrnum][3]) )
                Num2FoundCount=Num2FoundCount+1
        print Num1arr,Num2arr

        #判斷相鄰 (Check all num1 and num2 and if they're nearby , those two number is our target) 
        for i in range(0,len(Num1arr),+1):
            j=0
            while j <len(Num2arr):
                if(Num1arr[i][0]!=Num2arr[j][0]):
                    # Check if Num1 Y-bar and Num2 Y-bar point distance below 10
                    if(Num2arr[j][1]-Num1arr[i][1]<10 and Num2arr[j][1]-Num1arr[i][1]>-10):
                        # Check if Num1 X-bar and Num2 X-bar point distance below 30 and num2 X-bar must larger then num1
                        if(Num2arr[j][0]-Num1arr[i][0]<30 and Num2arr[j][0]-Num1arr[i][0]>0):
                            W=Num2arr[j][0]+Num2arr[j][2] # W must be Num2arr[m][0]+Num2arr[m][2] (0<=m<len(num2[]))
                            H=0 # H is the biggest height between Num1[n][3] and Num2[m][3] (0<=n<len(num1[]) , 0<=m<len(num2[])
                            X=Num1arr[i][0] # X must be Num1[n][0] X-bar (0<=n<len(num1[]))
                            Y=99999 # Y is the smallest Y-bar between Num1[n][1] and Num2[m][3] (0<=n<len(num1[]) , 0<=m<len(num2[])
                            # Finding Y and YH
                            if(H<Num1arr[i][3]):
                                H=Num1arr[i][3]
                            if(H<Num2arr[j][3]):
                                H=Num1arr[j][3]
                            if(Y>Num1arr[i][1]):
                                Y=Num1arr[i][1]
                            if(Y>Num2arr[j][1]):
                                Y=Num2arr[j][1]
                            im=Image.open('INVimg.bmp')
                            # Save the whole two numbers location (X,Y,W,H)=>(X=Num1 X-bar,Y=The less Y-bar from Num1 and Num2,W=X-bar of Num2 + Width of Num2 - X-bar of Num1,H=Button height)
                            location=X,Y,W,Y+H
                            print location
                            # crop and save two numbers button image
                            im.crop( (X,Y,W,Y+H) ).save('result.bmp')
                j+=1

    # If target elevator floor <9 (one number floor)
    else:
        global location

        # Start check all number of image by arr[]
        for arrnum in range(0,len(arr),+1):
            im=Image.open('INVimg.bmp')# Open thresholded image
            # Crop the image by arr and get the number picture
            im.crop( (arr[arrnum][0],arr[arrnum][1],arr[arrnum][0]+arr[arrnum][2],arr[arrnum][1]+arr[arrnum][3]) ).save('SplitPic.bmp')
            im=cv2.imread("SplitPic.bmp")
            im=thresholding(im)
            im=cv2.resize(im,(25,25)) # Resize the number picture to 25x25 pixel

            # Change the image into 0/1 list
            imarr=[]
            i=0
            while i < 25:# 5x5 Pixel 建立要讀取之數字陣列
                j=0
                while j < 25:
                    if im[i][j][0]==255: # If point is white = 0
                        imarr.append(0)
                    else: # If point is black = 1
                        imarr.append(1)
                    j+=1
                i+=1
        
        
            SmallestD=999999    #與所要讀取之數字相差最少者
            SmallestNumber='X'  #最小者的檔名
            for root in os.listdir(temp_path+'/templates'): #進入temp中
                for f in os.listdir(temp_path+'/templates/'+root):  #進入temp內的資料夾
                    DBimg=cv2.imread(temp_path+'/templates/'+os.path.join(root, f))
                    i=0
                    DBimgarr=[]     #清空DBimgArray
                    while i < 25:    #25x25 Pixel 建立DBimg陣列
                        j=0
                        while j < 25:
                            if DBimg[i][j][0]==255:
                                DBimgarr.append(0) # If point is white = 0
                            else: # If point is black = 1
                                DBimgarr.append(1)
                            j+=1
                        i+=1
        
                    Num=0
                    Different=0
                    while Num<625:
                        if imarr[Num]!=DBimgarr[Num]: # If database image point isn't same as robot image , Different +1
                            Different+=1
                        Num+=1
                    # Save the smallest different points of database image number
                    if(SmallestD>Different):
                        SmallestD=Different
                        SmallestNumber=root
                        if(Different>120): # If the smallest different point>120 then it must not the number we want
                            SmallestNumber="None"
            print SmallestNumber

            # Check if SmallestNumber is the number we want, if yes then return location
            if(SmallestNumber==Num1):
                im=Image.open('INVimg.bmp') # Open image
                location=(arr[arrnum][0],arr[arrnum][1],arr[arrnum][0]+arr[arrnum][2],arr[arrnum][1]+arr[arrnum][3])
                im.crop( (arr[arrnum][0],arr[arrnum][1],arr[arrnum][0]+arr[arrnum][2],arr[arrnum][1]+arr[arrnum][3]) ).save('SplitPic.bmp') # crop and save
                im=cv2.imread("SplitPic.bmp")
                im=thresholding(im)
                cv2.imwrite('25pix.bmp',im)
                break
    # If didn't find number  
    if(location=="0"):
        return "notfound",iii
    # If found number
    return  location,iii
# End CheckNumber #

# The define is used to making elevator button database by photos #
def GetAllNumbers(iii):
    img=cv2.imread("pic/"+str(iii)+".jpg",cv2.IMREAD_GRAYSCALE)

    img=thresholding_inv(img)
    cv2.imwrite('INVimg.bmp',img) #保留存下二值化後的img

    arr=ContoursBound(img) # Find all buttons in the image 
    
    cv2.imwrite('TestSave.bmp',img)

    AllNumsInPicArr=[]
    AllNumsInPicArrCount=0

    # Start check all number of image by arr[]
    for arrnum in range(0,len(arr),+1):
        im=Image.open('INVimg.bmp') # Open thresholded image
        # Crop the image by arr and get the number picture
        im.crop( (arr[arrnum][0],arr[arrnum][1],arr[arrnum][0]+arr[arrnum][2],arr[arrnum][1]+arr[arrnum][3]) ).save('SplitPic.bmp')
        im=cv2.imread("SplitPic.bmp")
        im=thresholding(im)
        im=cv2.resize(im,(25,25))
        cv2.imwrite('25pix.bmp',im) # Resize the number picture as 25x25 pixel
        cv2.imshow('0',im)
        cv2.waitKey(0) # Use to make database

# End GetAllNumbers #


# The define is used to press up / down button #
def CheckUpDownBtn(UPDOWN,iii):
    global location
    img=cv2.imread("Btn.jpg",cv2.IMREAD_GRAYSCALE)

    img=thresholding_inv(img)
    cv2.imwrite('INVimg.bmp',img) # Save image after thresholding
    cv2.imwrite("pic/"+str(iii)+'.bmp',img) # Record every picture
    iii=iii+1

    arr=ContoursBound(img) # Find all buttons in the image 

    TargetNum=-1
    for arrnum in range(0,len(arr),+1):
            im=Image.open('INVimg.bmp') # Open thresholded image
            # Crop the image by arr and get the number picture
            im.crop( (arr[arrnum][0],arr[arrnum][1],arr[arrnum][0]+arr[arrnum][2],arr[arrnum][1]+arr[arrnum][3]) ).save('SplitPic.bmp')
            im=cv2.imread("SplitPic.bmp")
            im=thresholding(im)
            im=cv2.resize(im,(25,25)) # Resize the number picture to 25x25 pixel
            cv2.imwrite('25pix.bmp',im)

            # Change the image into 0/1 list
            imarr=[]
            i=0
            while i < 25:#25x25 Pixel 建立要讀取之數字陣列
                j=0
                while j < 25:
                    if im[i][j][0]==255: # If point is white = 0
                        imarr.append(0)
                    else: # If point is black = 1
                        imarr.append(1)
                    j+=1
                i+=1

            temp_path = os.getcwd()

            for f in os.listdir(temp_path+'/temp_DownBtn/'):  #進入temp內的資料夾
                    DBimg=cv2.imread(temp_path+'/temp_DownBtn/'+os.path.join(f))
                    i=0
                    DBimgarr=[]     #清空DBimgArray
                    while i < 25:    #25x25 Pixel 建立DBimg陣列
                        j=0
                        while j < 25:
                            if DBimg[i][j][0]==255: # If point is white = 0
                                DBimgarr.append(0)
                            else: # If point is black = 1
                                DBimgarr.append(1)
                            j+=1
                        i+=1

                    Num=0
                    Different=0
                    while Num<625:
                        if imarr[Num]!=DBimgarr[Num]: # If database image point isn't same as robot image , Different +1
                            Different+=1
                        Num+=1
                    print Different

                    # If the smallest different point>150 then it must not the down button
                    if(Different>150):
                        SmallestNumber="None"
                    else:
                        TargetNum=arrnum
                        break

    # We've got the button location then have to tell main process if button location is in the right range to press
    if TargetNum!=-1:
        print arr[TargetNum][0]

        # Button is at middie of the image => press button
        if arr[TargetNum][0]>(640-arr[TargetNum][2])/2-10 and arr[TargetNum][0]<(640-arr[TargetNum][2])/2+10:
            return "press button",iii
        # Button is at right of the image => robot goes left
        elif arr[TargetNum][0]<(640-arr[TargetNum][2])/2-10:
            return "car go left",iii
        # Button is at left of the image => robot goes right
        else:
            return "car go right",iii
    # We got nothing with button location , random move
    else:
        rnd = random.randint(0,1)
        if rnd == 0:
            return "car go left",iii
        else:
            return "car go right",iii
# End CheckUpDownBtn #

