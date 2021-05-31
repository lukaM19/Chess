import re
start_Fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
##test_fen="rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
##test_fen="rnb1kbnr/ppp1pppp/3qQ3/3p4/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 1"
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
#FEN notation to 2D board translator
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
    #turn to move
    to_Move = st[1]
    #Which castes are left
    castling = st[2]
    #Seperate list of possible en Passant Moves
    if len(st[3])>1:

        en_Passant = re.findall('..',st[3])
    else:
        en_Passant= st[3]
    #Number of half moves made
    n_Hmove = int(st[4])
    #Number of fullmoves made
    n_Fmove = int(st[5])

    return board,to_Move,castling,en_Passant,n_Fmove,n_Hmove

#Move class for making handling a move easier, also produces notations for the given moves 
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
        return self.piece_moved+str(self.st_row)+str(self.st_col)+str(self.end_row) +str(self.end_col)
    def inChessNotation(self):
        return self.N2Piece[self.piece_moved]+self.Num2LETR[self.end_col+1]+str(8-self.end_row) 
    def test(self):
        return self.piece_moved+self.Num2LETR[self.end_col+1]+str(8-self.end_row) 

#Main Class for the Game board making moves etc
class GameState():
    N2Piece={'bR':'r','bB':'b','bN':'n','bP':'p','bQ':'q','bK':'k','wR':'R','wB':'B','wN':'N','wP':'P','wQ':'Q','wK':'K'}
    
    def __init__(self,init_fen):
        self.log=[]
        if init_fen:
            self.board,self.to_Move,self.castling,self.en_Passant,self.n_Hmove,self.n_Fmove = fen_2board(init_fen)
        else:
            self.board,self.to_Move,self.castling,self.en_Passant,self.n_Hmove,self.n_Fmove = fen_2board(start_Fen)
            self.cK = False
            self.ck= False
            self.cQ= False
            self.cq = False
        if "K" in self.castling:
            self.cK= True
        if "k" in self.castling:
            self.ck= True
        if "Q" in self.castling:
            self.cQ= True
        if "q" in self.castling:
            self.cq= True
            
            
    #Make a move , save it in the log
    def make_Move(self,move):
        if move.piece_moved[1] =='R':
            kq=""
            c_r=0
            if move.piece_moved[0] == "w":
                kq="KQ"
                c_r=7
            else:
                kq="kq"
                c_r=0
            if kq[0] in self.castling and move.st_row == c_r and move.st_col == 7:
                self.castling= self.castling.replace(kq[0],"")
            if kq[1] in self.castling and move.st_row == c_r and move.st_col == 0:
                self.castling= self.castling.replace(kq[1],"")
                
        if move.piece_moved[1] =='K':
            
            kq="KQ"
            rook=""
            row=0
            if move.piece_moved[0] == 'w':
                
                rook="wR"
                row=7
                n_m='b'
            else:
                rook="bR"
                row=0
                kq=kq.lower()
                n_m='w'
            if kq[0] in self.castling and move.end_row== row and move.end_col==6: 
                self.board[move.st_row ][move.st_col]= "em"
                self.board[move.st_row ][move.end_col+1]= "em"
                self.board[move.end_row ][move.end_col-1]= rook
                self.board[move.end_row ][move.end_col]= move.piece_moved
                self.log.append(move)
            elif kq[1] in self.castling and move.end_row== row and move.end_col==2:
                self.board[move.st_row ][move.st_col]= "em"
                self.board[move.st_row ][move.end_col-2]= "em"
                self.board[move.end_row ][move.end_col+1]= rook
                self.board[move.end_row ][move.end_col]= move.piece_moved
                self.log.append(move)
            else:
                self.board[move.st_row ][move.st_col]= "em"
                self.board[move.end_row ][move.end_col]= move.piece_moved
                self.log.append(move)
            
            self.to_Move=n_m
            self.castling= self.castling.replace(kq[1],"")
            self.castling= self.castling.replace(kq[0],"")
            
            rook="bR"
            row=0
            n_m='w'
            
        else:
            self.board[move.st_row ][move.st_col]= "em"
            self.board[move.end_row ][move.end_col]= move.piece_moved
            self.log.append(move)
            if self.to_Move == 'w':
                self.to_Move='b'
            else:
                self.to_Move='w'
        
    #UNDO MOVES from the move log
    def undo_Move(self):
        if len(self.log) != 0:
            move=self.log.pop()
            #UNDO CASTLING
            if move.piece_moved[1] == "K":
                row=0
                strs=["K","Q"]
                k_col=""
                r_col=""
                castle= False
                if move.piece_moved[0] == "w":
                    row=7
                    strs=strs
                    k_col="wK"
                    r_col="wR"
                else:
                    row=0
                    strs[0]=strs[0].lower()
                    strs[1]=strs[1].lower()
                    k_col="bK"
                    r_col="bR"
                r_s_c=0
                r_e_c=0
                k_e_c=0
                stt=""
                    
                if move.st_col ==4 and move.end_col == 6:
                   castle= True 
                   k_e_c=6
                   r_e_c=5
                   r_s_c=7
                   stt=strs[0]
                if move.st_col ==4 and move.end_col == 2:
                   castle = True 
                   k_e_c=2
                   r_e_c=3
                   r_s_c=0
                   stt=strs[1]
                if  castle and move.st_col == 4:
                        self.board[row][k_e_c]="em"
                        self.board[row][r_e_c]="em"
                        self.board[row][4]=k_col
                        self.board[row][r_s_c]=r_col
                        self.castling=strs[0]+strs[1]+self.castling
                else:
                        self.board[move.st_row ][move.st_col]=move.piece_moved
                        self.board[move.end_row ][move.end_col]=move.piece_cap
                        if self.cK:
                            self.castling=strs[1]+self.castling
                        if self.cQ:
                            self.castling=strs[0]+self.castling
            #UNDO REGULAR MOVES    
            else:
                self.board[move.st_row ][move.st_col]=move.piece_moved
                self.board[move.end_row ][move.end_col]=move.piece_cap
            
            if move.st_row == 7 and move.st_col == 7 and move.piece_moved == "wR" and "K" not in self.castling and self.cK:
                self.castling  = "K"+self.castling
            if move.st_row == 7 and move.st_col == 0 and move.piece_moved == "wR" and "Q" not in self.castling and self.ck:   
                self.castling  =self.castling+"Q"  
            if move.st_row == 0 and move.st_col == 7 and move.piece_moved == "bR" and "k" not in self.castling and self.cQ:
                self.castling  = "k"+self.castling
            if move.st_row == 0 and move.st_col == 0 and move.piece_moved == "bR" and "q" not in self.castling and self.cq:   
                self.castling  =self.castling+"q"
            
                    
            if self.to_Move == 'w':
                self.to_Move='b'
            else:
                self.to_Move='w'
