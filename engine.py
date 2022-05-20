from data.constants import *


class GameState():
    def __init__(self):

        self.board =[
            #  a    b    c    d    e    f     g    h     
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],  #1
            ['bp','bp','bp','bp','bp','bp','bp','bp'],  #2
            ['--','--','--','--','--','--','--','--'],  #3
            ['--','--','--','--','--','--','--','--'],  #4
            ['--','--','--','--','--','--','--','--'],  #5
            ['--','--','--','--','--','--','--','--'],  #6
            ['wp','wp','wp','wp','wp','wp','wp','wp'],  #7
            ['wR','wN','wB','wQ','wK','wB','wN','wR']   #8
        ]
        self.whiteMove = True
        self.moveLog = []
        self.bKingLocation = (0,4)
        self.wKingLocation = (7,4)

        """
        self.inCheck = False #kiểm tra chiếu tướng
        self.pins = []
        self.checks = []
        """

        self.enpassantPossible = ()

        self.currentCastling = castles(True, True, True, True)
        self.castlesLog = [castles(True, True, True, True)]

        self.checkmate = False
        self.stalemate = False
        
        self.moveFunc = {'p': self.getPawnMoves,
                        'R': self.getRookMoves,
                        'N': self.getKnightMoves,
                        'B': self.getBishopMoves,
                        'Q': self.getQueenMoves,
                        'K': self.getKingMoves
        }



    def makeMove(self, move):       
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieMoved
        self.moveLog.append(move)
        self.whiteMove = not self.whiteMove

        #cập nhật vị trí vua trên bàn cờ
        if move.pieMoved == 'wK':
            self.wKingLocation = (move.endRow,move.endCol)
        elif move.pieMoved == 'bK':
            self.bKingLocation = (move.endRow,move.endCol)

        # phong cấp cho chốt
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieMoved[0] + 'Q'

        # bắt chốt qua đường
        """
        Nếu tốt đen nhảy 2 ô từ hàng 7 lên hàng 5 thì tốt trắng ở cột bên cạnh nhưng cùng hàng với tốt đen có thể ăn chéo theo cách mà nó ăn tốt đen nếu tốt đen tiến 1 ô.
        """
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = '--'

        # cập nhật biến self.enpassantPossible
        if move.pieMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        # nhập thành 
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  #nhập thành phía vua
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:# nhập thành phía hậu
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        # cập nhật bước nhập thành phải mỗi khi vua hoặc xe di chuyển
        self.updatecastles(move)
        self.castlesLog.append(castles(self.currentCastling.wks, self.currentCastling.wqs,
                                                self.currentCastling.bks, self.currentCastling.bqs))

        """
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        for count,log in enumerate(self.castlesLog):
            print(count, log.wks, log.wqs, log.bks, log.bqs,',')
        """

    
    """
    Điều kiện nhập thành
    1.  Quân vua chưa bao giờ bị di chuyển;
    2.  Quân xe tham gia vào nhập thành cũng chưa bao giờ bị di chuyển;
    3.  Không có quân nào nằm giữa vua và xe đó;
    4.   Các ô mà vua sẽ di chuyển qua không nằm dưới sự kiểm soát (ô hay đường nằm trong tầm chiếu) của quân đối phương, cũng như việc nhập thành không làm được khi bị chiếu.
    """


    def updatecastles(self, move):
        #kiểm tra vua và xe có di chuyển hay chưa
        if move.pieMoved == 'wK':
            self.currentCastling.wks = False
            self.currentCastling.wqs = False
        elif move.pieMoved == 'bK':
            self.currentCastling.bks = False
            self.currentCastling.bqs = False
        elif move.pieMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastling.wqs = False
                if move.startCol == 7:
                    self.currentCastling.wks = False
        elif move.pieMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastling.bqs = False
                if move.startCol == 7:
                    self.currentCastling.bks = False

        #kiểm tra xe có bị ăn hay chưa
        if move.pieCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastling.wqs = False
                elif move.endCol == 7:
                    self.currentCastling.wks = False
        elif move.pieCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastling.bqs = False
                elif move.endCol == 7:
                    self.currentCastling.bks = False

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieMoved
            self.board[move.endRow][move.endCol] = move.pieCaptured
            self.whiteMove = not self.whiteMove

            #update vị trí
            if move.pieMoved == 'wK':
                self.wKingLocation = (move.startRow,move.startCol)
            elif move.pieMoved == 'bK':
                self.bKingLocation = (move.startRow,move.startCol)

            #undo nước bắt chốt
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            #undo nước đi 2 ô của chốt
            if move.pieMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            #undo nước nhập thành
            self.castlesLog.pop() 
            #lấy lại giá trị cuối bản log cho currentCastling
            newRights = self.castlesLog[-1]
            self.currentCastling = castles(newRights.wks, newRights.wqs, newRights.bks, newRights.bqs)

            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
               
    def getValidMove(self):
        """moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndCheck()

        if self.whiteMove:
            kingRow = self.wKingLocation[0]
            kingCol = self.wKingLocation[1]
        else:
            kingRow = self.bKingLocation[0]
            kingCol = self.bKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: # chiếu 1 hướng
                moves = self.getAllValidMove()
                # kiểm tra quân cờ đang chiếu vua
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieChecking = self.board[checkRow][checkCol]
                validSqs = []# những ô hợp lệ có thể di chuyển

                # bị mã chiếu                 
                if pieChecking[1] == 'N':
                    validSqs = [(checkRow, checkCol)]
                else:  
                    for i in range(1,8):
                        validSq = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSqs.append(validSq)
                        if validSq[0] == checkRow and validSq[1] == checkCol:
                            break

                #
                for i in range(len(moves) - 1 , -1, -1):
                    if moves[i].pieMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSqs:
                            moves.remove(moves[i])
                
            else: # chiếu nhiều hướng vua phải di chuyển
                self.getKingMoves(kingRow, kingCol, moves)
        
        else:
            moves = self.getAllValidMove()
            if self.whiteMove:
                self.getCastleMoves(self.wKingLocation[0], self.wKingLocation[1], moves)
            else:
                self.getCastleMoves(self.bKingLocation[0], self.bKingLocation[1], moves)

        return moves"""

        tempEnpassantPossible = self.enpassantPossible

        tempCastling = castles(self.currentCastling.wks, self.currentCastling.wqs,
                                  self.currentCastling.bks, self.currentCastling.bqs)

        moves = self.getAllValidMove()

        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteMove = not self.whiteMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteMove = not self.whiteMove
            self.undoMove()


        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True       
        
        if self.whiteMove:
            self.getCastleMoves(self.wKingLocation[0],self.wKingLocation[1], moves)
        else:
            self.getCastleMoves(self.bKingLocation[0], self.bKingLocation[1], moves)

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastling = tempCastling

        return moves
        
    """def checkForPinsAndCheck(self):
        pins =[]
        checks = []
        inCheck = False
        if self.whiteMove:
            enemy = 'b'
            ally = 'w'
            startRow = self.wKingLocation[0]
            startCol = self.wKingLocation[1]
        else:
            enemy = 'w'
            ally = 'b'
            startRow = self.bKingLocation[0]
            startCol = self.bKingLocation[1]
        # kiểm tra theo hướng 
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPie = self.board[endRow][endCol]
                    if endPie[0] == ally:
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPie[0] == enemy:
                        type = endPie[1]
                        if  (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'p' and ((enemy == 'w' and 6 <= j <= 7) or (enemy == 'b' and 4 <= j <= 5 ))) or \
                            (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        # kiểm tra quân mã
        moves = ((1,-2), (-1,-2), (1,2), (-1,2), (2,-1), (2,1), (-2,-1), (-2,1))
        for m in moves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPie = self.board[endRow][endCol]
                if endPie[0] == enemy and endPie[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        
        return inCheck, pins, checks
        """

        
    def inCheck(self):
        if self.whiteMove:
            return self.sqUnderAttack(self.wKingLocation[0], self.wKingLocation[1])
        else:
            return self.sqUnderAttack(self.bKingLocation[0], self.bKingLocation[1])

    def sqUnderAttack(self, row, col):
        self.whiteMove = not self.whiteMove
        oopMoves = self.getAllValidMove()
        self.whiteMove = not self.whiteMove 

        for move in oopMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False
    

    def getAllValidMove(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.whiteMove) or (turn == 'b' and not self.whiteMove):
                    pie = self.board[row][col][1]
                    self.moveFunc[pie](row, col, moves)
        
        return moves

    def getPawnMoves(self, row, col, moves):
        """piePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3]) 
                self.pins.remove(self.pins[i])
                break
"""
        # chốt trắng
        if self.whiteMove:
            if self.board[row - 1][col] == '--': 
                moves.append(Move((row, col),(row - 1, col), self.board))       
                if row == 6 and self.board[row - 2][col] == '--':
                    moves.append(Move((row, col),(row - 2, col), self.board))
            # ăn trái 
            if col - 1 >= 0: 
                if self.board[row - 1][col - 1][0] == 'b':
                    moves.append(Move((row , col ), (row - 1, col - 1), self.board))
                elif (row - 1, col - 1) == self.enpassantPossible:  # bắt chốt qua đường
                    moves.append(Move((row , col ), (row - 1, col - 1), self.board, isEnPassantMove = True))
            # ăn phải
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif (row - 1, col + 1) == self.enpassantPossible:  # bắt chốt qua đường
                    moves.append(Move((row , col ), (row - 1, col + 1), self.board, isEnPassantMove = True))
        #chốt đen 
        else:
            if self.board[row + 1][col] == '--':
                moves.append(Move((row, col),(row + 1, col), self.board))       
                if row == 1 and self.board[row + 2][col] == '--':
                    moves.append(Move((row, col),(row + 2, col), self.board))

            # ăn trái
            if col - 1 >= 0: 
                if self.board[row + 1][col - 1][0] == 'w':
                    moves.append(Move((row , col ), (row +1, col -1), self.board))
                elif (row + 1, col - 1) == self.enpassantPossible:  # bắt chốt qua đường
                    moves.append(Move((row , col ), (row + 1, col - 1), self.board, isEnPassantMove = True))

            # ăn phải
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif (row + 1, col + 1) == self.enpassantPossible:  # bắt chốt qua đường
                    moves.append(Move((row , col ), (row + 1, col + 1), self.board, isEnPassantMove = True))

    def getRookMoves(self, row, col, moves):
        """piePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break"""

        directions = ((0,-1), (0,1), (-1,0), (1,0))
        enemy = 'b' if self.whiteMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPie = self.board[endRow][endCol]
                    if endPie == '--':
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPie[0] == enemy:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, row, col, moves):
        """piePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
"""
        directions = ((1,-2), (-1,-2), (1,2), (-1,2), (2,-1), (2,1), (-2,-1), (-2,1))
        ally = 'w' if self.whiteMove else 'b'
        for d in directions:
            endRow = row + d[0]
            endCol = col + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPie = self.board[endRow][endCol]
                if endPie[0] != ally:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    def getBishopMoves(self, row, col, moves): 
        """piePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break"""
        directions = ((-1,-1), (-1,1), (1,-1), (1,1))
        enemy = 'b' if self.whiteMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPie = self.board[endRow][endCol]
                    if endPie == '--':
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPie[0] == enemy:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
                
    def getQueenMoves(self, row, col, moves):
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        """directions = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))
        ally = 'w' if self.whiteMove else 'b'
        for d in directions:
            endRow = row + d[0]
            endCol = col + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPie = self.board[endRow][endCol]
                if endPie[0] != ally:
                    if ally == 'w':
                        self.wKingLocation = (endRow, endCol)
                    elif ally == 'b':
                        self.bKingLocation = (endRow, endCol)
                        

                    inCheck, pins, checks = self.checkForPinsAndCheck()
                    if not inCheck:
                        moves.append(Move((row, col), (endRow, endCol), self.board))

                    if ally == 'w':
                        self.wKingLocation = (row, col)
                    elif ally == 'b':
                        self.bKingLocation = (row, col)"""

        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally = 'w' if self.whiteMove else 'b'
        for i in range(8):
            endRow = row + directions[i][0]
            endCol = col + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPie = self.board[endRow][endCol]
                if endPie[0] != ally:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

        
    
    def getCastleMoves(self, row, col, moves):
        if self.sqUnderAttack(row, col):
            return
        if (self.whiteMove and self.currentCastling .wks) or (not self.whiteMove and self.currentCastling.bks):
            self.getKingsideCastleMoves(row, col, moves)
        if (self.whiteMove and self.currentCastling.wqs) or (not self.whiteMove and self.currentCastling.bqs):
            self.getQueensideCastleMoves(row, col, moves)

    def getKingsideCastleMoves(self, row, col, moves):
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            if not self.sqUnderAttack(row, col + 1) and not self.sqUnderAttack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, isCastleMove = True))

    def getQueensideCastleMoves(self, row, col, moves):
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            if not self.sqUnderAttack(row, col - 1) and not self.sqUnderAttack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, isCastleMove = True))

class castles():
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs


class Move():

    rankToRows  =   {'1': 7, '2': 6, '3': 5, '4': 4,
                     '5': 3, '6': 2, '7': 1, '8': 0}

    rowsToRanks =   {v: k for k, v in rankToRows.items()}

    filesToCols =   {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                     'e': 4, 'f': 5, 'g': 6, 'h': 7}

    colsToFiles =   {v: k for k, v in filesToCols.items()}
    
    def __init__(self, start, end, board, isEnPassantMove = False, isCastleMove = False):
        # lấy thông tin của quân cờ di chuyển
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.pieMoved = board[self.startRow][self.startCol] 
        self.pieCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

        #phong cấp
        self.isPawnPromotion = ((self.pieMoved == 'wp' and self.endRow == 0) or (self.pieMoved == 'bp' and self.endRow == 7))  
        
        #bắt chốt qua đường
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieCaptured = 'wp' if self.pieMoved == 'bp' else 'bp'

        #nhập thành 
        self.isCastleMove = isCastleMove

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    