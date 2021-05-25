import pygame as pg
from Chess import Engine

pg.init()
WIDTH = HEIGHT = 512

DIMENSION = 8
SQ= HEIGHT//DIMENSION
MAX_FPS=15
IMAGES = {}

def loadPieces():
    pieces = ['wR','wN','wB','wQ','wK','wP','bR','bN','bB','bQ','bK','bP']
    for piece in pieces:
        IMAGES[piece] =pg.transform.scale( pg.image.load("Chess/images_HR/"+piece+".png"),(SQ-int(SQ/4),SQ-int(SQ/4)) )

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    clock=pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = Engine.GameState()
    loadPieces()
    running=True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running=False
        drawGame(screen,gs)
        clock.tick(MAX_FPS)
        pg.display.flip()

def drawGame(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    colors=[pg.Color("White"),pg.Color("Gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[((r+c)%2)]
            pg.draw.rect(screen, color, pg.Rect(c*SQ,r*SQ,SQ,SQ))
def drawPieces(screen,board):
     for r in range(DIMENSION):
        for c in range(DIMENSION):
            p= board[r][c]
            if p != "em": 
                screen.blit(IMAGES[p],pg.Rect(c*SQ+SQ/8,r*SQ+SQ/8,SQ,SQ))

if __name__ == "__main__":
    main()