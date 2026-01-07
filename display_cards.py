import pygame, os, math
from shuffle import shuffle_and_deal
from logic import find_winner

WIDTH, HEIGHT = 1000, 800
BG = (0,128,0)
WHITE = (255,255,255)
BLACK = (30,30,30)
GOLD = (255,215,0)

CARDS = 3

def display_cards(n, names):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None,24)
    btnf = pygame.font.SysFont(None,22)

    BASE = os.path.dirname(__file__)
    IMG = os.path.join(BASE,"images")

    CARD_W = max(55, min(75, WIDTH//(n*2)))
    CARD_H = int(CARD_W*1.4)
    GAP = int(CARD_W*0.2)

    back = pygame.image.load(os.path.join(IMG,"back.png")).convert_alpha()
    back = pygame.transform.smoothscale(back,(CARD_W,CARD_H))

    hands = shuffle_and_deal(n)

    def load():
        out=[]
        for h in hands:
            row=[]
            for c in h:
                img=pygame.image.load(os.path.join(IMG,f"{c}.png")).convert_alpha()
                img=pygame.transform.smoothscale(img,(CARD_W,CARD_H))
                row.append(img)
            out.append(row)
        return out

    imgs = load()
    flipped = [False]*n
    winner = None

    cx,cy = WIDTH//2, HEIGHT//2
    r = min(WIDTH,HEIGHT)*0.35
    step = 2*math.pi/n

    def btn(rect,text):
        pygame.draw.rect(screen,BLACK,rect,0,8)
        t=btnf.render(text,True,WHITE)
        screen.blit(t,t.get_rect(center=rect.center))

    shuffle_btn = pygame.Rect(cx-160,cy-20,140,40)
    show_btn    = pygame.Rect(cx+20,cy-20,160,40)
    again_btn   = pygame.Rect(cx-80,cy+40,160,40)

    show_again = False

    while True:
        clock.tick(60)

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit(); return

            if e.type==pygame.MOUSEBUTTONDOWN:
                mx,my = e.pos

                # ---------- SHUFFLE ----------
                if shuffle_btn.collidepoint(mx,my):
                    hands = shuffle_and_deal(n)
                    imgs = load()
                    flipped = [False]*n
                    winner = None
                    show_again = False

                # ---------- DISPLAY ALL ----------
                if show_btn.collidepoint(mx,my):
                    flipped = [True]*n
                    if not winner:
                        players={names[i]:hands[i] for i in range(n)}
                        winner,_ = find_winner(players)
                        show_again = True

                # ---------- PLAY AGAIN ----------
                if show_again and again_btn.collidepoint(mx,my):
                    hands = shuffle_and_deal(n)
                    imgs = load()
                    flipped = [False]*n
                    winner = None
                    show_again = False

                # ---------- PLAYER FLIP (FIXED) ----------
                for i,b in enumerate(flip_btns):
                    if b.collidepoint(mx,my) and not flipped[i]:
                        flipped[i] = True
                        if all(flipped) and not winner:
                            players={names[k]:hands[k] for k in range(n)}
                            winner,_ = find_winner(players)
                            show_again = True

        screen.fill(BG)
        flip_btns=[]

        for i in range(n):
            ang=i*step-math.pi/2
            px=cx+r*math.cos(ang)
            py=cy+r*math.sin(ang)

            w=CARDS*CARD_W+(CARDS-1)*GAP
            sx=px-w/2
            y=py-CARD_H/2

            for j in range(CARDS):
                screen.blit(imgs[i][j] if flipped[i] else back,
                            (sx+j*(CARD_W+GAP),y))

            # ---------- WINNER ----------
            if winner and winner[0]==names[i]:
                wt=font.render("WINNER",True,GOLD)
                screen.blit(wt,wt.get_rect(center=(px,y-18)))

            # ---------- NAME ----------
            name_y=y+CARD_H+8
            screen.blit(font.render(names[i],True,WHITE),(px-20,name_y))

            # ---------- FLIP BUTTON ----------
            b=pygame.Rect(px-35,name_y+18,70,26)
            btn(b,"FLIP" if not flipped[i] else "DONE")
            flip_btns.append(b)

        btn(shuffle_btn,"SHUFFLE")
        btn(show_btn,"DISPLAY ALL")
        if show_again:
            btn(again_btn,"PLAY AGAIN")

        pygame.display.flip()
