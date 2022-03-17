import pygame
from pygame.locals import *

import time
import variables as VAR
import fonctions as FCT

hauteur = 0
largeur = 0
cadreX = 0
cadreY = 0
HAUTEURCELLULE = 100

def afficher_highscore():
    global hauteur, largeur, cadreX, cadreY

    
    hauteur = ((VAR.nbJoueurs+2) * HAUTEURCELLULE )
    largeur = VAR.RESOLUTION[0] * 0.66
    

    cadre = FCT.image_vide(largeur, hauteur)
    pygame.draw.rect(cadre, (64,64,64,220), (0, 0, largeur, hauteur), 0)
    pygame.draw.rect(cadre, (32,200,32,240), (0, 0, largeur, hauteur), 4)

    cadreX = (VAR.RESOLUTION[0] - largeur ) // 2
    cadreY = (VAR.RESOLUTION[1] - hauteur) // 2
    VAR.fenetre.blit(cadre, (cadreX, cadreY))
    afficher_joueurs_dans_l_ordre()


def afficher_joueurs_dans_l_ordre():
    liste_scores = []
    for i in range(VAR.nbJoueurs):
        liste_scores.append((VAR.tetris_joueurs[i].Partie.score, i))
    
    rang = VAR.nbJoueurs
    liste_triee = sorted(liste_scores)
    for score,i in liste_triee:
        afficher_joueur(i)
        rang-=1

    
def afficher_joueur(i):
    global hauteur, largeur, cadreX, cadreY

    joueur = VAR.tetris_joueurs[i]
    j = joueur.rang

    cadre = FCT.image_vide(largeur - 10, HAUTEURCELLULE - 10)
    pygame.draw.rect(cadre, (80,80,80,220), (0, 0, largeur - 10, HAUTEURCELLULE - 10), 0)
    pygame.draw.rect(cadre, (128,128,128,240), (0, 0, largeur - 10, HAUTEURCELLULE - 10), 4)

    VAR.fenetre.blit(cadre, (cadreX, cadreY + (j * HAUTEURCELLULE)))


