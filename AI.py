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


def findMovesNegaMax(gsta, validMoves):
    global bestMoveFound, count
    count = 0
    bestMove = None
    random.shuffle(validMoves)
    negaMax(gsta, validMoves, DEPTH, 1 if gsta.whiteMove else -1, -INF, INF)
    return bestMoveFound, count



def negaMax(gsta, validMoves, depth, playerTurn, alpha, beta):
    global bestMoveFound, count
    count +=1
    if depth == 0 :
        return playerTurn * evaluate(gsta)


    value = -INF
    for move in validMoves:
        gsta.makeMove(move)
        bestMoves = gsta.getAllValidMove()
        orderMoves(bestMoves,gsta)
        temp = -negaMax(gsta, bestMoves, depth -1, -playerTurn, -beta, -alpha )
        gsta.undoMove()

        if temp > value:
                value = temp
                if depth == DEPTH:
                    bestMoveFound = move
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
        return -INF

    board = gsta.board
    value = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            sq = board[row][col]
            if sq[0] == 'w':
                if sq[1] == 'K':
                    value += pieValues[sq[1]] + bonusScore[sq[1]+ endGameCheck(gsta)][row][col]
                else: 
                    value += pieValues[sq[1]] + bonusScore[sq[1]][row][col]
            if sq[0] == 'b':
                if sq[1] == 'K':
                    value -= pieValues[sq[1]] + bonusScore[sq[1]+ endGameCheck(gsta)][row][col]
                else:
                    value -= pieValues[sq[1]]  + bonusScore[sq[1]][row][col]

    return value

def orderMoves(moves, gsta):
    moveScoreList = []
    for move in moves:
        moveScore = 0
        pieMoved = move.pieMoved[1]
        pieCaptured = move.pieCaptured[1]

        if pieCaptured != '-':
            moveScore += 10 * pieValues[pieCaptured] - pieValues[pieMoved]
        
        if move.isPawnPromotion:
            moveScore += pieValues['Q']

        # if gsta.sqUnderAttack(move.endRow, move.endCol):
        #     moveScore -= pieValues[pieMoved]
        
        moveScoreList.append(moveScore)

    for i in range(len(moves) - 1):
        for j in range(i+1, 0, -1):
            swap = j - 1
            if moveScoreList[swap] < moveScoreList[j]:
                moveScoreList[swap], moveScoreList[j] = moveScoreList[j], moveScoreList[swap]
                moves[swap], moves[j] = moves[j], moves[swap]