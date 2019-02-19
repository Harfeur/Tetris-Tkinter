from tkinter import Tk, Canvas, PhotoImage
from itertools import product
from random import randrange
from pieces import FORMES
from time import sleep

SIZE = 900
TAILLE_CARRE = SIZE//20 - 1
X0 = SIZE//2-5*TAILLE_CARRE
Y0 = SIZE//2-10*TAILLE_CARRE

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

def afficher(x, y, color):
    posX0 = X0+x*TAILLE_CARRE
    posY0 = Y0+y*TAILLE_CARRE
    cnv.create_rectangle(posX0, posY0, posX0+TAILLE_CARRE, posY0+TAILLE_CARRE, fill=color, tag=(str(y)))

def init_piece(piece):
    global GrilleDeJeu
    x = 3
    for i in range(len(piece[0])):
        for j in range(len(piece)):
            if piece[i][j] == 1:
                if GrilleDeJeu[i][j] == 2:
                    return False
                GrilleDeJeu[i][j] = 1
                print(GrilleDeJeu)
                afficher(j, i, 'yellow')
    return True

def descente():
    global GrilleDeJeu
    end = False
    for i,j in product(range(20), range(10)):
        if i == 0 and GrilleDeJeu[19-i][j] == 1:
            end = True
        if not end and GrilleDeJeu[19-i][j] == 1:
            if GrilleDeJeu[20-i][j] == 2:
                end = True
            GrilleDeJeu[20-i][j] = 1
            GrilleDeJeu[19-i][j] = 0
            cnv.delete(str(19-i))
            afficher(j, 19-i, 'yellow')
        
        if end == True:
            if GrilleDeJeu[19-i][j] == 1:
                GrilleDeJeu[19-i][j] == 2
    if end:
        return False
    return True
            

def init_game():
    for i,j in product(range(10), range(20)):
        afficher(i,j, 'gray20')
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

def game():
    while (True):
        piece = FORMES[randrange(7)]
        jeu = init_piece(piece[0])
        if not jeu:
            return False
        cnv.update()
        sleep(1)
        etatPiece = True
        while (etatPiece):
            etatPiece = descente()
            cnv.update()
            sleep(1)


def clic(event):
    if 747 < event.x < 874 and 762 < event.y <834:
        game()
        print("Fini")
 
def pos(event):
    print(event.x, event.y)

root = Tk()

cnv = Canvas(root, width=SIZE, height=SIZE, background="white")
cnv.pack()

init_game()

startImg = PhotoImage(file="assets/start.gif")
cnv.create_image(SIZE-SIZE//10, SIZE-SIZE//10, image=startImg)

root.bind("<Button>", clic)
#root.bind("<Motion>", pos)

root.mainloop()