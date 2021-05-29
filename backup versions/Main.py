import pygame as pg
import sys
from Chess import Engine
import time
pg.init()
WIDTH = HEIGHT = 720


DIMENSION = 8
SQ= HEIGHT//DIMENSION
MAX_FPS=15
IMAGES = {}
LETR={1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H' }
COLOR={'wR':'w','wN':'w','wB':'w','wQ':'w','wK':'w','wP':'w','bR':'b','bN':'b','bB':'b','bQ':'b','bK':'b','bP':'b'}
click = False
edge_pix=20
LAUNCH = True

font = pg.font.Font('freesansbold.ttf', 16)

def loadPieces():
    pieces = ['wR','wN','wB','wQ','wK','wP','bR','bN','bB','bQ','bK','bP']
    for piece in pieces:
        IMAGES[piece] =pg.transform.scale( pg.image.load("Chess/images_HR/"+piece+".png"),(SQ-int(SQ/4),SQ-int(SQ/4)) )

def main_game(START_POS):
    
    pg.display.set_caption('Play Game')
    start=time.time()
    screen = pg.display.set_mode((WIDTH+20,HEIGHT+40))
    screen_bl=pg.transform.rotate(screen, 180), (0, 0)
    clock=pg.time.Clock()
    screen.fill(pg.Color("white"))
    
    gs = Engine.GameState(START_POS)
    loadPieces()
    move_sound = pg.mixer.Sound("Chess/move.wav")
    running=True
    selected=()
    sel_list=[]
    last_move=[]
    t_brd=[]
    while running:
        mx,my = pg.mouse.get_pos()
        click = False
        for e in pg.event.get():
            if e.type == pg.QUIT:          
                running=False
            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
                if mx>20 and my<720:
                    row=(my)//SQ
                    col=(mx-edge_pix)//SQ
                    if selected == (row,col):
                        selected=()
                        sel_list=[]
                    else:
                        selected = (row,col)
                        sel_list.append(selected)
                    if len(sel_list)==2 :
                        
                       
                        if(gs.board[sel_list[0][0]][sel_list[0][1]]=="em") or gs.to_Move != COLOR[gs.board[sel_list[0][0]][sel_list[0][1]]]:
                            selected=()
                            sel_list=[]
                        else:
                            
                            move=Engine.Move(sel_list,gs.board)
                            gs.make_Move(move)
                            pg.mixer.Sound.play(move_sound)
                            pg.mixer.music.stop()
                            last_move=sel_list
                            
                            selected=()
                            sel_list=[]
                            
                    #print(mx,my,row,col)
        drawGame(screen,gs)
        end=time.time()
        
        text = font.render("Quit", True, 'pink')
        textRect = text.get_rect()
        textRect.center = (SQ-70,HEIGHT+10)
        screen.blit(text, textRect)
        if textRect.collidepoint((mx,my)) :
            if click:
            
                main_Menu()
        undot = font.render("Undo", True, 'pink')
        undoRect = undot.get_rect()
        undoRect.center = (SQ-70,HEIGHT+30)
        screen.blit(undot, undoRect)
        if undoRect.collidepoint((mx,my)) :
            if click:
                
                move=Engine.Move(last_move,gs.board)
                gs.undo_Move()
                pg.mixer.Sound.play(move_sound)
                pg.mixer.music.stop()
                
        clock.tick(MAX_FPS)
        pg.display.flip()
    print('time taken:',start-end)
    
def drawGame(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)



def drawBoard(screen):
    colors=[pg.Color(222,184,135),pg.Color(139,69,19)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[((r+c)%2)]
            pg.draw.rect(screen, color, pg.Rect(c*SQ+edge_pix,r*SQ,SQ,SQ))
            if r==7:
                text = font.render(LETR[c+1], True, 'black')
                textRect = text.get_rect()
                textRect.center = (c*SQ+edge_pix+SQ/2,HEIGHT+10)
                screen.blit(text, textRect)
            if c==0:
                text = font.render(str((8-r)), True, 'black')
                textRect = text.get_rect()
                textRect.center = (c*SQ+SQ/8,r*SQ+edge_pix)
                screen.blit(text, textRect)
    
    
def drawPieces(screen,board):
     for r in range(DIMENSION):
        for c in range(DIMENSION):
            p= board[r][c]
            if p != "em": 
                screen.blit(IMAGES[p],pg.Rect(c*SQ+SQ/8+edge_pix,r*SQ+edge_pix,SQ,SQ))




def main_Menu():
    pg.init()
    input = ''
    ST_INPUT=False
    START_POS=""
    while LAUNCH == True:
        pg.display.set_caption('MAIN MENU')
        settings_sc =  pg.display.set_mode((WIDTH+20,HEIGHT+20+20))
        settings_sc.fill('gray')
        clock=pg.time.Clock()
        button=[120,40]
        #valid=['0','1','2','3','4','5','6','7','8','9','r','n','b','k','q','p','-','/',' ','w','a','c','d','e','f','g','h']
        #valid_asc=[ord(v) for v in valid]
        #print(valid_asc)
        valid_asc=[48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 114, 110, 98, 107, 113, 112, 45, 47, 32, 119, 97, 99, 100, 101, 102, 103, 104]
        
        
        
        ###Set up buttons .........
        button_1 = pg.Rect(WIDTH//2-button[0]/2,HEIGHT//6-button[1]/2,120,40)
        pg.draw.rect(settings_sc,'black',button_1)
        text = font.render("PLAY", True, 'white')
        textRect = text.get_rect()
        textRect.center = (WIDTH//2,HEIGHT//6)
        settings_sc.blit(text, textRect)
        
        button_2 = pg.Rect(WIDTH//2-85, 20+HEIGHT//6+button[1]/2+60,170,40)
        pg.draw.rect(settings_sc,'black',button_2)
       
        text = font.render("Set Starting Position", True, 'white')
        textRect = text.get_rect()
        textRect.center = (WIDTH//2,100+HEIGHT//6+button[1]/2)
        settings_sc.blit(text, textRect)


        button_4 = pg.Rect(WIDTH//2-button[0]/2,5*HEIGHT//6-button[1]/2,120,40)
        pg.draw.rect(settings_sc,'red',button_4)
        text = font.render("QUIT", True, 'white')
        textRect = text.get_rect()
        textRect.center = (WIDTH//2,5*HEIGHT//6)
        settings_sc.blit(text, textRect)
        ###...............
        ###Intercations..........
        mx,my = pg.mouse.get_pos()
        if button_1.collidepoint((mx,my)) :
            if click:
            
                main_game(START_POS)
                
        if button_2.collidepoint((mx,my)) :
            if click:
                START_POS=input
        
        if button_4.collidepoint((mx,my)) :
            if click:
                pg.quit()
                sys.exit()
     
        click = False
        
        
        for e in pg.event.get():
            mods = pg.key.get_mods()
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if e.key == pg.K_BACKSPACE:
                    input = input[:-1]
                
                if e.key == pg.K_RETURN:
                    ST_INPUT = False
                print(e.key)
                if e.key in valid_asc and ST_INPUT:
                    if mods& pg.KMOD_CAPS or mods& pg.KMOD_LSHIFT:
                        input += e.unicode
                    else:
                        input += e.unicode.lower()
            
            font_i= pg.font.Font('freesansbold.ttf', 12)
            inp_text = font_i.render(input, True, 'green')
            inp_box = pg.Rect(WIDTH//2-125-180,20+HEIGHT//6+button[1]/2,174,40)
            if ST_INPUT:
                pg.draw.rect(settings_sc,'blue',inp_box)
            else:
                pg.draw.rect(settings_sc,'navy',inp_box)
            I_box_text=font_i.render("Put custom position FEN here:", True, 'green')
            settings_sc.blit(I_box_text, (inp_box.x, inp_box.y+12))
            button_3_w=max(250,inp_text.get_width()+5)
            button_3 = pg.Rect(WIDTH//2-125,20+HEIGHT//6+button[1]/2,button_3_w,40)
            pg.draw.rect(settings_sc,'black',button_3)
            settings_sc.blit(inp_text, (button_3.x+5, button_3.y+5))
            if button_3.collidepoint((mx,my)) :
                if click:
                 ST_INPUT = True

            pg.display.flip()
            clock.tick(60)
        
        
    
if __name__ == "__main__":
    main_Menu()
