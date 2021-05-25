import numpy as np
start_Fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


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
    board = [ ["em"]*8 for i in range(8)]
    st = fen.split()
    brd= st[0].split("/")
    
    for ind,row in enumerate(brd): 
        k = 0
        for index,i in enumerate(row):  
            if i.isdigit() :
                k = k+int(i)
            else:
                print(index)
                val = to_piece(i) 
                board[ind][k] = val
                k += 1
    for row in board:    
        print(row)
        
  ##  print(st[0][0])

fen_2board(start_Fen)