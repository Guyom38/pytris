
import pygame
from pygame.locals import *

from pieces import CPieces

import variables as VAR
import fonctions as FCT

class CGrille():
    def calcul_offSets_Global():
        j = 0
        if VAR.joueur_clavier: j = 1
        
        largeur_grilles = (VAR.nbManettes +j) * ((VAR.DIMENSION[0] * VAR.TAILLE)+VAR.ECARTX) -VAR.ECARTX
        hauteur = (VAR.DIMENSION[1] * VAR.TAILLE)
        
        offsetX = (VAR.RESOLUTION[0] - largeur_grilles) //2
        offsetY = ((VAR.RESOLUTION[1] - hauteur -  int(VAR.RESOLUTION[1] * 0.05)) //2 )  
                 
        return (offsetX, offsetY)
    
    def __init__(self, moteur):
        self.Moteur = moteur

        self.offX, self.offY = (0, 0)
        self.dimX, self.dimY = VAR.DIMENSION
        self.zones = FCT.GenereMat2D(self.dimX, self.dimY, "")

        self.couleur_fond_grille = (28, 28, 28, 200)
        self.couleur_cellule = (16,16,16,255)
        self.couleur_contour_grille = (128,128,128,200)
        
        self.image = None
        self.calcul_offsets()
        
        self.cadreHaut = (0, 0, 0, 0)
        self.cadreBas = (0, 0, 0, 0)
    
    def calcul_offsets(self):
        offX, offY = CGrille.calcul_offSets_Global()
        
        j = 0
        if VAR.joueur_clavier: j = 1
        
        x = (self.Moteur.id+j) * ((VAR.DIMENSION[0] * VAR.TAILLE)+VAR.ECARTX)
        self.offX, self.offY = offX + x, offY
     
    
    def dessiner_grille(self):
        t = VAR.TAILLE
        dim = VAR.TAILLE * 5
        self.image = FCT.image_vide((self.dimX * t)+40, (self.dimY * t)+40+ (dim*2))
        #self.image = FCT.image_vide((self.dimX * t)+40, VAR.RESOLUTION[1])
        
        # --- Cadre piece Suivante
        
        self.cadreHaut = [5, 5, (self.dimX * t)+30, dim]
        self.cadreBas = [5, 5 + (self.dimY * t)+dim+30, (self.dimX * t)+30, dim]
        pygame.draw.rect(self.image, self.Moteur.couleur, self.cadreHaut,0)
        pygame.draw.rect(self.image, self.Moteur.couleur, self.cadreBas ,0)
        
   
        
        # --- Grille 
        pygame.draw.rect(self.image, (40,40,40,230), (20, 20 + dim, (self.dimX * t)+2, (self.dimY * t)+2),0)
        pygame.draw.rect(self.image, self.couleur_contour_grille, (5, 5 + dim, (self.dimX * t)+30, (self.dimY * t)+30),4)
        for y in range(self.dimY):
            for x in range(self.dimX):
                pX = (x * t)
                pY = (y * t)
                
                #if self.zones[x][y] == "":
                if VAR.mode_bmp:
                    self.image.blit(VAR.IMAGES["X"][0], (pX +20, pY+20+dim))
                else:
                    pygame.draw.rect(self.image, self.couleur_fond_grille, (pX+20, pY+20+dim, t, t), 0)
                    pygame.draw.rect(self.image, self.couleur_cellule, (pX+20, pY+20+dim, t, t), 1)
                    
      
    def afficher_lignes_en_attente_detre_ajoutees(self):
        if self.Moteur.Mecanique.lignesAjouter == 0: return
        if self.Moteur.Mecanique.lignesAjouter > VAR.limiteLignesEnAttente: self.Moteur.Mecanique.lignesAjouter = VAR.limiteLignesEnAttente
        
        for i in range(self.Moteur.Mecanique.lignesAjouter):
            VAR.fenetre.blit(VAR.IMAGES["#"][0], (self.offX + (VAR.DIMENSION[0] * VAR.TAILLE) + 4, self.offY + (i * (VAR.TAILLE + 4))))
        
        
    def afficher(self):
                
        dim = VAR.TAILLE * 5
        t = VAR.TAILLE
         
        if self.image == None : self.dessiner_grille()
        self.calcul_offsets()
        
        if VAR.pouvoirId == self.Moteur.id:
            #pygame.draw.rect(VAR.fenetre, (200, 200, 200, 100), (self.offX-5, self.offY+ (self.dimY * t) +20, (self.dimX * t)+10, 10),0)
            pX, pY, dimX, dimY = self.offX-15, 0, (self.dimX * t)+30, VAR.RESOLUTION[1]
            image_pouvoir = FCT.image_vide(dimX, dimY)
            pygame.draw.rect(image_pouvoir, (32, 32, 32, 150), (0, 0, dimX, dimY ),0)
            VAR.fenetre.blit(image_pouvoir, (pX, pY))

        
        VAR.fenetre.blit(self.image, (self.offX-20, self.offY-20-dim))
       
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
                        
        self.afficher_lignes_en_attente_detre_ajoutees()
                        
