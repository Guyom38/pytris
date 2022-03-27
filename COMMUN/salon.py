
import pygame
from pygame.locals import *

import COMMUN.classes.fonctions as FCT

import JEU_Pytris.variables as VAR
from JEU_Pytris.variables import *

from COMMUN.classes.fonctions import *

from COMMUN.classes.avatars import CAvatars
from COMMUN.classes.controles import CControle

import COMMUN.variables as V

class CSalon:
    def __init__(self, c):
        self.C = c
        self.dimX = 0
        self.dimY = 0
        self.pX, self.pY = 0, 0
        self.init = False
        self.cycle, self.frequence, self.start = 0, 200, True
        self.boucleSalon = True
    
    def afficher_zone(self):
        self.dimX, self.dimY = self.dimX, self.dimY
        self.pX, self.pY = (V.RESOLUTION[0] - self.dimX) // 2, 200 
        
        cadre = FCT.GIMAGE.image_vide(self.dimX, self.dimY)
        pygame.draw.rect(cadre, (16,16,16, 150), (0, 0, self.dimX, self.dimY), 0)
        
        pygame.draw.rect(cadre, (64,64,64, 150), (0, 0, self.dimX, self.dimY), 2)
        pygame.draw.rect(cadre, (128,128,128, 150), (4, 4, self.dimX-8, self.dimY-8), 4)
        pygame.draw.rect(cadre, (64,64,64, 150), (10, 10, self.dimX-20, self.dimY-20), 2)
        
        V.fenetre.blit(cadre, (self.pX, self.pY))
    
    def initialisation(self):
        dX = self.dimX // 5
        dY = self.dimY // 7
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
        GAUDIO.charger_musique("COMMUN\\audios\\musics\\attente.mp3")
    
    def afficher_message(self):
        if pygame.time.get_ticks() - self.cycle > self.frequence:
            self.cycle = pygame.time.get_ticks()
            self.start = not self.start
        
        if self.start:            
            image_continue = GFONT.get_image_texte("APPUYEZ SUR START", 40, (255,255,255,255)) 
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
                etiquettes.append(GFONT.get_image_texte("Je suis prêt(e) !", 30, (0, 255, 0, 255)))
            etiquettes.append(GFONT.get_image_texte(joueur.nom, 30, (255, 255, 255, 255)))
                        
            pygame.draw.rect(V.fenetre, CAvatars.COULEUR[joueur.id], (pX + joueur.Avatar.salonX +20, pY + joueur.Avatar.salonY -30, etiquettes[0].get_width() + 40, (etiquettes[0].get_height() * len(etiquettes))), 0)
            
            y = 0
            for etiquette in etiquettes:
                V.fenetre.blit(etiquette, (pX + joueur.Avatar.salonX + 40, pY + joueur.Avatar.salonY + y - 30))
                y += etiquette.get_height()
                
       
                
            
           
    
    def controle_tous_prets(self):
        pret = False
        for i, joueur in V.joueurs.items():
            if V.joueurs_prets(): pret = True
        
        if pret: 
            self.boucleSalon = False
                
        
    def afficher_titre(self):
        image_titre = GFONT.get_image_texte("SALLE D'ATTENTE", 100, (0,0,0,0)) 
        pX = (V.RESOLUTION[0] -  image_titre.get_width()) // 2
        V.fenetre.blit(image_titre, (pX - 10, ((200 - image_titre.get_height()) //2) +10))
        
        image_titre = GFONT.get_image_texte("SALLE D'ATTENTE", 100, (255,255,255,255)) 
        pX = (V.RESOLUTION[0] -  image_titre.get_width()) // 2
        V.fenetre.blit(image_titre, (pX , (200 - image_titre.get_height()) //2))
        
                    
    def boucle(self):
        self.dimX, self.dimY = V.RESOLUTION[0] * 0.9, V.RESOLUTION[1] -400
        
        V.boucle = True
        while V.boucle and self.boucleSalon:
            CControle.capture_evements_utilisateurs()
            self.gestion_evenements_joueurs()    
            self.controle_tous_prets() 
            
            self.C.gestion_musique()
            self.C.afficher_fond()
            
            self.afficher()
            
            self.C.afficher_rendu()
        
        
    def afficher(self):
        

        self.afficher_zone()
        self.afficher_avatars()
        self.afficher_titre()
        self.afficher_message()

    def gestion_evenements_joueurs(self):
        for i, joueur in V.joueurs.items():
            self.gestion_evenements_salon(joueur)

    def gestion_evenements_salon(self, joueur):
        manette = joueur.Manette
        if manette.boutonL.get_etat():
            joueur.Avatar.animation_flip.bascule = False
        if manette.boutonR.get_etat():
            joueur.Avatar.animation_flip.bascule = True
        if manette.boutonA.get_etat():
            joueur.Avatar.changer_expression("BISOUS", -1)
        if manette.boutonB.get_etat():
            joueur.Avatar.changer_expression("ENERVE", -1)
        if manette.boutonX.get_etat():
            joueur.Avatar.changer_expression("EPUISE", -1)
        if manette.boutonY.get_etat():
            joueur.Avatar.changer_expression("DORT", -1)
        if manette.boutonSelect.get_etat():
            joueur.Avatar.charger_personnage()
        if manette.boutonStart.get_etat():    
            joueur.actif = True
                                
        if manette.axeX > 0.9:
            joueur.Avatar.salonX += 4
            joueur.Avatar.animation_flip.bascule = True
        elif manette.axeX < -0.9:
            joueur.Avatar.salonX -= 4
            joueur.Avatar.animation_flip.bascule = False
        if manette.axeY > 0.9:
            joueur.Avatar.salonY += 4
        elif manette.axeY < -0.9:
            joueur.Avatar.salonY -= 4  
            
        if joueur.Avatar.salonX<0: joueur.Avatar.salonX = 0
        if joueur.Avatar.salonX>self.dimX: joueur.Avatar.salonX =  self.dimX
        if joueur.Avatar.salonY<0: joueur.Avatar.salonY = 0
        if joueur.Avatar.salonY>self.dimY: joueur.Avatar.salonY =  self.dimY
        
            
        

        