from tkinter import *
from random import randint

fenetre = Tk()

fenetre.title('The Snake')

hauteur = fenetre.winfo_screenheight()
largeur = fenetre.winfo_screenwidth()

H = str(int(hauteur/1.1))
L = str(int(largeur/2))

fenetre.geometry(L + "x" + H + "+0+0")

LargeurPlateau = largeur /2
HauteurPlateau = hauteur /1.2

Plateau = Canvas(fenetre, width = LargeurPlateau, height = HauteurPlateau, bg = "black")
Plateau.pack(side="bottom")

Barre = Text(fenetre, width = int(largeur /2), height = int(HauteurPlateau / 10), bg = "light blue")
Barre.pack(side="top")
Barre.insert(END, "score: 0\n")

NombreDeCases= 40 #Faut changer ca pour la taille de la map

LargeurCase = (LargeurPlateau / NombreDeCases)
HauteurCase = (HauteurPlateau / NombreDeCases)

def remplir_case (x, y):

    OrigineCaseX1 = x * LargeurCase
    OrigineCaseY1 = y * HauteurCase
    OrigineCaseX2 = OrigineCaseX1 + LargeurCase
    OrigineCaseY2 = OrigineCaseY1 + HauteurCase

    Plateau.create_rectangle(OrigineCaseX1, OrigineCaseY1, OrigineCaseX2, OrigineCaseY2, fill="green")

def case_aleatoire():

    AleatoireX = randint(0, NombreDeCases - 1)
    AleatoireY = randint(0, NombreDeCases - 1)

    return (AleatoireX, AleatoireY)

def dessine_serpent(snake):

    for case in snake:

        x, y = case
        remplir_case(x, y)

def etre_dans_snake(case):

    if case in SNAKE:
        EtreDedans = 1
    else:
        EtreDedans = 0

    return EtreDedans

def fruit_aleatoire():

    FruitAleatoire = case_aleatoire()

    while (etre_dans_snake(FruitAleatoire)):
        FruitAleatoire = case_aleatoire

    return FruitAleatoire

def dessine_fruit():

    global FRUIT

    x, y = FRUIT

    OrigineCaseX1 = x * LargeurCase
    OrigineCaseY1 = y * HauteurCase
    OrigineCaseX2 = OrigineCaseX1 + LargeurCase
    OrigineCaseY2 = OrigineCaseY1 + HauteurCase

    Plateau.create_oval(OrigineCaseX1, OrigineCaseY1, OrigineCaseX2, OrigineCaseY2, fill = "red")

def left_key(event):
    global MOUVEMENT
    MOUVEMENT = (-1, 0)

def right_key(event):
    global MOUVEMENT
    MOUVEMENT = (1, 0)

def up_key(event):
    global MOUVEMENT
    MOUVEMENT = (0, -1)

def down_key(event):
    global MOUVEMENT
    MOUVEMENT = (0, 1)

fenetre.bind("<Left>", left_key)
fenetre.bind("<Right>", right_key)
fenetre.bind("<Up>", up_key)
fenetre.bind("<Down>", down_key)

def serpent_mort(NouvelleTete):

    global PERDU

    NouvelleTeteX, NouvelleTeteY = NouvelleTete

    if (etre_dans_snake(NouvelleTete) and MOUVEMENT != (0, 0)) or NouvelleTeteX < 0 or NouvelleTeteY < 0 or NouvelleTeteX >= NombreDeCases or NouvelleTeteY >= NombreDeCases:
        PERDU = 1

def mise_a_jour_score():

    global SCORE

    SCORE = SCORE + 1
    Barre.delete(0.0, 3.0)
    Barre.insert(END, "score: " + str(SCORE) + "\n")

def mise_a_jour_snake():

    global SNAKE, FRUIT

    (AncienneTeteX, AncienneTeteY) = SNAKE[0]
    MouvementX, MouvementY = MOUVEMENT
    NouvelleTete = (AncienneTeteX + MouvementX, AncienneTeteY + MouvementY)
    serpent_mort(NouvelleTete)
    SNAKE.insert(0, NouvelleTete)

    if NouvelleTete == FRUIT:
        FRUIT = fruit_aleatoire()
        mise_a_jour_score()

    else:
        SNAKE.pop()

def reinitialiser_jeu():

    global SNAKE, FRUIT, MOUVEMENT, SCORE, PERDU

    SNAKE = [case_aleatoire()]
    FRUIT = fruit_aleatoire()
    MOUVEMENT = (0,0)
    SCORE = 0
    PERDU = 0

def tache():

    fenetre.update
    fenetre.update_idletasks()
    mise_a_jour_snake()
    Plateau.delete("all")
    dessine_fruit()
    dessine_serpent(SNAKE)

    if PERDU:
        Barre.delete(0.0, 3.0)
        Barre.insert(END, "Perdu avec un score de " + str(SCORE))
        reinitialiser_jeu()
        fenetre.after(70, tache)
    else:
        fenetre.after(70, tache)

SNAKE = [case_aleatoire()]
FRUIT = fruit_aleatoire()
MOUVEMENT = (0, 0)
SCORE = 0
PERDU = 0
fenetre.after(0, tache())
fenetre.mainloop()