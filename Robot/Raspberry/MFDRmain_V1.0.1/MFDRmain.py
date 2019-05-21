# The whole main using camera(0) (The camera on the robot arm)
# variable iii from is a record of robot image (iii.jpg)
from __future__ import division
#for int/int => float
from Tkinter import *
##Built-in
import serial
##    sudo apt-get install python-serial
import tkMessageBox
##Built-in ¡A It comes with Tkinter
from time import sleep
##Built-in
import bluetooth
##sudo apt-get install pi-bluetooth
import numpy as np
##sudo apt-get install python-numpy python-scipy python-matplotlib ipython
import cv2
##sudo apt-get install libopencv-dev python-opencv 
import cv2.cv as cv
##sudo apt-get install libopencv-dev python-opencv
import datetime
##Built-in
import time
##Built-in
import threading
###Built-in
import sys
##Built-in
import os
##Built-in
import math
import urllib2
from HTMLParser import HTMLParser

#bd_addr="00:0D:19:03:19:FA" # Robot2 Bluetooth Address
bd_addr="00:0D:19:0E:14:E6" # Robot1 Bluetooth Address
port=1 # Robot port
servoAngle=90 # Set ServoAngle as 90 degree
StepperHeight=20 # Stander stepper height 20cm
import CheckWallColor as CWC
import NewCheck as NC

sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM) # Get Bluetooth

#
cap = cv2.VideoCapture(0) # Create a VideoCapture object
#
iii=0
temp_path = os.getcwd() # File path

# Check the target button and move to middle of button then ready to press it #
# NumberUWant=>Target Floor / BtnWidth=>Elevator Button Width
def CheckNumInElevator(NumberUWant,BtnWidth):#inside the elevator btnWid is 120
    global iii # Take picture and save by iii.jpg
    global temp_path # File path
    
    ret, frame = cap.read() # Read picture form camera
    ret, frame = cap.read()
    ret, frame = cap.read()
    ret, frame = cap.read()
    ret, frame = cap.read()
    ret, frame = cap.read()

    cv2.imwrite("Btn.jpg",frame)
    cv2.imwrite("pic/"+str(iii)+".jpg", frame) # Save image
    iii=iii+1
    
    if NumberUWant=="UPDOWN": # If press outside of elevator Button (up down btn)
        whatToDo=NC.CheckUpDownBtn(NumberUWant,iii) # Call NewCheck.py
        print (whatToDo)
        iii = whatToDo[1]
        return whatToDo[0]
    else: # If press inside of elevator Button (floor btn)
        location=NC.CheckNumber(NumberUWant,iii) # Call NewCheck.py
        
        Mid=640/2
        
        if location[0]=="notfound": # If did not found btn
            iii=location[1]
            return "not found"
        else: # Try if Target Button at the middle of image 
            BtnMid=(int(location[0][0])+int(location[0][2]))/2
            iii=location[1]
        
        print ("loca 0:")
        print(location[0][0])
        print ("loca 2:")
        print(location[0][2])
        print ("BtnMid:")
        print(BtnMid)
        
        if BtnMid>(Mid+(BtnWidth/2)): # If button is on the left side of camera then robot goes right
            return "car go right"
        elif BtnMid<(Mid-(BtnWidth/2)): # If button is on the right side of camera then robot goes left
            return "car go left"
        else: # If button is on the middle of camera then press button
            return "press button"
# End CheckNumInElevator #

# Bluetooth connecting #
def connect():
    while(True):    
        try: # Bluetooth socket connect between raspberry pi and arduino
            gaugeSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            gaugeSocket.connect((bd_addr, port))
            print (sock)
            break;
        except bluetooth.btcommon.BluetoothError as error: # If connect failed wait 5 seconds and retry
            gaugeSocket.close()
            print ("Could not connect: ", error, "; Retrying in 5s...")
            time.sleep(5)
    return gaugeSocket;

sock = connect()

# End connect #

