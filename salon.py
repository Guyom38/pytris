
import pygame
from pygame.locals import *

import variables as VAR
from variables import *

import fonctions as FCT

class CSalon:
    
    dimX = 0
    dimY = 0
    init = False
    cycle, frequence, start = 0, 200, True
    
    def afficher_zone():
        dimX, dimY = CSalon.dimX, CSalon.dimY
        pX, pY = (VAR.RESOLUTION[0] - dimX) // 2, 200 
        
        cadre = FCT.image_vide(dimX, dimY)
        pygame.draw.rect(cadre, (16,16,16, 150), (0, 0, dimX, dimY), 0)
        
        pygame.draw.rect(cadre, (64,64,64, 150), (0, 0, dimX, dimY), 2)
        pygame.draw.rect(cadre, (128,128,128, 150), (4, 4, dimX-8, dimY-8), 4)
        pygame.draw.rect(cadre, (64,64,64, 150), (10, 10, dimX-20, dimY-20), 2)
        
        VAR.fenetre.blit(cadre, (pX, pY))
    
    def initialisation():
        dX = CSalon.dimX // 5
        dY = CSalon.dimY // 7
        x, y = 0, 2
        for i, joueur in VAR.tetris_joueurs.items():
            joueur.Avatar.salonX = x * dX
            joueur.Avatar.salonY = y * dY
            x += 1
            if x >4: 
                y+=3
                x = 0
            joueur.Avatar.changer_expression("NORMAL", -1)
            joueur.Avatar.changer_expression("CONTENT", 500)
        CSalon.init = True
    
    def afficher_message():
        if pygame.time.get_ticks() - CSalon.cycle > CSalon.frequence:
            CSalon.cycle = pygame.time.get_ticks()
            CSalon.start = not CSalon.start
        
        if CSalon.start:            
            image_continue = VAR.ecritures[40].render("APPUYEZ SUR START", True, (255,255,255,255)) 
            x, y = ((VAR.RESOLUTION[0] - image_continue.get_width() ) // 2), VAR.RESOLUTION[1] - 100 + ((100 - image_continue.get_height()) // 2) 
            VAR.fenetre.blit(image_continue, (x, y))    
            
                  
    def afficher_avatars():
        if not CSalon.init:
            CSalon.initialisation()
       
        pX, pY = (VAR.RESOLUTION[0] -  CSalon.dimX) // 2, 100
        for i, joueur in VAR.tetris_joueurs.items():
            
            joueur.Controle.gestion_evenements()
            joueur.Avatar.gestion_personnage()
            joueur.Avatar.dessiner(pX + joueur.Avatar.salonX + 40, pY + joueur.Avatar.salonY + 40)

            etiquettes = []
            if joueur.actif:
                etiquettes.append(VAR.ecritures[30].render("Je suis prêt(e) !", True, (0,255,0,255)))
            etiquettes.append(VAR.ecritures[30].render(joueur.Partie.nom, True, (255,255,255,255)))
                        
            pygame.draw.rect(VAR.fenetre, joueur.couleur, (pX + joueur.Avatar.salonX +20, pY + joueur.Avatar.salonY -30, etiquettes[0].get_width() + 40, (etiquettes[0].get_height() * len(etiquettes))), 0)
            
            y = 0
            for etiquette in etiquettes:
                VAR.fenetre.blit(etiquette, (pX + joueur.Avatar.salonX + 40, pY + joueur.Avatar.salonY + y - 30))
                y += etiquette.get_height()
                
       
                
            
           
    
    def controle_tous_prets():
        pret = False
        for i, joueur in VAR.tetris_joueurs.items():
            if VAR.joueurs_prets(): pret = True
        
        if pret: FCT.changer_de_mode(VAR.MODE_JEU)
                
        
    def afficher_titre():
        image_titre = VAR.ecritures[100].render("SALLE D'ATTENTE", True, (0,0,0,0)) 
        pX = (VAR.RESOLUTION[0] -  image_titre.get_width()) // 2
        VAR.fenetre.blit(image_titre, (pX - 10, ((200 - image_titre.get_height()) //2) +10))
        
        image_titre = VAR.ecritures[100].render("SALLE D'ATTENTE", True, (255,255,255,255)) 
        pX = (VAR.RESOLUTION[0] -  image_titre.get_width()) // 2
        VAR.fenetre.blit(image_titre, (pX , (200 - image_titre.get_height()) //2))
        
                    
    def afficher():
        CSalon.dimX, CSalon.dimY = VAR.RESOLUTION[0] * 0.9, VAR.RESOLUTION[1] -400
                
        CSalon.afficher_zone()
        CSalon.afficher_avatars()
        CSalon.afficher_titre()
        CSalon.afficher_message()
        CSalon.controle_tous_prets()
        