#Get all POSSIBLE moves   
    def getAllMoves(self):
        moves=[]
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
    
#These Genereate all POSSIBLE moves for respective pieces   
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
        #Castling
        if same == 'w' and r== 7 and c==4:
            if "K" in self.castling and self.board[r][c+1]=="em" and self.board[r][c+2]== "em":
              move=Move(((r,c),(r,c+2)),self.board)
              movenot=Move.inNotation(move)
              moves.append(movenot)  
            if "Q" in self.castling and self.board[r][c-1]=="em" and self.board[r][c-2]== "em" and self.board[r][c-3]== "em":
              move=Move(((r,c),(r,c-2)),self.board)
              movenot=Move.inNotation(move)
              moves.append(movenot)  
        if same == 'b' and r== 0 and c==4:
            if "k" in self.castling and self.board[r][c+1]=="em" and self.board[r][c+2]== "em":
              move=Move(((r,c),(r,c+2)),self.board)
              movenot=Move.inNotation(move)
              moves.append(movenot)  
            if "q" in self.castling and self.board[r][c-1]=="em" and self.board[r][c-2]== "em" and self.board[r][c-3]== "em":
              move=Move(((r,c),(r,c-2)),self.board)
              movenot=Move.inNotation(move)
              moves.append(movenot) 

        return moves
   #Have to "optimize the  if statements"
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
            else:
                if self.board[row][c][0] != same and self.board[row][c] !="em":
                    move=Move(((r,c),(row,c)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)

                break
        #VerticalUp
        for i,row in enumerate(range(r-1,-1,-1)):
            if self.board[row][c] =="em":
                move=Move(((r,c),(row,c)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                
            else:
                if self.board[row][c][0] != same and  self.board[row][c] !="em":
                    move=Move(((r,c),(row,c)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)
                
                break
        #HorizontalRight
        for i,col in enumerate(range(c+1,8)):
            if self.board[r][col] =="em":
                move=Move(((r,c),(r,col)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
            else:    
                if self.board[r][col][0] != same and self.board[r][col] !="em" :
                    move=Move(((r,c),(r,col)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)
                
                break
        #HorizontalLeft
        for i,col in enumerate(range(c-1,-1,-1)):
            if self.board[r][col] =="em":
                move=Move(((r,c),(r,col)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
            else:
                if self.board[r][col][0] != same and self.board[r][col] !="em":
                    move=Move(((r,c),(r,col)),self.board)
                    movenot=Move.inNotation(move)
                    moves.append(movenot)
                
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
                else:
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
                else:
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
                    
                else:
                    
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
               
                else:
                    if self.board[r+i][c+i][0] != same and self.board[r+i][c+i] !="em":
                        move=Move(((r,c),(r+i,c+i)),self.board)
                        movenot=Move.inNotation(move)
                        moves.append(movenot) 
                    break
        return moves

    def Board2Fen(self):
        N2Piece={'bR':'r','bB':'b','bN':'n','bP':'p','bQ':'q','bK':'k','wR':'R','wB':'B','wN':'N','wP':'P','wQ':'Q','wK':'K'}
        FEN=""
        for r in range(len(self.board)):
            k=0
            for c in range(len(self.board[r])):
                if self.board[r][c] == "em":
                    
                    k+=1
                else:
                    if k != 0:
                      FEN+=str(k)
                      FEN+=N2Piece[self.board[r][c]]
                      k=0
                    else:
                     FEN+=N2Piece[self.board[r][c]]
                if k==8:
                    FEN+=str(k)
            if k != 8:    
                FEN+="/"
        FEN+=" "
        FEN+=self.to_Move
        FEN+=" "
        FEN+=self.castling
        FEN+=" "
        for v in self.en_Passant:
            FEN+=v
        FEN+=" "
        FEN+=str(self.n_Hmove)
        FEN+=" "
        FEN+=str(self.n_Fmove)
        return FEN  

