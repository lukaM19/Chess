# Chess
Chess engine project

## Done

- [x]  Board
- [x]  FEN2Board interpreter, Board2FEN export
- [x]  2-player mode
- [x]  Movable Pieces, Undo Moves, Move Order maintained, drag animation, add sound effect for moving
 - [x] Pawn,Rook,Knight,Bishop,King,Queen Move Rules added, Can generate all possible moves for the position
 - [X] pawn promotion, castling(&undo), enpassant(& undo)
    * - [x] Castling and undo 
    * - [x] Pawn promotion and undo  
    * - [x] En passant and undo <s>(Need to double check for bugs during undo)</s>     
 - [x] Checks 
 - [x] Checkmate, stalemate
 - [x] Pinned pieces, discovered checks 

## Done-ish

* add Comments in code, clear up useless code and variables
 > - [x] MainGame commented and cleared
 > - [ ] Engine partially

* GUI??
 > - [x] Menu skeleton 
 > - [x] Basic navigation
 > - [x] Custom starting positions
 > - [x] select Bot/2-player mode
 > - [ ] probably will need to set depth from menu in future
 > - [x] Change between 560/720 modes

## To-Do
* Position Evaluation&nbsp;\\
* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-> The Point Of this porject 
* Create an AI&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/

# Should I focus more on optimization , Decide on this soon.
* https://en.wikipedia.org/wiki/0x88
* SWITCH LANGUAGES??

# Known Bugs
* <s>the file and rank indexes get obstructed by piece drawings, if pieces are moved outside of board boundaries </s>
* Need to at an additional check for validity of Custom Fen
* <s>Pawns check to their back right</s>

# **Resources**
> https://www.pygame.org/docs/search.html?q=
> 
> https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
> 
> https://www.chessprogramming.org/Main_Page
> 
> https://stackoverflow.com/questions/1110439/chess-optimizations
> 

