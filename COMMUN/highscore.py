import pygame
from pygame.locals import *

import JEU_Pytris.variables as VAR
from COMMUN.classes.fonctions import *
import COMMUN.variables as V
import COMMUN.classes.fonctions as FCT


class CHighscore():
    def __init__(self, c):
        self.C = c
        self.dimX, self.dimY = 0, 0
        self.cycle, self.frequence, self.start = 0, 200, True
        self.dimX = V.RESOLUTION[0] * 0.9
        self.dimY = V.RESOLUTION[1] // 15          # 3 titre + 10 joueurs + 2 bouton 
         
    def afficher(self):       
       
        self.afficher_cadre_fond()
        self.afficher_titre()
        
        liste_scores = []
        for i, moteur in V.moteurs.items():
            liste_scores.append((moteur.Partie.score, i))

        liste_triee = sorted(liste_scores, reverse=True)

        u = 0
        for score, i in liste_triee:
            self.afficher_joueur(V.moteurs[i], u)
            u += 1
            
        self.afficher_message()

    def afficher_cadre_fond(self):
        cadre = GIMAGE.image_vide(V.RESOLUTION[0] * 0.92, V.RESOLUTION[1])
        pygame.draw.rect(cadre, (16,16,16,150), (0,0, cadre.get_width(), cadre.get_height()), 0)
        pygame.draw.rect(cadre, (255,255,255,150), (0,0, cadre.get_width(), cadre.get_height()), 4)
        V.fenetre.blit(cadre, ((V.RESOLUTION[0] - cadre.get_width()) // 2, 0, cadre.get_width(), V.RESOLUTION[1]))                 
        
    def afficher_titre(self):
        image_titre = FCT.GFONT.get_image_texte("TABLEAU DES SCORES", 80, (0,0,0,255)) 
        x, y = ((V.RESOLUTION[0] - image_titre.get_width() ) // 2), ( ((self.dimY * 3) - image_titre.get_height()) // 2 )
        V.fenetre.blit(image_titre, (x-2, y-2))    
        image_titre = FCT.GFONT.get_image_texte("TABLEAU DES SCORES", 80, (255,255,255,255)) 
        x, y = ((V.RESOLUTION[0] - image_titre.get_width() ) // 2), ( ((self.dimY * 3) - image_titre.get_height()) // 2 )
        V.fenetre.blit(image_titre, (x, y))      
        
        
    def afficher_message(self):
        if pygame.time.get_ticks() - self.cycle > self.frequence:
            self.cycle = pygame.time.get_ticks()
            self.start = not self.start
        
        if self.start:            
            image_continue = FCT.GFONT.get_image_texte("APPUYEZ SUR START", 40, (255,255,255,255)) 
            x, y = ((V.RESOLUTION[0] - image_continue.get_width() ) // 2), V.RESOLUTION[1] - ( ((self.dimY * 3) - image_continue.get_height()) // 2 )
            V.fenetre.blit(image_continue, (x, y))      


    def afficher_joueur(self, moteur, i):
        dimCadreY = ((V.RESOLUTION[1] - (5 * self.dimY)) // V.get_nb_joueurs() )        
        cadre = FCT.GIMAGE.image_vide(self.dimX, dimCadreY)
        pygame.draw.rect(cadre, moteur.Joueur.couleur, (0, 0, self.dimX, dimCadreY-10))
                
        cX = ((V.RESOLUTION[0] - self.dimX) //2)
        y = (self.dimY * 3) + (i * (dimCadreY + 10))
        
        # --- Cadre
        V.fenetre.blit(cadre, (cX, y))
        
        x = 0
        for titreTxt, info, largeur in (("Rang", moteur.Partie.rang, 1), ("Nom", moteur.Joueur.nom, 15) , ("Niveau", moteur.Partie.niveau, 30), ("Nb. Lignes", moteur.Partie.nbLignes, 10), ("Score : ", moteur.Partie.score, 20)):
            x += ((V.RESOLUTION[0] / 100) * largeur)
            
            # --- Titre
            if i == 0:
                image = FCT.GFONT.get_image_texte(str(titreTxt), 20, (0,0,0,255)) 
                V.fenetre.blit(image, (x+cX-2, y-22))
                image = FCT.GFONT.get_image_texte(str(titreTxt), 20, (255,255,255,255)) 
                V.fenetre.blit(image, (x+cX, y-20))
                
            # --- Info    
            image = FCT.GFONT.get_image_texte(str(info), 60, (0,0,0,255)) 
            cY = ((dimCadreY + 10) - image.get_height()) // 2
            V.fenetre.blit(image, (x+cX-2, y+cY-2))
            image = FCT.GFONT.get_image_texte(str(info), 60, (255,255,255,255)) 
            V.fenetre.blit(image, (x+cX, y+cY))
        
        
        # -- AVATAR
        cY = (y + dimCadreY) - (780 * moteur.Joueur.Avatar.ratioY)
        moteur.Joueur.Avatar.dessiner(cX + 50, cY)
        
        
        