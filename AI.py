import random
from data.constants import *

pieValues = {'K': 20000,
            'Q': 900,
            'R': 500,
            'B': 330,
            'N': 320,
            'p': 100 }

#bản dùng cho đối thủ là quân trắng (người)
bonusScore = {
    'p': [      
                [0,   0,  0,  0,  0,  0,  0,  0,],
                [5,  10, 10,-20,-20, 10, 10,  5,],
                [5,  -5,-10,  0,  0,-10, -5,  5,],
                [0,   0,  0, 20, 20,  0,  0,  0,],
                [5,   5, 10, 25, 25, 10,  5,  5,],
                [10, 10, 20, 30, 30, 20, 10, 10,],
                [50, 50, 50, 50, 50, 50, 50, 50,],
                [0,   0,  0,  0,  0,  0,  0,  0 ]
    ],

    'N':[   
            [-50,-40,-30,-30,-30,-30,-40,-50,],
            [-40,-20,  0,  5,  5,  0,-20,-40,],
            [-30,  5, 10, 15, 15, 10,  5,-30,],
            [-30,  0, 15, 20, 20, 15,  0,-30,],
            [-30,  5, 15, 20, 20, 15,  5,-30,],
            [-30,  0, 10, 15, 15, 10,  0,-30,],
            [-40,-20,  0,  0,  0,  0,-20,-40,],
            [-50,-40,-30,-30,-30,-30,-40,-50]     
    ],

            
    'B':[      
            [-20,-10,-10,-10,-10,-10,-10,-20,],
            [-10,  5,  0,  0,  0,  0,  5,-10,],
            [-10, 10, 10, 10, 10, 10, 10,-10,],
            [-10,  0, 10, 10, 10, 10,  0,-10,],
            [-10,  5,  5, 10, 10,  5,  5,-10,],
            [-10,  0,  5, 10, 10,  5,  0,-10,],
            [-10,  0,  0,  0,  0,  0,  0,-10,],
            [-20,-10,-10,-10,-10,-10,-10,-20]

    ],

    'R':[      
            [ 0,  0,  0,  5,  5,  0,  0,  0,],
            [-5,  0,  0,  0,  0,  0,  0, -5,],
            [-5,  0,  0,  0,  0,  0,  0, -5,],
            [-5,  0,  0,  0,  0,  0,  0, -5,],
            [-5,  0,  0,  0,  0,  0,  0, -5,],
            [-5,  0,  0,  0,  0,  0,  0, -5,],
            [ 5, 10, 10, 10, 10, 10, 10,  5,],
            [ 0,  0,  0,  0,  0,  0,  0,  0]
    ],

    'Q':[   
            [-20,-10,-10, -5, -5,-10,-10,-20,],
            [-10,  0,  5,  0,  0,  0,  0,-10,],
            [-10,  5,  5,  5,  5,  5,  0,-10,],
            [  0,  0,  5,  5,  5,  5,  0, -5,],
            [ -5,  0,  5,  5,  5,  5,  0, -5,],
            [-10,  0,  5,  5,  5,  5,  0,-10,],
            [-10,  0,  0,  0,  0,  0,  0,-10,],
            [-20,-10,-10, -5, -5,-10,-10,-20],
    ],

    'Kmid':[
            [ 20, 30, 10,  0,  0, 10, 30, 20,],
            [ 20, 20,  0,  0,  0,  0, 20, 20,],
            [-10,-20,-20,-20,-20,-20,-20,-10,],
            [-20,-30,-30,-40,-40,-30,-30,-20,],
            [-30,-40,-40,-50,-50,-40,-40,-30,],
            [-30,-40,-40,-50,-50,-40,-40,-30,],
            [-30,-40,-40,-50,-50,-40,-40,-30,],
            [-30,-40,-40,-50,-50,-40,-40,-30]
    ],

    'Kend':[
            [-50,-30,-30,-30,-30,-30,-30,-50,],
            [-30,-30,  0,  0,  0,  0,-30,-30,],
            [-30,-10, 20, 30, 30, 20,-10,-30,],
            [-30,-10, 30, 40, 40, 30,-10,-30,],
            [-30,-10, 30, 40, 40, 30,-10,-30,],
            [-30,-10, 20, 30, 30, 20,-10,-30,],
            [-30,-20,-10,  0,  0,-10,-20,-30,],
            [-50,-40,-30,-20,-20,-30,-40,-50]
    ]
}


def endGameCheck(gsta):
    if gsta.endGameCount <=0:
        return 'end'
    else:
        return 'mid'                

def getrandmmove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findMovesNegaMax(gsta, validMoves):
    global bestMove, count
    count = 0
    bestMove = None
    random.shuffle(validMoves)
    negaMax(gsta, validMoves, DEPTH, 1 if gsta.whiteMove else -1, -INF, INF)
    return bestMove, count



def negaMax(gsta, validMoves, depth, playerTurn, alpha, beta):
    global bestMove, count
    count +=1
    if depth == 0 :
        return playerTurn * evaluate(gsta)

    value = -INF
    for move in validMoves:
        gsta.makeMove(move)
        bestMoves = gsta.getValidMove()
        temp = -negaMax(gsta, bestMoves, depth -1, -playerTurn, -beta, -alpha )
        gsta.undoMove()

        if temp > value:
                value = temp
                if depth == DEPTH:
                    bestMove = move
        alpha = max(alpha, value)           
        if alpha >= beta:
            break

    return value

    


def evaluate(gsta): 
    if gsta.checkmate:
        if gsta.whiteMove:
            return -INF
        else:
            return INF
    elif gsta.stalemate:
        return 0

    board = gsta.board
    wMaterial = 0
    bMaterial = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            sq = board[row][col]
            if sq[0] == 'w':
                if sq[1] == 'K':
                    wMaterial += pieValues[sq[1]] + bonusScore[sq[1]+ endGameCheck(gsta)][row][col]
                else: 
                    wMaterial += pieValues[sq[1]] + bonusScore[sq[1]][row][col]
            if sq[0] == 'b':
                if sq[1] == 'K':
                    bMaterial += pieValues[sq[1]] + bonusScore[sq[1]+ endGameCheck(gsta)][row][col]
                else:
                    bMaterial += pieValues[sq[1]]  + bonusScore[sq[1]][row][col]

    return wMaterial - bMaterial