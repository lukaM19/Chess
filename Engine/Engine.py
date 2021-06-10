import re
import random
import copy
import time

from pygame.mixer import get_num_channels
start_Fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#start_Fen="rnb1k2r/pp1pp1pp/1b2qp2/2p5/4P1n1/3PK2Q/PPP2PPP/RNB2BNR w kq - 0 1"
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
    wking=()
    bking=()
    for ind,row in enumerate(brd): 
        k = 0
        for index,i in enumerate(row):  
            if i.isdigit() :
                k = k+int(i)
            else:
                
                val = to_piece(i) 
                if val=="wK":
                    wking=(ind,k)
                if val == "bK":
                    bking=(ind,k)
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
    if len(st)>4:
        #Number of half moves made
        n_Hmove = int(st[4])
        #Number of fullmoves made
        n_Fmove = int(st[5])
    else:
        #Number of half moves made
        n_Hmove = 0
        #Number of fullmoves made
        n_Fmove = 0

    return board,to_Move,castling,en_Passant,n_Fmove,n_Hmove,(wking,bking)

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
    backup_en_passant=[]
    N2Piece={'bR':'r','bB':'b','bN':'n','bP':'p','bQ':'q','bK':'k','wR':'R','wB':'B','wN':'N','wP':'P','wQ':'Q','wK':'K'}
    
    def __init__(self,init_fen):
        self.log=[]
        if init_fen:
            self.board,self.to_Move,self.castling,self.en_Passant,self.n_Hmove,self.n_Fmove,self.king_pos = fen_2board(init_fen)
        else:
            self.board,self.to_Move,self.castling,self.en_Passant,self.n_Hmove,self.n_Fmove,self.king_pos = fen_2board(start_Fen)
        self.cK = False
        self.ck= False
        self.cQ= False
        self.cq = False
        self.en_Pc = 0
        self.move_N = 0
        self.enPcl =[]
        self.c=0
        self.cl_m=[]
        self.inCheck = False
        self.checks = []
        self.pins = []
        
        if "K" in self.castling:
            self.cK= True
        if "k" in self.castling:
            self.ck= True
        if "Q" in self.castling:
            self.cQ= True
        if "q" in self.castling:
            self.cq= True
            
    def ai_Make_Move(self):
        
        ai_move=""
        if(len(self.valid_Moves)==0 ):
                return "END"
        else:
            test=random.randint(0,len(self.valid_Moves)-1)
            t=self.valid_Moves[test]
            ai_move=Move(((int(t[2]),int(t[3])),(int(t[4]),int(t[5]))),self.board)
        
        
        return ai_move     
    #Make a move , save it in the log
    def make_Move(self,move):
        c_Func={"k":self.ck,"K":self.cK,"q":self.cq,"Q":self.cQ}
        self.move_N+=1
       
        self.backup_en_passant.append(self.en_Passant)
        self.en_Passant=""
        #if rook move disable corresponding castle
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
                if kq[0] == "K":
                     self.cK = False
                else:
                    self.ck = False
                self.cl_m.append(self.move_N)
            if kq[1] in self.castling and move.st_row == c_r and move.st_col == 0:
                self.castling= self.castling.replace(kq[1],"")
                if kq[1] == "Q":
                     self.cQ = False
                else:
                    self.cq = False
                self.cl_m.append(self.move_N)
        if move.piece_cap[1] == 'R':
            cr=move.end_row
            cc = move.end_col
            if move.piece_moved[0] == "b" and cr ==7 and (cc==7 or cc==0 ) :
                if self.cK and cc==7:
                    self.cK = False
                    self.castling= self.castling.replace("K","")
                if self.cQ and cc==0:
                    self.cQ = False
                    self.castling= self.castling.replace("Q","")
            if move.piece_moved[0] == "w" and cr ==0 and (cc==7 or cc==0 ) :
                if self.ck and cc==7:
                    self.ck = False
                    self.castling= self.castling.replace("k","")
                if self.cq and cc==0:
                    self.cq = False            
                    self.castling= self.castling.replace("q","")
            self.cl_m.append(self.move_N)
            
        #if King Move disable castle, or do castle move       
        if move.piece_moved[1] =='K':
            
            kq="KQ"
            rook="wR"
            row=7
            kpos= True
            if move.piece_moved[0] == 'b':
                kpos=False
                rook="bR"
                row=0
                kq=kq.lower()
                
            if kq[0] in self.castling and move.end_row== row and move.end_col==6 and self.board[move.st_row ][move.end_col+1] == rook: 
                self.board[move.st_row ][move.st_col]= "em"
                self.board[move.st_row ][move.end_col+1]= "em"
                self.board[move.end_row ][move.end_col-1]= rook
                self.board[move.end_row ][move.end_col]= move.piece_moved
                self.log.append(move)
            elif kq[1] in self.castling and move.end_row== row and move.end_col==2 and self.board[move.st_row ][move.end_col-2] == rook:
                self.board[move.st_row ][move.st_col]= "em"
                self.board[move.st_row ][move.end_col-2]= "em"
                self.board[move.end_row ][move.end_col+1]= rook
                self.board[move.end_row ][move.end_col]= move.piece_moved
                self.log.append(move)
            else:
                self.board[move.st_row ][move.st_col]= "em"
                self.board[move.end_row ][move.end_col]= move.piece_moved
                self.log.append(move)
            if kpos:
                self.king_pos=((move.end_row,move.end_col),self.king_pos[1] )
            else:
                self.king_pos=(self.king_pos[0],(move.end_row,move.end_col) )
            self.castling= self.castling.replace(kq[1],"")
            self.castling= self.castling.replace(kq[0],"")
            
            
        #do en passant moves
        elif  self.board[move.end_row ][move.end_col]=="em" and (move.piece_moved =='wP' and move.end_row==2 and self.board[move.end_row+1 ][move.end_col]== "bP") or(move.piece_moved == "bP" and move.end_row==5 and self.board[move.end_row-1 ][move.end_col]== "wP"): 
            
            if move.piece_moved == "wP" :
               
               self.board[move.st_row ][move.st_col]= "em"
               self.board[move.end_row ][move.end_col]= move.piece_moved
               self.board[move.end_row+1 ][move.end_col]="em"
               self.log.append(move) 
            if move.piece_moved == "bP" :
               self.board[move.st_row ][move.st_col]= "em"
               self.board[move.end_row ][move.end_col]= move.piece_moved
               self.board[move.end_row-1 ][move.end_col]="em"
               self.log.append(move) 
            self.en_Pc+=1
            
            self.enPcl .append(self.move_N)
        #Regular moves      
        else:
            self.board[move.st_row ][move.st_col]= "em"
            self.board[move.end_row ][move.end_col]= move.piece_moved
            self.log.append(move)
        #Record POSSIBLE en passants   
        if (move.piece_moved == "wP" and move.st_row == 6 and move.end_row==4) or (move.piece_moved == "bP" and move.st_row == 1 and move.end_row==3) :
            
            self.en_Passant+=(Move.Num2LETR[move.end_col+1]+str((8-move.end_row)))
        if self.to_Move == 'w':
            self.to_Move='b'
        else:
            self.to_Move='w'  
    #UNDO MOVES from the move log
    def undo_Move(self):
        self.c+=1
        c_Func={"k":self.ck,"K":self.cK,"q":self.cq,"Q":self.cQ}
        if len(self.log) != 0:
            move=self.log.pop()
            self.temp=move



            #UNDO CASTLING
            if move.piece_moved[1] == "K" and move.st_col == 4:
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
                    
                if move.end_col == 6:
                   castle= True 
                   k_e_c=6
                   r_e_c=5
                   r_s_c=7
                   stt=strs[0]
                if move.end_col == 2:
                   castle = True 
                   k_e_c=2
                   r_e_c=3
                   r_s_c=0
                   stt=strs[1]
                if  castle :
                        self.board[row][k_e_c]="em"
                        self.board[row][r_e_c]="em"
                        self.board[row][4]=k_col
                        self.board[row][r_s_c]=r_col
                        if strs[0] == "K":
                            if self.cK:
                                self.castling=strs[0]+self.castling
                            if self.cQ:
                                self.castling=strs[1]+self.castling     
                        else:
                            if  self.ck:
                                self.castling=strs[0]+self.castling
                            if self.cq:
                                self.castling=strs[1]+self.castling                            
                else:
                        
                        self.board[move.st_row ][move.st_col]=move.piece_moved
                        self.board[move.end_row ][move.end_col]=move.piece_cap
                        if strs[0] == "K":
                            if self.cK:
                                self.castling=strs[0]+self.castling
                            if self.cQ:
                                self.castling=strs[1]+self.castling     
                        else:
                            if  self.ck:
                                self.castling=strs[0]+self.castling
                            if self.cq:
                                self.castling=strs[1]+self.castling  
            #UNDO En-Passant
            if self.en_Pc>0 and self.move_N == self.enPcl[len(self.enPcl)-1]:
                st="w"
                k=-1
                if move.piece_moved[0]=='w':
                    st="b"
                    k=1
                
                self.board[move.st_row ][move.st_col]=move.piece_moved
                self.board[move.end_row ][move.end_col]=move.piece_cap
                self.board[move.end_row+k ][move.end_col]=st+"P"
                self.en_Pc+=-1
                self.enPcl.pop()
                #self.en_Passant+=(Move.Num2LETR[move.end_col+1]+str((8-move.end_row-k)))
            #UNDO REGULAR MOVES and  Pawn Promotion   
            else:
                self.board[move.st_row ][move.st_col]=move.piece_moved
                self.board[move.end_row ][move.end_col]=move.piece_cap
    #Special cases and maintnance           
            if ((move.st_row == 7 and move.st_col == 7) or (move.end_row == 7 and move.end_col == 7)) and "K" not in self.castling and not self.cK and self.move_N in self.cl_m:
                self.castling  = "K"+self.castling
                self.cK = True
                self.cl_m.pop()
            if ((move.st_row == 7 and move.st_col == 0) or (move.end_row == 7 and move.end_col == 0))  and "Q" not in self.castling and not self.cQ and self.move_N in self.cl_m:   
                self.castling  =self.castling+"Q" 
                self.cQ = True 
                self.cl_m.pop()
            if ((move.st_row == 0 and move.st_col == 7) or (move.end_row == 0 and move.end_col == 7)) and "k" not in self.castling and not self.ck and self.move_N in self.cl_m:
                self.castling  = "k"+self.castling
                self.ck = True
                self.cl_m.pop()
            if ((move.st_row == 0 and move.st_col == 0) or (move.end_row == 0 and move.end_col == 0)) and "q" not in self.castling and not self.cq and self.move_N in self.cl_m:   
                self.castling  =self.castling+"q"
                self.cq = True
                self.cl_m.pop()
            if move.piece_moved[1] == "K":
                if move.piece_moved[0] == "w":
                    self.king_pos=((move.st_row,move.st_col),self.king_pos[1] )
                else:
                    self.king_pos=(self.king_pos[0],(move.st_row,move.st_col) ) 
            
            self.en_Passant=self.backup_en_passant.pop()       
            
            if self.to_Move == 'w':
                self.to_Move='b'
            else:
                self.to_Move='w'
            self.move_N+=-1

