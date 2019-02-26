from tkinter import Tk, Canvas, PhotoImage, ALL
from itertools import product
from random import randrange
from pieces import FORMES
from time import sleep

SIZE = 900
TAILLE_CARRE = SIZE//20 - 1
X0 = SIZE//2-5*TAILLE_CARRE
Y0 = SIZE//2-10*TAILLE_CARRE
COLORS=["gray20", None, "red", "yellow", "green", "blue", "purple", "orange", "brown"]

GrilleDeJeu = []

def afficher(x, y, pieceNumber, GrilleDeJeu):
    posX0 = X0+x*TAILLE_CARRE
    posY0 = Y0+y*TAILLE_CARRE
    if GrilleDeJeu[y][x] == 1:
        color = COLORS[pieceNumber+2]
    else:
        color = COLORS[GrilleDeJeu[y][x]]
    cnv.create_rectangle(posX0, posY0, posX0+TAILLE_CARRE, posY0+TAILLE_CARRE, fill=color)

def update_():
    pass

def update_affichage(GrilleDeJeu, pieceNumber):
    cnv.delete(ALL)
    for i,j in product(range(20), range(10)):
        afficher(j, i, pieceNumber, GrilleDeJeu)
    cnv.update()

def init_piece(GrilleDeJeu, piece):
    global x,y
    x = 3
    y = 0
    print("Nouvelle pièce")
    for i in range(len(piece[0])):
        for j in range(len(piece)):
            if piece[i][j] == 1:
                if GrilleDeJeu[i][j+x] > 2:
                    return False
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
            if GrilleDeJeu[i+1][j] > 1:
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
            

def init_game():
    global GrilleDeJeu
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

def game():
    init_game()
    global etatPiece
    etatPiece = False
    cnv_in_game()


def cnv_in_game():
    global GrilleDeJeu, pieceNumber, etatPiece, pieceRotation
    time = 500
    if not etatPiece:
        pieceRotation = 0
        pieceNumber = randrange(7)
        piece = FORMES[pieceNumber]
        GrilleDeJeu, jeu = init_piece(GrilleDeJeu, piece[0])
        if not jeu:
            return False
        update_affichage(GrilleDeJeu, pieceNumber)
        cnv.after(time, cnv_in_game)
        etatPiece = True
    else:
        etatPiece, GrilleDeJeu = descente(GrilleDeJeu, pieceNumber)
        update_affichage(GrilleDeJeu, pieceNumber)
        cnv.after(time, cnv_in_game)

def clic(event):
    if 747 < event.x < 874 and 762 < event.y <834:
        game()
        print("Fini")

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
            if GrilleDeJeu[y+i][x+j] < 2 and x+j>=0:
                GrilleDeJeu[y+i][x+j] = 1
            else:
                return oldGrille

    pieceRotation = nouvelleRotation
    return GrilleDeJeu

def move(sens, GrilleDeJeu):
    global x
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
    return GrilleDeJeu

def touches(event):
    t = event.keysym
    global GrilleDeJeu, etatPiece
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
        etatPiece, GrilleDeJeu = descente(GrilleDeJeu, pieceNumber)
        update_affichage(GrilleDeJeu, pieceNumber)

root = Tk()

cnv = Canvas(root, width=SIZE, height=SIZE, background="white")
cnv.pack()

init_game()

startImg = PhotoImage(file="assets/start.gif")
cnv.create_image(SIZE-SIZE//10, SIZE-SIZE//10, image=startImg)

root.bind("<Button>", clic)
root.bind("<Key>", touches)

root.mainloop()