# Using bluetooth send msg to control robot moving #
class Car():

   def _init_(self):
      pass
   def send(self,data1,data2,data3): # moving data send to arduino
      CarTXD=chr(128)+chr(127)+chr(data1)+chr(data2)+chr(15)+chr(data3)+chr(0)+chr(128)
      sock.send(CarTXD) # Send command to Arduino
   def sendn(self,data1,data2,data3,data4): # special moving data send to arduino (MOVEn)
      CarTXD=chr(128)+chr(127)+chr(data1)+chr(data2)+chr(15)+chr(data3)+chr(data4)+chr(128)
      sock.send(CarTXD) # Send command to Arduino
   # Robot go-ahead and get back
   # Pone => positive&negetive (go or back) / Amount => distance to go (cm)
   def MOVE(self,Pone,Amount): # If moving need avoidance (ex:go straight) then use this define
       if(Amount>255): # Because of bluetooth can only send 8 bit (0~255) so if moving distance over 255 , then must send over 2 times
           car.send(1,Pone,255)
           GetArduino("move")
           car.MOVE(Pone,Amount-255) # Call MOVE() again and amont=amount-255
       else: # If moving distance under 255cm
           car.send(1,Pone,Amount)
           GetArduino("move")
   def MOVEn(self,Pone,Amount,Avoidance): # If moving don't need avoidance (ex:inside of elevator , get/put box) then use this define
       if(Amount>255): # Because of bluetooth can only send 8 bit (0~255) so if moving distance over 255 , then must send over 2 time
           car.sendn(1,Pone,255,Avoidance)
           GetArduino("move")
           car.MOVEn(Pone,Amount-255,Avoidance) # Call MOVE() again and amont=amount-255
       else: # If moving distance under 255cm
           car.sendn(1,Pone,Amount,Avoidance)
           GetArduino("move")

   # Robot turn left or right
   # Pone => positive&negetive (right or left) / Amount => angle to go
   def TURN(self,Pone,Amount):
       car.send(2,Pone,Amount)
       GetArduino("TURN")

   # Robot Servo turnning
   # Amount => angle to go , range = 0 ~ 170 (degree)
   def SERVO(self,Amount): 
       car.send(3,1,Amount)
       global servoAngle
       servoAngle=Amount
       GetArduino("SERVO")

   # Robot stepper up and down
   # Pone => positive&negetive (up or down) / Amount => height to go
   def STEPPER(self,Pone,Amount): # ground to stepper = 20 cm
       car.send(4,Pone,Amount)
       global StepperHeight
       if Pone==1:
           StepperHeight=StepperHeight+Amount
       else:
           StepperHeight=StepperHeight-Amount
       GetArduino("STEPPER")

   # Robot Panning left or right
   # Pone => positive&negetive (right or left) / Amount => distance to go
   def HORIZONTAL(self,Pone,Amount): # 1=right 0=left
        car.send(5,Pone,Amount)
        GetArduino("HORIZONTAL")

   # Using ultra sound to align the wall
   # distance => how far between wall and robot
   def Aligned(self,distance): 
       car.send(6,1,distance)
       GetArduino("aligned")

   # wait the elevator door open and move
   # distance => If door open go a-head distance (cm) 
   def WaitingAndMove(self,distance): 
       car.send(7,1,distance)
       GetArduino("move")
# End Car #       

# Using bluetooth send msg to control robot arm #
class ArmMove():

    def _init_(self):
        pass

    #arm move action:
    """
    if data =
    1 => U_init
    2 => Push button
    3 => Take things
    4 => Put things
    5 => Plat put
    6 => Plat take
    7 => Relex pose
    """
    def move(self,data):
      ArmTXD=chr(255)+chr(255)+chr(1)+chr(data)+chr(255)+chr(255)+chr(255)
      sock.send(ArmTXD)
      time.sleep(5)
# End arm #

# Robot stepper up and down #
# TargetHIGH => Target height which stepper should go
def StepperGo(TargetHIGH): 
    if TargetHIGH<=20:
        TargetHIGH=20
    GoHeight=StepperHeight-TargetHIGH
    if GoHeight>0:
        car.STEPPER(0,GoHeight)
    elif GoHeight==0:
        pass
    else:
        car.STEPPER(1,abs(GoHeight))
# End StepperGo #

# Get msg from Arduino #
# Inp => the state of robot now
def GetArduino(Inp):
    i=0
    while True:
        global sock
        GetText=sock.recv(1024) # Get message from Arduino by bluetooth
        print (GetText)
        if i==0: # Record first time msg into C
            C=GetText
            i=i+1
        else:
            if Inp=="move": # if robot state is moving
                print (C,GetText)
            else:
                print (GetText)
        if(GetText=="O"): # If Arduino return O , robot stop 
            GetText=""
            break
# End GetArduino#

