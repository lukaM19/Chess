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
    def __init__(self):
        self.board,to_Move,castling,en_Passant,n_Hmove,n_Fmove =fen_2board(start_Fen)

