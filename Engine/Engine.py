import re
import random
import copy
import time

start_Fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#start_Fen="r3k2r/Pppp1ppp/1b3nbN/nPP5/BB2P3/q4N2/Pp1P2PP/R2Q1RK1 b kq - 0 1"
# rnbq1bnr/pppp1ppp/8/6P1/3kp2R/8/PPPPPPBP/RNBQK1N1 w Q - 0 1
#start_Fen="rnbq1bnr/pppp1ppp/8/6P1/2k1p2R/2P5/PP1PPPBP/RNBQK1N1 w Q - 1 2"
points = {"wP": 100, "wN": 320, "wB": 330, "wR": 500, "wQ": 900, "bP": 100,
          "bN": 320, "bB": 330, "bR": 500, "bQ": 900, "wK": 0, "bK": 0, "em": 0}
#
wrook_Heatmap = [[0,  0,  0,  0,  0,  0,  0,  0],
                 [5, 10, 10, 10, 10, 10, 10,  5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [-5,  0,  0,  0,  0,  0,  0, -5],
                 [0,  0,  0,  5,  5,  0,  0,  0]]
brook_Heatmap = [[0, 0, 0, 5, 5, 0, 0, 0],
                 [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [-5, 0, 0, 0, 0, 0, 0, -5], [5, 10, 10, 10, 10, 10, 10, 5], [0, 0, 0, 0, 0, 0, 0, 0]]
queen_Heatmap = [[-20, -10, -10, -5, -5, -10, -10, -20],
                 [-10,  0,  0,  0,  0,  0,  0, -10],
                 [-10,  0,  5,  5,  5,  5,  0, -10],
                 [-5,  0,  5,  5,  5,  5,  0, -5],
                 [-5,  0,  5,  5,  5,  5,  0, -5],
                 [-10,  5,  5,  5,  5,  5,  0, -10],
                 [-10,  0,  5,  0,  0,  0,  0, -10],
                 [-20, -10, -10, -5, -5, -10, -10, -20]]
wking_Heatmap = [[-30, -40, -40, -50, -50, -40, -40, -30],
                 [-30, -40, -40, -50, -50, -40, -40, -30],
                 [-30, -40, -40, -50, -50, -40, -40, -30],
                 [-30, -40, -40, -50, -50, -40, -40, -30],
                 [-20, -30, -30, -40, -40, -30, -30, -20],
                 [-10, -20, -20, -20, -20, -20, -20, -10],
                 [20, 20,  0,  0,  0,  0, 20, 20],
                 [20, 30, 10,  0,  0, 10, 30, 20]]
bking_Heatmap = [
    [20, 30, 10, 0, 0, 10, 30, 20], [20, 20, 0, 0, 0, 0, 20, 20], [-10, -20, -20, -20, -20, -20, -20, -10], [-20, -30, -30, -40, -40, -30, -30, -20], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30], [-30, -40, -40, -50, -50, -40, -40, -30]]
wbishop_Heatmap = [[-20, -10, -10, -10, -10, -10, -10, -20],
                   [-10,  0,  0,  0,  0,  0,  0, -10],
                   [-10,  0,  5, 10, 10,  5,  0, -10],
                   [-10,  5,  5, 10, 10,  5,  5, -10],
                   [-10,  0, 10, 10, 10, 10,  0, -10],
                   [-10, 10, 10, 10, 10, 10, 10, -10],
                   [-10,  5,  0,  0,  0,  0,  5, -10],
                   [-20, -10, -10, -10, -10, -10, -10, -20]]
bbishop_Heatmap = [[-20, -10, -10, -10, -10, -10, -10, -20], [-10, 5, 0, 0, 0, 0, 5, -10], [-10, 10, 10, 10, 10, 10, 10, -10], [-10, 0,
                                                                                                                                10, 10, 10, 10, 0, -10], [-10, 5, 5, 10, 10, 5, 5, -10], [-10, 0, 5, 10, 10, 5, 0, -10], [-10, 0, 0, 0, 0, 0, 0, -10], [-20, -10, -10,
                                                                                                                                                                                                                                                        -10, -10, -10, -10, -20]]
wknight_Heatmap = [[-50, -40, -30, -30, -30, -30, -40, -50],
                   [-40, -20,  0,  0,  0,  0, -20, -40],
                   [-30,  0, 10, 15, 15, 10,  0, -30],
                   [-30,  5, 15, 20, 20, 15,  5, -30],
                   [-30,  0, 15, 20, 20, 15,  0, -30],
                   [-30,  5, 10, 15, 15, 10,  5, -30],
                   [-40, -20,  0,  5,  5,  0, -20, -40],
                   [-50, -40, -30, -30, -30, -30, -40, -50]]
bknight_Heatmap = [[-50, -40, -30, -30, -30, -30, -40, -50], [-40, -20, 0, 5, 5, 0, -20, -40], [-30, 5, 10, 15, 15, 10, 5, -30], [-30, 0, 15, 20, 20, 15, 0, -30], [-30, 5, 15, 20, 20, 15, 5, -30], [-30, 0, 10, 15, 15, 10, 0, -30], [-40, -20, 0, 0, 0, 0, -20, -40], [-50,
                                                                                                                                                                                                                                                                          -40, -30, -30, -30, -30, -40, -50]]
wpawn_Heatmap = [[0,  0,  0,  0,  0,  0,  0,  0],
                 [50, 50, 50, 50, 50, 50, 50, 50],
                 [10, 10, 20, 30, 30, 20, 10, 10],
                 [5,  5, 10, 25, 25, 10,  5,  5],
                 [0,  0,  0, 20, 20,  0,  0,  0],
                 [5, -5, -10,  0,  0, -10, -5,  5],
                 [5, 10, 10, -20, -20, 10, 10,  5],
                 [0,  0,  0,  0,  0,  0,  0,  0]]
bpawn_Heatmap = [
    [0, 0, 0, 0, 0, 0, 0, 0], [5, 10, 10, -20, -20, 10, 10, 5], [5, -5, -10, 0, 0, -10, -5, 5], [0, 0, 0, 20, 20, 0, 0, 0], [5, 5, 10, 25, 25, 10, 5, 5], [10, 10, 20, 30, 30, 20, 10, 10], [50, 50, 50, 50, 50, 50, 50, 50], [0, 0, 0, 0, 0, 0, 0, 0]]


def to_piece(ch):
    return {
        'r': "bR",
        'n': "bN",
        'b': "bB",
        'q': "bQ",
        'k': "bK",
        'p': "bP",
        'R': "wR",
        'N': "wN",
        'B': "wB",
        'Q': "wQ",
        'K': "wK",
        'P': "wP",

    }.get(ch)
# FEN notation to 2D board translator


def fen_2board(fen):
    board = [["em"]*8 for i in range(8)]
    st = fen.split()
    brd = st[0].split("/")
    wking = ()
    bking = ()
    for ind, row in enumerate(brd):
        k = 0
        for index, i in enumerate(row):
            if i.isdigit():
                k = k+int(i)
            else:

                val = to_piece(i)
                if val == "wK":
                    wking = (ind, k)
                if val == "bK":
                    bking = (ind, k)
                board[ind][k] = val
                k += 1
    # turn to move
    to_Move = st[1]
    # Which castes are left
    castling = st[2]
    # Seperate list of possible en Passant Moves
    if len(st[3]) > 1:

        en_Passant = re.findall('..', st[3])
    else:
        en_Passant = st[3]
    if len(st) > 4:
        # Number of half moves made
        n_Hmove = int(st[4])
        # Number of fullmoves made
        n_Fmove = int(st[5])
    else:
        # Number of half moves made
        n_Hmove = 0
        # Number of fullmoves made
        n_Fmove = 0

    return board, to_Move, castling, en_Passant, n_Fmove, n_Hmove, (wking, bking)

# Move class for making handling a move easier, also produces notations for the given moves


class Move():
    Num2LETR = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H'}
    Piece2N = {'r': 'bR',
               'n': 'bN',
               'b': 'bB',
               'q': 'bQ',
               'k': 'bK',
               'p': 'bP',
               'R': 'wR',
               'N': 'wN',
               'B': 'wB',
               'Q': 'wQ',
               'K': 'wK',
               'P': 'wP',

               }
    N2Piece = {'bR': 'r', 'bB': 'b', 'bN': 'n', 'bP': 'p', 'bQ': 'q', 'bK': 'k',
               'wR': 'R', 'wB': 'B', 'wN': 'N', 'wP': 'P', 'wQ': 'Q', 'wK': 'K'}

    def __init__(self, selected, board):
        self.st_row = selected[0][0]
        self.st_col = selected[0][1]
        self.end_row = selected[1][0]
        self.end_col = selected[1][1]
        self.piece_moved = board[self.st_row][self.st_col]
        self.piece_cap = board[self.end_row][self.end_col]

    def inNotation(self):
        return self.piece_moved+str(self.st_row)+str(self.st_col)+str(self.end_row) + str(self.end_col)

    def inChessNotation(self):
        return self.Num2LETR[self.st_col+1]+str(8-self.st_row)+self.Num2LETR[self.end_col+1]+str(8-self.end_row)

    def test(self):
        return self.piece_moved+self.Num2LETR[self.end_col+1]+str(8-self.end_row)

# Main Class for the Game board making moves etc


class GameState():
    backup_en_passant = []
    N2Piece = {'bR': 'r', 'bB': 'b', 'bN': 'n', 'bP': 'p', 'bQ': 'q', 'bK': 'k',
               'wR': 'R', 'wB': 'B', 'wN': 'N', 'wP': 'P', 'wQ': 'Q', 'wK': 'K'}

    def __init__(self, init_fen):
        self.log = []
        if init_fen:
            self.board, self.to_Move, self.castling, self.en_Passant, self.n_Hmove, self.n_Fmove, self.king_pos = fen_2board(
                init_fen)
        else:
            self.board, self.to_Move, self.castling, self.en_Passant, self.n_Hmove, self.n_Fmove, self.king_pos = fen_2board(
                start_Fen)
        self.cK = False
        self.ck = False
        self.cQ = False
        self.cq = False
        self.wkf = []
        self.bkf = []
        self.rookcap = []
        self.en_Pc = 0
        self.move_N = 0
        self.enPcl = []
        self.castlingfilter = ""
        self.king_move_n = (-1, -1)
        self.c = 0
        self.cl_m = []
        self.inCheck = False
        self.checks = []
        self.pins = []
        self.notKing = []

        self.win_Con = ""

        if "K" in self.castling:
            self.cK = True
        else:
            self.castlingfilter += "K"
        if "k" in self.castling:
            self.ck = True
        else:
            self.castlingfilter += "k"
        if "Q" in self.castling:
            self.cQ = True
        else:
            self.castlingfilter += "Q"
        if "q" in self.castling:
            self.cq = True
        else:
            self.castlingfilter += "q"

    def ai_Make_Move(self):

        ai_move = ""
        if(len(self.validmoves) == 0):
            return "END"
        else:
            test = random.randint(0, len(self.validmoves)-1)
            t = self.validmoves[test]
            ai_move = Move(
                ((int(t[2]), int(t[3])), (int(t[4]), int(t[5]))), self.board)

        return ai_move
    # Make a move , save it in the log

    def make_Move(self, moveSTR):
        move = Move(((int(moveSTR[2]), int(moveSTR[3])),
                    (int(moveSTR[4]), int(moveSTR[5]))), self.board)

        self.move_N += 1

        self.backup_en_passant.append(self.en_Passant)
        self.en_Passant = ""
        # if rook move disable corresponding castle
        if move.piece_moved[1] == 'R':
            kq = ""
            c_r = 0
            if move.piece_moved[0] == "w":
                kq = "KQ"
                c_r = 7
            else:
                kq = "kq"
                c_r = 0
            if kq[0] in self.castling and move.st_row == c_r and move.st_col == 7:
                self.castling = self.castling.replace(kq[0], "")
                self.castlingfilter += kq[0]
                self.cl_m.append(self.move_N)
            if kq[1] in self.castling and move.st_row == c_r and move.st_col == 0:
                self.castling = self.castling.replace(kq[1], "")
                self.castlingfilter += kq[1]
                self.cl_m.append(self.move_N)
        if move.piece_cap[1] == 'R':
            cr = move.end_row
            cc = move.end_col
            if move.piece_moved[0] == "b" and cr == 7 and (cc == 7 or cc == 0):
                if "K" in self.castling and cc == 7:
                    self.castling = self.castling.replace("K", "")
                    self.castlingfilter += "K"
                    self.rookcap.append(self.move_N)
                if "Q" in self.castling and cc == 0:
                    self.castlingfilter += "Q"
                    self.castling = self.castling.replace("Q", "")
                    self.rookcap.append(self.move_N)
            if move.piece_moved[0] == "w" and cr == 0 and (cc == 7 or cc == 0):
                if "k" in self.castling and cc == 7:
                    self.castling = self.castling.replace("k", "")
                    self.castlingfilter += "k"
                    self.rookcap.append(self.move_N)
                if "q" in self.castling and cc == 0:
                    self.castling = self.castling.replace("q", "")
                    self.castlingfilter += "q"
                    self.rookcap.append(self.move_N)

        # if King Move disable castle, or do castle move
        if move.piece_moved[1] == 'K':
            kq = "KQ"
            rook = "wR"
            row = 7
            kpos = True
            id = 0
            if move.piece_moved[0] == 'b':
                kpos = False
                rook = "bR"
                row = 0
                kq = kq.lower()
                id = 1
            if len(self.wkf) == 0 and kpos:
                self.wkf.append(self.move_N)
            if len(self.bkf) == 0 and not kpos:
                self.bkf.append(self.move_N)

            if kq[0] in self.castling and move.end_row == row and move.end_col == 6 and self.board[move.st_row][move.end_col+1] == rook:
                self.board[move.st_row][move.st_col] = "em"
                self.board[move.st_row][move.end_col+1] = "em"
                self.board[move.end_row][move.end_col-1] = rook
                self.board[move.end_row][move.end_col] = move.piece_moved
                self.log.append(move)
            elif kq[1] in self.castling and move.end_row == row and move.end_col == 2 and self.board[move.st_row][move.end_col-2] == rook:
                self.board[move.st_row][move.st_col] = "em"
                self.board[move.st_row][move.end_col-2] = "em"
                self.board[move.end_row][move.end_col+1] = rook
                self.board[move.end_row][move.end_col] = move.piece_moved
                self.log.append(move)
            else:
                self.board[move.st_row][move.st_col] = "em"
                self.board[move.end_row][move.end_col] = move.piece_moved
                self.log.append(move)
            if kpos:
                self.king_pos = ((move.end_row, move.end_col),
                                 self.king_pos[1])
            else:
                self.king_pos = (
                    self.king_pos[0], (move.end_row, move.end_col))
            self.castling = self.castling.replace(kq[1], "")
            self.castling = self.castling.replace(kq[0], "")

        # do en passant moves
        elif self.board[move.end_row][move.end_col] == "em" and (move.piece_moved == 'wP' and move.end_row == 2 and self.board[move.end_row+1][move.end_col] == "bP") or (move.piece_moved == "bP" and move.end_row == 5 and self.board[move.end_row-1][move.end_col] == "wP"):

            if move.piece_moved == "wP":

                self.board[move.st_row][move.st_col] = "em"
                self.board[move.end_row][move.end_col] = move.piece_moved
                self.board[move.end_row+1][move.end_col] = "em"
                self.log.append(move)
            if move.piece_moved == "bP":
                self.board[move.st_row][move.st_col] = "em"
                self.board[move.end_row][move.end_col] = move.piece_moved
                self.board[move.end_row-1][move.end_col] = "em"
                self.log.append(move)
            self.en_Pc += 1

            self.enPcl .append(self.move_N)
        # do pawn promotion moves
        elif len(moveSTR) == 7:
            self.board[move.st_row][move.st_col] = "em"
            self.board[move.end_row][move.end_col] = self.to_Move + \
                moveSTR[6].upper()
            self.log.append(move)
        # Regular moves
        else:

            self.board[move.st_row][move.st_col] = "em"
            self.board[move.end_row][move.end_col] = move.piece_moved
            self.log.append(move)
        # Record POSSIBLE en passants
        if (move.piece_moved == "wP" and move.st_row == 6 and move.end_row == 4) or (move.piece_moved == "bP" and move.st_row == 1 and move.end_row == 3):

            self.en_Passant += (Move.Num2LETR[move.end_col+1] +
                                str((8-move.end_row)))
        if self.to_Move == 'w':
            self.to_Move = 'b'
        else:
            self.to_Move = 'w'
    # UNDO MOVES from the move log

    def undo_Move(self):
        self.c += 1
        c_Func = {"k": self.ck, "K": self.cK, "q": self.cq, "Q": self.cQ}
        if len(self.log) != 0:
            move = self.log.pop()
            self.temp = move

            # UNDO CASTLING
            if move.piece_moved[1] == "K" and move.st_col == 4 and ((move.piece_moved[0] == "w" and self.wkf[0] == self.move_N) or (move.piece_moved[0] == "b" and self.bkf[0] == self.move_N)):
                row = 0
                strs = ["K", "Q"]
                k_col = ""
                r_col = ""
                castle = False
                if move.piece_moved[0] == "w":
                    row = 7
                    strs = strs
                    k_col = "wK"
                    r_col = "wR"
                    self.wkf.pop()
                else:
                    row = 0
                    strs[0] = strs[0].lower()
                    strs[1] = strs[1].lower()
                    k_col = "bK"
                    r_col = "bR"
                    self.bkf.pop()
                r_s_c = 0
                r_e_c = 0
                k_e_c = 0
                stt = ""

                if move.end_col == 6:
                    castle = True
                    k_e_c = 6
                    r_e_c = 5
                    r_s_c = 7
                    stt = strs[0]
                if move.end_col == 2:
                    castle = True
                    k_e_c = 2
                    r_e_c = 3
                    r_s_c = 0
                    stt = strs[1]
                if castle:
                    self.board[row][k_e_c] = "em"
                    self.board[row][r_e_c] = "em"
                    self.board[row][4] = k_col
                    self.board[row][r_s_c] = r_col
                    if strs[0] == "K":
                        if "K" not in self.castlingfilter:
                            self.castling = strs[0]+self.castling
                        if "Q" not in self.castlingfilter:
                            self.castling = strs[1]+self.castling
                    else:
                        if "k" not in self.castlingfilter:
                            self.castling = strs[0]+self.castling
                        if "q" not in self.castlingfilter:
                            self.castling = strs[1]+self.castling
                else:

                    self.board[move.st_row][move.st_col] = move.piece_moved
                    self.board[move.end_row][move.end_col] = move.piece_cap
                    if move.piece_moved[0] == "w":
                        if "K" not in self.castlingfilter:
                            self.castling = strs[0]+self.castling
                        if "Q" not in self.castlingfilter:
                            self.castling = strs[1]+self.castling
                    else:  # move.piece_moved[0] == "b" :
                        if "k" not in self.castlingfilter:
                            self.castling = strs[0]+self.castling
                        if "q" not in self.castlingfilter:
                            self.castling = strs[1]+self.castling

            # UNDO En-Passant
            if self.en_Pc > 0 and self.move_N == self.enPcl[len(self.enPcl)-1]:
                st = "w"
                k = -1
                if move.piece_moved[0] == 'w':
                    st = "b"
                    k = 1

                self.board[move.st_row][move.st_col] = move.piece_moved
                self.board[move.end_row][move.end_col] = move.piece_cap
                self.board[move.end_row+k][move.end_col] = st+"P"
                self.en_Pc += -1
                self.enPcl.pop()
                # self.en_Passant+=(Move.Num2LETR[move.end_col+1]+str((8-move.end_row-k)))
            # UNDO REGULAR MOVES and  Pawn Promotion
            else:
                self.board[move.st_row][move.st_col] = move.piece_moved
                self.board[move.end_row][move.end_col] = move.piece_cap
    # Special cases and maintnance
            if (move.st_row == 7 and move.st_col == 7) and self.cK and self.move_N in self.cl_m:
                self.castling = "K"+self.castling
                self.castlingfilter = self.castlingfilter.replace("K", "")
                self.cl_m.pop()
            if (move.st_row == 7 and move.st_col == 0) and self.cQ and self.move_N in self.cl_m:
                self.castling = self.castling+"Q"
                self.castlingfilter = self.castlingfilter.replace("Q", "")
                self.cl_m.pop()
            if (move.st_row == 0 and move.st_col == 7) and self.ck and self.move_N in self.cl_m:
                self.castling = "k"+self.castling
                self.castlingfilter = self.castlingfilter.replace("k", "")
                self.cl_m.pop()
            if (move.st_row == 0 and move.st_col == 0) and self.cq and self.move_N in self.cl_m:
                self.castling = self.castling+"q"
                self.castlingfilter = self.castlingfilter.replace("q", "")
                self.cl_m.pop()
    # Rook capture redo enable castle

            if (move.end_row == 7 and move.end_col == 7) and self.cK and self.move_N in self.rookcap:
                self.castling = "K"+self.castling
                self.castlingfilter = self.castlingfilter.replace("K", "")
                self.rookcap.pop()
            if (move.end_row == 7 and move.end_col == 0) and self.cQ and self.move_N in self.rookcap:
                self.castling = self.castling+"Q"
                self.castlingfilter = self.castlingfilter.replace("Q", "")
                self.rookcap.pop()
            if (move.end_row == 0 and move.end_col == 7) and self.ck and self.move_N in self.rookcap:
                self.castlingfilter = self.castlingfilter.replace("k", "")
                self.castling = "k"+self.castling
                self.rookcap.pop()
            if (move.end_row == 0 and move.end_col == 0) and self.cq and self.move_N in self.rookcap:
                self.castling = self.castling+"q"
                self.castlingfilter = self.castlingfilter.replace("q", "")
                self.rookcap.pop()
    #
            if move.piece_moved[1] == "K":
                if move.piece_moved[0] == "w":
                    self.king_pos = (
                        (move.st_row, move.st_col), self.king_pos[1])
                else:
                    self.king_pos = (
                        self.king_pos[0], (move.st_row, move.st_col))

            self.en_Passant = self.backup_en_passant.pop()

            if self.to_Move == 'w':
                self.to_Move = 'b'
            else:
                self.to_Move = 'w'
            self.move_N += -1

# Get all POSSIBLE moves
    def getAllMoves(self):
        self.moves = []
       # print(self.to_Move)
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):

                temp = self.board[r][c]
                color = temp[0]
                piece = temp[1].lower()
                if color == self.to_Move:
                    if piece == 'k':
                        self.moves = self.getKingMoves(r, c, self.moves, temp)
                    if piece == 'p':
                        self.moves = self.getPawnMoves(r, c, self.moves, temp)
                    if piece == 'n':
                        self.moves = self.getKnightMoves(
                            r, c, self.moves, temp)
                    if piece == 'q':
                        self.moves = self.getQueenMoves(r, c, self.moves, temp)
                    if piece == 'b':
                        self.moves = self.getBishopMoves(
                            r, c, self.moves, temp)
                    if piece == 'r':
                        self.moves = self.getRookMoves(r, c, self.moves, temp)
        # print(self.moves,"PAWNED")
        return self.moves

