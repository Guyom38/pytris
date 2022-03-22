
import pygame
from pygame.locals import *

import JEU_Pytris.variables as VAR
from JEU_Pytris.variables import *

import COMMUN.classes.fonctions as FCT
from COMMUN.classes.avatars import CAvatars

import COMMUN.variables as V

class CSalon:
    def __init__(self):
        self.dimX = 0
        self.dimY = 0
        self.init = False
        self.cycle, self.frequence, self.start = 0, 200, True
    
    def afficher_zone(self):
        self.dimX, self.dimY = CSalon.dimX, CSalon.dimY
        self.pX, self.pY = (V.RESOLUTION[0] - self.dimX) // 2, 200 
        
        cadre = FCT.image_vide(self.dimX, self.dimY)
        pygame.draw.rect(cadre, (16,16,16, 150), (0, 0, self.dimX, self.dimY), 0)
        
        pygame.draw.rect(cadre, (64,64,64, 150), (0, 0, self.dimX, self.dimY), 2)
        pygame.draw.rect(cadre, (128,128,128, 150), (4, 4, self.dimX-8, self.dimY-8), 4)
        pygame.draw.rect(cadre, (64,64,64, 150), (10, 10, self.dimX-20, self.dimY-20), 2)
        
        V.fenetre.blit(cadre, (self.pX, self.pY))
    
    def initialisation(self):
        dX = CSalon.dimX // 5
        dY = CSalon.dimY // 7
        x, y = 0, 2
        for i, joueur in V.joueurs.items():
            joueur.Avatar.salonX = x * dX
            joueur.Avatar.salonY = y * dY
            x += 1
            if x >4: 
                y+=3
                x = 0
            joueur.Avatar.changer_expression("NORMAL", -1)
            joueur.Avatar.changer_expression("CONTENT", 500)
        self.init = True
        FCT.charger_musique("COMMUN\\audios\\musics\\attente.mp3")
    
    def afficher_message(self):
        if pygame.time.get_ticks() - self.cycle > self.frequence:
            self.cycle = pygame.time.get_ticks()
            self.start = not self.start
        
        if self.start:            
            image_continue = V.ecritures[40].render("APPUYEZ SUR START", True, (255,255,255,255)) 
            x, y = ((V.RESOLUTION[0] - image_continue.get_width() ) // 2), V.RESOLUTION[1] - 100 + ((100 - image_continue.get_height()) // 2) 
            V.fenetre.blit(image_continue, (x, y))    
            
                  
    def afficher_avatars(self):
        if not self.init:
            self.initialisation()
       
        pX, pY = (V.RESOLUTION[0] -  self.dimX) // 2, 100
        for i, joueur in V.joueurs.items():

            joueur.Avatar.gestion_personnage()
            joueur.Avatar.dessiner(pX + joueur.Avatar.salonX + 40, pY + joueur.Avatar.salonY + 40)

            etiquettes = []
            if joueur.actif:
                etiquettes.append(V.ecritures[30].render("Je suis prêt(e) !", True, (0,255,0,255)))
            etiquettes.append(V.ecritures[30].render(joueur.nom, True, (255,255,255,255)))
                        
            pygame.draw.rect(V.fenetre, CAvatars.COULEUR[joueur.id], (pX + joueur.Avatar.salonX +20, pY + joueur.Avatar.salonY -30, etiquettes[0].get_width() + 40, (etiquettes[0].get_height() * len(etiquettes))), 0)
            
            y = 0
            for etiquette in etiquettes:
                V.fenetre.blit(etiquette, (pX + joueur.Avatar.salonX + 40, pY + joueur.Avatar.salonY + y - 30))
                y += etiquette.get_height()
                
       
                
            
           
    
    def controle_tous_prets(self):
        pret = False
        for i, joueur in VAR.tetris_joueurs.items():
            if V.joueurs_prets(): pret = True
        
        if pret: FCT.changer_de_mode(VAR.MODE_JEU)
                
        
    def afficher_titre(self):
        image_titre = V.ecritures[100].render("SALLE D'ATTENTE", True, (0,0,0,0)) 
        pX = (V.RESOLUTION[0] -  image_titre.get_width()) // 2
        V.fenetre.blit(image_titre, (pX - 10, ((200 - image_titre.get_height()) //2) +10))
        
        image_titre = V.ecritures[100].render("SALLE D'ATTENTE", True, (255,255,255,255)) 
        pX = (V.RESOLUTION[0] -  image_titre.get_width()) // 2
        V.fenetre.blit(image_titre, (pX , (200 - image_titre.get_height()) //2))
        
                    
    def afficher(self):
        self.dimX, self.dimY = V.RESOLUTION[0] * 0.9, V.RESOLUTION[1] -400

        self.gestion_evenements_joueurs()       
        self.afficher_zone()
        self.afficher_avatars()
        self.afficher_titre()
        self.afficher_message()
        self.controle_tous_prets()


    def gestion_evenements_joueurs(self):
        for i, joueur in V.joueurs.items():
            self.gestion_evenements_salon(joueur)

    def gestion_evenements_salon(self, joueur):
        manette = joueur.Manette
        if manette.boutonL:
            joueur.Avatar.animation_flip = False
        if manette.boutonR:
            joueur.Avatar.animation_flip = True
        if manette.boutonA:
            joueur.Avatar.changer_expression("BISOUS", -1)
        if manette.boutonB:
            joueur.Avatar.changer_expression("ENERVE", -1)
        if manette.boutonX:
            joueur.Avatar.changer_expression("EPUISE", -1)
        if manette.boutonY:
            joueur.Avatar.changer_expression("DORT", -1)
        if manette.boutonSelect:
            joueur.Avatar.charger_personnage()
        if manette.boutonStart:    
            joueur.actif = True
                                
        if manette.axeX > 0.9:
            joueur.Avatar.salonX += 16
            joueur.Avatar.animation_flip = True
        elif manette.axeX < -0.9:
            joueur.Avatar.salonX -= 16
            joueur.Avatar.animation_flip = False
        if manette.axeY > 0.9:
            joueur.Avatar.salonY += 16
        elif manette.axeY < -0.9:
            joueur.Avatar.salonY -= 16     

        