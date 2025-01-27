#Ver 0.1.0: Create board and movement logic
#Ver 0.1.1: Reformat to use dictionaries instead of purely lists
#Ver 0.2.0: Finish single player 1, missing Hold and Next Pieces + splash screen.
#Ver 0.3.0: 2 player finished
#Ver 0.4.0: Damage send, recieve, buffer, indicator added

import math
import random

playerList = ('A','B')

background = Rect(0,0,400,400,fill=rgb(30,30,30)) 



sys = {}
sys['hasStarted'] = False
sys['width'] = 400
sys['height'] = 400
sys['verbose'] = False
sys['scale'] = 15

for i in range(0,len(playerList)):
    p = playerList[i]

    sys['canMove'+p] = True
    sys['pieceNum'+p] = 2
    sys['anchorPos'+p] = {'y':0,'x':0}
    sys['rotateState'+p] = 0
    sys['pieceType'+p] = 't'
    
    sys['moveTimerMid'+p] = 2
    sys['moveTimerMax'+p] = 6
    sys['moveTimer'+p] = sys['moveTimerMax'+p]
    
    sys['placeTimerMax'+p] = 30
    sys['placeTimerTemp'+p] = sys['placeTimerMax'+p]
    sys['placeRate'+p] = 1
    
    sys['upcomingPieces'+p] = []
    sys['bagPieces'+p] = []
    
    sys['maxFallTime'+p] = 20
    sys['currentFallTime'+p] = sys['maxFallTime'+p]
    
    sys['combo'+p] = 0


        
    sys['garbageBuffer'+p] = 0
    sys['garbageReceive'+p] = 0
    sys['garbageTimer'+p] = 400
    sys['garbageTimerMid'+p] = 200
    sys['garbageTimerMax'+p] = 400
    
    sys['board'+p] = [
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0]
        ]
        
    sys['boardDisplay'+p] = []
    sys['comboDisplay'+p] = []
    
    sys['garbageReceiveDisplay'+p] = []
    sys['garbageSendDisplay'+p] = []



pieceData = {'t':[0,0,0,0],'j':[0,0,0,0],'l':[0,0,0,0],'o':[0,0,0,0],'s':[0,0,0,0],'z':[0,0,0,0],'i':[0,0,0,0]}
#0:origin, 1:clock, 2: double, 3: counter
pieceData['t'][0] = [{'y':0,'x':1},{'y':1,'x':0},{'y':1,'x':1},{'y':1,'x':2}] 
pieceData['t'][1] = [{'y':0,'x':1},{'y':1,'x':1},{'y':1,'x':2},{'y':2,'x':1}] 
pieceData['t'][2] = [{'y':1,'x':0},{'y':1,'x':1},{'y':1,'x':2},{'y':2,'x':1}] 
pieceData['t'][3] = [{'y':0,'x':1},{'y':1,'x':0},{'y':1,'x':1},{'y':2,'x':1}]

pieceData['j'][0] = [{'y':0,'x':0},{'y':1,'x':0},{'y':1,'x':1},{'y':1,'x':2}]
pieceData['j'][1] = [{'y':0,'x':1},{'y':0,'x':2},{'y':1,'x':1},{'y':2,'x':1}]
pieceData['j'][2] = [{'y':1,'x':0},{'y':1,'x':1},{'y':1,'x':2},{'y':2,'x':2}]
pieceData['j'][3] = [{'y':0,'x':1},{'y':1,'x':1},{'y':2,'x':0},{'y':2,'x':1}]

pieceData['l'][0] = [{'y':0,'x':2},{'y':1,'x':0},{'y':1,'x':1},{'y':1,'x':2}]
pieceData['l'][1] = [{'y':0,'x':1},{'y':1,'x':1},{'y':2,'x':1},{'y':2,'x':2}]
pieceData['l'][2] = [{'y':1,'x':0},{'y':1,'x':1},{'y':1,'x':2},{'y':2,'x':0}]
pieceData['l'][3] = [{'y':0,'x':0},{'y':0,'x':1},{'y':1,'x':1},{'y':2,'x':1}]