# GOOD ALGO
    def getValidMoves(self):
        moves = self.getAllMoves()
        self.validmoves = []
        available = []
        pin_dir = []
        self.whP = []
        pd = ""

        self.inCheck, self.checks, self.pins, available, pin_dir, self.whP = self.get_Checks_Pins()
        # print(self.inCheck,self.checks,self.pins,self.whP)
        aCol = 'w'
        kp = 0
        if self.to_Move == 'b':
            aCol = 'b'
            kp = 1
        if len(set(self.checks)) > 1:
            mvs = self.getKingMoves(
                self.king_pos[kp][0], self.king_pos[kp][1], self.validmoves, aCol+"K")
            m = []
            # for v in mvs:
            # if (int(v[4]), int(v[5])) not in self.notKing and (int(v[4]), int(v[5])) not in sec_p :
            # m.append(v)
            return mvs
        else:
            if not self.inCheck:
                for m in moves:

                    if (int(m[2]), int(m[3])) not in self.pins:
                        self.validmoves.append(m)
                    else:
                        if int(m[2]) == self.king_pos[kp][0]:
                            pd = "h"
                        elif int(m[3]) == self.king_pos[kp][1]:
                            pd = "v"
                        else:
                            pd = "d"
                        pin = ""
                        if int(m[4]) == self.king_pos[kp][0]:
                            pin = "h"
                        elif int(m[5]) == self.king_pos[kp][1]:
                            pin = "v"
                        else:
                            pin = "d"
                        if ((int(m[4]), int(m[5])) in pin_dir and pd == pin) or self.whP[self.pins.index((int(m[2]), int(m[3])))] == (int(m[4]), int(m[5])):

                            self.validmoves.append(m)

            else:
                enpd = -1
                if aCol == "b":
                    enpd = 1
                for m in moves:
                    # Use all king moves
                    if m[1] == "K":
                        self.validmoves.append(m)
                    # All move by pieces which are not pinned  and block/kill the attacking piece(stored in available)
                    elif (int(m[2]), int(m[3])) not in self.pins:

                        for index, a in enumerate(available):
                            if a == (int(m[4]), int(m[5])) and m[1] != "K":

                                self.validmoves.append(m)
                    # En passant to kill checking pawn
                    if ((int(m[4])-enpd, int(m[5])) in self.checks) and ((Move.Num2LETR[int(m[5])+1]+str((8-int(m[4]) + enpd))) in self.en_Passant) and m[1] == "P":
                        self.validmoves.append(m)

        return self.validmoves

    def get_Checks_Pins(self):
        inCheck = False
        pins = []
        checks = []
        pind = []
        aCol = self.to_Move
        eCol = 'b'
        kp = 0
        if self.to_Move == 'b':
            eCol = 'w'
            kp = 1

        king = self.king_pos[kp]

        dir = [(0, 1), (0, -1), (1, 0), (-1, 0),
               (1, 1), (-1, -1), (1, -1), (-1, 1)]
        avals = []
        wpin = []
        notKing = []
        for j, d in enumerate(dir):
            ppin = ()
            tmp = []

            for i in range(1, 8):
                r = king[0]+i*d[0]
                c = king[1]+i*d[1]

                if 0 <= r and r < 8 and c < 8 and c >= 0:
                    if self.board[r][c][0] == aCol and self.board[r][c][1] != "K":
                        if ppin == ():
                            ppin = (r, c)  # ,d[0],d[1])

                        else:
                            break
                    elif self.board[r][c] == "em":
                        tmp.append((r, c))

                    elif self.board[r][c][0] == eCol:
                        piece = self.board[r][c][1]
                        if (piece == "R" and 0 <= j and j < 4) or (piece == "B" and 4 <= j and j < 8) or (piece == "P" and i == 1 and ((eCol == 'w' and (j == 4 or j == 6)) or (eCol == 'b' and (j == 5 or j == 7)))) or piece == 'Q' or (piece == 'K' and i == 1):
                            if ppin == ():

                                inCheck = True
                                checks.append((r, c))

                                tmp.append((r, c))
                                avals += tmp

                                break

                            else:
                                pins.append(ppin)  # ,(r,c))
                                wpin.append((r, c))
                                pind += tmp
                                break
                        else:
                            break
        knightpos = []
        knightpos = self.getKnightMoves(king[0], king[1], knightpos, aCol+"N")
        for k in knightpos:
            if self.board[int(k[4])][int(k[5])] == eCol+"N":
                inCheck = True
                checks.append((int(k[4]), int(k[5]), int(
                    k[4])-king[0], int(k[5])-king[1]))
                avals.append((int(k[4]), int(k[5])))

        return inCheck, checks, pins, avals, pind, wpin

    def getCheck(self):
        inCheck = False
        pins = []
        checks = []
        sec_Pins = []
        aCol = self.to_Move
        eCol = 'b'
        kp = 0
        if aCol == 'b':
            eCol = 'w'
            kp = 1

        king = self.king_pos[kp]

        dir = [(0, 1), (0, -1), (1, 0), (-1, 0),
               (1, 1), (-1, -1), (1, -1), (-1, 1)]
        notKing = []
        for j, d in enumerate(dir):
            ppin = ()
            tmp = []

            for i in range(1, 8):
                r = king[0]+i*d[0]
                c = king[1]+i*d[1]

                if 0 <= r and r < 8 and c < 8 and c >= 0:
                    if self.board[r][c][0] == aCol and self.board[r][c][1] != "K":
                        if ppin == ():
                            ppin = (r, c)  # ,d[0],d[1])

                        else:
                            break
                    elif self.board[r][c][0] == eCol:
                        piece = self.board[r][c][1]
                        if (piece == "R" and 0 <= j and j < 4) or piece == 'Q' or (piece == "B" and 4 <= j and j < 8) or (piece == "P" and i == 1 and ((self.board[r][c][0] == 'w' and (j == 4 or j == 6)) or (self.board[r][c][0] == 'b' and (j == 5 or j == 7)))) or (piece == 'K' and i == 1):
                            if ppin == ():
                                inCheck = True
                                checks.append((r, c, d[0], d[1]))
                                break

                            else:
                                pins.append(ppin)  # ,(r,c))
                                break
                        else:
                            break
        knightpos = []
        knightpos = self.getKnightMoves(king[0], king[1], knightpos, aCol+"N")
        for k in knightpos:
            if self.board[int(k[4])][int(k[5])] == eCol+"N":
                inCheck = True
                checks.append((int(k[4]), int(k[5]), int(
                    k[4])-king[0], int(k[5])-king[1]))

        return inCheck

