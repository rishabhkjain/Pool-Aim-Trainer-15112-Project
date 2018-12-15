import cv2
import numpy as np
import random
#animation framework is from 112 notes
#some masking stuff and opencv stuff is derived from stack overflow and opencv docs
#I received help from jcao2 in regards to how to use the entry widget


import math
from tkinter import *
def runSetup():
    def draw(canvas, width, height):
        result = StringVar()
        result2 = StringVar()
        result3 = StringVar()
        def moveOn():
            path = result.get()
            # ball = int(result2.get())
            # pocket = int(result3.get())
            runSim(path)
        def aimTrainer():
            runTrainer()
        def playGame():
            runGame()
            
    
        e1 = Entry(canvas, textvariable = result, width = 50, font = "Helvetica 20")
        # e2 = Entry(canvas, textvariable = result2, width = 50, font = "Helvetica 20")
        # e3 = Entry(canvas, textvariable = result3, width = 50, font = "Helvetica 20")
        b1 = Button(canvas, text = "Submit", command = moveOn, bg = "white", font = "Helvetica 20")
        b2 = Button(canvas, text = "Aim Trainer", command = aimTrainer, bg = "white", font = "Helvetica 20")
        b3 = Button(canvas, text = "Play a Game", command = playGame, bg = "white", font = "Helvetica 20")
        canvas.create_rectangle(0,0, width, height, fill = "teal")
        canvas.create_text(width/2, height/2 - 100, text = "Welcome to Pooltastic", font = "Helvetica 28 bold", fill = "white")
        canvas.create_text(width/2 , height/2 + 50, text = "What is your file name?", font = "Helvetica 20", fill = "white")
        # canvas.create_text(width/2, height/2 + 100, text = "What ball are you aiming for?", font = "Helvetica 20", fill = "white")
        canvas.create_window( width/2 - 50, height/2 + 100, window=e1)
        # canvas.create_text(width/2, height/2 + 50, text = "What ball are you aiming for?", font = "Helvetica 20", fill = "white")
        # canvas.create_window( width/2, height/2 + 100, window=e2)
        # canvas.create_text(width/2, height/2 + 150, text = "Into what pocket?", font = "Helvetica 20", fill = "white")
        # canvas.create_window( width/2, height/2 + 200, window=e3)
        canvas.create_window( width/2 + 390, height/2 + 100, window=b1)
        canvas.create_window( width/2, height/2 + 300, window=b2)
        canvas.create_window( width/2, height/2 + 200, window=b3)

    
        
    
    def runDrawing(width=300, height=300):
        root = Tk()
        root.resizable(width=False, height=False) # prevents resizing window
        canvas = Canvas(root, width=width, height=height)
        canvas.configure(bd=0, highlightthickness=0)
        canvas.pack()
        draw(canvas, width, height)
        root.mainloop()
        print("bye!")
    
    runDrawing(1430, 850)



    