pieceData['o'][0] = [{'y':0,'x':0},{'y':0,'x':1},{'y':1,'x':0},{'y':1,'x':1}]
pieceData['o'][1] = [{'y':0,'x':0},{'y':0,'x':1},{'y':1,'x':0},{'y':1,'x':1}]
pieceData['o'][2] = [{'y':0,'x':0},{'y':0,'x':1},{'y':1,'x':0},{'y':1,'x':1}]
pieceData['o'][3] = [{'y':0,'x':0},{'y':0,'x':1},{'y':1,'x':0},{'y':1,'x':1}]


pieceData['s'][0] = [{'y':0,'x':1},{'y':0,'x':2},{'y':1,'x':0},{'y':1,'x':1}]
pieceData['s'][1] = [{'y':0,'x':1},{'y':1,'x':1},{'y':1,'x':2},{'y':2,'x':2}]
pieceData['s'][2] = [{'y':1,'x':1},{'y':1,'x':2},{'y':2,'x':0},{'y':2,'x':1}]
pieceData['s'][3] = [{'y':0,'x':0},{'y':1,'x':0},{'y':1,'x':1},{'y':2,'x':1}]

pieceData['z'][0] = [{'y':0,'x':0},{'y':0,'x':1},{'y':1,'x':1},{'y':1,'x':2}]
pieceData['z'][1] = [{'y':0,'x':2},{'y':1,'x':1},{'y':1,'x':2},{'y':2,'x':1}]
pieceData['z'][2] = [{'y':1,'x':0},{'y':1,'x':1},{'y':2,'x':1},{'y':2,'x':2}]
pieceData['z'][3] = [{'y':0,'x':1},{'y':1,'x':0},{'y':1,'x':1},{'y':2,'x':0}]

pieceData['i'][0] = [{'y':1,'x':0},{'y':1,'x':1},{'y':1,'x':2},{'y':1,'x':3}]
pieceData['i'][1] = [{'y':0,'x':2},{'y':1,'x':2},{'y':2,'x':2},{'y':3,'x':2}]
pieceData['i'][2] = [{'y':2,'x':0},{'y':2,'x':1},{'y':2,'x':2},{'y':2,'x':3}]
pieceData['i'][3] = [{'y':0,'x':1},{'y':1,'x':1},{'y':2,'x':1},{'y':3,'x':1}]


kickTableR = [0,0,0,0]
kickTableR[0] = [{'x':0,'y':0},{'x':-1,'y':0},{'x':-1,'y':-1},{'x':0,'y':2},{'x':-1,'y':2}]
#manually adjusted kickTableR[1], kickNum3 to be {'x':0,'y':-1}, instead of 'y':-2.
#don't know why that causes the T to jump when clockwise but not when counter
kickTableR[1] = [{'x':0,'y':0},{'x':1,'y':0},{'x':1,'y':1},{'x':0,'y':-1},{'x':1,'y':-2}]
kickTableR[2] = [{'x':0,'y':0},{'x':1,'y':0},{'x':1,'y':-1},{'x':0,'y':2},{'x':1,'y':2}]
kickTableR[3] = [{'x':0,'y':0},{'x':-1,'y':0},{'x':-1,'y':1},{'x':0,'y':-2},{'x':-1,'y':-2}]

kickTableI = [0,0,0,0]
kickTableI[0] = [{'x':0,'y':0},{'x':-2,'y':0},{'x':1,'y':0},{'x':-2,'y':1},{'x':1,'y':-2}]
kickTableI[1] = [{'x':0,'y':0},{'x':-1,'y':0},{'x':2,'y':0},{'x':-1,'y':-2},{'x':2,'y':1}]
kickTableI[2] = [{'x':0,'y':0},{'x':2,'y':0},{'x':-1,'y':0},{'x':2,'y':-1},{'x':-1,'y':2}]
kickTableI[3] = [{'x':0,'y':0},{'x':1,'y':0},{'x':-2,'y':0},{'x':1,'y':2},{'x':-2,'y':1}]

comboTable = [0,0,1,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5]


labelA = Label(sys['garbageTimerA'], 0+30,370,visible=False)

