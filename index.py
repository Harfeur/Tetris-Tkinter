from tkinter import Tk, Canvas, PhotoImage, ALL
from itertools import product
from random import randrange
from pieces import FORMES

SIZE = 700
TAILLE_CARRE = SIZE//20 - 1
X0 = SIZE//2-5*TAILLE_CARRE
Y0 = SIZE//2-10*TAILLE_CARRE
COLORS=["gray60", None, "red", "yellow", "green", "blue", "purple", "orange", "brown", "white","gray20"]

GrilleDeJeu = []
score = 0
level = 0
futurePieceNumber = randrange(7)
IDs = []
x = 0
y = 0
game_started = False
after_id = None
time = 0

high_score = open("high_scores.txt", "r")
high_score_text = high_score.read()

def afficher(x, y, pieceNumber, GrilleDeJeu):
    global IDs
    posX0 = X0+x*TAILLE_CARRE
    posY0 = Y0+y*TAILLE_CARRE
    if GrilleDeJeu[y][x] == 1:
        color = COLORS[pieceNumber+2]
    else:
        color = COLORS[GrilleDeJeu[y][x]]
    IDs.append(cnv.create_rectangle(posX0, posY0, posX0+TAILLE_CARRE, posY0+TAILLE_CARRE, fill=color))

def update_affichage(GrilleDeJeu, pieceNumber):
    global IDs, textScore
    for x in IDs:
        cnv.delete(x)
    IDs = []
    for i,j in product(range(20), range(10)):
        afficher(j, i, pieceNumber, GrilleDeJeu)
    scoreText = "Score : " + str(score)
    cnv.itemconfig(textScore, text=scoreText)
    cnv.update()

def init_piece(GrilleDeJeu, piece):
    global x,y
    x = 3
    y = 0
    for i in range(len(piece[0])):
        for j in range(len(piece)):
            if piece[i][j] == 1:
                if GrilleDeJeu[i][j+x] > 2:
                    return GrilleDeJeu, False
                GrilleDeJeu[i][j+x] = 1
    return GrilleDeJeu, True

def descente(GrilleDeJeu, pieceNumber):
    global y
    oldGrille = []
    for i in range(20):
        L = []
        for j in range(10):
            L.append(GrilleDeJeu[i][j])
        oldGrille.append(L)

    end = False

    for i,j in product(range(20), range(10)):
        i = 19-i
        if i == 19 and GrilleDeJeu[i][j] == 1:
            end = True
        if not end and GrilleDeJeu[i][j] == 1:
            if 10 > GrilleDeJeu[i+1][j] > 1:
                end = True
            else:
                GrilleDeJeu[i+1][j] = 1
                GrilleDeJeu[i][j] = 0
            
        if end:
            GrilleDeJeu = oldGrille
            for i,j in product(range(20), range(10)):
                if GrilleDeJeu[i][j] == 1:
                    GrilleDeJeu[i][j] = pieceNumber+2
            return False, GrilleDeJeu
    y+=1
    return True, GrilleDeJeu

def ombre(GrilleDeJeu, pieceNumber):
    global y
    oldY = y
    etat= False
    Ombre = []
    Ngdj = []
    for i in range(20):
        L = []
        for j in range(10):
            if GrilleDeJeu[i][j]==1:
                etat = True
            if GrilleDeJeu[i][j]==10:
                L.append(0)
                GrilleDeJeu[i][j] = 0
            else:
                L.append(GrilleDeJeu[i][j])
        Ngdj.append(L)
        Ombre.append(L)
    if not etat:
        return GrilleDeJeu
    while etat:
        etat,Ngdj=descente(Ngdj, pieceNumber)
        if etat:
            Ombre = []
            for i in range(20):
                L = []
                for j in range(10):
                    L.append(Ngdj[i][j])
                Ombre.append(L)

    for i,j in product(range(20), range(10)):
        if Ombre[i][j] == 1 and GrilleDeJeu[i][j] != 1:
            GrilleDeJeu[i][j]=10
    y = oldY
    return GrilleDeJeu

def init_game():
    global GrilleDeJeu, score
    GrilleDeJeu = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
    ]
    update_affichage(GrilleDeJeu, 0)
    score = 0

def game():
    init_game()
    global etatPiece, imageDepart, game_started
    cnv.delete(imageDepart)
    etatPiece = False
    game_started = True
    cnv_in_game()