def runSim(path):
    
    #some of this code (the masking) is from stack overflow and opencv docs but I have heavily modified it to work with my requirements
    image = cv2.imread(path, 0)
    uimage = cv2.imread(path)
    cimage = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    ret, thresh = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, param2 = 20, minRadius = 15, maxRadius = 30)
    colorDict = dict()
    def getColor(i):
        height,width = image.shape
        mask = np.zeros((height,width), np.uint8)
        (x,y,r) = circles[0][i]
        cv2.circle(mask,(x,y),r,(255,255,255),thickness=-1)
        masked_data = cv2.bitwise_and(uimage, uimage, mask=mask)
        _,thresh = cv2.threshold(mask,1,255,cv2.THRESH_BINARY)
        contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        x,y,w,h = cv2.boundingRect(contours[0])
        crop = masked_data[y:y+h,x:x+w]
        average = crop.mean(axis=0).mean(axis=0)
        return average
    for i in range (len(circles[0,:])):
        colorDict[i] = getColor(i)
        
    #see attached excel for source data
    colorLst = [0]*16
    colorLst[0] = (150,148,137)
    colorLst[1] = (52, 122, 146)
    colorLst[2] = (117, 65, 29)
    colorLst[3] = (71, 45, 118)
    colorLst[4] = (101, 63, 67)
    colorLst[5] = (50, 77,157)
    colorLst[6] = (50, 136, 98)
    colorLst[7] = (123, 138, 68)
    colorLst[8] = (37, 26, 16)
    colorLst[9] = (96, 123, 119)
    colorLst[10] = (105, 97, 74)
    colorLst[11] = (108,84,99)
    colorLst[12] = (121,90,81)
    colorLst[13] = (93, 103, 145)
    colorLst[14] = (115, 142, 124)
    colorLst[15] = (129.5, 142, 97)
    
    def findNumber(i):
        color = colorDict[i] 
        a = color[0]
        b = color[1]
        c = color[2]
        minDiff = 9999999
        minVal = None
        for i in range (len(colorLst)):
            diffA = colorLst[i][0] - a
            diffB = colorLst[i][1] - b
            diffC = colorLst[i][2] - c
            totalDiff = diffA**2 + diffB**2 + diffC**2
            totalDiff = math.sqrt(totalDiff)
            if totalDiff < minDiff:
                minDiff = totalDiff
                minVal = i
        return (minVal)
    
    def findCoord(num):
    
        for i in range (len(circles[0,:])):
            

            if findNumber(i) == num:
                return circles[0][i]
        
        
    # Basic Animation Framework
    
    
    ####################################
    # customize these functions
    ####################################
    
    def init(data):
        #these variables will be sourced from the gui in future iterations
        # data.circles = circles[0]
        # data.path = "multi4.gif"
       
        formatCircles(data)
        # for i in range(1, len(data.circles)):
        #     if data.circles[i][0] > 0:
        #         data.ball = i
        data.ball = 7
        data.pocket = 0
        data.width = 1430
        data.height = 850
        data.r = 20
        data.pocketr = 60
        data.boardColor = "navy blue"
    
        data.pocketLst = [(100, 100), (700, 100), (1350, 100),(100, 740), (700, 740), (1350, 740)]
        data.cueX = data.circles[0][0]
        data.cueY = data.circles[0][1]
        data.ballX = data.circles[data.ball][0]
        data.ballY = data.circles[data.ball][1]
      
        data.cueYM = -1 * data.circles[0][1]
        data.ballYM = -1*data.ballY
        data.pocketX = data.pocketLst[data.pocket][0]
        data.pocketY = data.pocketLst[data.pocket][1]
        data.pocketYM = -1*data.pocketLst[data.pocket][1]
        data.colorDict = {0: ('white', 0), 1: ('yellow', 0), 2: ('blue', 0), 3: ('red', 0), 4: ('purple', 0), 5: ('orange', 0), 6: ('green', 0), 7: ('teal', 0), 8: ('black', 0), 9: ('yellow', 1), 10: ('blue', 1), 11: ('red', 1), 12: ('purple', 1), 13: ('orange', 1), 14: ('green', 1), 15: ('teal', 1)}
        
        data.count = 0
    
        data.friction = 0.05
        data.power = 15
        data.state = 4
        data.pocketDiff = [(20, -20), (0, -10), (-20, -20), (20, 20), (0, 10), (-20, 20)]
        data.help = False
        
    def formatCircles(data):
        newLst = []
        finLst = [newLst]*16
        for i in range (16):
            result = findCoord(i)
            
            try:
                x = result[0] - 20
                y = result[1]
            except:
                x, y = -100, -100
                
            finLst[i] = [x, y, i, 0, 0]
        data.circles = finLst
    def getLine(x1, y1, x2, y2):
        if x2 - x1 == 0: return (0, 0)
        slope = (y2-y1)/(x2-x1)
        intercept1 = y1 - (slope*x1)
        intercept2 = y2 - (slope*x2)
        if math.isclose(intercept1, intercept2):
            return (slope, intercept1)
            
   
    def findConflict(x1, x2, slope, intercept, data, constant):
        diameter = 40
        slope *= constant
        for i in range (len(data.circles)):
            slope2 = -1/slope
            ballX = data.circles[i][0]
            ballY = -1* data.circles[i][1]
            if x1  < x2:
                if ballX <= x1:
                    continue
                if ballX >= x2:
                    continue
            elif x1 > x2:
                if ballX <= x2:
                    continue
                if ballX >= x1:
                    continue
            intercept2 = ballY - ballX*slope2
            iX = (intercept - intercept2)/( slope2 - slope)
            iY1 = slope2*iX + intercept2
            iY2 = slope*iX + intercept
            sD = getDistance(ballX, ballY, iX, iY2)
    
                
                
            if sD < diameter:
                return True
                
        return False
    
    def findContact(ballX, ballY, slope, intercept, data):
        t = abs(slope)
        radius = 40
        param = math.sqrt(t**2 + 1)
        s = radius/param
        if data.ballX < data.pocketX:
            x = ballX - s
        else:
            x = ballX + s
        if data.cueY < data.pocketY:
            y = ballY + abs(slope*s)
        else:
            y = ballY - abs(slope*s)
        
        return (x,y)
    
    def findCue(data):
        (xD, yD) = data.pocketDiff[data.pocket]
        (data.slope1,data.intercept1) = getLine(data.ballX, data.ballYM, data.pocketX + xD, data.pocketYM + yD)
        (data.cX, data.cYM) = findContact(data.ballX,data.ballYM, data.slope1, data.intercept1, data)
        (data.slope2, data.intercept2) = getLine(data.cX, data.cYM, data.cueX, data.cueYM)
        data.slope2 = -1*data.slope2
        if data.cX > data.cueX:
            data.x2 =  data.cueX - 50
            data.x1 = data.cueX - 300
            data.y2 = (data.cueX - 50)*(data.slope2)  - data.intercept2
            data.y1 = (data.cueX - 300)*(data.slope2) - data.intercept2
        else:
            data.x2 =  data.cueX + 50
            data.x1 = data.cueX + 300
            data.y2 = (data.cueX + 50)*(data.slope2)  - data.intercept2
            data.y1 = (data.cueX + 300)*(data.slope2) - data.intercept2
            
        
    def getDistance(x1, y1, x2, y2):
        d = abs(x1 - x2)**2 + abs(y1 - y2)**2
        return math.sqrt(d)
    
    def checkCollision(i, j, data):
        x1 = data.circles[i][0]
        y1 = data.circles[i][1]
        x2 = data.circles[j][0]
        y2 = data.circles[j][1]
        d = getDistance(x1, y1, x2, y2)
        if x1 < 0 or x2 < 0:
            return None
        if d <= 2 * data.r:
            diff = 2*(data.r) - d 
        
           
                
            if data.circles[i][3] == 0 and data.circles[i][4] == 0:
                if data.circles[j][3] == 0 and data.circles[j][4] == 0:
                    
                    return None
                if diff > 0.2 and diff < 10:

                    oneLen = math.sqrt(data.circles[j][3]**2 + data.circles[j][4]**2 )
                    if oneLen != 0:
                        t = diff/oneLen
                        data.circles[j][0] -= data.circles[j][3] * t
                        data.circles[j][1] -= data.circles[j][4] * t
                        x1 = data.circles[i][0]
                        y1 = data.circles[i][1]
                        x2 = data.circles[j][0]
                        y2 = data.circles[j][1]
                       
                energyLoss = 0.7
                speed = energyLoss*math.sqrt(data.circles[j][3]**2 + data.circles[j][4]**2 )
                slope, intercept1 = getLine(x1, -1*y1, x2, -1*y2)
                param = math.sqrt(slope**2 + 1)
                x1 = data.circles[i][0]
                y1 = data.circles[i][1]
                x2 = data.circles[j][0]
                y2 = data.circles[j][1]
                if slope == 0: 
                    s = 1
                else:
                    s = abs(speed/param)
                if x1 < x2:
                    
                    data.circles[i][3] = -1*s
                    data.circles[j][3] = -0.5*abs(s * slope)
                else:
                    data.circles[i][3] = s
                    data.circles[j][3] = 0.5*abs(s * slope)
    
                if y1 < y2:
                    data.circles[i][4] = -1*abs(s * slope)
                    

                else:
                    data.circles[i][4] = abs(s * slope)
                if data.circles[j][4] > 0:
                    data.circles[j][4] = 0.5*s
                else:
                    if abs(data.circles[j][4]) > 5:
                        
                        data.circles[j][4] = -0.5*s
                    else:
                        data.circles[j][4] = 0.5*s
                if abs(data.circles[i][3]/data.circles[j][3]) < 1.4:
                    data.circles[j][3] *= -1
                if abs(data.circles[i][4]/data.circles[j][4]) < 1.4:
                    data.circles[j][4] *= -1
          
          
    
            
            elif data.circles[j][3] == 0 and data.circles[j][4] == 0:
                if data.circles[i][3] == 0 and data.circles[i][4] == 0:
                   
                    return None
                if diff > 0.2 and diff < 10:

                    oneLen = math.sqrt(data.circles[i][3]**2 + data.circles[i][4]**2 )
                    if oneLen != 0:
                        t = diff/oneLen
                        data.circles[i][0] -= data.circles[i][3] * t
                        data.circles[i][1] -= data.circles[i][4] * t
                        x1 = data.circles[j][0]
                        y1 = data.circles[j][1]
                        x2 = data.circles[i][0]
                        y2 = data.circles[i][1]
                       
                        

                     
                energyLoss = 0.7
                speed = energyLoss*math.sqrt(data.circles[i][3]**2 + data.circles[i][4]**2 )
                slope, intercept1 = getLine(x1, -1*y1, x2, -1*y2)

                param = math.sqrt(slope**2 + 1)
                x1 = data.circles[j][0]
                y1 = data.circles[j][1]
                x2 = data.circles[i][0]
                y2 = data.circles[i][1]

                if slope == 0: 
                    s = 1
                else:
                    s = abs(speed/param)
                if x1 < x2:
                    data.circles[j][3] = -1*s
                    data.circles[i][3] = -0.5*abs(s * slope)
                else:
                    data.circles[j][3] = s
                    data.circles[i][3] = 0.5*abs(s * slope)
    
                if y1 < y2:
                    data.circles[j][4] = -1*abs(s * slope)
                else:
                    data.circles[j][4] = abs(s * slope)
                if data.circles[i][4] > 0:
                    data.circles[i][4] = 0.5*s
                else:
                    if abs(data.circles[i][4]) > 5:
                        
                        data.circles[i][4] = -0.5*s
                    else:
                        data.circles[i][4] = 0.5*s
            else:
                data.circles[i][3], data.circles[j][3] = data.circles[j][3], data.circles[i][3]
                data.circles[i][4], data.circles[j][4] = data.circles[j][4], data.circles[i][4]
            if abs(data.circles[i][3]/data.circles[j][3]) < 1.4:
                    data.circles[i][3] *= -1
            if abs(data.circles[i][4]/data.circles[j][4]) < 1.4:
                    data.circles[i][4] *= -1
                
        
    def mousePressed(event, data):
        # use event.x and event.y
        pass
    
    def keyPressed(event, data):
        if data.state == 4:
            if event.keysym == "s":
                findCue(data)
                param = math.sqrt((abs(data.slope2))**2 + 1)
                scale = data.power/param
                if data.cueX > data.cX:
                    xSpeed = -1 * scale 
                else:
                    xSpeed = scale
                if data.cueYM > data.cYM:
                    ySpeed = abs(scale * data.slope2)
                else:
                    ySpeed = abs(scale * data.slope2) * -1
                data.circles[0][3] = xSpeed
                data.circles[0][4] = ySpeed
            if event.keysym == "r":
                init(data)
            if event.keysym == "Up":
                data.power += 1
            if event.keysym == "Down":
                data.power -= 1
            if event.keysym == "0":
                data.pocket = 0
                data.pocketX = data.pocketLst[data.pocket][0]
                data.pocketY = data.pocketLst[data.pocket][1]
                data.pocketYM = -1*data.pocketLst[data.pocket][1]
            if event.keysym == "1":
                data.pocket = 1
                data.pocketX = data.pocketLst[data.pocket][0]
                data.pocketY = data.pocketLst[data.pocket][1]
                data.pocketYM = -1*data.pocketLst[data.pocket][1]
            if event.keysym == "2":
                data.pocket = 2
                data.pocketX = data.pocketLst[data.pocket][0]
                data.pocketY = data.pocketLst[data.pocket][1]
                data.pocketYM = -1*data.pocketLst[data.pocket][1]
            if event.keysym == "3":
                data.pocket = 3
                data.pocketX = data.pocketLst[data.pocket][0]
                data.pocketY = data.pocketLst[data.pocket][1]
                data.pocketYM = -1*data.pocketLst[data.pocket][1]
            if event.keysym == "4":
                data.pocket = 4
                data.pocketX = data.pocketLst[data.pocket][0]
                data.pocketY = data.pocketLst[data.pocket][1]
                data.pocketYM = -1*data.pocketLst[data.pocket][1]
            if event.keysym == "5":
                data.pocket = 5
                data.pocketX = data.pocketLst[data.pocket][0]
                data.pocketY = data.pocketLst[data.pocket][1]
                data.pocketYM = -1*data.pocketLst[data.pocket][1]
            if event.keysym == "Left":
                nextBall(data)
            if event.keysym == "p":
                print(data.circles)
            if event.keysym == "q":
                print(data.circles[0][4], "cue speed")
            if event.keysym == "h":
                data.help = not data.help
    def nextBall(data):
        curBall = data.ball
        newLst = list(range(curBall + 1, 16))
        newLst.extend(list(range(1, curBall + 1)))
        for i in (newLst):
            if data.circles[i][0] < 0:
                continue
            data.newBall = i
            data.ball = data.newBall
            data.ballX = data.circles[data.ball][0]
            data.ballY = data.circles[data.ball][1]
            data.ballYM = -1*data.ballY
            findCue(data)
            if findConflict(data.cX, data.circles[0][0], data.slope2, data.intercept2, data, -1):
                continue
            if findConflict(data.ballX, data.pocketLst[data.pocket][0],  data.slope1, data.intercept1, data, 1):
                continue
            if data.pocketX > data.cueX:
                if data.ballX > data.pocketX or data.ballX < data.cueX:
                    if abs(data.slope2) < 10:
                        continue
                        
            else:
                if data.ballX < data.pocketX or data.ballX > data.cueX:
                    if abs(data.slope2) <10:
                        continue
                        
            if data.pocketY < data.cueY:
                if data.ballY < data.pocketY or data.ballY > data.cueY:
                    if abs(data.slope2) > 1:
                        continue
            else:
                if data.ballY > data.pocketY or data.ballY < data.cueY:
                    if abs(data.slope2) > 1:
                        continue
            break 
        if data.ball == curBall:
            data.ball += 1
            if data.ball == 16:
                data.ball = 0
            data.pocket += 1
            if data.pocket == 6: data.pocket = 0
            data.ballX = data.circles[data.ball][0]
            data.ballY = data.circles[data.ball][1]
            data.ballYM = -1*data.ballY
            data.pocketX = data.pocketLst[data.pocket][0]
            data.pocketY = data.pocketLst[data.pocket][1]
            data.pocketYM = -1*data.pocketLst[data.pocket][1]
            return nextBall(data)
       
            
                
    def nextBall1(data):
        if 1 == 1:
            newLst = []
            data.newBall = data.ball + 1
            # print(data.newBall)
            if data.newBall == 16:
                data.newBall = 1
            for i in range (len(data.circles)):
                if data.circles[i][0] > 0:
                    
                    newLst.append(i)
            while data.newBall not in newLst:
                data.newBall += 1
                if data.newBall == 16: data.newBall = 1
            data.ball = data.newBall
            data.ballX = data.circles[data.ball][0]
            data.ballY = data.circles[data.ball][1]
            data.ballYM = -1*data.ballY
            findCue(data)
            if findConflict(data.cX, data.circles[0][0], data.slope2, data.intercept2, data, -1):
                return nextBall(data)
            if findConflict(data.ballX, data.pocketLst[data.pocket][0],  data.slope1, data.intercept1, data, 1):
                return nextBall(data)
            if data.pocketX > data.cueX:
                if data.ballX > data.pocketX or data.ballX < data.cueX:
                    if abs(data.slope2) < 10:
                        return nextBall(data)
                        
            else:
                if data.ballX < data.pocketX or data.ballX > data.cueX:
                    if abs(data.slope2) <10:
                        return nextBall(data)
                        
            if data.pocketY < data.cueY:
                if data.ballY < data.pocketY or data.ballY > data.cueY:
                    if abs(data.slope2) > 1:
                        return nextBall(data)
            else:
                if data.ballY > data.pocketY or data.ballY < data.cueY:
                    if abs(data.slope2) > 1:
                        return nextBall(data)
       
            
                
    def timer4(data):
        data.count += 1
        
        for i in range (len(data.circles)):
            cX = data.circles[i][3]
            cY = data.circles[i][4]
            data.circles[i][0] += data.circles[i][3]
            data.circles[i][1] += data.circles[i][4]
            param = math.sqrt(data.circles[i][3]**2 + data.circles[i][4] ** 2)
            if param != 0:
                scale = data.friction/param
            else: scale = 1
            xFric = abs(data.circles[i][3] * scale)
            yFric = abs(data.circles[i][4] * scale)
            
            
            if abs(data.circles[i][3]) <= xFric or abs(data.circles[i][4]) <= yFric:
                data.circles[i][3] = 0
                data.circles[i][4] = 0
            if data.circles[i][3] > 0:
                data.circles[i][3] -= xFric
            elif data.circles[i][3] < 0:
                data.circles[i][3] += xFric
            if data.circles[i][4] > 0:
                data.circles[i][4] -= yFric
            elif data.circles[i][4] < 0:
                data.circles[i][4] += yFric
        for i in range (len(data.circles)):
            for j in range (i, len(data.circles)):
                if i == j:
                    continue
                checkCollision(i,j, data)
        for i in range (len(data.circles)):
            for j in range (len(data.pocketLst)):
                x1 = data.circles[i][0]
                y1 = data.circles[i][1]
                x2 = data.pocketLst[j][0]
                y2 = data.pocketLst[j][1]
                if j == 1 or j == 4:
                    if getDistance(x1, y1, x2, y2) < data.pocketr/2 + 10:
                        pass
                        data.circles[i][0] = -100
                        data.circles[i][1] = -100
                else:   
                    if getDistance(x1, y1, x2, y2) < data.pocketr + 10:
                        pass
                        data.circles[i][0] = -100
                        data.circles[i][1] = -100
    
            if data.circles[i][0] < data.r + 100 or data.circles[i][0] > data.width - 100 - data.r:
                data.circles[i][3] *= -0.7
            if data.circles[i][1] < data.r + 100 or data.circles[i][1] > data.height - 100 - 2 * data.r:
                data.circles[i][4] *= -0.7
        data.cueX = data.circles[0][0]
        data.cueY = data.circles[0][1]
        data.cueYM = -1*data.circles[0][1]
        data.ballX = data.circles[data.ball][0]
        data.ballY = data.circles[data.ball][1]
    def timerFired(data):
        if data.state == 4:
            timer4(data)
        for i in range (len(data.circles)):
            if data.circles[i][4] != 0:
                pass
        
                
                
    def drawState4(canvas,data):   
        findCue(data)
        # canvas.create_oval(data.cX - 4, -1*data.cYM - 5, data.cX + 5, -1*data.cYM + 5, fill = "black")
        canvas.create_rectangle(0,0,data.width, data.height, fill = data.boardColor)
        canvas.create_rectangle(100, 100, 1345, 740, width = 5)
        
        if data.circles[0][3] == 0:
            canvas.create_line(data.x1, data.y1, data.x2, data.y2, width = 10, fill = "black")
            canvas.create_oval(data.cX - 5, -1*data.cYM - 5, data.cX + 5, -1*data.cYM + 5, fill = "black")
            if data.ballX > 0:
                canvas.create_line( data.pocketX + data.pocketDiff[data.pocket][0], data.pocketY - data.pocketDiff[data.pocket][1], data.ballX, data.ballY, fill = "white")
        for i in range (len(data.pocketLst)):
            x = data.pocketLst[i][0]
            y = data.pocketLst[i][1]
            if i == 1 or i == 4:
                radius = 0.75* data.pocketr
            else:
                radius = data.pocketr
            if i == data.pocket:
                canvas.create_oval(x-radius -5, y-radius-5, x+radius+5, y+radius+5, fill = "green" )
            canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill = "black" )
        for i in range (len(data.circles)):
            x = data.circles[i][0]
            y = data.circles[i][1]
            num = data.circles[i][2]
            color = data.colorDict[num][0]
    
            canvas.create_oval(x - data.r, y - data.r, x + data.r, y + data.r, fill = color)
            if data.colorDict[num][1] == 1:
                innerRadius = 10
                canvas.create_oval(x - innerRadius, y- innerRadius, x + innerRadius, y + innerRadius, fill = "white")
        

        canvas.create_text(data.width/2, data.height - 30, anchor = "center", text = "Power: " + str(data.power), font = "Helvetica 20", fill = "white")
        canvas.create_text(data.width/2 -200, data.height - 30, anchor = "center", text = "Pocket: " + str(data.pocket), font = "Helvetica 20", fill = "white")
        canvas.create_text(data.width/2 + 200, data.height - 30, anchor = "center", text = "Ball: " + str(data.ball), font = "Helvetica 20", fill = "white")
        if data.help == False:
            canvas.create_text(data.width/2, 30, anchor = "center", text = "Press 'h' for help", font = "Helvetica 20", fill = "white")
        else:
            canvas.create_rectangle(data.width/2 - 400, data.height/2 - 200, data.width/2 + 400, data.height/2 + 200, fill = "teal")
            canvas.create_text(data.width/2, 300, anchor = "center", text = "Press 's' to shoot", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2, 350, anchor = "center", text = "Use numbers 0-5 to choose pocket", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2, 400, anchor = "center", text = "Use up/down to change power", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2, 450, anchor = "center", text = "Press 'r' to reset", font = "Helvetica 20", fill = "white")
     
    def redrawAll(canvas, data):
        if data.state == 0:
            drawState0(canvas, data)
        if data.state == 4:
            drawState4(canvas, data)
    
    
    ####################################
    # use the run function as-is
    ####################################
    
    
    def run(width=300, height=300):
        def redrawAllWrapper(canvas, data):
            canvas.delete(ALL)
            canvas.create_rectangle(0, 0, data.width, data.height,
                                    fill='white', width=0)
            redrawAll(canvas, data)
            canvas.update()    
    
        def mousePressedWrapper(event, canvas, data):
            mousePressed(event, data)
            redrawAllWrapper(canvas, data)
    
        def keyPressedWrapper(event, canvas, data):
            keyPressed(event, data)
            redrawAllWrapper(canvas, data)
    
        def timerFiredWrapper(canvas, data):
            timerFired(data)
            redrawAllWrapper(canvas, data)
            # pause, then call timerFired again
            canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        # Set up data and call init
        class Struct(object): pass
        data = Struct()
        data.width = width
        data.height = height
        data.timerDelay = 25
        root = Tk()
        root.resizable(width=False, height=False) # prevents resizing window
        init(data)
        # create the root and the canvas
        canvas = Canvas(root, width=data.width, height=data.height)
        canvas.configure(bd=0, highlightthickness=0)
        canvas.pack()
        # set up events
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, canvas, data))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, canvas, data))
        timerFiredWrapper(canvas, data)
        # and launch the app
        root.mainloop()  # blocks until window is closed
        print("bye!")
    run(1430, 850)
    
