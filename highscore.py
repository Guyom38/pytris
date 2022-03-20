import pygame
from pygame.locals import *

import time, os
import variables as VAR
import fonctions as FCT

#     - 

class CHighscore():
    dimX, dimY = 0, 0
    cycle, frequence, start = 0, 200, True
         
    def afficher():
        CHighscore.dimX = VAR.RESOLUTION[0] * 0.9
        CHighscore.dimY = VAR.RESOLUTION[1] // 15          # 3 titre + 10 joueurs + 2 bouton 
       
        CHighscore.afficher_cadre_fond()
        CHighscore.afficher_titre()
        
        liste_scores = []
        for i in range(VAR.nbJoueurs):
            liste_scores.append((VAR.tetris_joueurs[i].Partie.score, i))

        liste_triee = sorted(liste_scores, reverse=True)

        u = 0
        for score, i in liste_triee:
            CHighscore.afficher_joueur(VAR.tetris_joueurs[i], u)
            u += 1
            
            
        CHighscore.afficher_message()

    def afficher_cadre_fond():
        cadre = FCT.image_vide(VAR.RESOLUTION[0] * 0.92, VAR.RESOLUTION[1])
        pygame.draw.rect(cadre, (16,16,16,150), (0,0, cadre.get_width(), cadre.get_height()), 0)
        pygame.draw.rect(cadre, (255,255,255,150), (0,0, cadre.get_width(), cadre.get_height()), 4)
        VAR.fenetre.blit(cadre, ((VAR.RESOLUTION[0] - cadre.get_width()) // 2, 0, cadre.get_width(), VAR.RESOLUTION[1]))                 
        
    def afficher_titre():
        image_titre = VAR.ecritures[80].render("TABLEAU DES SCORES", True, (0,0,0,255)) 
        x, y = ((VAR.RESOLUTION[0] - image_titre.get_width() ) // 2), ( ((CHighscore.dimY * 3) - image_titre.get_height()) // 2 )
        VAR.fenetre.blit(image_titre, (x-2, y-2))    
        image_titre = VAR.ecritures[80].render("TABLEAU DES SCORES", True, (255,255,255,255)) 
        x, y = ((VAR.RESOLUTION[0] - image_titre.get_width() ) // 2), ( ((CHighscore.dimY * 3) - image_titre.get_height()) // 2 )
        VAR.fenetre.blit(image_titre, (x, y))      
        
        
    def afficher_message():
        if pygame.time.get_ticks() - CHighscore.cycle > CHighscore.frequence:
            CHighscore.cycle = pygame.time.get_ticks()
            CHighscore.start = not CHighscore.start
        
        if CHighscore.start:            
            image_continue = VAR.ecritures[40].render("APPUYEZ SUR START", True, (255,255,255,255)) 
            x, y = ((VAR.RESOLUTION[0] - image_continue.get_width() ) // 2), VAR.RESOLUTION[1] - ( ((CHighscore.dimY * 3) - image_continue.get_height()) // 2 )
            VAR.fenetre.blit(image_continue, (x, y))      


    def afficher_joueur(joueur, i):
        dimCadreY = ((VAR.RESOLUTION[1] - (5 * CHighscore.dimY)) // VAR.nbJoueurs )        
        cadre = FCT.image_vide(CHighscore.dimX, dimCadreY)
        pygame.draw.rect(cadre, joueur.couleur, (0, 0, CHighscore.dimX, dimCadreY-10))
                
        cX = ((VAR.RESOLUTION[0] - CHighscore.dimX) //2)
        y = (CHighscore.dimY * 3) + (i * (dimCadreY + 10))
        
        # --- Cadre
        VAR.fenetre.blit(cadre, (cX, y))
        
        x = 0
        for titreTxt, info, largeur in (("Rang", joueur.Partie.rang, 1), ("Nom", joueur.Partie.nom, 15) , ("Niveau", joueur.Partie.niveau, 30), ("Nb. Lignes", joueur.Partie.nbLignes, 10), ("Score : ", joueur.Partie.score, 20)):
            x += ((VAR.RESOLUTION[0] / 100) * largeur)
            
            # --- Titre
            if i == 0:
                image = VAR.ecritures[20].render(str(titreTxt), True, (0,0,0,255)) 
                VAR.fenetre.blit(image, (x+cX-2, y-22))
                image = VAR.ecritures[20].render(str(titreTxt), True, (255,255,255,255)) 
                VAR.fenetre.blit(image, (x+cX, y-20))
                
            # --- Info    
            image = VAR.ecritures[60].render(str(info), True, (0,0,0,255)) 
            cY = ((dimCadreY + 10) - image.get_height()) // 2
            VAR.fenetre.blit(image, (x+cX-2, y+cY-2))
            image = VAR.ecritures[60].render(str(info), True, (255,255,255,255)) 
            VAR.fenetre.blit(image, (x+cX, y+cY))
        
        
        # -- AVATAR
        cY = (y + dimCadreY) - (780 * joueur.Avatar.ratioY)
        joueur.Avatar.dessiner(cX + 50, cY)
        
        
        