for i in range(0,len(playerList)):
    playerNum = i
    p = playerList[i] 
    
    overallWidth = sys['scale']*len(sys['board'+p][0])
    overallHeight = sys['scale']*len(sys['board'+p])
    
    
    
    for i in range(0,len(sys['board'+p])):
        tempY = i
        sys['boardDisplay'+p].append([])
        for i in range(0,len(sys['board'+p][tempY])):
            tempX = i
    
                
            scale = sys['scale']

            
                
            offsetLeft = 25 + tempX*scale + playerNum*200
            offsetTop = sys['height']/2-overallHeight/2 + tempY*scale
    
            
            sys['boardDisplay'+p][tempY].append(Rect(offsetLeft,offsetTop,scale,scale,borderWidth=1))
    
    barLeft = 25 + len(sys['board'+p][0])*scale + playerNum*200
    barTop = sys['height']/2-overallHeight/2
    barLength = len(sys['board'+p])*scale
    percentR = sys['garbageReceive'+p] / len(sys['board'+p])
    percentS = sys['garbageBuffer'+p] / len(sys['board'+p])

    

    
    sys['garbageReceiveDisplay'+p].append(Line(barLeft, barTop - percentR*barLength, barLeft, barTop ,fill='red',lineWidth=5))
    sys['garbageSendDisplay'+p].append(Line(barLeft+5, barTop - percentS*barLength, barLeft+5, barTop ,fill='yellow',lineWidth=5))


title = Group()
title.add(Rect(0,0,400,400,fill='tan'))

text=[]
text.append('')
text.append('Dear Valued Employees:')
text.append('')
text.append('Today\'s agenda is training the trash compacting algorithm.')
text.append('')
text.append('Recently, we\'ve implemented')
text.append('a new system to allow for competitions.')
text.append('')
text.append('This will allow us to collect more data')
text.append('while increasing employee engagement.')
text.append('')
text.append('Please excuse us for the disruption in the workflow.')
text.append('')
text.append('Signed, Boss')
text.append('')
text.append('{Press SPACE to start}')
text.append('')
text.append('Note: 2 Players Required, A: WASD vs. B;Arrows')
text.append('Red: Damage Received, Yellow: Damage Sent')

for i in range (0,len(text)):
    title.add(Label(text[i],200,20+20*i,size=14,fill='black'))
    

        


def onKeyPress(key):
    
    #piece movement
    if key == 'up':
        #should remove or become hard drop?
        #movePiece('up', 'A')
        rotatePiece('clockwise','B')
    if key == 'left':
        movePiece('left', 'B')
    if key == 'right':
        movePiece('right', 'B')
    if key == 'down':
        #should get special treatement at some point (soft drop)
        movePiece('down', 'B')
    #if key == 'space':
    #    pass
        #pieceToGround('B')
    
        
    if key == 'w':
        #should remove or become hard drop?
        #movePiece('up', 'B')
        rotatePiece('clockwise','A')
    if key == 'a':
        movePiece('left', 'A')
    if key == 'd':
        movePiece('right', 'A')
    if key == 's':
        #should get special treatement at some point (soft drop)
        movePiece('down', 'A')
    #if key == 'enter':
    #    pieceToGround('A')
    
        
    #generate t piece
    if key == 'space':
        if sys['hasStarted'] == False:
            generatePiece('A')
            generatePiece('B')
            title.visible = False
            sys['hasStarted'] = True

    """
    #rotate clockwise
    if key == 'z':
        rotatePiece('clockwise','A')
    if key == 'x':
        rotatePiece('counter','A')
        
    if key == 'j':
        rotatePiece('clockwise','B')
    if key == 'k':
        rotatePiece('counter','B')
    """

def onStep():
    
    sys['garbageTimerA'] -= 1
    sys['garbageTimerB'] -= 1
    
    labelA.value = sys['garbageTimerA']  


    for i in range(0,len(playerList)):
        p = playerList[i]
        
 

    
        sys['currentFallTime'+p] -= 1
        if sys['currentFallTime'+p] < 0:
            sys['currentFallTime'+p] = sys['maxFallTime'+p]
            movePiece('down', p)
        pass
    
        if pieceIsGrounded(p):
            sys['placeTimerTemp'+p] -= sys['placeRate'+p]
            if sys['placeTimerTemp'+p] < 0:
                placePiece(p)
                sys['placeTimerTemp'+p] = sys['placeTimerMax'+p]
    
    #print('upcomingPiece is: ' + str(sys['upcomingPieces'+p]))
    #print('bagPiece is: ' + str(sys['bagPieces'+p]))