def runGame():

        
        
    # Basic Animation Framework from 112 Notes
    
    
    ###################################
    # customize these functions
    ###################################
    
    def init(data):
        
       
        getCircles(data)
        # for i in range(1, len(data.circles)):
        #     if data.circles[i][0] > 0:
        #         data.ball = i
        data.ball = 7
        data.pocket = 0
        data.width = 1430
        data.height = 850
        data.r = 20
        data.pocketr = 60
        data.boardColor = "navy blue"
    
        data.pocketLst = [(100, 100), (700, 100), (1350, 100),(100, 740), (700, 740), (1350, 740)]
        data.cueX = data.circles[0][0]
        data.cueY = data.circles[0][1]
        data.ballX = data.circles[data.ball][0]
        data.ballY = data.circles[data.ball][1]
      
        data.cueYM = -1 * data.circles[0][1]
        data.ballYM = -1*data.ballY
        data.pocketX = data.pocketLst[data.pocket][0]
        data.pocketY = data.pocketLst[data.pocket][1]
        data.pocketYM = -1*data.pocketLst[data.pocket][1]
        data.colorDict = {0: ('white', 0), 1: ('yellow', 0), 2: ('blue', 0), 3: ('red', 0), 4: ('purple', 0), 5: ('orange', 0), 6: ('green', 0), 7: ('teal', 0), 8: ('black', 0), 9: ('yellow', 1), 10: ('blue', 1), 11: ('red', 1), 12: ('purple', 1), 13: ('orange', 1), 14: ('green', 1), 15: ('teal', 1)}
        
        data.count = 0
    
        data.friction = 0.05
        data.power = 15
        data.state = 4
        data.pocketDiff = [(20, -20), (0, -10), (-20, -20), (20, 20), (0, 10), (-20, 20)]
        data.angle = 0
        data.angleDiff = math.pi/64
        data.help = False
        
 
    def getCircles(data):
        data.circles = [0]*16
        locLst = list(range(16))
        random.shuffle(locLst)
        for i in range (16):
            box = locLst[i]
            row = box//4
            col = box%4
            x = random.randint(200 + col*250, 200 + (col + 1)*250)
            y = random.randint(200 + row*125, 200 + (row + 1)*125)
            for j in range (0, i):
                x2 = data.circles[j][0]
                y2 = data.circles[j][1]
                d = getDistance(x, y, x2, y2)
                if d < 40:
                    x = random.randint(200 + col*250, 200 + (col + 1)*250)
                    y = random.randint(200 + row*125, 200 + (row + 1)*125)
            data.circles[i] = [x, y, i, 0, 0]
            
        
        

            
    
        
    def formatCircles(data):
        newLst = []
        finLst = [newLst]*16
        # print(findCoord(5))
        for i in range (16):
            result = findCoord(i)
            
            try:
                x = result[0] - 20
                y = result[1]
            except:
                x, y = -100, -100
                
            finLst[i] = [x, y, i, 0, 0]
        data.circles = finLst
    def getLine(x1, y1, x2, y2):
        if x2 - x1 == 0: return (0, 0)
        slope = (y2-y1)/(x2-x1)
        intercept1 = y1 - (slope*x1)
        intercept2 = y2 - (slope*x2)
        if math.isclose(intercept1, intercept2):
            return (slope, intercept1)
            
   
    def findConflict(x1, x2, slope, intercept, data, constant):
        diameter = 40
        slope *= constant
        for i in range (len(data.circles)):
            slope2 = -1/slope
            ballX = data.circles[i][0]
            ballY = -1* data.circles[i][1]
            if x1  < x2:
                if ballX <= x1:
                    continue
                if ballX >= x2:
                    continue
            elif x1 > x2:
                if ballX <= x2:
                    continue
                if ballX >= x1:
                    continue
            intercept2 = ballY - ballX*slope2
            iX = (intercept - intercept2)/( slope2 - slope)
            iY1 = slope2*iX + intercept2
            iY2 = slope*iX + intercept
            sD = getDistance(ballX, ballY, iX, iY2)
    
                
                
            if sD < diameter:
                return True
                
        return False
    
    def findContact(ballX, ballY, slope, intercept, data):
        t = abs(slope)
        radius = 40
        param = math.sqrt(t**2 + 1)
        s = radius/param
        if data.ballX < data.pocketX:
            x = ballX - s
        else:
            x = ballX + s
        if data.cueY < data.pocketY:
            y = ballY + abs(slope*s)
        else:
            y = ballY - abs(slope*s)
        
        return (x,y)
    
    def findCue(data):
        (xD, yD) = data.pocketDiff[data.pocket]
        (data.slope1,data.intercept1) = getLine(data.ballX, data.ballYM, data.pocketX + xD, data.pocketYM + yD)
        (data.cX, data.cYM) = findContact(data.ballX,data.ballYM, data.slope1, data.intercept1, data)
        (data.slope2, data.intercept2) = getLine(data.cX, data.cYM, data.cueX, data.cueYM)
        data.slope2 = -1*data.slope2
        if data.cX > data.cueX:
            data.x2 =  data.cueX - 50
            data.x1 = data.cueX - 300
            data.y2 = (data.cueX - 50)*(data.slope2)  - data.intercept2
            data.y1 = (data.cueX - 300)*(data.slope2) - data.intercept2
        else:
            data.x2 =  data.cueX + 50
            data.x1 = data.cueX + 300
            data.y2 = (data.cueX + 50)*(data.slope2)  - data.intercept2
            data.y1 = (data.cueX + 300)*(data.slope2) - data.intercept2
            
    def findPracticeCue(data):
        if math.cos(data.angle) == 0:
            if math.sin(data.angle == 1):
                 data.slope3 = -1000
            else: data.slope3 = 1000
        else:
            data.slope3 = math.sin(data.angle)/math.cos(data.angle)
        data.intercept3 = data.cueY*-1  - data.slope3*data.cueX 
        param = math.sqrt((data.slope3)**2 + 1)
        t = 50/param
    
        
        if data.angle > math.pi/2 and data.angle < 3*math.pi/2:
            data.x3 =  data.cueX + t
            data.x4 = data.cueX + 6*t
            data.y3 = -1*((data.cueX + t)*(data.slope3)  + data.intercept3)
            data.y4 = -1*((data.cueX + 6*t)*(data.slope3) + data.intercept3)
        else:
            data.x3 =  data.cueX - t
            data.x4 = data.cueX - 6*t
            data.y3 = -1*((data.cueX - t)*(data.slope3)  + data.intercept3)
            data.y4 = -1*((data.cueX - 6*t)*(data.slope3) + data.intercept3)
        
    def getDistance(x1, y1, x2, y2):
        d = abs(x1 - x2)**2 + abs(y1 - y2)**2
        return math.sqrt(d)
    
    def checkCollision(i, j, data):
        x1 = data.circles[i][0]
        y1 = data.circles[i][1]
        x2 = data.circles[j][0]
        y2 = data.circles[j][1]
        d = getDistance(x1, y1, x2, y2)
        if x1 < 0 or x2 < 0:
            return None
        if d <= 2 * data.r:
            diff = 2*(data.r) - d 
        
           
                
            if data.circles[i][3] == 0 and data.circles[i][4] == 0:
                if data.circles[j][3] == 0 and data.circles[j][4] == 0:
                    
                    return None
                if diff > 0.2 and diff < 10:
                    print("one")

                    oneLen = math.sqrt(data.circles[j][3]**2 + data.circles[j][4]**2 )
                    if oneLen != 0:
                        t = diff/oneLen
                        data.circles[j][0] -= data.circles[j][3] * t
                        data.circles[j][1] -= data.circles[j][4] * t
                        x1 = data.circles[i][0]
                        y1 = data.circles[i][1]
                        x2 = data.circles[j][0]
                        y2 = data.circles[j][1]
                       
                # print("enter")
                energyLoss = 0.7
                speed = energyLoss*math.sqrt(data.circles[j][3]**2 + data.circles[j][4]**2 )
                slope, intercept1 = getLine(x1, -1*y1, x2, -1*y2)
                # print(slope)
                # print (slope, "hit slope")
                param = math.sqrt(slope**2 + 1)
                x1 = data.circles[i][0]
                y1 = data.circles[i][1]
                x2 = data.circles[j][0]
                y2 = data.circles[j][1]
                if slope == 0: 
                    s = 1
                else:
                    s = abs(speed/param)
                    # print(s, 1)
                print("one")
                print (x1, x2, i , j, slope)
                if x1 < x2:
                    
                    data.circles[i][3] = -1*s
                    data.circles[j][3] = -0.5*abs(s * slope)
                else:
                    data.circles[i][3] = s
                    data.circles[j][3] = 0.5*abs(s * slope)
    
                if y1 < y2:
                    data.circles[i][4] = -1*abs(s * slope)
                    

                else:
                    data.circles[i][4] = abs(s * slope)
                if data.circles[j][4] > 0:
                    data.circles[j][4] = 0.5*s
                else:
                    if abs(data.circles[j][4]) > 5:
                        
                        data.circles[j][4] = -0.5*s
                    else:
                        data.circles[j][4] = 0.5*s
                if abs(data.circles[i][3]/data.circles[j][3]) < 1.4:
                    data.circles[j][3] *= -1
                if abs(data.circles[i][4]/data.circles[j][4]) < 1.4:
                    data.circles[j][4] *= -1
          
          
    
            
            elif data.circles[j][3] == 0 and data.circles[j][4] == 0:
                if data.circles[i][3] == 0 and data.circles[i][4] == 0:
                   
                    return None
                if diff > 0.2 and diff < 10:
                    print("two")

                    oneLen = math.sqrt(data.circles[i][3]**2 + data.circles[i][4]**2 )
                    if oneLen != 0:
                        t = diff/oneLen
                        data.circles[i][0] -= data.circles[i][3] * t
                        data.circles[i][1] -= data.circles[i][4] * t
                        x1 = data.circles[j][0]
                        y1 = data.circles[j][1]
                        x2 = data.circles[i][0]
                        y2 = data.circles[i][1]
                       
                        

                     
                energyLoss = 0.7
                speed = energyLoss*math.sqrt(data.circles[i][3]**2 + data.circles[i][4]**2 )
                slope, intercept1 = getLine(x1, -1*y1, x2, -1*y2)
                # print(slope, "test2")

                # print (slope, "hit slope")
                param = math.sqrt(slope**2 + 1)
                x1 = data.circles[j][0]
                y1 = data.circles[j][1]
                x2 = data.circles[i][0]
                y2 = data.circles[i][1]

                if slope == 0: 
                    s = 1
                else:
                    s = abs(speed/param)
                    # print(s, 2)
                print (x1, x2, i , j, slope)
                if x1 < x2:
                    data.circles[j][3] = -1*s
                    data.circles[i][3] = -0.5*abs(s * slope)
                else:
                    data.circles[j][3] = s
                    data.circles[i][3] = 0.5*abs(s * slope)
    
                if y1 < y2:
                    data.circles[j][4] = -1*abs(s * slope)
                else:
                    data.circles[j][4] = abs(s * slope)
                if data.circles[i][4] > 0:
                    data.circles[i][4] = 0.5*s
                else:
                    if abs(data.circles[i][4]) > 5:
                        
                        data.circles[i][4] = -0.5*s
                    else:
                        data.circles[i][4] = 0.5*s
            else:
                data.circles[i][3], data.circles[j][3] = data.circles[j][3], data.circles[i][3]
                data.circles[i][4], data.circles[j][4] = data.circles[j][4], data.circles[i][4]
            if abs(data.circles[i][3]/data.circles[j][3]) < 1.4:
                    data.circles[i][3] *= -1
            if abs(data.circles[i][4]/data.circles[j][4]) < 1.4:
                    data.circles[i][4] *= -1
                
        
    def mousePressed(event, data):
        # use event.x and event.y
        pass
    
    def keyPressed(event, data):
        if event.keysym == "h":
            data.help = not data.help
        if data.state == 4:
            if event.keysym == "s":
                
                findCue(data)
                newSlope = 1
                param = math.sqrt((abs(data.slope2))**2 + 1)
                scale = data.power/param
                if data.cueX > data.cX:
                    xSpeed = -1 * scale 
                else:
                    xSpeed = scale
                if data.cueYM > data.cYM:
                    ySpeed = abs(scale * data.slope2)
                else:
                    ySpeed = abs(scale * data.slope2) * -1
                data.circles[0][3] = xSpeed
                data.circles[0][4] = ySpeed
            if event.keysym == "c":
                chooseBall(data)
            if event.keysym == "r":
                init(data)
            if event.keysym == "Up":
                data.power += 1
            if event.keysym == "Down":
                data.power -= 1
            
            if event.keysym == "p":
                print ("changing from computer to you")
                data.state = 1
                
            if event.keysym == "p":
                print(data.circles)
            if event.keysym == "q":
                print(data.circles[0][4], "cue speed")
        if data.state == 1:
            if event.keysym == "c":
                print ("changing to computer")
                data.state = 4
            if event.keysym == "Left":
                data.angle += data.angleDiff
                while data.angle >= 2*math.pi:
                    data.angle -= 2*math.pi
                while data.angle < 0:
                    data.angle += 2*math.pi
            if event.keysym == "Right":
                data.angle -= data.angleDiff
                while data.angle >= 2*math.pi:
                    data.angle -= 2*math.pi
                while data.angle < 0:
                    data.angle += 2*math.pi
            if event.keysym == "s":
                findPracticeCue(data)
                param = math.sqrt((abs(data.slope3))**2 + 1)
                scale = data.power/param
                if data.angle >= 3* math.pi/2:
                    xSpeed = scale
                    ySpeed = abs(scale * data.slope3)
                elif data.angle >= math.pi and data.angle < 3*math.pi/2:
                    xSpeed = -1*scale
                    ySpeed = abs(scale * data.slope3)
                elif data.angle >= math.pi/2 and data.angle < math.pi:
                    xSpeed = -1*scale
                    ySpeed = -1*abs(scale * data.slope3)
                else:
                    xSpeed = scale
                    ySpeed = -1*abs(scale * data.slope3)
                
                data.circles[0][3] = xSpeed
                data.circles[0][4] = ySpeed
            if event.keysym == "Up":
                data.power += 1
            if event.keysym == "Down":
                data.power -= 1
            if event.keysym == "r":
                init(data)
    def chooseBall(data):
        availableBalls = []
        ballFound = False
        for l in range (len(data.circles)):
            if l > 8 or l == 0:
                continue
            if data.circles[l][0] > 0 and data.circles[l][1] > 0:
                data.newBall = l
                data.ball = data.newBall
                data.ballX = data.circles[data.ball][0]
                data.ballY = data.circles[data.ball][1]
                data.ballYM = -1*data.ballY
                for m in range (len(data.pocketLst)):
                    data.pocket = m
                    data.pocketX = data.pocketLst[data.pocket][0]
                    data.pocketY = data.pocketLst[data.pocket][1]
                    data.pocketYM = -1*data.pocketLst[data.pocket][1]
                    
                    findCue(data)
                    if findConflict(data.cX, data.circles[0][0], data.slope2, data.intercept2, data, -1):
                        continue
                
                    if findConflict(data.ballX, data.pocketLst[data.pocket][0],  data.slope1, data.intercept1, data, 1):
                        continue 
                    print(data.pocket)
                    ballFound = True
                    break
            if ballFound == True:
                break
        
                
           
   
       
            
                
    def timer4(data):
        data.count += 1
        if data.state == 4:
            findCue(data)
        if data.state == 1:
            findPracticeCue(data)
        
        for i in range (len(data.circles)):
            cX = data.circles[i][3]
            cY = data.circles[i][4]
            data.circles[i][0] += data.circles[i][3]
            data.circles[i][1] += data.circles[i][4]
            param = math.sqrt(data.circles[i][3]**2 + data.circles[i][4] ** 2)
            if param != 0:
                scale = data.friction/param
            else: scale = 1
            xFric = abs(data.circles[i][3] * scale)
            yFric = abs(data.circles[i][4] * scale)
            
            
            if abs(data.circles[i][3]) <= xFric or abs(data.circles[i][4]) <= yFric:
                data.circles[i][3] = 0
                data.circles[i][4] = 0
            if data.circles[i][3] > 0:
                data.circles[i][3] -= xFric
            elif data.circles[i][3] < 0:
                data.circles[i][3] += xFric
            if data.circles[i][4] > 0:
                data.circles[i][4] -= yFric
            elif data.circles[i][4] < 0:
                data.circles[i][4] += yFric
        for i in range (len(data.circles)):
            for j in range (i, len(data.circles)):
                if i == j:
                    continue
                checkCollision(i,j, data)
        for i in range (len(data.circles)):
            for j in range (len(data.pocketLst)):
                # print (data.circles)
                x1 = data.circles[i][0]
                y1 = data.circles[i][1]
                x2 = data.pocketLst[j][0]
                y2 = data.pocketLst[j][1]
                if j == 1 or j == 4:
                    if getDistance(x1, y1, x2, y2) < data.pocketr/2 + 10:
                        pass
                        data.circles[i][0] = -100
                        data.circles[i][1] = -100
                else:   
                    if getDistance(x1, y1, x2, y2) < data.pocketr + 10:
                        pass
                        data.circles[i][0] = -100
                        data.circles[i][1] = -100
    
            if data.circles[i][0] < data.r + 100 or data.circles[i][0] > data.width - 100 - data.r:
                data.circles[i][3] *= -0.7
            if data.circles[i][1] < data.r + 100 or data.circles[i][1] > data.height - 100 - 2 * data.r:
                data.circles[i][4] *= -0.7
        data.cueX = data.circles[0][0]
        data.cueY = data.circles[0][1]
        data.cueYM = -1*data.circles[0][1]
        data.ballX = data.circles[data.ball][0]
        data.ballY = data.circles[data.ball][1]
    def timerFired(data):
        if data.state == 4 or data.state == 1:
            timer4(data)
        for i in range (len(data.circles)):
            if data.circles[i][4] != 0:
                pass
        
                
                
    def drawState4(canvas,data):   
        canvas.create_rectangle(0,0,data.width, data.height, fill = data.boardColor)
        canvas.create_rectangle(100, 100, 1345, 740, width = 5)
        if data.state == 4:
            findCue(data)
            
            if data.circles[0][3] == 0:
                canvas.create_oval(data.cX - 5, -1*data.cYM - 5, data.cX + 5, -1*data.cYM + 5, fill = "black")
                canvas.create_line(data.x1, data.y1, data.x2, data.y2, width = 10, fill = "black")
           
     
        if data.state == 1:
            findPracticeCue(data)
            if data.circles[0][3] == 0:
                canvas.create_line(data.x3, data.y3, data.x4, data.y4, width = 10, fill = "white")
        
        # canvas.create_oval(data.cX - 4, -1*data.cYM - 5, data.cX + 5, -1*data.cYM + 5, fill = "black")
        
        
        
            
        for i in range (len(data.pocketLst)):
            x = data.pocketLst[i][0]
            y = data.pocketLst[i][1]
            if i == 1 or i == 4:
                radius = 0.75* data.pocketr
            else:
                radius = data.pocketr
            
            canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill = "black" )
        for i in range (len(data.circles)):
            x = data.circles[i][0]
            y = data.circles[i][1]
            num = data.circles[i][2]
            color = data.colorDict[num][0]
    
            canvas.create_oval(x - data.r, y - data.r, x + data.r, y + data.r, fill = color)
            if data.colorDict[num][1] == 1:
                innerRadius = 10
                canvas.create_oval(x - innerRadius, y- innerRadius, x + innerRadius, y + innerRadius, fill = "white")
        

        canvas.create_text(data.width/2, data.height - 30, anchor = "center", text = "Power: " + str(data.power), font = "Helvetica 20", fill = "white")
        canvas.create_text(data.width/2 -200, data.height - 30, anchor = "center", text = "Pocket: " + str(data.pocket), font = "Helvetica 20", fill = "white")
        canvas.create_text(data.width/2 + 200, data.height - 30, anchor = "center", text = "Ball: " + str(data.ball), font = "Helvetica 20", fill = "white")
        if data.help == False:
            canvas.create_text(data.width/2, 30, anchor = "center", text = "Press 'h' for help", font = "Helvetica 20", fill = "white")
        else:
            canvas.create_rectangle(data.width/2 - 400, data.height/2 - 400, data.width/2 + 400, data.height/2 + 200, fill = "teal")
            canvas.create_text(data.width/2 - 200, 100, anchor = "nw", text = "When it's the computer's turn", fill = "white", font = "Helvetica 20")
            canvas.create_text(data.width/2 - 150, 150, anchor = "nw", text = "Press 'c' to choose the pocket", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2- 150, 200, anchor = "nw", text = "Press 's' to shoot", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2- 150, 250, anchor = "nw", text = "Press 'r' to reset", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2- 150, 300, anchor = "nw", text = "Press 'p' to switch to player", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2 - 200, 350, anchor = "nw", text = "When it's the player's turn", fill = "white", font = "Helvetica 20")
            canvas.create_text(data.width/2- 150, 400, anchor = "nw", text = "Use left/right to move cue'", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2- 150, 450, anchor = "nw", text = "Use up/down to adjust power", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2- 150, 500, anchor = "nw", text = "Press 's' to shoot", font = "Helvetica 20", fill = "white")
            canvas.create_text(data.width/2- 150, 550, anchor = "nw", text = "Press 'c' to switch to computer", font = "Helvetica 20", fill = "white")
     
     
    def redrawAll(canvas, data):
        if data.state == 0:
            drawState0(canvas, data)
        if data.state == 4 or data.state == 1:
            drawState4(canvas, data)
    ####################################
    # use the run function as-is
    ####################################
    
    
    def run(width=300, height=300):
        def redrawAllWrapper(canvas, data):
            canvas.delete(ALL)
            canvas.create_rectangle(0, 0, data.width, data.height,
                                    fill='white', width=0)
            redrawAll(canvas, data)
            canvas.update()    
    
        def mousePressedWrapper(event, canvas, data):
            mousePressed(event, data)
            redrawAllWrapper(canvas, data)
    
        def keyPressedWrapper(event, canvas, data):
            keyPressed(event, data)
            redrawAllWrapper(canvas, data)
    
        def timerFiredWrapper(canvas, data):
            timerFired(data)
            redrawAllWrapper(canvas, data)
            # pause, then call timerFired again
            canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        # Set up data and call init
        class Struct(object): pass
        data = Struct()
        data.width = width
        data.height = height
        data.timerDelay = 25
        root = Tk()
        root.resizable(width=False, height=False) # prevents resizing window
        init(data)
        # create the root and the canvas
        canvas = Canvas(root, width=data.width, height=data.height)
        canvas.configure(bd=0, highlightthickness=0)
        canvas.pack()
        # set up events
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, canvas, data))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, canvas, data))
        timerFiredWrapper(canvas, data)
        # and launch the app
        root.mainloop()  # blocks until window is closed
        print("bye!")
    run(1430, 850)