# Use camera look color blocks on wall to go a-head straight #
class GoStraight():
    def __init__(self):
        pass

    # Go straight and count distance
    # amount => distance / ROG => Color block on wall
    def Straight(self,amount,ROG):
        complement = amount%50 # Every 50cm check once color
        cnt = int((amount-complement)/50)
        for i in range(cnt):
            car.MOVE(1,50)
            gs.GetWallPoint(ROG)
        if(complement!=0):
            car.MOVEn(1,complement,1)
            gs.GetWallPoint(ROG)
            
    # Using TestWallColor.py to check if robot is straight
    #ROG => Color block on wall
    def GetWallPoint(self, ROG):
        global iii
        countpoint=(CWC.WallColor(ROG,iii)) # TWC return color point of robot image
        leftpoint=countpoint[0]
        middiepoint=countpoint[1]
        rightpoint=countpoint[2]
        iii=countpoint[3]

        print (leftpoint,middiepoint,rightpoint)

        if leftpoint > rightpoint: # Turn left
            car.TURN(0,5)
        elif rightpoint > leftpoint: # Turn right
            car.TURN(1,5)
# End of GoStraight #

# Contain get and put box , every elevator button press #
class BoxAndBtn():
    def __init__(self):
        pass

    # let robot come to the middle of box and get it by arm
    # BoxHeight => how tall stepper should go to and then get the box
    def getBox(self,BoxHeight):
        def CheckBox(): # Check if box at the middle of image
            global iii
            while True:
                time.sleep(0.1)
                ret, frame = cap.read() # Read picture form camera
                ret, frame = cap.read()
                ret, frame = cap.read()
                ret, frame = cap.read()
                ret, frame = cap.read()
                ret, frame = cap.read()

                cv2.imwrite("pic/"+str(iii)+".jpg",frame) # Save box image
                iii=iii+1
                
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # become gray
                equalizeHist = cv2.equalizeHist(gray) # equalize image
                cv2.imwrite("pic/"+str(iii)+".jpg",equalizeHist) # Save equalizeHist image
                iii=iii+1
                
                ret, thresh = cv2.threshold(equalizeHist,240,255,0) # threshold image
                cv2.imwrite("pic/"+str(iii)+".jpg",thresh) # Save processed image
                iii=iii+1
                
                contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # find contours in whole image
                cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key=lambda x:x[1])
                        
                arr = []
                for index, (c, _) in enumerate(cnts): # bound everything in image
                    (x, y, w, h) = cv2.boundingRect(c) # bound by rectangle
                    #print (x,y,w,h)
                    try:
                        # save to arr if rectangle 20<width<480 40<height<360 (pixel)
                        if w > 20 and h > 40 and w < 480 and h < 360: 
                            if (h-w)<200 or (w-h)<200:
                                arr.append((x, y, w, h))
                    except IndexError:
                        pass
                print (arr)

                if arr[0][0]<280-(arr[0][2]/2): # if box too right
                    "GO LEFT"
                    car.HORIZONTAL(0,3)
                elif arr[0][0]>300-(arr[0][2]/2): # if box too left
                    "GO RIGHT"
                    car.HORIZONTAL(1,2)
                else: # box at middle , break and catch
                    "CATCH"
                    break
                
        # Catching the box
        car.SERVO(135)
        StepperGo(BoxHeight)
        CheckBox()
        car.Aligned(12)
        CheckBox()
        arm.move(3)
        car.MOVEn(0,36,1)
        StepperGo(98)
        car.SERVO(0)
        arm.move(5)
        car.SERVO(135)
        StepperGo(20)
        car.SERVO(0)
    # End getBox #

    # let robot come to the middle of counter and put box on it by arm
    # CabinetHeight => how tall stepper should go to and then put the box on counter
    def putBox(self,CabinetHeight):
        car.SERVO(135)
        car.Aligned(25)
        StepperGo(93)
        car.SERVO(0)
        arm.move(6)
        car.SERVO(135)
        car.Aligned(15)
        StepperGo(CabinetHeight)      
        arm.move(4)
        car.MOVEn(0,36,1)
        StepperGo(20)
        car.SERVO(0)
    # End putBox #

    # Check if elevator panel is in the middle of camera #
    # Then use CheckWallColor.py (CWC) to check and press elevator up and down button #
    # BtnHeight => how tall stepper should go to and then press button
    def elevator(self,BtnHeight):
        global iii
        car.SERVO(135)
        amount=130
        while amount != 0: # amount => distance to go forword (cm)
            if(amount>=15):
                time.sleep(2)
                NowaPlace=CWC.UpDownBtnPress(iii) # TWC return where elevator panel in camera
                iii=NowaPlace[1]
                if NowaPlace[0]=="MID": # If middle then keep moving
                    amount=amount-15
                    car.MOVEn(1,15,1)
                elif NowaPlace[0]=="LEFT": # If too right then horizon to left
                    car.HORIZONTAL(0,2)
                elif NowaPlace[0]=="RIGHT": # If too left then horizon to right
                    car.HORIZONTAL(1,3)
                elif NowaPlace[0]=="PASS": # If pass then maybe too close to the wall , just keep going and lift the stepper to check button
                    car.MOVEn(1,amount,1)
                    amount=0
            else: # keep going amount cm
                car.MOVEn(1,amount,1)
                amount=0

        car.Aligned(20)
        StepperGo(109) #21

        # After lift stepper , recognition up and down button
        while True:  #40*27
            car.Aligned(20) #check if Ultrasound is about 20 cm from wall

            time.sleep(1)

            global LastTimeFunc
            global TargetFloor
            # Use NewCheck.py to check the up down button , return if button too left or too right in camera image
            Ans=CheckNumInElevator("UPDOWN",60)
            print (Ans)
            if Ans=="not found":
                Ans=LastTimeFunc
            if Ans=="car go left": # If too right then horizon to left
                car.HORIZONTAL(0,3)
            elif Ans=="car go right": # If too left then horizon to right
                car.HORIZONTAL(1,3)
            elif Ans=="press button": # If middle then press the button , lift the stepper to BtnHeight
                StepperGo(BtnHeight) # DOWN=>car.STEPPER(0,5)
                car.Aligned(15) # check if Ultrasound is about 15 cm from wall
                arm.move(2) # button press
                arm.move(7) # arm relax
                break
            LastTimeFunc=Ans # record if last time too left or right
        car.MOVEn(0,70,1)
        car.SERVO(0)
    # End elevator #

    # Use CheckWallColor.py (CWC) to check and press elevator floor button #
    # Targetfloor => which floor robot should press 
    def floor(self,TargetFloor):
        car.WaitingAndMove(170) # Wait elevator door open and go forword
        car.Aligned(40) # check if Ultrasound is about 40 cm from wall
        car.TURN(0,90)
        car.SERVO(135)
        car.MOVEn(1,35,87)
        car.Aligned(20) # check if Ultrasound is about 20 cm from wall
        StepperGo(93)

        LastTimeFunc="0" # record last time status

        while True:
            car.Aligned(20) # check if Ultrasound is about 20 cm from wall

            time.sleep(1)
            
            ret, frame = cap.read() # Read picture form camera
            ret, frame = cap.read()
            ret, frame = cap.read()
            ret, frame = cap.read()
            ret, frame = cap.read()
            ret, frame = cap.read()
            ret, frame = cap.read()

            # Use NewCheck.py to check the target floor button , return if button too left or too right in camera image
            Ans=CheckNumInElevator(TargetFloor,60) 
            print (Ans)
            if Ans=="not found":
                Ans=LastTimeFunc
            if Ans=="car go left": # If too right then horizon to left
                car.HORIZONTAL(0,3)
            elif Ans=="car go right": # If too left then horizon to right
                car.HORIZONTAL(1,3)
            elif Ans=="press button": # If press button then press button
                car.STEPPER(0,8)
                if TargetFloor<6:
                    car.STEPPER(0,6)
                car.Aligned(15) # check if Ultrasound is about 15 cm from wall
                arm.move(2) # press button
                arm.move(7) # arm relax
                break
            LastTimeFunc=Ans

        # turn and ready to wait the door open
        car.MOVEn(0,30,87) 
        car.TURN(0,90) #0
        StepperGo(100)
        car.SERVO(0)

        # If door is open , use CheckWallColor.py (CWC) to check if the color block is same as target floor
        while True:
            # go forword if the color block color is same as database target floor color
            eleFloor=CWC.CheckFloorColor() 
            if TargetFloor==eleFloor:
                car.MOVE(1,320) # leave elevator               
                car.SERVO(135)
                StepperGo(20)
                car.SERVO(0)
                break
        # End floor #