# These Genereate all POSSIBLE moves for respective pieces
    def getPawnMoves(self, r, c, moves, piece):

        k = 1
        same = piece[0]

        if same == 'w':
            k = -1
        else:
            k = 1

        for i in range(-1, 2):

            if (r+k*1) <= 7 and (r+k*1) >= 0 and (c+i) >= 0 and (c+i) <= 7:
                prom = "QNRB"
                if r+k*1 == 7:
                    prom = prom.lower()
                if i != 0:
                    if(self.board[r+k*1][c+i] != "em" and self.board[r+k*1][c+i][0] != same):
                        move = Move(((r, c), (r+k*1, c+i)), self.board)
                        movenot = Move.inNotation(move)

                        if r+k*1 == 0 or r+k*1 == 7:
                            moves.append(movenot+prom[0])
                            moves.append(movenot+prom[1])
                            moves.append(movenot+prom[2])
                            moves.append(movenot+prom[3])
                        else:
                            moves.append(movenot)
                else:
                    if(self.board[r+k*1][c+i] == "em"):
                        move = Move(((r, c), (r+k*1, c+i)), self.board)
                        movenot = Move.inNotation(move)
                        if r+k*1 == 0 or r+k*1 == 7:
                            moves.append(movenot+prom[0])
                            moves.append(movenot+prom[1])
                            moves.append(movenot+prom[2])
                            moves.append(movenot+prom[3])
                        else:
                            moves.append(movenot)
        if((r == 1 and same == 'b') or (r == 6 and same == 'w')):
            if(self.board[r+k*2][c] == "em" and self.board[r+k][c] == "em"):
                move = Move(((r, c), (r+k*2, c)), self.board)
                movenot = Move.inNotation(move)
                moves.append(movenot)

        enp = [-1, 1]
        inx = -1
        # EN PASSANT CHECK
        for i in enp:
            if same == 'b':
                inx = 1
            if (c+i) < 8 and (c+i) >= 0:

                if (Move.Num2LETR[c+i+1]+str(8-r)) in self.en_Passant:

                    move = Move(((r, c), (r+inx, c+i)), self.board)
                    movn = move.inNotation()
                    self.make_Move(movn)
                    if self.to_Move == 'w':
                        self.to_Move = 'b'
                    else:
                        self.to_Move = "w"
                    if not self.getCheck():

                        movenot = move.inNotation()
                        moves.append(movenot)
                    if self.to_Move == 'w':
                        self.to_Move = 'b'
                    else:
                        self.to_Move = "w"
                    self.undo_Move()

        return moves

    def getKnightMoves(self, r, c, moves, piece):
        same = piece[0]
        possibilities = [(r+2, c+1), (r+2, c-1), (r-2, c+1), (r-2, c-1),
                         (r-1, c+2), (r+1, c+2), (r+1, c-2), (r-1, c-2)]
        pval = [p for p in possibilities if p[0] <=
                7 and p[1] <= 7 and p[0] >= 0 and p[1] >= 0]
        for p in pval:
            if self.board[p[0]][p[1]] == "em" or self.board[p[0]][p[1]][0] != same:
                move = Move(((r, c), (p[0], p[1])), self.board)
                movenot = Move.inNotation(move)
                moves.append(movenot)
        return moves

    def getRookMoves(self, r, c, moves, piece):
        same = piece[0]
        startR = [r+1, r-1, c+1, c-1]
        edgeR = [8, -1, 8, -1]
        incrR = [1, -1, 1, -1]
        for i in range(4):
            # Vertical
            for row in range(startR[i], edgeR[i], incrR[i]):
                change = self.board[row][c]
                end = (row, c)
                if i > 1:
                    change = self.board[r][row]
                    end = (r, row)
                if change == "em":
                    move = Move(((r, c), end), self.board)
                    movenot = Move.inNotation(move)
                    moves.append(movenot)
                else:
                    if change[0] != same and change != "em":
                        move = Move(((r, c), end), self.board)
                        movenot = Move.inNotation(move)
                        moves.append(movenot)

                    break

        return moves

    def getBishopMoves(self, r, c, moves, piece):
        same = piece[0]
        # Diagonal^->
        for i in range(1, 8):
            if (r-i) >= 0 and (c+i) <= 7:
                if self.board[r-i][c+i] == "em":
                    move = Move(((r, c), (r-i, c+i)), self.board)
                    movenot = Move.inNotation(move)
                    moves.append(movenot)
                else:
                    if self.board[r-i][c+i][0] != same and self.board[r-i][c+i] != "em":
                        move = Move(((r, c), (r-i, c+i)), self.board)
                        movenot = Move.inNotation(move)
                        moves.append(movenot)
                    break
        # Diagonal<-^
        for i in range(1, 8):
            if (r-i) >= 0 and (c-i) >= 0:
                if self.board[r-i][c-i] == "em":
                    move = Move(((r, c), (r-i, c-i)), self.board)
                    movenot = Move.inNotation(move)
                    moves.append(movenot)
                else:
                    if self.board[r-i][c-i][0] != same and self.board[r-i][c-i] != "em":
                        move = Move(((r, c), (r-i, c-i)), self.board)
                        movenot = Move.inNotation(move)
                        moves.append(movenot)
                    break
        # Diagonal<-v
        for i in range(1, 8):
            if (r+i) <= 7 and (c-i) >= 0:
                if self.board[r+i][c-i] == "em":
                    move = Move(((r, c), (r+i, c-i)), self.board)
                    movenot = Move.inNotation(move)
                    moves.append(movenot)

                else:

                    if self.board[r+i][c-i][0] != same and self.board[r+i][c-i] != "em":

                        move = Move(((r, c), (r+i, c-i)), self.board)
                        movenot = Move.inNotation(move)
                        moves.append(movenot)

                    break
        # Diagonalv->
        for i in range(1, 8):
            if (r+i) <= 7 and (c+i) <= 7:
                if self.board[r+i][c+i] == "em":
                    move = Move(((r, c), (r+i, c+i)), self.board)
                    movenot = Move.inNotation(move)
                    moves.append(movenot)

                else:
                    if self.board[r+i][c+i][0] != same and self.board[r+i][c+i] != "em":
                        move = Move(((r, c), (r+i, c+i)), self.board)
                        movenot = Move.inNotation(move)
                        moves.append(movenot)
                    break
        return moves

    def getQueenMoves(self, r, c, moves, piece):
        same = piece[0]
        moveQ = []
        moves = self.getRookMoves(r, c, moves, piece)
        moves += self.getBishopMoves(r, c, moveQ, piece)
        return moves

    def getKingMoves(self, r, c, moves, piece):
        same = piece[0]
        movesK = []
        filter_Castle = []
        castle_dir = []
        possibilities = [(r+1, c), (r+1, c+1), (r+1, c-1),
                         (r, c-1), (r, c+1), (r-1, c+1), (r-1, c-1), (r-1, c)]
        pval = [p for p in possibilities if p[0] <=
                7 and p[1] <= 7 and p[0] >= 0 and p[1] >= 0]
        for p in pval:
            if self.board[p[0]][p[1]] == "em" or self.board[p[0]][p[1]][0] != same:
                move = Move(((r, c), (p[0], p[1])), self.board)
                movenot = Move.inNotation(move)
                movesK.append(movenot)
                filter_Castle.append("n")
                castle_dir.append("n")
        # Castling
        if not self.getCheck() and same == 'w' and r == 7 and c == 4:
            if "K" in self.castling and self.board[r][c+1] == "em" and self.board[r][c+2] == "em":
                move = Move(((r, c), (r, c+2)), self.board)
                movenot = Move.inNotation(move)
                movesK.append(movenot)
                filter_Castle.append("y")
                castle_dir.append(
                    ((int(movenot[4]), int(movenot[5])-1), self.king_pos[1]))
            if "Q" in self.castling and self.board[r][c-1] == "em" and self.board[r][c-2] == "em" and self.board[r][c-3] == "em":
                move = Move(((r, c), (r, c-2)), self.board)
                movenot = Move.inNotation(move)
                movesK.append(movenot)
                filter_Castle.append("y")
                castle_dir.append(
                    ((int(movenot[4]), int(movenot[5])+1), self.king_pos[1]))
        if not self.getCheck() and same == 'b' and r == 0 and c == 4:
            if "k" in self.castling and self.board[r][c+1] == "em" and self.board[r][c+2] == "em":
                move = Move(((r, c), (r, c+2)), self.board)
                movenot = Move.inNotation(move)
                movesK.append(movenot)
                filter_Castle.append("y")
                castle_dir.append(
                    (self.king_pos[0], (int(movenot[4]), int(movenot[5])-1)))
            if "q" in self.castling and self.board[r][c-1] == "em" and self.board[r][c-2] == "em" and self.board[r][c-3] == "em":
                move = Move(((r, c), (r, c-2)), self.board)
                movenot = Move.inNotation(move)
                movesK.append(movenot)
                filter_Castle.append("y")
                castle_dir.append(
                    (self.king_pos[0], (int(movenot[4]), int(movenot[5])+1)))

        # Filter to not walk into checks

        ogKing = self.king_pos

        valid_Kingmoves = []
        for num, m in enumerate(movesK):
            if same == 'w':
                self.king_pos = ((int(m[4]), int(m[5])), ogKing[1])
                castle = ((int(m[4]), int(m[5])-1), ogKing[1])

            else:
                self.king_pos = (ogKing[0], (int(m[4]), int(m[5])))
                castle = (ogKing[0], (int(m[4]), int(m[5])-1))
            CheckBool = self.getCheck()
            if not CheckBool:
                if filter_Castle[num] == "y":
                    self.king_pos = castle_dir[num]
                    if not self.getCheck():
                        valid_Kingmoves.append(m)
                else:
                    valid_Kingmoves.append(m)
            self.king_pos = ogKing
        moves += valid_Kingmoves
        return moves

    def Board2Fen(self):
        N2Piece = {'bR': 'r', 'bB': 'b', 'bN': 'n', 'bP': 'p', 'bQ': 'q', 'bK': 'k',
                   'wR': 'R', 'wB': 'B', 'wN': 'N', 'wP': 'P', 'wQ': 'Q', 'wK': 'K'}
        FEN = ""
        for r in range(len(self.board)):
            k = 0
            for i, c in enumerate(range(len(self.board[r]))):
                if self.board[r][c] == "em":

                    k += 1
                else:
                    if k != 0:
                        FEN += str(k)
                        FEN += N2Piece[self.board[r][c]]
                        k = 0
                    else:
                        FEN += N2Piece[self.board[r][c]]
            if i == 7 and k != 0:
                FEN += str(k)
            if r != 7:
                FEN += "/"
        FEN += " "
        FEN += self.to_Move
        FEN += " "
        if self.castling == "":
            FEN += "-"
        if self.castling != "-":
            FEN += self.castling.replace("-", "")
        FEN += " "
        for v in self.en_Passant:
            FEN += v.lower()
        if self.en_Passant == "":
            FEN += "-"
        FEN += " "
        FEN += str(self.n_Hmove)
        FEN += " "
        FEN += str(self.n_Fmove)
        return FEN+" "+str(self.cK) + str(self.ck)+str(self.cQ)+str(self.cq) #+ " "+self.castlingfilter

