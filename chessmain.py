# from python import * 
import pygame as p
import chessEngine
import turtle

WIDTH = HEIGHT = 512

DIMENSION = 8

SQ_SIZE = HEIGHT//DIMENSION

MAX_FPS = 15

IMAGES = {}

p.display.set_caption("CHESS_GAME_2_PLAYER")

icon=p.image.load("images/icon.png")

p.display.set_icon(icon)


def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK','wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('Images/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))   

def main():

    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock() 
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate=False
    loadImages()   #only do this once , before the while loop
    running = True
    sqSelected = ()  #no square is slected ,keep track of the last click of the user (tuple:(row,col))
    playerClicks = []  #keep track of player clicks(two tuples:[;(6,4),(4,4)])
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            elif e.type == p.MOUSEBUTTONDOWN:
                if gameOver!=True:
                    location = p.mouse.get_pos()#(x,y) location of mouse motion
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):# user clicked the same squre twice
                        sqSelected = ()# deselected
                        playerClicks = []#cler player click
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2: #after 2nd
                        move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]          
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                if e.key ==p.K_r :# reset
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks=[]
                    moveMade = False
                    animate = False 
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1] ,screen , gs.board , clock )
            validMoves = gs.getValidMoves()
            moveMade = False
            animate =False

        drawGameState(screen, gs,validMoves,sqSelected)

        if gs.checkMate :
            gameOver =True
            if gs.whiteToMove:
                drawText(screen,'Black Win by CheckMate')
            else :
                drawText(screen,'White  win by CheckMet')
        elif gs.staleMate:
            gameOver = True
            drawText(screen,'Check')

        clock.tick(MAX_FPS)
        p.display.flip()


def highlightsquares(screen,gs,validMoves,sqSelected):
    if sqSelected != ():
        r, c =sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s=p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha((100)) # transperancy value ->0, flags=0
            s.fill((21,15,187))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))
            s.fill((255,0,0))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawGameState(screen, gs,validMoves,sqSelected):
    drawBoard(screen)
    highlightsquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen, gs.board)



def drawBoard(screen):
    global colors
    colors = [(225,225,225),(125,125,125)]
    for c in range(DIMENSION):
        for r in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def animateMove(move,screen,board,clock):
    global color
    dR =move.endRow - move.startRow
    dC = move.endCol -move.startCol
    framesPerSquare = 10
    frameCount =(abs(dR)+abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r,c=(move.startRow + dR*frame/frameCount , move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        color = colors[(move.endRow + move.endCol)%2]
        endSquare =p.Rect(move.endCol*SQ_SIZE , move.endRow*SQ_SIZE ,SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen , color , endSquare)
        if move.pieceCaptured !="--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE,r*SQ_SIZE , SQ_SIZE ,SQ_SIZE))
        p.display.flip()
        clock.tick(60)



def drawText(screen,text):
    font = p.font.SysFont(" Times New Roman",28,True,False)
    textObject = font.render(text,0,(25,25,0))
    textLocation = p.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2 - textObject.get_width()/2 , HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject , textLocation)
    textObject = font.render(text , 0,(124,55,225))
    screen.blit(textObject,textLocation.move(2,2))




main()
    