# End BoxAndBtn #

car=Car() # Use class Car() as car
arm=ArmMove() # Use class ArmMove() as arm
gs=GoStraight() # Use class GoStraight() as gs
BnB=BoxAndBtn() # Use class BoxAndBtn() as bnb

NAME = "RB1" # Robot Name
ROBOT = "" # Get which robot user calling 
STATUS = "" # If user command has been read
COMMAND = "" # Get command by server
cmd = []

# Analysis html file data #
class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.ROBOT = ""
        self.STATUS = ""
        self.COMMAND = ""

    # Read data from html
    def handle_data(self, data):
        if data.strip(): # split by space
            if self.lasttag == 'h1': # read h1 tag
                self.ROBOT = data
            if self.lasttag == 'h2': # read h2 tag
                self.STATUS = data
            if self.lasttag == 'h3': # read h3 tag
                self.COMMAND = data
# End MyHTMLParser #

# Catch target html url data #
def Extract(url):            

    global ROBOT,STATUS,COMMAND
    
    try: # try to open html
        html = urllib2.urlopen(url).read()
    except urllib2.HTTPError as e: # open failed
        print(e, 'while fetching', url)
        return
   
    parser = MyHTMLParser() # Use class MyHTMLParser() as parser
    parser.feed(html) # give parser html file

    ROBOT = parser.ROBOT
    STATUS = parser.STATUS
    COMMAND = parser.COMMAND
