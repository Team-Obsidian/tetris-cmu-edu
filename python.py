#Ver 0.1: Create board and movement logic


import math
app = {}
app['timePass'] = False
app['canMove'] = True
app['pieceNum'] = 2






app['board'] = [
    [0,0,0,0,0],
    [0,0,2,0,0],
    [0,2,2,2,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [1,1,0,0,0],
        ]
 
for i in range(0,len(app['board'])):
    Label(app['board'][i],200,100+15*i)
 


#board[y][x]


def onKeyPress(key):
    if key == 't':
        app['timePass'] = True
    if key == 'up':
        movePiece('up')
    if key == 'left':
        movePiece('left')
    if key == 'right':
        movePiece('right')
    if key == 'down':
        movePiece('down')
    


def onStep():
    pass






def movePiece(direction):
    #coordinates with 2s
    piecePos = []
    tempPiecePos = []
    outOfBounds = [False, False, False, False]
    offsetY = 0
    offsetX = 0
    canMove = True
    
    #[up, down, left, right]
    
    #find all coordinates with 2 and put them into piecePos
    for i in range(0,len(app['board'])):
        tempY = i
        for i in range(0,len(app['board'][tempY])):
            tempX = i
            if app['board'][tempY][tempX] == app['pieceNum']:
                piecePos.append([tempY,tempX])
    print('current positions'+ str(piecePos))
    
    #check if any value will be out of bounds assuming movement
    for i in range(0, len(piecePos)):
        #check top
        if piecePos[i][0] == 0:
            outOfBounds[0] = True
        # check bottom
        if piecePos[i][0] == len(app['board'])-1:
            outOfBounds[1] = True
        #check left
        if piecePos[i][1] == 0:
            outOfBounds[2] = True
        #check right
        if piecePos[i][1] == len(app['board'][0])-1:
            outOfBounds[3] = True
    
    #set offset depending on direction pressed
    if direction == 'up' and outOfBounds[0] == False:
        offsetY = -1
    elif direction == 'down' and outOfBounds[1] == False:
        offsetY = 1
    elif direction == 'left' and outOfBounds[2] == False:
        offsetX = -1
    elif direction == 'right' and outOfBounds[3] == False:
        offsetX = 1
    else:
        print('no movement, bounded')
        canMove = False
    
    #implement offset and store new coordinates in tempPiecePos    
    if canMove:
        for i in range(0,len(piecePos)):
            tempCoord = []
            tempCoord.append(piecePos[i][0] + offsetY)
            tempCoord.append(piecePos[i][1] + offsetX)
            if app['board'][tempCoord[0]][tempCoord[1]] == 1:
                print('no movement, blocked by 1')
                canMove = False
            tempPiecePos.append(tempCoord)
        print('new positions: '+str(tempPiecePos))
    
    #remove old positions and implement new positions
    if canMove:
        for i in range(0,len(piecePos)):
            app['board'][piecePos[i][0]][piecePos[i][1]] = 0
        for i in range(0,len(piecePos)):
            app['board'][tempPiecePos[i][0]][tempPiecePos[i][1]] = app['pieceNum']