
import pygame
from pygame.locals import *

from JEU_Pytris.classes.pieces import CPieces
import JEU_Pytris.variables as VAR

import COMMUN.variables as V
from COMMUN.classes.fonctions import *

class CGrille:
    
    
    def calcul_offSets_Global():
        j = 0
        if V.joueur_clavier: j = 1
        
        largeur_grilles = (V.nbManettes +j) * ((VAR.DIMENSION[0] * VAR.TAILLE)+VAR.ECARTX) -VAR.ECARTX
        hauteur = (VAR.DIMENSION[1] * VAR.TAILLE)
        
        offsetX = (V.RESOLUTION[0] - largeur_grilles) //2
        offsetY = ((V.RESOLUTION[1] - hauteur -  int(V.RESOLUTION[1] * 0.05)) //2 )  
                 
        return (offsetX, offsetY)
    
    def __init__(self, m):
        self.Moteur = m

        self.offX, self.offY = (0, 0)
        self.dimX, self.dimY = VAR.DIMENSION
        self.zones = GBASE.GenereMat2D(self.dimX, self.dimY, "")

        self.couleur_fond_grille = (28, 28, 28, 200)
        self.couleur_cellule = (16,16,16,255)
        self.couleur_contour_grille = (128,128,128,200)
        
        self.image = None
        self.calcul_offsets()
        
        self.cadreHaut = (0, 0, 0, 0)
        self.cadreBas = (0, 0, 0, 0)
        
        self.margesDim = VAR.marge *2
        self.marges, self.margesL = (VAR.marge // 4), VAR.marge * 1.5
    
    
    def calcul_offsets(self):
        offX, offY = CGrille.calcul_offSets_Global()
        
        j = 0
        if V.joueur_clavier: j = 1
        
        x = (self.Moteur.Joueur.id+j) * ((VAR.DIMENSION[0] * VAR.TAILLE)+VAR.ECARTX)
        self.offX, self.offY = offX + x, offY
     
    
    def dessiner_grille(self):
        t = VAR.TAILLE
        grilleDimX, grilleDimY, dimCadre = self.dimX * t, self.dimY * t, VAR.TAILLE * 4
        self.image = GIMAGE.image_vide(grilleDimX + self.margesDim, grilleDimY + (dimCadre*2) + self.margesDim)
        
        # --- Cadre piece Suivante
        self.cadreHaut = [self.marges, self.marges, (self.dimX * t) + self.margesL, dimCadre]
        self.cadreBas = [self.marges, self.marges + (self.dimY * t) + dimCadre + self.margesL, (self.dimX * t) + self.margesL, dimCadre]
        pygame.draw.rect(self.image, self.Moteur.Joueur.couleur, self.cadreHaut, 0)
        pygame.draw.rect(self.image, self.Moteur.Joueur.couleur, self.cadreBas, 0)
       
        # --- Grille 
        pygame.draw.rect(self.image, (40,40,40,230), (VAR.marge, VAR.marge + dimCadre, (self.dimX * t)+2, (self.dimY * t)+2), 0)
        pygame.draw.rect(self.image, self.couleur_contour_grille, (self.marges, self.marges + dimCadre, (self.dimX * t) + self.margesL, (self.dimY * t) + self.margesL),4)
        
        for y in range(self.dimY):
            for x in range(self.dimX):
                pX, pY = (x * t),  (y * t)
           
                if VAR.mode_bmp:
                    self.image.blit(V.IMAGES["X"][0], (pX + VAR.marge, pY + dimCadre + VAR.marge))
                else:
                    pygame.draw.rect(self.image, self.couleur_fond_grille, (pX + VAR.marge, pY + dimCadre + VAR.marge, t, t), 0)
                    pygame.draw.rect(self.image, self.couleur_cellule, (pX + VAR.marge, pY + dimCadre + VAR.marge, t, t), 1)
                    
      
    def afficher_lignes_en_attente_detre_ajoutees(self):
        if self.Moteur.Mecanique.lignesAjouter == 0: return
        if self.Moteur.Mecanique.lignesAjouter > VAR.lignes_en_attente: self.Moteur.Mecanique.lignesAjouter = VAR.lignes_en_attente
        
        for i in range(self.Moteur.Mecanique.lignesAjouter):
            V.fenetre.blit(V.IMAGES["#"][0], (self.offX + (VAR.DIMENSION[0] * VAR.TAILLE) + 4, self.offY + (i * (VAR.TAILLE + 4))))
        
        
    def afficher(self):
        dimCadre, t = self.cadreHaut[3], VAR.TAILLE
        if self.image == None : self.dessiner_grille()
        self.calcul_offsets()
        
        if VAR.pouvoirId == self.Moteur.Joueur.id:
            pX, pY, dimX, dimY = self.offX-(VAR.marge-self.marges), 0, (self.dimX * t)+self.margesL, V.RESOLUTION[1]
            image_pouvoir = GIMAGE.image_vide(dimX, dimY)
            pygame.draw.rect(image_pouvoir, (32, 32, 32, 150), (0, 0, dimX, dimY ),0)
            V.fenetre.blit(image_pouvoir, (pX, pY))
        
        V.fenetre.blit(self.image, (self.offX-VAR.marge, self.offY-dimCadre-VAR.marge))
       
        for y in range(self.dimY):
            for x in range(self.dimX):
                pX = self.offX + (x * t)
                pY = self.offY + (y * t)
                
                if self.zones[x][y] != "":
                    if VAR.mode_bmp:
                        V.fenetre.blit(V.IMAGES[self.zones[x][y]][0], (pX, pY))
                    else:
                        pygame.draw.rect(V.fenetre, CPieces.pieces_couleurs[self.zones[x][y]], (pX, pY, t, t), 0)
                        pygame.draw.rect(V.fenetre, self.couleur_contour_grille, (pX, pY, t, t), 1)
                        
        self.afficher_lignes_en_attente_detre_ajoutees()
                        