# End Extract #

# Keep running as a loop and wait before get any command
while(True):

    Extract("http://isla.shu.edu.tw:8066/gt2017/MFDR/php/commandfile.txt")

    print ("ROBOT   : ", ROBOT)
    print ("STATUS  : ", STATUS)
    print ("COMMAND : ", COMMAND)
    print ("--------------------------------------------------")

    # Check the command of robot name
    if(NAME != ROBOT):
        print (ROBOT, "It's not ME!")
    else:
        print (ROBOT, "It's ME!")
        if(STATUS != "1"):
            print ("STATUS is OFF")
        else:
            print ("STATUS is ON")
            if(COMMAND != ""):
                print ("Get Command!!")
                break
            else:
                print ("Command it's empty!")
            
    print ("Waitting 5 sec......")
    time.sleep(5)

# Start process
for text in COMMAND.split('_'):
    cmd.append(text)

print (cmd)


print ("--------------------------------------------------")


# Analysis by h3 data from COMMAND
for i in range(len(cmd)):
    KEY = cmd[i][0]
    
    if KEY == 'M': # M = Move (0=>Go straight 1=>Go back)
        if cmd[i][1] == "-":
            print ("car.MOVE(0,", cmd[i][2:len(cmd[i])],")")
            car.MOVE(0,int(cmd[i][2:len(cmd[i])]))
        else:
            print ("car.MOVE(1,", cmd[i][1:len(cmd[i])],")")
            car.MOVE(1,int(cmd[i][1:len(cmd[i])]))
        
    elif KEY == 'W': # W = Go Straight and check wall color
        tmp = (len(cmd[i])-1)
        print ("gs.Straight(", cmd[i][1:tmp],",",cmd[i][tmp],")")
        gs.Straight(int(cmd[i][1:tmp]),cmd[i][tmp])
        
    elif KEY == 'T': # T = Turn (0=>Turn left 1=>Turn right)
        if cmd[i][1] == "-":
            print ("car.TURN(0,", cmd[i][2:len(cmd[i])],")")
            car.TURN(0,int(cmd[i][2:len(cmd[i])]))
        else:
            print ("car.TURN(1,", cmd[i][1:len(cmd[i])],")")
            car.TURN(1,int(cmd[i][1:len(cmd[i])]))
            
    elif KEY == 'H': # H = Horizon (0=>Go left 1=>Go right)
        if cmd[i][1] == "-":
            print ("car.HORIZONTAL(0,", cmd[i][2:len(cmd[i])],")")
            car.HORIZONTAL(0,int(cmd[i][2:len(cmd[i])]))
        else:
            print ("car.HORIZONTAL(1,", cmd[i][1:len(cmd[i])],")")
            car.HORIZONTAL(1,int(cmd[i][1:len(cmd[i])]))
        
    elif KEY == 'G': # G = Check the box location and get it
        print ("getBox(", cmd[i][1:len(cmd[i])],")")
        BnB.getBox(int(cmd[i][1:len(cmd[i])]))
        
    elif KEY == 'P': # P = Put the box and leave
        print ("putBox(", cmd[i][1:len(cmd[i])],")")
        BnB.putBox(int(cmd[i][1:len(cmd[i])]))
        
    elif KEY == 'E': # E = Robot check elevator up / down button and press it  
        print ("elevator(", cmd[i][1:len(cmd[i])],")")
        BnB.elevator(int(cmd[i][1:len(cmd[i])]))
        
    elif KEY == 'F': # F = After get in elevator , check the floor button which robot should go
        print ("floor(", cmd[i][1:len(cmd[i])],")")
        BnB.floor(int(cmd[i][1:len(cmd[i])]))
    else:
        print ("else cmd")
       