def onKeyHold(keys):
    if 'left' in keys:
        if sys['moveTimerB'] <= 0:
            sys['moveTimerB'] = sys['moveTimerMidB']
            movePiece('left', 'B')
        else:
            sys['moveTimerB'] -= 1
    if 'right' in keys:
        if sys['moveTimerB'] <= 0:
            sys['moveTimerB'] = sys['moveTimerMidB']
            movePiece('right', 'B')
        else:
            sys['moveTimerB'] -= 1
    if 'down' in keys:
        if sys['moveTimerB'] <= 0:
            sys['moveTimerB'] = sys['moveTimerMidB']
            movePiece('down', 'B')
        else:
            sys['moveTimerB'] -= 1
            sys['placeRateB'] = 4
    if 'a' in keys:
        if sys['moveTimerA'] <= 0:
            sys['moveTimerA'] = sys['moveTimerMidB']
            movePiece('left', 'A')
        else:
            sys['moveTimerA'] -= 1
    if 'd' in keys:
        if sys['moveTimerA'] <= 0:
            sys['moveTimerA'] = sys['moveTimerMidB']
            movePiece('right', 'A')
        else:
            sys['moveTimerA'] -= 1
    if 's' in keys:
        if sys['moveTimerA'] <= 0:
            sys['moveTimerA'] = sys['moveTimerMidB']
            movePiece('down', 'A')
        else:
            sys['moveTimerA'] -= 1
            sys['placeRateA'] = 4

def onKeyRelease(key):
    if key == 'left' or key =='right' or key == 'down':
        sys['moveTimerB'] = sys['moveTimerMaxB']
        sys['placeRateB'] = 1

    if key == 'a' or key =='d' or key == 's':
        sys['moveTimerA'] = sys['moveTimerMaxA']
        sys['placeRateA'] = 1

def movePiece(direction, p):
    piecePos = findPiecePos(p)
    tempPiecePos = []
    
    outOfBounds = checkBounds(p)
    offsetY = 0
    offsetX = 0
    canMove = True

    #set offset depending on direction pressed
    if outOfBounds[direction] == False:
        if direction == 'up':
            offsetY = -1
        elif direction == 'down':
            offsetY = 1
        elif direction == 'left':
            offsetX = -1
        elif direction == 'right':
            offsetX = 1
    else:
        canMove = False
        if sys['verbose']:
            print('no movement, bounded')
    
    #implement offset and store new coordinates in tempPiecePos    
    if canMove:
        for i in range(0,len(piecePos)):
            tempCoord = {'y':0,'x':0}
            tempCoord['y'] = piecePos[i]['y'] + offsetY
            tempCoord['x'] = piecePos[i]['x'] + offsetX
            if sys['board'+p][tempCoord['y']][tempCoord['x']] != 0 and sys['board'+p][tempCoord['y']][tempCoord['x']] != sys['pieceNum'+p]:
                canMove = False
                if sys['verbose']:
                    print('no movement, blocked by 1')
            tempPiecePos.append(tempCoord)
        if sys['verbose']:
            print('new positions: '+str(tempPiecePos))
    
    #remove old positions and implement new positions
    if canMove:
        for i in range(0,len(piecePos)):
            sys['board'+p][piecePos[i]['y']][piecePos[i]['x']] = 0
        for i in range(0,len(piecePos)):
            sys['board'+p][tempPiecePos[i]['y']][tempPiecePos[i]['x']] = sys['pieceNum'+p]
        
        #update anchor position
        sys['anchorPos'+p]['y'] += offsetY
        sys['anchorPos'+p]['x'] += offsetX
        
        updateBoard(p)

