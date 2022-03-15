
import pygame
from pygame.locals import *

import fonctions as FCT
from pieces import CPieces
import variables as VAR


class CGrille():
    def __init__(self, moteur):
        self.MOTEUR = moteur

        self.offX, self.offY = self.MOTEUR.location
        self.dimX, self.dimY = VAR.DIMENSION
        self.zones = FCT.GenereMat2D(self.dimX, self.dimY, "")

        self.couleur_fond_grille = (28, 28, 28, 255)
        self.couleur_contour_grille = (16,16,16,255)

    def afficher(self):
        t = VAR.TAILLE
        for y in range(self.dimY):
            for x in range(self.dimX):
                pX = self.offX + (x * t)
                pY = self.offY + (y * t)
                
                if self.zones[x][y] == "":
                    pygame.draw.rect(VAR.fenetre, self.couleur_fond_grille, (pX, pY, t, t), 0)
                    pygame.draw.rect(VAR.fenetre, self.couleur_contour_grille, (pX, pY, t, t), 1)
                else:
                    pygame.draw.rect(VAR.fenetre, CPieces.pieces_couleurs[self.zones[x][y]], (pX, pY, t, t), 0)
                    pygame.draw.rect(VAR.fenetre, self.couleur_contour_grille, (pX, pY, t, t), 1)
