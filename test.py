# import AI,engine
# gsta= engine.GameState()
# # print(AI.evaluate(gsta))

print(-float('inf') < -999999999)


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