#generate new pieces
def generatePiece(p):
    if len(sys['upcomingPieces'+p]) == 0:
        bufferPieceInit(p)
    sys['pieceType'+p] = sys['upcomingPieces'+p][0]
    sys['upcomingPieces'+p].pop(0)

    
    print('piece generated is: ' + sys['pieceType'+p])
    sys['rotateState'+p] = 0
    match sys['pieceType'+p]:
        case 'i':
            sys['anchorPos'+p] = {'y':1,'x':3}
            pass
        case 'j':
            sys['anchorPos'+p] = {'y':1,'x':3}
            pass
        case 'l':
            sys['anchorPos'+p] = {'y':1,'x':3}
            pass
        case 'o':
            sys['anchorPos'+p] = {'y':1,'x':4}
            pass
        case 's':
            sys['anchorPos'+p] = {'y':1,'x':3}
            pass
        case 'z':
            sys['anchorPos'+p] = {'y':1,'x':3}
            pass
        case 't':
            sys['anchorPos'+p] = {'y':1,'x':3}
            
    for i in range(0,len(pieceData[sys['pieceType'+p]])):
        #add piece data to anchor, make spawn adjustments
        genPosY = sys['anchorPos'+p]['y'] + pieceData[sys['pieceType'+p]][0][i]['y']
        genPosX = sys['anchorPos'+p]['x'] + pieceData[sys['pieceType'+p]][0][i]['x']
        if sys['board'+p][genPosY][genPosX] == 1:
            print('game over, new piece topped out')
            Rect(0,0,400,400,fill='black')
            Label("Game Over.",200,100,fill='white',font='arial',size=48,border='gray')
            for i in range(0,len(playerList)):
                if playerList[i] == p:
                    pass
                else:
                    Label('Player ' + p + ' wins!',200,200,fill='white',size=24,border='gray')
                    Label('Thanks for your work, your paycheck',200,230,fill='black',size=18,border='gray')
                    Label('will arrive in the mail within',200,260,fill='black',size=18,border='gray')
                    Label('3 business days.',200,290,fill='black',size=18,border='gray')
            app.stop()
        else:
            sys['board'+p][genPosY][genPosX] = sys['pieceNum'+p]

    updateBoard(p)    

#update graphics from board values
def updateBoard(p):
    for i in range(0,len(sys['board'+p])):
        tempY = i
        for i in range(0,len(sys['board'+p][tempY])):
            tempX = i
            tempColor = 'black'
            tempBorder = 'dimGray'
            
            #check for each value, set color and border color
            if sys['board'+p][tempY][tempX] == 0:
                tempColor = 'black'
                tempBorder = 'dimGray'
            elif sys['board'+p][tempY][tempX] == 1:
                tempColor = 'yellow'
                tempBorder = 'dimGray'
            elif sys['board'+p][tempY][tempX] == 2:
                tempColor = 'cyan'
                tempBorder = 'dimGray'
            elif sys['board'+p][tempY][tempX] == 3:
                tempColor = 'gray'
                tempBorder = 'dimGray' 
            sys['boardDisplay'+p][tempY][tempX].fill = tempColor
            sys['boardDisplay'+p][tempY][tempX].border = tempBorder
            
    playernum = playerList.index(p)
    
    barTop = sys['height']/2-overallHeight/2
    barLength = len(sys['board'+p])*scale
    percentR = sys['garbageReceive'+p] / len(sys['board'+p])
    percentS = sys['garbageBuffer'+p] / len(sys['board'+p])

    
    for i in range(0,len(playerList)):
        sys['garbageReceiveDisplay'+p][0].y1 = barTop + percentR*barLength
        sys['garbageSendDisplay'+p][0].y1 = barTop + percentS*barLength
    
        
        
        


