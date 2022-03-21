
import pygame
from pygame.locals import *

import moteur
import random

import COMMUN.variables as V
import variables as VAR
from variables import *

# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
class CBouton:
    B_X = 0
    B_A = 1
    B_B = 2
    B_Y = 3
    B_L = 4
    B_R = 5
    B_START = 9
    B_SELECT = 8
    
    
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
class CControle():
    
    # ---------------------------------------------------------------------------------------------------------------
    # -
    # ---------------------------------------------------------------------------------------------------------------
    def initialiser_manettes():
        pygame.joystick.init()
        V.nbManettes = pygame.joystick.get_count()
        if V.nbManettes == 0: return False

        V.manettes = {}
        for idManette in range(V.nbManettes):
            V.manettes[idManette] = pygame.joystick.Joystick(idManette) 
            V.manettes[idManette].init()
        V.nbBoutons = V.manettes[0].get_numbuttons()

    def capture_evements_utilisateurs():
        V.evenements = pygame.event.get()
        
        for event in V.evenements:        
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                V.boucle = False


    
    # ---------------------------------------------------------------------------------------------------------------
    # -
    # ---------------------------------------------------------------------------------------------------------------
    def __init__(self, moteur, idManette):
        self.Moteur = moteur
        self.manetteId = idManette
        self.cyclePoseRapide = pygame.time.get_ticks()
        
        self.direction = 0
        self.chute = False
        self.cycleDirection = pygame.time.get_ticks()
    
    
    def action_chute(self):
        self.Moteur.Mecanique.faire_descendre_a_fond_la_piece(self.Moteur.Pieces)
    
    
    def action_start(self):
        if VAR.mode == VAR.MODE_SALON:
            self.Moteur.Joueur.actif = True
            
        elif VAR.mode == VAR.MODE_JEU:
            if self.Moteur.Partie.mort:
                #self.Moteur.Partie.redemarre()
                pass            
            elif not self.Moteur.Joueur.actif:
                #if VAR.cycle_partie == -1:
                #    VAR.cycle_partie = pygame.time.get_ticks()
                #    VAR.fin_partie = False
                #self.Moteur.actif = True
                self.Moteur.Avatar.changer_expression ("NORMAL", -1)
            else:
                self.Moteur.Partie.pause = not self.Moteur.Partie.pause
                
        elif VAR.mode == VAR.MODE_SCORE:
            #for i, joueur in VAR.tetris_joueurs.items():
            #    joueur.Partie.redemarre()
            VAR.pp = True    
           
            FCT.changer_de_mode(VAR.MODE_JEU)
            VAR.partie_demarree = False
            VAR.fin_partie = False
            VAR.compteARebours_cycle = -1
            
            
    
    
    def action_select(self):
        self.Moteur.Partie.aide = not self.Moteur.Partie.aide

    def action_rotation(self, sens):
        self.Moteur.Pieces.faire_tourner_la_piece(sens)
    
    
    
    def executer_actions(self):
        if pygame.time.get_ticks() - self.cycleDirection > vitesseDeplacement:
            self.Moteur.Pieces.controle_deplacement_lateral(self.direction)
            if self.chute:
                self.Moteur.Mecanique.faire_descendre_la_piece(self.Moteur.Pieces)
            self.cycleDirection = pygame.time.get_ticks()
            
    
    
                        
    def gestion_evenements(self):
        for event in V.evenements:
            self.gestion_evenements_demarrage_partie(event)
            self.gestion_evenements_joueurs(event)
            self.gestion_evenements_salon(event)

            
    
    def gestion_evenements_demarrage_partie(self, event):
        if self.manetteId == -1 and V.joueur_clavier:
            if event.type == KEYDOWN:  
                if event.key == 13: self.action_start()
                        
        elif V.manettes[self.manetteId].get_button(CBouton.B_START) == 1:
                if pygame.time.get_ticks() - self.cyclePoseRapide > VAR.poseRapideDelais: 
                    self.cyclePoseRapide = pygame.time.get_ticks()
                    self.action_start()   
                                   
    def gestion_evenements_salon(self, event):
        if VAR.mode == VAR.MODE_SALON:
            if event.type == pygame.JOYBUTTONDOWN:
                if V.manettes[self.manetteId].get_button(CBouton.B_L) == 1:
                    self.Moteur.Avatar.animation_flip = False
                if V.manettes[self.manetteId].get_button(CBouton.B_R) == 1:
                    self.Moteur.Avatar.animation_flip = True
                if V.manettes[self.manetteId].get_button(CBouton.B_A) == 1:
                    self.Moteur.Avatar.changer_expression("BISOUS", -1)
                if V.manettes[self.manetteId].get_button(CBouton.B_B) == 1:
                    self.Moteur.Avatar.changer_expression("ENERVE", -1)
                if V.manettes[self.manetteId].get_button(CBouton.B_X) == 1:
                    self.Moteur.Avatar.changer_expression("EPUISE", -1)
                if V.manettes[self.manetteId].get_button(CBouton.B_Y) == 1:
                    self.Moteur.Avatar.changer_expression("DORT", -1)
                if V.manettes[self.manetteId].get_button(CBouton.B_SELECT) == 1:
                    #self.Moteur.Avatar.changer_expression(random.choice(("MORT", "NORMAL", "CONTENT", "ENERVE", "CONCENTRE", "EPUISE", "DORT", "POUVOIR")), -1)
                    self.Moteur.Avatar.charger_personnage()
                if V.manettes[self.manetteId].get_button(CBouton.B_START) == 1:    
                    self.action_start()
                                
            elif event.type == pygame.JOYAXISMOTION:
                if event.joy == self.manetteId:
                    if event.axis == 0:
                        if event.value > 0.9:
                            self.Moteur.Avatar.salonX += 16
                            self.Moteur.Avatar.animation_flip = True
                        elif event.value < -0.9:
                            self.Moteur.Avatar.salonX -= 16
                            self.Moteur.Avatar.animation_flip = False
                    elif event.axis == 1:
                        if event.value > 0.9:
                            self.Moteur.Avatar.salonY += 16
                        elif event.value < -0.9:
                            self.Moteur.Avatar.salonY -= 16     
                             
                                       
    def gestion_evenements_joueurs(self, event):
        if not VAR.partie_en_cours() : return  
            
        if self.manetteId == -1 and VAR.joueur_clavier:
            if event.type == KEYDOWN:  
                if not (self.pause or not self.Joueur.actif):
                    if event.key == K_DOWN: 
                        self.Moteur.Mecanique.faire_descendre_la_piece(self.Moteur.Pieces)
                    elif event.key == K_LEFT: 
                        self.Moteur.Pieces.controle_deplacement_lateral(-1)
                    elif event.key == K_RIGHT: 
                        self.Moteur.Pieces.controle_deplacement_lateral(1)
                    elif event.key == K_UP: 
                        if pygame.time.get_ticks() - self.cyclePoseRapide > VAR.poseRapideDelais: 
                            self.cyclePoseRapide = pygame.time.get_ticks()
                            self.action_chute()
                    elif event.key == K_SPACE:
                        self.action_rotation(True)
          
        elif V.manettes[self.manetteId].get_button(CBouton.B_SELECT) == 1:
                self.action_select()

        elif not (self.Moteur.Partie.pause or not self.Moteur.Joueur.actif):
            if event.type == pygame.JOYBUTTONDOWN:
                if V.manettes[self.manetteId].get_button(CBouton.B_L) == 1:
                    self.Moteur.Pieces.faire_tourner_la_piece(False)
                if V.manettes[self.manetteId].get_button(CBouton.B_R) == 1:
                    self.Moteur.Pieces.faire_tourner_la_piece(True)
                if V.manettes[self.manetteId].get_button(CBouton.B_A) == 1:
                    self.Moteur.Pieces.faire_tourner_la_piece(True)
                if V.manettes[self.manetteId].get_button(CBouton.B_B) == 1:
                    if pygame.time.get_ticks() - self.cyclePoseRapide > VAR.poseRapideDelais: 
                        self.cyclePoseRapide = pygame.time.get_ticks()
                        self.action_chute()
                        
            elif event.type == pygame.JOYAXISMOTION:
                if event.joy == self.manetteId:
                    if event.axis == 0:
                        if event.value > 0.9:
                            self.direction = 1
                        elif event.value < -0.9:
                            self.direction = -1
                        else:
                            self.direction = 0
                    elif event.axis == 1:
                        if event.value > 0.9:
                            self.chute = True
                        else:
                            self.chute = False
                            
        self.executer_actions()
                            
        
                