# INEFFICIENT AND BAD ALGO NOT BEING USED HERE FOR TESTING ONLY
    def getVaalidMoves(self):
        self.valid_Moves = []
        moves = self.getAllMoves()
        sc = self.to_Move
        t = 0
        t_b = GameState(self.Board2Fen())

        for m in moves:
            t += 1
            t_move = Move(
                ((int(m[2]), int(m[3])), (int(m[4]), int(m[5]))), t_b.board)
            t_b.make_Move(t_move)

            op_moves = t_b.getAllMoves()

            k = 0
            for p in op_moves:
                if t_b.board[int(p[4])][int(p[5])] == sc+"K":

                    k += 1
                    break

            if k == 0:
                self.valid_Moves.append(m)
            t_b.undo_Move()
            # self.undo_Move()

        self.c = 0
        return self.valid_Moves
# Temp test Methods

    def getPositions(self, depth, test, eval, c, tm, og):
        if depth == 0:
            m = self.getEvaluation(c)
            if m > eval:
                eval = m
                test = tm
                print(test, eval)

            return 1, test, eval
        movess = self.getValidMoves()
        positions = 0
        p = 0

        for t in movess:

            # move=Move(((int(t[2]),int(t[3])),(int(t[4]),int(t[5]))),self.board)
            if depth == og:
                tm = t
            self.make_Move(t)
            # print(pos)
            p, test, eval = self.getPositions(depth-1, test, eval, c, tm, og)
            positions += p
            self.undo_Move()
            # print((4-depth)*"|",self.Board2Fen())

        return positions, test, eval

    def getEvaluation(self, col):
        boardsum = 0
        bonus = 0
        t = {"em": 0, "wP": wpawn_Heatmap, "bP": bpawn_Heatmap, "wN": wknight_Heatmap, "bN": bknight_Heatmap, "wB": wbishop_Heatmap, "bB": bbishop_Heatmap,
             "wR": wrook_Heatmap, "bR": brook_Heatmap, "wK": wking_Heatmap, "bK": bking_Heatmap, "wQ": queen_Heatmap, "bQ": queen_Heatmap}
        # print(self.to_Move)
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                temp = self.board[r][c]
                color = temp[0]
                piece = temp[1].lower()
                if temp != "em":
                    bonus += t[temp][r][c]

                if color == col:

                    boardsum += points[self.board[r][c]]
                    boardsum += bonus

                else:
                    boardsum -= points[self.board[r][c]]
                    boardsum -= bonus
        # print("sum:",boardsum)
        return boardsum

    def changeTurn(self, c):
        if c == "w":
            return "b"
        else:
            return "w"

# PERFT TESTING


gs = GameState(start_Fen)
depth = 1
c = ""
c = gs.to_Move
for i in range(depth-1):
    c = gs.changeTurn(c)
start = time.time()
og = depth
k = 0
test, st, k = gs.getPositions(depth, "", -99999, c, "", og)
end = time.time()
print(end-start)
print(test, st)
sum = 0
# tm=gs.getValidMoves()
"""
    #
    for t in tm:
            
            move=Move(((int(t[2]),int(t[3])),(int(t[4]),int(t[5]))),gs.board)
            gs.make_Move(t)
        
                
            s=gs.getPositions(depth-1,"",0)
            sum+=s
            gs.undo_Move()
            
            if len(t)==7:
                print(move.inChessNotation()+t[6]+":",s)
            else:
                print(move.inChessNotation()+":",s)   
            print( gs.Board2Fen())# != start_Fen:
                #break


    
    print(end-start)
    print(sum)#,test)
    print("FIN",gs.Board2Fen())
    """
# a,b,c,d,e,f,g=gs.getCheckPin()
# print("a",a,"b",b,"c",c,"d",d,"e",e,"f",f,"g",g)
# m=gs.getValidMoves()
