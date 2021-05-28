import re
start_Fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
##test_fen="rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"

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
 
class GameState():
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
            pass
        
        
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
        return self.N2Piece[self.piece_moved]+self.Num2LETR[self.end_col+1]+str(8-self.end_row) 
    def test(self):
        return self.piece_moved+self.Num2LETR[self.end_col+1]+str(8-self.end_row) 