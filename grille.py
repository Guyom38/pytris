
import pygame
from pygame.locals import *

from pieces import CPieces

import variables as VAR
import fonctions as FCT

class CGrille():
    def __init__(self, moteur):
        print("        + GRILLE")

        self.Moteur = moteur

        self.offX, self.offY = self.Moteur.location
        self.dimX, self.dimY = VAR.DIMENSION
        self.zones = FCT.GenereMat2D(self.dimX, self.dimY, "")

        self.couleur_fond_grille = (28, 28, 28, 200)
        self.couleur_cellule = (16,16,16,255)
        self.couleur_contour_grille = (128,128,128,200)
        
        self.image = None
        
    def dessiner_grille(self):
        t = VAR.TAILLE
        self.image = FCT.image_vide((self.dimX * t)+40, (self.dimY * t)+140)
        
        
        pygame.draw.rect(self.image, self.couleur_fond_grille, (5, 5, 100, 100),0)
        pygame.draw.rect(self.image, self.couleur_contour_grille, (5, 5, 100, 100),4)
        
        pygame.draw.rect(self.image, self.couleur_contour_grille, (5, 105, (self.dimX * t)+30, (self.dimY * t)+30),4)
        for y in range(self.dimY):
            for x in range(self.dimX):
                pX = (x * t)
                pY = (y * t)
                
                #if self.zones[x][y] == "":
                if VAR.mode_bmp:
                    self.image.blit(VAR.IMAGES["X"][0], (pX +20, pY+120))
                else:
                    pygame.draw.rect(self.image, self.couleur_fond_grille, (pX+20, pY+120, t, t), 0)
                    pygame.draw.rect(self.image, self.couleur_cellule, (pX+20, pY+120, t, t), 1)
                    
      
        
    def afficher(self):
        if self.image == None : self.dessiner_grille()
        
        VAR.fenetre.blit(self.image, (self.offX-20, self.offY-120))
        t = VAR.TAILLE
        for y in range(self.dimY):
            for x in range(self.dimX):
                pX = self.offX + (x * t)
                pY = self.offY + (y * t)
                
                if self.zones[x][y] != "":
                    if VAR.mode_bmp:
                        VAR.fenetre.blit(VAR.IMAGES[self.zones[x][y]][0], (pX, pY))
                    else:
                        pygame.draw.rect(VAR.fenetre, CPieces.pieces_couleurs[self.zones[x][y]], (pX, pY, t, t), 0)
                        pygame.draw.rect(VAR.fenetre, self.couleur_contour_grille, (pX, pY, t, t), 1)