#Get all POSSIBLE moves   
    def getAllMoves(self):
        self.moves=[]
       #print(self.to_Move)
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                
                temp=self.board[r][c]
                color=temp[0]
                piece=temp[1].lower()
                if color== self.to_Move:
                    if piece =='p':
                        self.moves=self.getPawnMoves(r,c,self.moves,temp)
                    if piece =='n':
                        self.moves=self.getKnightMoves(r,c,self.moves,temp)
                    if piece =='k':
                        self.moves=self.getKingMoves(r,c,self.moves,temp)
                    if piece =='q':
                        self.moves=self.getQueenMoves(r,c,self.moves,temp)
                    if piece =='b':
                        self.moves=self.getBishopMoves(r,c,self.moves,temp)
                    if piece =='r':
                        self.moves=self.getRookMoves(r,c,self.moves,temp)       
        #print(moves)
        return self.moves
    #INEFFICIENT AND BAD ALGO
    def getVaalidMoves(self):
        self.valid_Moves=[]
        moves=self.getAllMoves()
        sc=self.to_Move
        t=0
        t_b=GameState(self.Board2Fen())
        
        for m in moves:
            t+=1
            t_move= Move(((int(m[2]),int(m[3])),(int(m[4]),int(m[5]))),t_b.board)
            t_b.make_Move(t_move)
            
            op_moves= t_b.getAllMoves()
            
            k=0
            for p in op_moves:
                if t_b.board[int(p[4])][int(p[5])] == sc+"K":
                    
                    k+=1
                    break
            
            
            if k==0:
                self.valid_Moves.append(m)
            t_b.undo_Move()
            #self.undo_Move()
       
        self.c=0 
        return self.valid_Moves
    def getValidMoves(self):
        moves=self.getAllMoves()
        validmoves=[]
        self.inCheck,self.checks,self.pins=self.getCheckPin()
        print(self.inCheck,self.checks,self.pins)
        aCol='w'
        kp=0
        if self.to_Move=='b':
            aCol='b'
            kp=1
        if len(self.checks)>1:
            return self.getKingMoves(self.king_pos[kp][0],self.king_pos[kp][1],validmoves,aCol+"K")
        else:
            if not self.inCheck :
              for m in moves:
                    if (int(m[2]),int(m[3])) not in self.pins:
                        validmoves.append(m)
            else:
                if (int(m[2]),int(m[3])) not in self.pins and :
                        validmoves.append(m)  
        return validmoves
    def getCheckPin(self):
        inCheck= False
        pins=[]
        checks=[]
        aCol= self.to_Move
        eCol= 'b'
        kp=0
        if self.to_Move=='b':
            eCol='w'
            kp=1
        
        king=self.king_pos[kp]
        dir=[(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
        for j,d in enumerate(dir):
            ppin=()
            for i in range(1,8):
                r=king[0]+i*d[0]
                c=king[1]+i*d[1]
                if 0<=r and r<8 and c<8 and c>=0:
                    if self.board[r][c][0] == aCol:
                        if ppin==():
                            ppin=(r,c)#,d[0],d[1])
                        else:
                            break
                    elif self.board[r][c][0] == eCol: 
                        piece=self.board[r][c][1]
                        if (piece == "R" and  0<=j and j<4) or (piece=="B" and 4<=j and j<8 ) or (piece == "P" and( (self.board[r][c][0]=='w' and j == 4 or j== 7) or (self.board[r][c][0]=='b' and j == 5 or j== 6) ) ) or piece=='Q' or (piece=='K' and i==1):
                            if ppin == ():
                                inCheck = True
                                checks.append((r,c,d[0],d[1]))
                                break
                            else:
                                pins.append(ppin)
                                break
                        else:
                            break
            knightpos=[]
            knightpos= self.getKnightMoves(king[0],king[1],knightpos,aCol+"N")
            for k in knightpos:
                if self.board[int(k[4])][int(k[5])] == eCol+"N":
                   inCheck = True
                   checks.append(( int(k[4]),int(k[5]),int(k[4])-king[0],int(k[5])-king[1] ))      

        return inCheck,checks,pins

          
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
            if(self.board[r+k*2][c]=="em" and self.board[r+k][c]=="em"):
                move=Move(((r,c),(r+k*2,c)),self.board)
                movenot=Move.inNotation(move)
                moves.append(movenot)
                
        enp=[-1,1]
        inx=-1
        #EN PASSANT CHECK
        for i in enp:
            if same == 'b':
                inx=1
            if (c+i)<8 and (c+i)>=0 :
                
                if  (Move.Num2LETR[c+i+1]+str(8-r)) in self.en_Passant:
                   
                    move=Move(((r,c),(r+inx,c+i)),self.board)
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
    def getRookMoves(self,r,c,moves,piece):
        same=piece[0]
        startR = [r+1,r-1,c+1,c-1]
        edgeR = [8,-1,8,-1]
        incrR = [1,-1,1,-1]
        for i in range (4):
        #Vertical
            for row in range(startR[i],edgeR[i],incrR[i]):
                        change = self.board[row][c]
                        end=(row,c)
                        if i>1:
                            change = self.board[r][row]
                            end=(r,row)
                        if change =="em":
                            move=Move(((r,c),end),self.board)
                            movenot=Move.inNotation(move)
                            moves.append(movenot)
                        else:
                            if change[0] != same and change !="em":
                                move=Move(((r,c),end),self.board)
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
    def getQueenMoves(self,r,c,moves,piece):
        same=piece[0]
        moveQ=[]
        moves= self.getRookMoves(r,c,moves,piece)
        moves+= self.getBishopMoves(r,c,moveQ,piece)
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
    def Board2Fen(self):
        N2Piece={'bR':'r','bB':'b','bN':'n','bP':'p','bQ':'q','bK':'k','wR':'R','wB':'B','wN':'N','wP':'P','wQ':'Q','wK':'K'}
        FEN=""
        for r in range(len(self.board)):
            k=0
            for i,c in enumerate(range(len(self.board[r]))):
                if self.board[r][c] == "em":
                    
                    k+=1
                else:
                    if k != 0:
                      FEN+=str(k)
                      FEN+=N2Piece[self.board[r][c]]
                      k=0
                    else:
                     FEN+=N2Piece[self.board[r][c]]
            if i==7 and k!=0:
                FEN+=str(k)
            if r != 7:   
                FEN+="/"
        FEN+=" "
        FEN+=self.to_Move
        FEN+=" "
        if self.castling=="":
            FEN+="-"
        if self.castling != "-":
            FEN+=self.castling.replace("-","")
        FEN+=" "
        for v in self.en_Passant:
            FEN+=v.lower()
        if self.en_Passant == "":
            FEN+="-"
        FEN+=" "
        FEN+=str(self.n_Hmove)
        FEN+=" "
        FEN+=str(self.n_Fmove)
        return FEN+" "+str(self.cK) +str(self.ck)+str(self.cQ)+str(self.cq)    
#Temp test Methods
    def getPositions(self,depth):
        if depth == 0 :
            
            return 1
        movess=self.getValidMoves()
        positions=0
        for t in movess:
            
            move=Move(((int(t[2]),int(t[3])),(int(t[4]),int(t[5]))),self.board)
            
            self.make_Move(move)
            positions +=self.getPositions(depth-1)
            self.undo_Move()
            
        return positions 

gs= GameState(start_Fen)
depth=3
start=time.time()

test=gs.getPositions(depth)


end=time.time()
print(end-start)
print(test)
a,b,c=gs.getCheckPin()
print(a,b,c)