def rotatePiece(direction,p):
    piecePos = findPiecePos(p)
    tempPiecePos = []
    
    offX = 0
    offY = 0
    
    kickPass = False
    dir = 0
    
    
    if direction == 'clockwise':
        dir = 1
        if sys['rotateState'+p] < 3:
            sys['rotateState'+p] += 1
        else:
            sys['rotateState'+p] = 0
    elif direction == 'counter':
        dir = -1
        if sys['rotateState'+p] > 0:
            sys['rotateState'+p] -= 1
        else:
            sys['rotateState'+p] = 3
            
    for i in range(0,len(pieceData[sys['pieceType'+p]])):
        tempCoord = {'y':0,'x':0}
        tempCoord['y'] = sys['anchorPos'+p]['y'] + pieceData[sys['pieceType'+p]][sys['rotateState'+p]][i]['y']
        tempCoord['x'] = sys['anchorPos'+p]['x'] + pieceData[sys['pieceType'+p]][sys['rotateState'+p]][i]['x']
        tempPiecePos.append(tempCoord)
        
    for i in range(0,len(kickTableR[sys['rotateState'+p]])):
        #print('rotate')
        kickNum = i
        #print('testing kickNum' + str(kickNum))
        if kickPass == False:
            
            kickPass = True
            
            if sys['pieceType'+p] != 'i':
                offY = (kickTableR[sys['rotateState'+p]][kickNum]['y'] * dir)
                offX = (kickTableR[sys['rotateState'+p]][kickNum]['x'] * dir)
            else:
                offY = (kickTableI[sys['rotateState'+p]][kickNum]['y'] * dir)
                offX = (kickTableI[sys['rotateState'+p]][kickNum]['x'] * dir)
            

            
            for i in range(0,len(tempPiecePos)):
                if tempPiecePos[i]['y'] + offY >= len(sys['board'+p]) or tempPiecePos[i]['x'] + offX >= len(sys['board'+p][tempPiecePos[i]['y'] + offY]):
                    realCoordVal = -1
                elif tempPiecePos[i]['y'] + offY < 0 or tempPiecePos[i]['x'] + offX < 0:
                    realCoordVal = -1
                else:
                    realCoordVal = sys['board'+p][tempPiecePos[i]['y'] + offY][tempPiecePos[i]['x'] + offX]
                #print('realCoordVal: ' + str(realCoordVal))
                
                if realCoordVal != 0 and realCoordVal != sys['pieceNum'+p]:
                    kickPass = False
                    #print('fails: ' + str(kickPass))
                else:
                    pass
                    #print('passes: ' + str(kickPass))
            
            if kickPass == True:
                #print('testing kickNum' + str(kickNum))
                break
                
    
        
            
    if kickPass == True:
        #print('offY is: ' + str(offY))
        #print('offX is: ' + str(offX))
        for i in range(0,len(piecePos)):
            sys['board'+p][piecePos[i]['y']][piecePos[i]['x']] = 0
        for i in range(0,len(piecePos)):
            sys['board'+p][tempPiecePos[i]['y'] + offY][tempPiecePos[i]['x'] + offX] = sys['pieceNum'+p]
        updateBoard(p)
        
        sys['anchorPos'+p]['y'] += offY
        sys['anchorPos'+p]['x'] += offX
        
    else:
        print('kick Failed, stop')

#find all coordinates with sys['pieceNum' and returns as array of dictionaries
def findPiecePos(p):
    piecePos = []
    tempBoard = []
    tempBoard = sys['board'+p]

        
    for i in range(0,len(tempBoard)):
        tempY = i
        for i in range(0,len(tempBoard[tempY])):
            tempX = i
            if tempBoard[tempY][tempX] == sys['pieceNum'+p]:
                piecePos.append({'y':tempY,'x':tempX})
                
    if sys['verbose']:
        print('current positions'+ str(piecePos))
        
    return piecePos
    
def pieceIsGrounded(p):
    grounded = False
    if checkBounds(p)['down']:
        grounded = True
    else:
        piecePos = findPiecePos(p)
        for i in range(0,len(piecePos)):
            offsetVal = sys['board'+p][piecePos[i]['y'] + 1][piecePos[i]['x']]
            if offsetVal != sys['pieceNum'+p] and offsetVal != 0:
                #print('grounded is True')
                grounded = True
            
    return grounded
    
def pieceToGround(p):
    grounded = False
    piecePos = findPiecePos(p)
    offsetY = 0
    
    if checkBounds(p)['down']:
        grounded = True
    
    for i in range(piecePos[-1]['y'],len(sys['board'+p])):
        for i in range(0,len(piecePos)):

            if sys['board'+p][piecePos[i]['y']+offsetY+1][piecePos[i]['x']] != sys['pieceNum'+p] and sys['board'+p][piecePos['y']+offsetY][piecePos['x']] != 0:
                grounded = True
        if grounded == True:
            break
        else:
            offsetY += 1
    
    for i in range(0,len(piecePos)):
        sys['board'+p][piecePos[i]['y']][piecePos[i]['x']] = 0
    
    for i in range(0,len(piecePos)):
        sys['board'+p][piecePos[i]['y']+offsetY][piecePos[i]['x']] = sys['pieceNum'+p]
        
    placePiece(p)
        
        
        

    
    