def cnv_in_game():
    global GrilleDeJeu, pieceNumber, etatPiece, pieceRotation, futurePieceNumber, after_id, time, score
    time = 500 - (50 * level//10)
    if not etatPiece:
        GrilleDeJeu = check_ligne_complete(GrilleDeJeu)
        pieceRotation = 0
        pieceNumber = futurePieceNumber
        futurePieceNumber = randrange(7)
        piece = FORMES[pieceNumber]
        GrilleDeJeu, jeu = init_piece(GrilleDeJeu, piece[0])
        if not jeu:
            cnv.create_text(SIZE//2, SIZE//2, text="Game Over !", font=('Helvetica', 50), fill='white')
            cnv.create_text(SIZE//2, SIZE//2,text=score, font=('Helvetica', 20), fill='black')
            return
            
        GrilleDeJeu = ombre(GrilleDeJeu, pieceNumber)
        update_affichage(GrilleDeJeu, pieceNumber)
        after_id = cnv.after(time, cnv_in_game)
        etatPiece = True
    else:
        etatPiece, GrilleDeJeu = descente(GrilleDeJeu, pieceNumber)
        GrilleDeJeu = ombre(GrilleDeJeu, pieceNumber)
        update_affichage(GrilleDeJeu, pieceNumber)
        if not etatPiece:
            cnv_in_game()
        else:
            after_id = cnv.after(time, cnv_in_game)

def cancel():
    global after_id
    if after_id is not None:
        cnv.after_cancel(after_id)
        after_id = None

def check_ligne_complete(GrilleDeJeu):
    global score, level
    session = 0
    for i in range(20):
        state = True
        for j in range(10):
            if GrilleDeJeu[i][j] == 0:
                state = False
                break
        if state:
            session+=1
            level+=1
            for j in range(10):
                GrilleDeJeu[i][j] = 9
            update_affichage(GrilleDeJeu, pieceNumber)
            for j in range(10):
                GrilleDeJeu[i][j] = 0
            for ii in range(i-1, -1, -1):
                for j in range(10):
                    GrilleDeJeu[ii+1][j] = GrilleDeJeu[ii][j]
            update_affichage(GrilleDeJeu, pieceNumber)
    if session == 1:
        score += 40 * (level//10 + 1)
    elif session == 2:
        score += 100 * (level//10 + 1)
    elif session == 3:
        score += 300 * (level//10 + 1)
    elif session == 4:
        score += 1200 * (level//10 + 1)
    return GrilleDeJeu

def clic(event):
    global game_started
    if not game_started:
        game()

def changement(GrilleDeJeu):
    global pieceRotation, x, y
    oldGrille = []
    for i in range(20):
        L = []
        for j in range(10):
            L.append(GrilleDeJeu[i][j])
        oldGrille.append(L)
    
    for i,j in product(range(20), range(10)):
        if GrilleDeJeu[i][j] == 1:
            GrilleDeJeu[i][j] = 0
    
    if len(FORMES[pieceNumber])-1 == pieceRotation:
        nouvelleRotation = 0 
    else:
        nouvelleRotation = pieceRotation + 1

    nouvellePiece = FORMES[pieceNumber][nouvelleRotation]

    for i,j in product(range(len(nouvellePiece)), range(len(nouvellePiece[0]))):
        if nouvellePiece[i][j] == 1:
            if x+j>=0 and x+j<10 and GrilleDeJeu[y+i][x+j] < 2:
                GrilleDeJeu[y+i][x+j] = 1
            else:
                return oldGrille

    pieceRotation = nouvelleRotation
    return ombre(GrilleDeJeu, pieceNumber)

def move(sens, GrilleDeJeu):
    global x, game_started
    if not game_started:
        return
    oldGrille = []
    for i in range(20):
        L = []
        for j in range(10):
            L.append(GrilleDeJeu[i][j])
        oldGrille.append(L)

    if sens == 0:
        for i,j in product(range(20), range(10)):
            if GrilleDeJeu[i][j] == 1:
                if j == 0:
                    return oldGrille
                if GrilleDeJeu[i][j-1] > 0:
                    return oldGrille
                GrilleDeJeu[i][j-1] = 1
                GrilleDeJeu[i][j] = 0

    else:
        for i,j in product(range(19, -1, -1), range(9, -1, -1)):
            if GrilleDeJeu[i][j] == 1:
                if j == 9:
                    return oldGrille
                if GrilleDeJeu[i][j+1] > 0:
                    return oldGrille
                GrilleDeJeu[i][j+1] = 1
                GrilleDeJeu[i][j] = 0
    if sens == 0:
        x -= 1
    else:
        x += 1
    GrilleDeJeu = ombre(GrilleDeJeu, pieceNumber)
    return GrilleDeJeu

def touches(event):
    t = event.keysym
    global GrilleDeJeu, etatPiece, after_id, time
    if t == "Left":
        GrilleDeJeu = move(0, GrilleDeJeu)
        update_affichage(GrilleDeJeu, pieceNumber)
    elif t == "Right":
        GrilleDeJeu = move(1, GrilleDeJeu)
        update_affichage(GrilleDeJeu, pieceNumber)
    elif t == "Up":
        GrilleDeJeu = changement(GrilleDeJeu)
        
        update_affichage(GrilleDeJeu, pieceNumber)
    elif t == "Down":
        if not etatPiece:
            return
        #cancel()
        etatPiece, GrilleDeJeu = descente(GrilleDeJeu, pieceNumber)
        #after_id = cnv.after(time, cnv_in_game)
        update_affichage(GrilleDeJeu, pieceNumber)


root = Tk()

cnv = Canvas(root, width=SIZE, height=SIZE, background="white")
cnv.pack()

startImg = PhotoImage(file="assets/start.gif")
imageDepart = cnv.create_image(SIZE//2, SIZE//2, image=startImg)
cnv.create_text(SIZE//2+6*TAILLE_CARRE, 100, text=high_score_text, font=('Helvetica', '16'), anchor='nw')
textScore = cnv.create_text(10, 100, text="", font=('Helvetica', '20'), anchor='nw')

root.bind("<Button>", clic)
root.bind("<Key>", touches)

root.mainloop()