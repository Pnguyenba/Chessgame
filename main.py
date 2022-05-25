from pickle import FALSE
import pygame, pygame_menu, sys, ctypes

from sympy import capture
from data.constants import *
import engine, AI

pygame.init()    
screen = pygame.display.set_mode((WIDTH , HEIGHT))
screen.fill(pygame.Color('white'))
pygame.display.set_caption('Chess Game')

IMAGES={}

def loadImages():
    pie=['bR','bN','bB','bQ','bK','bp','wp','wK','wQ','wB','wN','wR']
    for item in pie:
        IMAGES[item] = pygame.transform.scale(pygame.image.load('data/images/'+ item +'.png'), (PIE_SIZE,PIE_SIZE))

def drawGameState(screen, gsta,validMoves, sqSelected):
    drawBoard(screen)
    hightlightSq(screen, gsta, validMoves, sqSelected)
    drawPiece(screen,gsta.board)
    
def drawBoard(screen):
    global colors
    colors = [pygame.Color(WHITE), pygame.Color(GRAY)]
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            color = colors[( (row+col) % 2 )]
            pygame.draw.rect(screen, color, pygame.Rect(col * PIE_SIZE, row * PIE_SIZE, PIE_SIZE, PIE_SIZE))
            
def drawPiece(screen,board):
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            piece = board[row][col]
            if piece != '--':
                screen.blit(IMAGES[piece], pygame.Rect( col * PIE_SIZE, row * PIE_SIZE, PIE_SIZE, PIE_SIZE))

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def hightlightSq(screen, gsta, validMoves, sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if gsta.board[row][col][0] ==  ('w' if gsta.whiteMove else 'b'):
            #highlight ô đang chọn
            s = pygame.Surface((PIE_SIZE, PIE_SIZE))
            s.set_alpha(100)
            s.fill(pygame.Color('blue'))
            screen.blit(s, (col * PIE_SIZE, row * PIE_SIZE))
            #highlight những ô đi được
            s.fill(pygame.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol* PIE_SIZE, move.endRow * PIE_SIZE))

def soundMove(Capture):
    if not Capture:
        pygame.mixer.music.load('data/sound/Move.WAV')
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.load('data/sound/Capture.WAV')
        pygame.mixer.music.play()
   
def soundGameOver():
    pygame.mixer.music.load('data\sound\GameOver.wav')
    pygame.mixer.music.play()

def animateMove(move, screen, board, clock):
    global colors
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    famesPerSq = 20 if (move.endRow != move.startRow) and (move.endCol != move.startCol) else 10        
    fameCount = (abs(dR) - abs(dC)) * famesPerSq +1
    for fame in range(fameCount):
        row, col = (move.startRow + dR*fame/fameCount, move.startCol + dC*fame/fameCount)
        drawBoard(screen)
        drawPiece(screen, board)
        color = colors[(move.endRow - move.endCol) % 2]
        endSq = pygame.Rect(move.endCol * PIE_SIZE,move.endRow * PIE_SIZE, PIE_SIZE, PIE_SIZE)
        pygame.draw.rect(screen, color, endSq)

        if move.pieCaptured != '--':
            screen.blit(IMAGES[move.pieCaptured], endSq)

        screen.blit(IMAGES[move.pieMoved], pygame.Rect( col * PIE_SIZE, row * PIE_SIZE, PIE_SIZE, PIE_SIZE))
        pygame.display.flip()
        clock.tick(FPS)

def drawText(screen, text, ms_rs = False):
    font = pygame.font.SysFont('tahoma', 30, True, False)
    message = font.render(text, 0, pygame.Color(L_RED))
    messageLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - message.get_width()/2, HEIGHT/2 - message.get_height()/2)
    screen.blit(message, messageLocation)
    if ms_rs:
        msReset = font.render('Nhấn r để reset lại trò chơi!',0, pygame.Color(L_RED))
        msResetLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - msReset.get_width()/2, HEIGHT/2 + msReset.get_height()/2)
        screen.blit(msReset, msResetLocation)

def menuScreen(screen):
    menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', GameStart(screen))
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

def GameStart(screen):
    run = True
    clock = pygame.time.Clock()
    gsta = engine.GameState()
    validMoves = gsta.getValidMove()
    loadImages()

    animate = True
    pieSelected = ()
    playerClick = []
    moveMade = False
    gameOver = False
    captureMove = False
    playerFirst = True # chọn người đi đầu tiên


    while run:
        playerTurn = gsta.whiteMove
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # xử lí nhấp chuột
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not gameOver and playerTurn:
                    location = pygame.mouse.get_pos()
                    col = location[0]//PIE_SIZE
                    row = location[1]//PIE_SIZE
                    
                    # hủy khi double click tại 1 ô
                    if pieSelected == (row,col):
                        pieSelected = ()
                        playerClick = []
                    else:
                        pieSelected = (row,col)
                        playerClick.append(pieSelected)
                    if len(playerClick) == 2:
                        move = engine.Move(playerClick[0], playerClick[1],gsta.board)
                        for i in range(len(validMoves)):                   
                            if move == validMoves[i]:
                                gsta.makeMove(validMoves[i])
                                moveMade = True
                                if validMoves[i].pieCaptured != '--':
                                    captureMove = True
                                pieSelected = ()
                                playerClick = []
                        if not moveMade:
                            playerClick = [pieSelected]

            # xữ lí nhập từ phím
            elif event.type == pygame.KEYDOWN:
                # undo move (phím : Z )
                if event.key == pygame.K_z:
                    if playerTurn:                 
                        gsta.undoMove()
                        gsta.undoMove()
                        moveMade = True

                if event.key == pygame.K_r:
                    gsta = engine.GameState()
                    pieSelected = ()
                    playerClick = []
                    validMoves = gsta.getValidMove()
                    moveMade = False
                """
                if event.key == pygame.K_ESCAPE:
                    menuScreen(screen)"""
        
        if not gameOver and not playerTurn:
            BotMove, count = AI.findMovesNegaMax(gsta, validMoves) 
            if BotMove != None:
                gsta.makeMove(BotMove)
                print('count: ',count)
                moveMade = True 

        if moveMade:
            """if animate:
                animateMove(gsta.moveLog[-1], screen, gsta.board, clock)"""
            validMoves = gsta.getValidMove()
            soundMove(captureMove)
            if gsta.checkmate or gsta.stalemate:
                soundGameOver()
            captureMove = False
            moveMade = False

        drawGameState(screen,gsta, validMoves, pieSelected)

        if gsta.checkmate:
            gameOver = True
            if gsta.whiteMove:
                drawText(screen, 'Trắng bị chiếu chết !',gameOver)
            else:
                drawText(screen, 'Đen bị chiếu chết !',gameOver)
        elif gsta.stalemate:
            if gsta.whiteMove:
                drawText(screen, 'Đen hết nước đi !',gameOver)
            else:
                drawText(screen, 'Trắng hết nước đi !',gameOver)          
        elif gsta.inCheck():
            if gsta.whiteMove:
                drawText(screen, 'Trắng đang bị chiếu !!!')
            else:
                drawText(screen, 'Đen đang bị chiếu !!!')

        clock.tick(FPS)
        pygame.display.flip()



if __name__ == "__main__":
    GameStart(screen)
