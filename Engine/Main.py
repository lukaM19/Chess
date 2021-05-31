import pygame as pg
import sys
from Chess import Engine
import time
pg.init()

#Global Variables
WIDTH = HEIGHT = 720
DIMENSION = 8
SQ= HEIGHT//DIMENSION
MAX_FPS = 60
IMAGES = {}
LETR = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h' }
COLOR = {'wR':'w','wN':'w','wB':'w','wQ':'w','wK':'w','wP':'w','bR':'b','bN':'b','bB':'b','bQ':'b','bK':'b','bP':'b'}
click = False
edge_pix=20
LAUNCH = True
font = pg.font.Font('freesansbold.ttf', 14)

#Loading Pieces
def loadPieces():
    pieces = ['wR','wN','wB','wQ','wK','wP','bR','bN','bB','bQ','bK','bP']
    for piece in pieces:
        IMAGES[piece] =pg.transform.scale( pg.image.load("Chess/images_HR/"+piece+".png"),(SQ-int(SQ/4),SQ-int(SQ/4)) )

#Main Game Process
def mainGame(START_POS,SHOW_MOVES):
    
    #Draw Game Window
    pg.display.set_caption('Play Game')
    start=time.time()
    screen = pg.display.set_mode((WIDTH+20,HEIGHT+40))
    #screen_bl=pg.transform.rotate(screen, 180), (0, 0)
    clock=pg.time.Clock()
    screen.fill(pg.Color("white"))

    #load game position, Pieces and load images for chess pieces, Load Valid moves
    gs = Engine.GameState(START_POS)
    loadPieces()
    validmoves=gs.getAllMoves()
    
    #variables for making moves, drag animation
    move_sound = pg.mixer.Sound("Chess/move.wav")
    running=True
    selected=()
    sel_list=[]
    last_move=[]
    hold = False 
    cur=""
    pos=()

    #Variables for drawing board highlights during moves
    t=IMAGES["wR"]
    tr=pg.Rect(0,0,150,150)
    gh_col = (0, 255, 0)
    bh_col = (0, 0, 255)
    h_loc=()
    highlight=(SQ,SQ)
    
    cir=pg.Surface((20,20))
    cir.set_alpha(60)
    high_sur=pg.Surface(highlight)
    high_sur.set_alpha(25)
    move_made= False
    highB=False
    out = False
    #Helps us make sure we only load valid moves once, after each move has been played
    counter=0
    mark_d=0
    mark_md=0
    promotion_Move_w= False
    promotion_Move_b = False
    #While game instance is open
    while running:
        counter+=1
        #mouse co-ordiantes on board
        mx,my = pg.mouse.get_pos()
        click = False
        #Main Event loop
        for e in pg.event.get():
            if e.type == pg.QUIT:          
                running=False
            #Mouse button is pressed
            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
                    hold=False
                #Mouse button is pressed inside the loop
                if mx>20 and my<720:
                    
                    row=(my)//SQ
                    col=(mx-edge_pix)//SQ
                    if gs.board[row][col] != "em":
                        selected = (row,col)
                        hold=True
                        sel_list.append(selected)
                        cur=gs.board[row][col]
                        t=IMAGES[cur]
                        tr=t.get_rect()
                        h_loc=(row,col)
                        
                        
                        
            #Mouse button is let go           
            if e.type == pg.MOUSEBUTTONUP and hold:
                if mx>20 and my<=720:  
                    row=(my)//SQ
                    col=(mx-edge_pix)//SQ    
                    if selected == (row,col):
                        selected=()
                        sel_list=[]
                        hold=False
                    else:
                        selected = (row,col)
                        sel_list.append(selected)
                    

                    #if 2 Squares have been selected for a move
                    if len(sel_list)==2 :
                        hold=False
                        #if staring square is empty or not your turn to move, reset move selection
                        if(gs.board[sel_list[0][0]][sel_list[0][1]]=="em") or gs.to_Move != COLOR[gs.board[sel_list[0][0]][sel_list[0][1]]]:
                            selected=()
                            sel_list=[]
                        else:
                            
                            move=Engine.Move(sel_list,gs.board)
                            #print(Engine.Move.inNotation(move))
                            rn=Engine.Move.inNotation(move)
                            #Make move if Valid
                            if(rn in validmoves):
                                gs.make_Move(move)
                                pg.mixer.Sound.play(move_sound)
                                pg.mixer.music.stop()
                                if move.piece_moved[1] == "P":
                                    ##Check if promotion move
                                    if move.piece_moved[0] == 'w' and move.end_row==0:
                                        promotion_Move_w= True
                                    if move.piece_moved[0] == 'b' and move.end_row==7:
                                        promotion_Move_b= True
                                last_move=sel_list
                                move_made=True
                                selected=()
                                sel_list=[]
                                mark_md=counter
                            else:
                                selected=()
                                sel_list=[]
                else:
                    hold = False
                    selected=()
                    sel_list=[]

            #Drag animation
            if e.type == pg.MOUSEMOTION:
                pos=pg.mouse.get_pos()
                
        #Highlight last square from and to which  the move was made, Bound set to avoid the bug of pieces showing up on the side of the board
        if hold  and (mx>30 and my<720):
            highB= True
        #UPDATE Valid moves for new board position after a move was amde
        if move_made and mark_d<mark_md:
            validmoves=gs.getAllMoves()  
            mark_d=counter

        
            
        #update the display   
        drawGame(screen,gs,high_sur, gh_col,bh_col,h_loc,highB,move_made,last_move,pos,t,tr,validmoves,selected,cir,SHOW_MOVES)
        highB = False
        #Handle pawn promotion
        if promotion_Move_w:
            gs.to_Move='w'
            Rt = font.render("R", True, 'pink')
            RtRect = Rt.get_rect()
            RtRect.center = (10,20)
            screen.blit(Rt, RtRect)
            if RtRect.collidepoint((mx,my)) :
                if click:
                    gs.board[move.end_row][move.end_col]="wR"
                    promotion_Move_w=False
                    gs.to_Move='b'
            Nt = font.render("N", True, 'pink')
            NtRect = Nt.get_rect()
            NtRect.center = (10,40)
            screen.blit(Nt, NtRect)
            if NtRect.collidepoint((mx,my)) :
                if click:
                    gs.board[move.end_row][move.end_col]="wN"
                    promotion_Move_w=False
                    gs.to_Move='b'
            Bt = font.render("B", True, 'pink')
            BtRect = Bt.get_rect()
            BtRect.center = (10,60)
            screen.blit(Bt, BtRect)
            if BtRect.collidepoint((mx,my)) :
                if click:
                    gs.board[move.end_row][move.end_col]="wB"
                    promotion_Move_w=False
                    gs.to_Move='b'
            Qt = font.render("Q", True, 'pink')
            QtRect = Qt.get_rect()
            QtRect.center = (10,80)
            screen.blit(Qt, QtRect)
            if QtRect.collidepoint((mx,my)) :
                if click:
                    gs.board[move.end_row][move.end_col]="wQ"
                    promotion_Move_w=False
                    gs.to_Move='b'
        if promotion_Move_b:
            gs.to_Move='b'
            Rt = font.render("R", True, 'pink')
            RtRect = Rt.get_rect()
            RtRect.center = (10,20)
            screen.blit(Rt, RtRect)
            if RtRect.collidepoint((mx,my)) :
                if click:
                    gs.board[move.end_row][move.end_col]="bR"
                    promotion_Move_b=False
                    gs.to_Move='w'
            Nt = font.render("N", True, 'pink')
            NtRect = Nt.get_rect()
            NtRect.center = (10,40)
            screen.blit(Nt, NtRect)
            if NtRect.collidepoint((mx,my)) :
                if click:
                    gs.board[move.end_row][move.end_col]="bN"
                    promotion_Move_b=False
                    gs.to_Move='w'
            Bt = font.render("B", True, 'pink')
            BtRect = Bt.get_rect()
            BtRect.center = (10,60)
            screen.blit(Bt, BtRect)
            if BtRect.collidepoint((mx,my)) :
                if click:
                    gs.board[move.end_row][move.end_col]="bB"
                    promotion_Move_b=False
                    gs.to_Move='w'
            Qt = font.render("Q", True, 'pink')
            QtRect = Qt.get_rect()
            QtRect.center = (10,80)
            screen.blit(Qt, QtRect)
            if QtRect.collidepoint((mx,my)) :
                if click:
                    gs.board[move.end_row][move.end_col]="bQ"
                    promotion_Move_b=False
                    gs.to_Move='w'
        end=time.time()

        #Quit Button and interaction on Click
        Quitt = font.render("Quit", True, 'pink')
        QuitRect = Quitt.get_rect()
        QuitRect.center = (SQ-70,HEIGHT+10)
        screen.blit(Quitt, QuitRect)
        if QuitRect.collidepoint((mx,my)) :
            if click:
            
                main_Menu()

        #UNDO button and interaction on Click        
        undot = font.render("Undo", True, 'pink')
        undoRect = undot.get_rect()
        undoRect.center = (SQ-70,HEIGHT+30)
        screen.blit(undot, undoRect)
        if undoRect.collidepoint((mx,my)) :
            if click and len(last_move) !=0:
                
                move=Engine.Move(last_move,gs.board)
                gs.undo_Move()
                pg.mixer.Sound.play(move_sound)
                pg.mixer.music.stop()
                validmoves=gs.getAllMoves()  
                move_made = False
        #Give FEN of given position
        givet = font.render("Export Fen", True, 'pink')
        giveRect = givet.get_rect()
        giveRect.center = (WIDTH//4,HEIGHT+25)
        screen.blit(givet, giveRect)
        if giveRect.collidepoint((mx,my)) :
            if click :
                out = not out
        if out:
            font_c = pg.font.Font('freesansbold.ttf', 10)
            txt=gs.Board2Fen()
            txt_t=font_c.render(txt, True, 'black')
            out_w=txt_t.get_width()+5
            outRect = txt_t.get_rect()
            outRect.center = (WIDTH//4+givet.get_width()//2 + out_w//2 ,HEIGHT+25)
            screen.blit(txt_t, outRect)
                
            
        #Set FPS apply Changes
        clock.tick(60)
        pg.display.flip()
    print('time taken:',start-end)



#Function for Drawing all parts of the game: Board, Pieces, Highlights    
def drawGame(screen,gs,high_sur, gh_col,bh_col,h_loc,highB,move_made,last_move,pos,t,tr,validmoves,selected,cir,SHOW_MOVES):
    if gs.to_Move == 'w':
        screen.fill(pg.Color("white"))
    else:
        screen.fill(pg.Color((82,88,84)))
    drawBoard(screen)
    drawPieces(screen,gs.board)
    drawHighlights(high_sur, gh_col,bh_col,h_loc,screen,highB,move_made,last_move,pos,t,tr,validmoves,gs.board,selected,cir,SHOW_MOVES)

#Function for drawing highlights on the board   
def drawHighlights(high_sur, gh_col,bh_col,h_loc,screen,highB,move_made,last_move,pos,t,tr,validmoves,board,selected,cir,SHOW_MOVES):
    if highB:
        tr.center = pos
        screen.blit(t,tr)
        pg.draw.rect(high_sur, gh_col, high_sur.get_rect())
        screen.blit(high_sur,(h_loc[1]*SQ+edge_pix,h_loc[0]*SQ))
        
        if SHOW_MOVES== True:
            for v in validmoves :
                
                if str(v[:4]) == str(board[selected[0]][selected[1]]+str(selected[0])+str(selected[1])):

                    #cr=pg.draw.circle(cir, gh_col, (int(v[5])*SQ+edge_pix+SQ/2-10, int(v[4])*SQ+SQ/2-10), 10,2)
                    pg.draw.rect(cir,gh_col,cir.get_rect())
                    screen.blit(cir,(int(v[5])*SQ+edge_pix+SQ/2-10, int(v[4])*SQ+SQ/2-10)) 
                
                
    if move_made: 
        pg.draw.rect(high_sur, bh_col, high_sur.get_rect())
        screen.blit(high_sur,(last_move[0][1]*SQ+edge_pix,last_move[0][0]*SQ)) 
        screen.blit(high_sur,(last_move[1][1]*SQ+edge_pix,last_move[1][0]*SQ))
#Function for Drawing the board, also the File, Rank indexes on the sides    
def drawBoard(screen):
    colors=[pg.Color(222,184,135),pg.Color(139,69,19)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color=colors[((r+c)%2)]
            cl=colors[1-((r+c)%2)]
            pg.draw.rect(screen, color, pg.Rect(c*SQ+edge_pix,r*SQ,SQ,SQ))
            if r==7:
                text = font.render(LETR[c+1], True, cl)
                textRect = text.get_rect()
                textRect.center = (c*SQ+SQ+14,HEIGHT-10)
                screen.blit(text, textRect)
            if c==0:
                text = font.render(str((8-r)), True, cl)
                textRect = text.get_rect()
                textRect.center = (c*SQ+30,r*SQ+edge_pix)
                screen.blit(text, textRect)
    
# Draw the pieces on the screen 
def drawPieces(screen,board):
     for r in range(DIMENSION):
        for c in range(DIMENSION):
            p= board[r][c]
            if p != "em": 
                screen.blit(IMAGES[p],pg.Rect(c*SQ+SQ/8+edge_pix,r*SQ+edge_pix,SQ,SQ))


def main_Menu():
    pg.init()
    input = ''
    #Bool variable for indicating if we should accept input from keyboard for the FEN String
    ST_INPUT = False
    START_POS=""
    SHOW_MOVES = False
    click= False
    while LAUNCH == True:
        
        #INITIALIZE the display
        pg.display.set_caption('MAIN MENU')
        settings_sc =  pg.display.set_mode((WIDTH+20,HEIGHT+20+20))
        settings_sc.fill('gray')
        clock=pg.time.Clock()
        button=[120,40]
        #VALID characters that can be in the FEN notation
        #valid=['0','1','2','3','4','5','6','7','8','9','r','n','b','k','q','p','-','/',' ','w','a','c','d','e','f','g','h']
        #valid_asc=[ord(v) for v in valid]
        #print(valid_asc)
        valid_asc=[48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 114, 110, 98, 107, 113, 112, 45, 47, 32, 119, 97, 99, 100, 101, 102, 103, 104]
        
        
        
        ###Set up buttons .........
        #BUTTON_1~PLAY
        button_1 = pg.Rect(WIDTH//2-button[0]/2,HEIGHT//6-button[1]/2,120,40)
        pg.draw.rect(settings_sc,'black',button_1)
        text = font.render("PLAY", True, 'white')
        textRect = text.get_rect()
        textRect.center = (WIDTH//2,HEIGHT//6)
        settings_sc.blit(text, textRect)
        #BUTTON_2/Returnbutton~ Confirm Starting FEN
        button_2 = pg.Rect(WIDTH//2-85, 20+HEIGHT//6+button[1]/2+60,170,40)
        pg.draw.rect(settings_sc,'black',button_2)
        text = font.render("Set Starting Position", True, 'white')
        textRect = text.get_rect()
        textRect.center = (WIDTH//2,100+HEIGHT//6+button[1]/2)
        settings_sc.blit(text, textRect)

        button_5 = pg.Rect(WIDTH//2-85, 20+HEIGHT//6+button[1]/2+120,170,40)
        color=""
        if SHOW_MOVES:
            color='green'
        else:
            color='red'
        pg.draw.rect(settings_sc,color,button_5)
        text = font.render("Higlight available moves", True, 'white')
        textRect = text.get_rect()
        textRect.center = (WIDTH//2,160+HEIGHT//6+button[1]/2)
        settings_sc.blit(text, textRect)

        #BUTTON_4~Quit Button 
        button_4 = pg.Rect(WIDTH//2-button[0]/2,5*HEIGHT//6-button[1]/2,120,40)
        pg.draw.rect(settings_sc,'red',button_4)
        text = font.render("QUIT", True, 'white')
        textRect = text.get_rect()
        textRect.center = (WIDTH//2,5*HEIGHT//6)
        settings_sc.blit(text, textRect)

        ###...............
        ###Intercations..........
        ###Mouse position
        mx,my = pg.mouse.get_pos()
        #Play~ Launch the game
        if button_1.collidepoint((mx,my)) :
            if click:
            
                mainGame(START_POS,SHOW_MOVES)
        #Set the input string as the starting positoin     
        if button_2.collidepoint((mx,my)) :
            if click:
                START_POS=input
        #Quit button
        if button_4.collidepoint((mx,my)) :
            if click:
                pg.quit()
                sys.exit()
        if button_5.collidepoint((mx,my)) :
            if click:
                SHOW_MOVES = not SHOW_MOVES
     
        click = False
        
        
        for e in pg.event.get():
            mods = pg.key.get_mods()
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            #Click Event
            if e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
            #Escape definitoin~ Quits app
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                #Delte last Char from input
                if e.key == pg.K_BACKSPACE:
                    input = input[:-1]
                #Confirm input
                if e.key == pg.K_RETURN:
                    ST_INPUT = False
                #if valid FEN Character, and input is started add to the input string
                if e.key in valid_asc and ST_INPUT:
                    if mods& pg.KMOD_CAPS or mods& pg.KMOD_LSHIFT:
                        input += e.unicode
                    else:
                        input += e.unicode.lower()

            #Take in the input for the FEN String
            font_i= pg.font.Font('freesansbold.ttf', 12)
            inp_text = font_i.render(input, True, 'green')
            inp_box = pg.Rect(WIDTH//2-125-180,20+HEIGHT//6+button[1]/2,174,40)
            #Indicate by colors if we are currently accepting keyboard input for FEN
            if ST_INPUT:
                pg.draw.rect(settings_sc,'blue',inp_box)
            else:
                pg.draw.rect(settings_sc,'navy',inp_box)
            I_box_text=font_i.render("Put custom position FEN here:", True, 'green')
            settings_sc.blit(I_box_text, (inp_box.x, inp_box.y+12))
            #Change input box width if needed
            button_3_w=max(250,inp_text.get_width()+5)
            button_3 = pg.Rect(WIDTH//2-125,20+HEIGHT//6+button[1]/2,button_3_w,40)
            pg.draw.rect(settings_sc,'black',button_3)
            settings_sc.blit(inp_text, (button_3.x+5, button_3.y+5))
            #Start takingin input if the input box ahs been clicked
            if button_3.collidepoint((mx,my)) :
                if click:
                 ST_INPUT = True

            pg.display.flip()
            clock.tick(60)
        
        
    
if __name__ == "__main__":
    main_Menu()