import pygame as pg
from Chess import Engine


WIDTH = HEIGHT = 512
DIMENSION = 8
SQ= HEIGHT//DIMENSION
MAX_FPS=15
IMAGES = {}

def loadPieces():
    pieces = ['wR','wN','wB','wQ','wK','wP','bR','bN','bB','bQ','bK','bP']
    for piece in pieces:
        IMAGES[piece] =pg.transform.scale( pg.image.load("images/"+piece+".png"),(SQ,SQ) )

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    clock=pg.time.Clock()
    screen.fill(p.Color("white"))
    gs = Engine.GameState()
    print(gs.board)
main()