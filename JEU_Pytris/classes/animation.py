
from re import M
import pygame
from pygame.locals import *

from JEU_Pytris.classes.pieces import CPieces
import JEU_Pytris.variables as VAR

import COMMUN.variables as V
from COMMUN.classes.fonctions import *
import COMMUN.classes.fonctions as FCT


class CAnimation:
    def __init__(self, m):
        self.Moteur = m

        self.cycle = 0
        self.frequence = 20
        self.cpt = 0
        self.anime = False

        self.init_mort()
        self.init_niveau_sup()
        self.init_destruction_de_lignes()

        self.niv_sup = False
        self.destr_lignes = False

    def rythme(self):
        if pygame.time.get_ticks() - self.cycle > self.frequence:
            self.anime = True
            self.cpt += 1
            VAR.animation_cpt += 1
            self.cycle = pygame.time.get_ticks()

    def afficher(self):
        self.rythme()

        self.afficher_animation_gameover()
        self.afficher_animation_niveau_superieur()
        self.afficher_animation_destruction_de_lignes()
        self.sprite_score()
        
        self.anime = False

# -------------------------------------------------------- ANIMATION GAMEOVER
    def init_mort(self):
        self.mortActif = False
        self.mortY = 0

    def meurt(self):
        self.mortActif = True
        self.mortY = VAR.DIMENSION[1]-1

    def afficher_animation_gameover(self):
        if self.mortActif and self.anime:
            for x in range(VAR.DIMENSION[0]):
                self.Moteur.grille.zones[x][self.mortY] = "#"
            self.mortY -= 1

            if self.mortY == -1: self.mortActif = False
            
# -------------------------------------------------------- ANIMATION NIVEAU SUPERIEUR
    def init_niveau_sup(self):
        self.nivSupActif = False
        self.nivSupAlpha = 255

    def afficher_animation_niveau_superieur(self):
        if self.nivSupActif:
            largeur, hauteur = (VAR.DIMENSION[0] * VAR.TAILLE), (VAR.DIMENSION[1] * VAR.TAILLE)

            image = GIMAGE.image_vide(largeur, 60)
            image.fill((16, 16, 16, self.nivSupAlpha))

            couleur =  (self.Moteur.Joueur.couleur[0],  self.Moteur.Joueur.couleur[1],  self.Moteur.Joueur.couleur[2], self.nivSupAlpha)
            pygame.draw.rect(image, couleur, (0, 0, image.get_width(), image.get_height()), 4)
            
            image_texte =FCT.GFONT.get_image_texte("NIVEAU " + str(self.Moteur.Partie.niveau), 20, (255,255,255,self.nivSupAlpha))

            pX = (image.get_width() - image_texte.get_width()) // 2
            pY = (image.get_height() - image_texte.get_height()) // 2
            image.blit(image_texte, (pX, pY))

            pX = (largeur - image.get_width()) // 2
            pY = (hauteur - image.get_height()) // 2
            V.fenetre.blit(image, (self.Moteur.grille.offX, self.Moteur.grille.offY+ pY ))

            if self.anime:
                self.nivSupAlpha -= 8
                if self.nivSupAlpha <= 10:
                    self.nivSupAlpha = 255
                    self.nivSupActif = False        

# -------------------------------------------------------- ANIMATION DESTRUCTION DE LIGNE
    def init_destruction_de_lignes(self):
        self.destLignesActif = False
        self.destLignesX = 0


    def afficher_animation_destruction_de_lignes(self):
        if self.destLignesActif and self.anime:
            listeLignes = self.Moteur.Mecanique.lignesADetruire
            nbLignes = len(listeLignes)

            if self.destLignesX == 0 and nbLignes > 0: self.Moteur.Partie.fige_le_temps()
            if nbLignes > 0:
                for y in listeLignes:
                    if self.destLignesX < VAR.DIMENSION[0]:                         # --- Ajoute un delais supplémentaire avec la derniere case
                        self.Moteur.grille.zones[self.destLignesX][y] = ""
                
                self.destLignesX+=1
                if self.destLignesX > VAR.DIMENSION[0]: 
                    self.destLignesX = 0
                    self.Moteur.Mecanique.detruire_lignes(listeLignes)
                    self.Moteur.Mecanique.balance_les_lignes(nbLignes)
                    self.Moteur.Mecanique.lignesADetruire = []
            else:
                self.destLignesActif = False
                self.Moteur.Partie.libere_le_temps()




    def sprite_score(self):
        pass
