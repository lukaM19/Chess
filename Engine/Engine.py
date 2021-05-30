import re
start_Fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
##test_fen="rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
test_fen="rnb1kbnr/ppp1pppp/3qQ3/3p4/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 1"
def to_piece(ch):
    return {
        'r':"bR",
        'n':"bN",
        'b':"bB",
        'q':"bQ",
        'k':"bK",
        'p':"bP",
        'R':"wR",
        'N':"wN",
        'B':"wB",
        'Q':"wQ",
        'K':"wK",
        'P':"wP",

    }.get(ch)

def fen_2board(fen):
    board =[ ["em"]*8 for i in range(8)]
    st = fen.split()
    brd= st[0].split("/")

    for ind,row in enumerate(brd): 
        k = 0
        for index,i in enumerate(row):  
            if i.isdigit() :
                k = k+int(i)
            else:
               
                val = to_piece(i) 
                board[ind][k] = val
                k += 1
    
    to_Move = st[1]
    castling = st[2]
    en_Passant = re.findall('..',st[3])
    n_Hmove = int(st[4])
    n_Fmove = int(st[5])

    ##for row in board:    
       ## print(row)
    return board,to_Move,castling,en_Passant,n_Fmove,n_Hmove
 
class Move():
    Num2LETR={1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H' }
    Piece2N={'r':'bR',
            'n':'bN',
            'b':'bB',
            'q':'bQ',
            'k':'bK',
            'p':'bP',
            'R':'wR',
            'N':'wN',
            'B':'wB',
            'Q':'wQ',
            'K':'wK',
            'P':'wP',

        }
    N2Piece={'bR':'r','bB':'b','bN':'n','bP':'p','bQ':'q','bK':'k','wR':'R','wB':'B','wN':'N','wP':'P','wQ':'Q','wK':'K'}

    def __init__(self,selected,board):
        self.st_row = selected[0][0]
        self.st_col = selected[0][1]
        self.end_row = selected[1][0]
        self.end_col = selected[1][1]
        self.piece_moved = board[self.st_row][self.st_col] 
        self.piece_cap = board[self.end_row][self.end_col]
    
    def inNotation(self):
        return self.piece_moved+self.Num2LETR[self.end_col+1]+str(8-self.end_row) 
    def inChessNotation(self):
        return self.N2Piece[self.piece_moved]+self.Num2LETR[self.end_col+1]+str(8-self.end_row) 
    def test(self):
        return self.piece_moved+self.Num2LETR[self.end_col+1]+str(8-self.end_row) 

class GameState():
    N2Piece={'bR':'r','bB':'b','bN':'n','bP':'p','bQ':'q','bK':'k','wR':'R','wB':'B','wN':'N','wP':'P','wQ':'Q','wK':'K'}
    def __init__(self,init_fen):
        self.log=[]
        if init_fen:
            self.board,self.to_Move,self.castling,self.en_Passant,self.n_Hmove,self.n_Fmove = fen_2board(init_fen)
        else:
            self.board,self.to_Move,self.castling,self.en_Passant,self.n_Hmove,self.n_Fmove = fen_2board(start_Fen)
    def make_Move(self,move):
            
        self.board[move.st_row ][move.st_col]= "em"
        self.board[move.end_row ][move.end_col]= move.piece_moved
        self.log.append(move)
        if self.to_Move == 'w':
            self.to_Move='b'
        else:
            self.to_Move='w'
    def undo_Move(self):
        if len(self.log) != 0:
            move=self.log[len(self.log)-1]
            self.board[move.st_row ][move.st_col]=move.piece_moved
            self.board[move.end_row ][move.end_col]=move.piece_cap
            self.log.pop()
        
        
            if self.to_Move == 'w':
                self.to_Move='b'
            else:
                self.to_Move='w'
    
    def getAllMoves(self):
        moves=[]
        rs=[6,1]
       #print(self.to_Move)
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                
                temp=self.board[r][c]
                color=temp[0]
                piece=temp[1].lower()
                if color== self.to_Move:
                    if piece =='p':
                        moves=self.getPawnMoves(r,c,moves,temp)
                    if piece =='n':
                        moves=self.getKnightMoves(r,c,moves,temp)
                    if piece =='k':
                        moves=self.getKingMoves(r,c,moves,temp)
                    if piece =='q':
                        moves=self.getQueenMoves(r,c,moves,temp)
                    if piece =='b':
                        moves=self.getBishopMoves(r,c,moves,temp)
                    if piece =='r':
                        moves=self.getRookMoves(r,c,moves,temp)       
        #print(moves)
        return moves
    
    
    def getPawnMoves(self,r,c,moves,piece):
        
        k=1
        same=piece[0]
        
        
        if same=='w':
             k=-1
        else:
             k=1
        
        for i in range(-1,2):
            
            if  (r+k*1)<=7 and (r+k*1)>=0 and (c+i)>=0 and (c+i)<=7:
                if i != 0:
                    if(self.board[r+k*1][c+i]!="em" and self.board[r+k*1][c+i][0] != same):
                        move=Move(((r,c),(r+k*1,c+i)),self.board)
                        movenot=Move.inNotation(move)
                        print(movenot)
                        moves.append(movenot)
                else:
                    if(self.board[r+k*1][c+i]=="em"):
                        move=Move(((r,c),(r+k*1,c+i)),self.board)
                        movenot=Move.inNotation(move)
                        
                        moves.append(movenot)
        if((r==1 and same=='b') or (r==6 and same=='w')):                
            if(self.board[r+k*2][c]=="em"):
                move=Move(((r,c),(r+k*2,c)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
        return moves
    def getKnightMoves(self,r,c,moves,piece):
        same=piece[0]
        possibilities=[(r+2,c+1),(r+2,c-1),(r-2,c+1),(r-2,c-1),(r-1,c+2),(r+1,c+2),(r+1,c-2),(r-1,c-2)]  
        pval=[p for p in possibilities if p[0]<=7 and p[1]<=7 and p[0]>=0 and p[1]>=0 ]
        for p in pval:
            if self.board[p[0]][p[1]]=="em" or self.board[p[0]][p[1]][0] != same:
              move=Move(((r,c),(p[0],p[1])),self.board)
              movenot=Move.inNotation(move)
              moves.append(movenot)  
        return moves
    def getKingMoves(self,r,c,moves,piece):
        same=piece[0]
        possibilities=[(r+1,c),(r+1,c+1),(r+1,c-1),(r,c-1),(r,c+1),(r-1,c+1),(r-1,c-1),(r-1,c)]
        pval=[p for p in possibilities if p[0]<=7 and p[1]<=7 and p[0]>=0 and p[1]>=0 ]
        for p in pval:
            if self.board[p[0]][p[1]]=="em" or self.board[p[0]][p[1]][0] != same:
              move=Move(((r,c),(p[0],p[1])),self.board)
              movenot=Move.inNotation(move)
              moves.append(movenot)  
        return moves
    def getQueenMoves(self,r,c,moves,piece):
        same=piece[0]
        
        #VerticalDown
        for i,row in enumerate(range(r+1,8)):
            if self.board[row][c] =="em":
               move=Move(((r,c),(row,c)),self.board)
               movenot=Move.inNotation(move)
               moves.append(movenot)
               v_max=i 
            if self.board[row][c][0] == same:
               break
            if self.board[row][c][0] != same and self.board[row][c] !="em":
               move=Move(((r,c),(row,c)),self.board)
               movenot=Move.inNotation(move)
               moves.append(movenot)
               v_max=i 
               break
        #VerticalUp
        for i,row in enumerate(range(r-1,-1,-1)):
            if self.board[row][c] =="em":
               move=Move(((r,c),(row,c)),self.board)
               movenot=Move.inNotation(move)
               moves.append(movenot)
               v_min=i 
            if self.board[row][c][0] == same:
               break
            if self.board[row][c][0] != same and  self.board[row][c] !="em":
               move=Move(((r,c),(row,c)),self.board)
               movenot=Move.inNotation(move)
               moves.append(movenot)
               v_min=i 
               break
        #HorizontalRight
        for i,col in enumerate(range(c+1,8)):
            if self.board[r][col] =="em":
               move=Move(((r,c),(r,col)),self.board)
               movenot=Move.inNotation(move)
               moves.append(movenot)
               v_min=i 
            if self.board[r][col][0] == same:
               break
            if self.board[r][col][0] != same and self.board[r][col] !="em" :
               move=Move(((r,c),(r,col)),self.board)
               movenot=Move.inNotation(move)
               moves.append(movenot)
               v_min=i 
               break
        #HorizontalLeft
        for i,col in enumerate(range(c-1,-1,-1)):
            if self.board[r][col] =="em":
               move=Move(((r,c),(r,col)),self.board)
               movenot=Move.inNotation(move)
               moves.append(movenot)
               h_max=i 
            if self.board[r][col][0] == same:
               break
            if self.board[r][col][0] != same and self.board[r][col] !="em":
               move=Move(((r,c),(r,col)),self.board)
               movenot=Move.inNotation(move)
               moves.append(movenot)
               h_min=i 
               break
        #Diagonal^->
        for i in range(1,8):
            if (r-i)>=0 and (c+i)<=7:
                if self.board[r-i][c+i] =="em":
                    move=Move(((r,c),(r-i,c+i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)
                if self.board[r-i][c+i][0] == same:
                    break
                if self.board[r-i][c+i][0] != same and self.board[r-i][c+i] !="em":
                    move=Move(((r,c),(r-i,c+i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)
                    break
        #Diagonal<-^
        for i in range(1,8):
            if (r-i)>=0 and (c-i)>=0:
                if self.board[r-i][c-i] =="em":
                    move=Move(((r,c),(r-i,c-i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                if self.board[r-i][c-i][0] == same:
                    break
                if self.board[r-i][c-i][0] != same and self.board[r-i][c-i] !="em":
                    move=Move(((r,c),(r-i,c-i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                    break
        #Diagonal<-v
        for i in range(1,8):
            if (r+i)<=7 and (c-i)>=0:
                if self.board[r+i][c-i] =="em":
                    move=Move(((r,c),(r+i,c-i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)
                    
                if self.board[r+i][c-i][0] == same:
                    break
                if self.board[r+i][c-i][0] != same and self.board[r+i][c-i] !="em":
                    
                    move=Move(((r,c),(r+i,c-i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                    
                    break
        #Diagonalv->
        for i in range(1,8):
            if (r+i)<=7 and (c+i)<=7:
                if self.board[r+i][c+i] =="em":
                    move=Move(((r,c),(r+i,c+i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                if self.board[r+i][c+i][0] == same:
                    break
                if self.board[r+i][c+i][0] != same and self.board[r+i][c+i] !="em":
                    move=Move(((r,c),(r+i,c+i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                    break
        return moves
    def getRookMoves(self,r,c,moves,piece):
        same=piece[0]
        #VerticalDown
        for i,row in enumerate(range(r+1,8)):
            if self.board[row][c] =="em":
                move=Move(((r,c),(row,c)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                v_max=i 
            if self.board[row][c][0] == same:
                break
            if self.board[row][c][0] != same and self.board[row][c] !="em":
                move=Move(((r,c),(row,c)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                v_max=i 
                break
        #VerticalUp
        for i,row in enumerate(range(r-1,-1,-1)):
            if self.board[row][c] =="em":
                move=Move(((r,c),(row,c)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                v_min=i 
            if self.board[row][c][0] == same:
                break
            if self.board[row][c][0] != same and  self.board[row][c] !="em":
                move=Move(((r,c),(row,c)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                v_min=i 
                break
        #HorizontalRight
        for i,col in enumerate(range(c+1,8)):
            if self.board[r][col] =="em":
                move=Move(((r,c),(r,col)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                v_min=i 
            if self.board[r][col][0] == same:
                break
            if self.board[r][col][0] != same and self.board[r][col] !="em" :
                move=Move(((r,c),(r,col)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                v_min=i 
                break
        #HorizontalLeft
        for i,col in enumerate(range(c-1,-1,-1)):
            if self.board[r][col] =="em":
                move=Move(((r,c),(r,col)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                h_max=i 
            if self.board[r][col][0] == same:
                break
            if self.board[r][col][0] != same and self.board[r][col] !="em":
                move=Move(((r,c),(r,col)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                h_min=i 
                break
        return moves
    def getBishopMoves(self,r,c,moves,piece):
        same=piece[0]
        #Diagonal^->
        for i in range(1,8):
            if (r-i)>=0 and (c+i)<=7:
                if self.board[r-i][c+i] =="em":
                    move=Move(((r,c),(r-i,c+i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)
                if self.board[r-i][c+i][0] == same:
                    break
                if self.board[r-i][c+i][0] != same and self.board[r-i][c+i] !="em":
                    move=Move(((r,c),(r-i,c+i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)
                    break
        #Diagonal<-^
        for i in range(1,8):
            if (r-i)>=0 and (c-i)>=0:
                if self.board[r-i][c-i] =="em":
                    move=Move(((r,c),(r-i,c-i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                if self.board[r-i][c-i][0] == same:
                    break
                if self.board[r-i][c-i][0] != same and self.board[r-i][c-i] !="em":
                    move=Move(((r,c),(r-i,c-i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                    break
        #Diagonal<-v
        for i in range(1,8):
            if (r+i)<=7 and (c-i)>=0:
                if self.board[r+i][c-i] =="em":
                    move=Move(((r,c),(r+i,c-i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)
                    
                if self.board[r+i][c-i][0] == same:
                    break
                if self.board[r+i][c-i][0] != same and self.board[r+i][c-i] !="em":
                    
                    move=Move(((r,c),(r+i,c-i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                    
                    break
        #Diagonalv->
        for i in range(1,8):
            if (r+i)<=7 and (c+i)<=7:
                if self.board[r+i][c+i] =="em":
                    move=Move(((r,c),(r+i,c+i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                if self.board[r+i][c+i][0] == same:
                    break
                if self.board[r+i][c+i][0] != same and self.board[r+i][c+i] !="em":
                    move=Move(((r,c),(r+i,c+i)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot) 
                    break
        return moves

       
