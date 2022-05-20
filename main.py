import pygame, pygame_menu, sys
from data.constants import *
import engine

pygame.init()    
screen = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption('Chess Game')
gsta = engine.GameState()

IMAGES={}

def loadImages():
    pie=['bR','bN','bB','bQ','bK','bp','wp','wK','wQ','wB','wN','wR']
    for item in pie:
        IMAGES[item] = pygame.transform.scale(pygame.image.load('data/images/'+ item +'.png'), (PIE_SIZE,PIE_SIZE))

def drawGameState(screen, gsta):
    drawBoard(screen)
    drawPiece(screen,gsta.board)
    
def drawBoard(screen):
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
    loadImages()
    screen.fill(pygame.Color('white'))

    pieSelected = ()
    playerClick = []
    validMoves = gsta.getAllValidMove()
    moveMade = False

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            #
            if event.type == pygame.QUIT:
                run = False

            # xử lí nhấp chuột
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
                            pieSelected = ()
                            playerClick = []
                    if not moveMade:
                        playerClick = [pieSelected]

            # xữ lí nhập từ phím
            elif event.type == pygame.KEYDOWN:
                # undo move (phím : Z )
                if event.key == pygame.K_z:
                    gsta.undoMove()
                    moveMade = True
                """
                if event.key == pygame.K_ESCAPE:
                    menuScreen(screen)"""


        if moveMade:
            validMoves = gsta.getValidMove()
            moveMade = False

        drawGameState(screen,gsta)
        pygame.display.flip()


    pygame.quit()


if __name__ == "__main__":
    GameStart(screen)
