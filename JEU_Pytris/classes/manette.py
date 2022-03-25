

import pygame
from pygame.locals import *

from COMMUN.classes.controles import CBouton

import COMMUN.variables as V
import JEU_Pytris.variables as VAR
from JEU_Pytris.variables import *

class CManette:
    # ---------------------------------------------------------------------------------------------------------------
    # -
    # ---------------------------------------------------------------------------------------------------------------
    def __init__(self, moteur, idManette):
        self.Moteur = moteur
        self.manetteId = self.Moteur.Joueur.id
        self.cyclePoseRapide = pygame.time.get_ticks()
        
        self.direction = 0
        self.chute = False
        self.cycleDirection = pygame.time.get_ticks()
    
    

    
    def action_start(self):
        if VAR.mode == ENUM_MODE.MODE_JEU:
            if self.Moteur.Partie.mort:
                pass            
            elif not self.Moteur.Joueur.actif:
                self.Moteur.Avatar.changer_expression ("NORMAL", -1)
            else:
                self.Moteur.Partie.pause = not self.Moteur.Partie.pause
                
        elif VAR.mode == ENUM_MODE.MODE_SCORE:
            VAR.relancePartie = True    
           
            VAR.changer_de_mode(ENUM_MODE.MODE_JEU)
            V.partie_demarree = False
            V.fin_partie = False
            VAR.temps_de_partie.reset(-1)
            
            
    
    
    
    
    
    def executer_actions(self):
        if pygame.time.get_ticks() - self.cycleDirection > vitesseDeplacement:
            self.Moteur.Pieces.controle_deplacement_lateral(self.direction)
            if self.chute:
                self.Moteur.Mecanique.faire_descendre_la_piece(self.Moteur.Pieces)
            self.cycleDirection = pygame.time.get_ticks()
            
    
    
    def gestion_evenements_start(self):
        for event in V.evenements:
            self.gestion_evenements_demarrage_partie(event)
           
    def gestion_evenements(self):
        for event in V.evenements:
            self.gestion_evenements_demarrage_partie(event)
            self.gestion_evenements_joueurs(event)
        self.executer_actions()
            
            
    
    def gestion_evenements_demarrage_partie(self, event):
        if self.manetteId == -1 and V.joueur_clavier:
            if event.type == KEYDOWN:  
                if event.key == 13: self.action_start()
                        
        elif V.manettes[self.manetteId].get_button(CBouton.B_START) == 1:
                if pygame.time.get_ticks() - self.cyclePoseRapide > VAR.poseRapideDelais: 
                    self.cyclePoseRapide = pygame.time.get_ticks()
                    self.action_start()   
                                   
    
                             
                                       
    def gestion_evenements_joueurs(self, event):
        if not V.partie_demarree or not self.Moteur.Joueur.actif: return  

        manette = self.Moteur.Joueur.Manette
        if manette.boutonL:
            self.Moteur.Pieces.faire_tourner_la_piece(False)
        if manette.boutonR:
            self.Moteur.Pieces.faire_tourner_la_piece(True)
        if manette.boutonA:
            self.Moteur.Pieces.faire_tourner_la_piece(True)
        if manette.boutonB:
            if pygame.time.get_ticks() - self.cyclePoseRapide > VAR.poseRapideDelais: 
                self.cyclePoseRapide = pygame.time.get_ticks()
                self.Moteur.Mecanique.faire_descendre_a_fond_la_piece(self.Moteur.Pieces)
        #if manette.boutonX:
        #if manette.boutonY:
           
        if manette.boutonSelect:
            self.Moteur.Partie.aide = not self.Moteur.Partie.aide
        #if manette.boutonStart:    
            
                                
        if manette.axeX > 0.9:
            self.direction = 1
        elif manette.axeX < -0.9:
            self.direction = -1
        else:
            self.direction = 0
      
        if manette.axeY > 0.9:
            self.chute = True
        else:
            self.chute = False


                            
        