def runTrainer():
    # Basic Animation Framework
        
    
    ####################################
    # customize these functions
    ####################################
    
    def init(data):
        # load data.xyz as appropriate
        data.ball = 8
        data.ballX = random.randint(900, 1200)
        data.ballY = random.randint(200, 600)
        data.cueX = random.randint(500, 900)
        data.cueY = random.randint(300, 600)
        data.cueYM = -1*data.cueY
        data.ballYM = -1*data.ballY
        data.pocketLst = [(70, 70), (700, 70), (1350, 70),(70, 750), (700, 750), (1350, 750)]
        data.pocket = 2 
        if data.ballY > data.cueY:
            data.pocket = 5
        data.pocketX = data.pocketLst[data.pocket][0]
        data.pocketY = data.pocketLst[data.pocket][1]
        data.pocketYM = -1*data.pocketLst[data.pocket][1]
        data.width = 1430
        data.height = 850
        data.pocketr = 60
        data.r = 20
        data.change = random.choice([-4,-3,-2,-1,0,1,2,3,4])
        data.marker = False
        data.state = 0
        data.hard = 2
        data.angleDiff = math.pi/(8*data.hard)
        

        

        
    def findCue(data):
        (data.slope1,data.intercept1) = getLine(data.ballX, data.ballYM, data.pocketX, data.pocketYM)
        (data.cX, data.cYM) = findContact(data.ballX,data.ballYM, data.slope1, data.intercept1, data)
        
        (data.slope2, data.intercept2) = getLine(data.cX, data.cYM, data.cueX, data.cueYM)
        data.slope2 = -1*data.slope2
        if data.ballX > data.cueX:
            data.x2 =  data.cueX - 50
            data.x1 = data.cueX - 300
            data.y2 = (data.cueX - 50)*(data.slope2)  - data.intercept2
            data.y1 = (data.cueX - 300)*(data.slope2) - data.intercept2
        else:
            data.x2 =  data.cueX + 50
            data.x1 = data.cueX + 300
            data.y2 = (data.cueX + 50)*(data.slope2)  - data.intercept2
            data.y1 = (data.cueX + 300)*(data.slope2) - data.intercept2
        data.angle = np.arctan(-1*data.slope2) + data.change* data.angleDiff
        while data.angle >= 2*math.pi:
            data.angle -= 2*math.pi
        while data.angle < 0:
            data.angle += 2*math.pi
        findPracticeCue(data)
    def findPracticeCue(data):
        if math.cos(data.angle) == 0:
            if math.sin(data.angle == 1):
                 data.slope3 = -1000
            else: data.slope3 = 1000
        else:
            data.slope3 = math.sin(data.angle)/math.cos(data.angle)
        data.intercept3 = data.cueY*-1  - data.slope3*data.cueX 
        param = math.sqrt((data.slope3)**2 + 1)
        t = 50/param
    
        
        if data.angle > math.pi/2 and data.angle < 3*math.pi/2:
            data.x3 =  data.cueX + t
            data.x4 = data.cueX + 6*t
            data.y3 = -1*((data.cueX + t)*(data.slope3)  + data.intercept3)
            data.y4 = -1*((data.cueX + 6*t)*(data.slope3) + data.intercept3)
        else:
            data.x3 =  data.cueX - t
            data.x4 = data.cueX - 6*t
            data.y3 = -1*((data.cueX - t)*(data.slope3)  + data.intercept3)
            data.y4 = -1*((data.cueX - 6*t)*(data.slope3) + data.intercept3)
        print(data.x3, data.y3, data.intercept3, data.cueY, data.cueX, data.angle, t, data.slope3)
        
    def findContact(ballX, ballY, slope, intercept, data):
        data.angleDiff = math.pi/(8*data.hard)

        t = abs(slope)
        radius = 40
        param = math.sqrt(t**2 + 1)
        s = radius/param
        if data.ballX < data.pocketX:
            x = ballX - s
        else:
            x = ballX + s
        if data.cueY < data.pocketY:
            y = ballY + abs(slope*s)
        else:
            y = ballY - abs(slope*s)
        
        return (x,y)
    def getLine(x1, y1, x2, y2):
        if x2 - x1 == 0: return (0, 0)
        slope = (y2-y1)/(x2-x1)
        intercept1 = y1 - (slope*x1)
        intercept2 = y2 - (slope*x2)
        if math.isclose(intercept1, intercept2):
            return (slope, intercept1)
            
    
    def mousePressed(event, data):
        # use event.x and event.y
        pass
    
    def keyPressed(event, data):
        # use event.char and event.keysym
        if event.keysym == "0":
            data.pocket = 0
            resetVals(data)
        if event.keysym == "1":
            data.pocket = 1
            resetVals(data)
        if event.keysym == "2":
            data.pocket = 2
            resetVals(data)
        if event.keysym == "3":
            data.pocket = 3
            resetVals(data)
        if event.keysym == "4":
            data.pocket = 4
            resetVals(data)
        if event.keysym == "5":
            data.pocket = 5
            resetVals(data)
        if event.keysym == "c":
            data.marker = not data.marker
            if data.change == 0:
                data.state = 1
            else:
                data.state = 2
        if event.keysym == "Left":
            data.change -= 1
            data.angle = np.arctan(-1*data.slope2) + data.change* data.angleDiff
            while data.angle >= 2*math.pi:
                data.angle -= 2*math.pi
            while data.angle < 0:
                data.angle += 2*math.pi
        if event.keysym == "Right":
            data.change += 1
            data.angle = np.arctan(-1*data.slope2) + data.change* data.angleDiff
            while data.angle >= 2*math.pi:
                data.angle -= 2*math.pi
            while data.angle < 0:
                data.angle += 2*math.pi
        if event.keysym == "r":
            init(data)
        if event.keysym == "Down":
            if data.hard > 1:
                data.hard -= 1
        if event.keysym == "Up":
            data.hard += 1
            
    def resetVals(data):
        data.pocketX = data.pocketLst[data.pocket][0]
        data.pocketY = data.pocketLst[data.pocket][1]
        data.pocketYM = -1*data.pocketLst[data.pocket][1]
        findCue(data)
        
    def redrawAll(canvas, data):
        findCue(data)
        canvas.create_rectangle(0,0,data.width, data.height, fill = "navy blue")
        for i in range (len(data.pocketLst)):
            x = data.pocketLst[i][0]
            y = data.pocketLst[i][1]
            if i == 1 or i == 4:
                radius = 0.5* data.pocketr
            else:
                radius = data.pocketr
            if i == data.pocket:
                canvas.create_oval(x-radius -5, y-radius-5, x+radius+5, y+radius+5, fill = "green" )
            canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill = "black" )
        

        canvas.create_oval(data.cueX - data.r, data.cueY - data.r, data.cueX + data.r, data.cueY + data.r, fill = "white")
        canvas.create_oval(data.ballX - data.r, data.ballY - data.r, data.ballX + data.r, data.ballY + data.r, fill = "orange")
        canvas.create_line(data.x3, data.y3, data.x4, data.y4, width = 10, fill = "white")
        if data.marker:
            canvas.create_oval(data.cX - 5, -1*data.cYM - 5, data.cX + 5, -1*data.cYM + 5, fill = "teal")
            canvas.create_line(data.x1, data.y1, data.x2, data.y2, width = 10, fill = "black")
        if data.state == 0:
            canvas.create_text(data.width/2, data.height - 40, anchor = "center", text = "Use the left/right arrows to move, up/down to change difficulty. Press 'c' to check.", font = "Helvetica 20 bold", 
            fill = "white")
        canvas.create_text(data.width/2, 200, anchor = "center", text = str("Difficulty: " + str(data.hard)), font = "Helvetica 24 bold", fill = "white")
        if data.state == 1:
            canvas.create_text(data.width/2, data.height - 40, anchor = "center", text = "Correct! Press 'r' to try again!", font = "Helvetica 24 bold", 
            fill = "white")
        if data.state == 2:
            canvas.create_text(data.width/2, data.height - 40, anchor = "center", text = "Incorrect! Press 'r' to try again!", font = "Helvetica 24 bold", 
            fill = "white")
    ####################################
    # use the run function as-is
    ####################################
    
    def run(width=300, height=300):
        def redrawAllWrapper(canvas, data):
            canvas.delete(ALL)
            canvas.create_rectangle(0, 0, data.width, data.height,
                                    fill='white', width=0)
            redrawAll(canvas, data)
            canvas.update()    
    
        def mousePressedWrapper(event, canvas, data):
            mousePressed(event, data)
            redrawAllWrapper(canvas, data)
    
        def keyPressedWrapper(event, canvas, data):
            keyPressed(event, data)
            redrawAllWrapper(canvas, data)
    
        # Set up data and call init
        class Struct(object): pass
        data = Struct()
        data.width = width
        data.height = height
        root = Tk()
        root.resizable(width=False, height=False) # prevents resizing window
        init(data)
        # create the root and the canvas
        canvas = Canvas(root, width=data.width, height=data.height)
        canvas.configure(bd=0, highlightthickness=0)
        canvas.pack()
        # set up events
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, canvas, data))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, canvas, data))
        redrawAll(canvas, data)
        # and launch the app
        root.mainloop()  # blocks until window is closed
        print("bye!")
    
    run(1430, 850)

    
runSetup()