def checkBounds(p):
    
    piecePos = findPiecePos(p)
    
    outOfBounds = {
        'up':False,
        'down':False,
        'left':False,
        'right':False
    }

    #check if any value will be out of bounds assuming movement
    for i in range(0, len(piecePos)):
        #check up
        if piecePos[i]['y'] == 0:
            outOfBounds['up'] = True
        # check down
        if piecePos[i]['y'] == len(sys['board'+p])-1:
            outOfBounds['down'] = True
        #check left
        if piecePos[i]['x'] == 0:
            outOfBounds['left'] = True
        #check right
        if piecePos[i]['x'] == len(sys['board'+p][0])-1:
            outOfBounds['right'] = True
        
    return outOfBounds

def placePiece(p):
    piecePos = findPiecePos(p)
    for i in range(0, len(piecePos)):
        sys['board'+p][piecePos[i]['y']][piecePos[i]['x']] = 1
        
    if len(sys['upcomingPieces'+p]) < 7:
        bufferPieceInit(p)
        print('upcomingPieces empty')
    
    isLineClear(p)

    
        
    
    if sys['garbageTimer'+p] <= 0:
        sys['garbageTimer'+p] = sys['garbageTimerMax'+p]
        addGarbage(sys['garbageReceive'+p],p)
        sys['garbageReceive'+p] = 0
        
    generatePiece(p)
    
def isLineClear(p):
    tempX = 0
    tempY = 0
    consecLines = 0
    totAttack = 0
    
    for i in range(0, len(sys['board'+p])):
        lineExists = True
        tempY = i
        for i in range(0, len(sys['board'+p][tempY])):
            tempX = i
            if sys['board'+p][tempY][tempX] == 0:
                lineExists = False
                if consecLines == 1:
                    totAttack += 1
                elif consecLines == 2 or consecLines == 3:
                    totAttack += 2
                elif consecLines >= 4:
                    totAttack += 4
                
                consecLines = 0
                #print('line does not exist')

                
                
        if lineExists == True:
            consecLines += 1
            i -= 1
            sys['board'+p].pop(tempY)
            sys['board'+p].insert(0, [0,0,0,0,0,0,0,0,0,0])
            print('line exists!')
    if consecLines == 1:
        totAttack += 0
    elif consecLines == 2:
        totAttack += 1
    elif consecLines == 3:
        totAttack += 2
    elif consecLines >= 4:
        totAttack += 4
    
    if totAttack > 0:
        sys['combo'+p] += 1
    else:
        sys['combo'+p] = 0
        
    totAttack += comboTable[sys['combo'+p]]
    
    if sys['combo'+p] == 0:
        totAttack += sys['garbageBuffer'+p]
        sys['garbageBuffer'+p] = 0
        
        if sys['garbageReceive'+p] >= totAttack:
            sys['garbageReceive'+p] -= totAttack
            totAttack = 0
        elif sys['garbageReceive'+p] < totAttack:
            totAttack -= sys['garbageReceive'+p]
            sys['garbageReceive'+p] = 0
            
            for i in range(0,len(playerList)):
                if playerList[i] == p:
                    pass
                else:
                    sys['garbageReceive'+playerList[i]] += totAttack
        pass
    else:
        sys['garbageBuffer'+p] += totAttack




                

def bufferPieceInit(p):

    sys['bagPieces'+p] = ['t','j','l','o','s','z','i']
    
    for i in range(0,len(['t','j','l','o','s','z','i'])):
        
        randomNum = random.randint(0,len(sys['bagPieces'+p]) - 1)
        
        #print('appends: ' + str(sys['bagPieces'+p][randomNum]))
        sys['upcomingPieces'+p].append(sys['bagPieces'+p][randomNum])
        #print('upcomingPieces are' + str(sys['upcomingPieces'+p]))
        sys['bagPieces'+p].pop(randomNum)
        #print('backPieces: ' + str(sys['bagPieces']))
    pass
bufferPieceInit('A')
bufferPieceInit('A')

bufferPieceInit('B')
bufferPieceInit('B')

def addGarbage(amount,p):
    print('addGarbage: ' + str(amount) + ' player: ' + p)
    if amount >= len(sys['board'+p]):
        amount == len(sys['board'+p])
    
    for i in range(0, amount):
        tempLine = [3,3,3,3,3,3,3,3,3,3]
        tempLine[random.randint(0,9)] = 0
        sys['board'+p].pop(0)
        sys['board'+p].append(tempLine)



          
                    
