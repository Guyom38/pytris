
import pygame
from pygame.locals import *

import moteur

import variables as VAR
from variables import *
from grille import *

class CControle():
    def initialiser_manettes():
        pygame.joystick.init()
        VAR.nbManettes = pygame.joystick.get_count()
        if VAR.nbManettes == 0: return False

        VAR.manettes = {}
        for idManette in range(VAR.nbManettes):
            VAR.manettes[idManette] = pygame.joystick.Joystick(idManette) 
            VAR.manettes[idManette].init()
            
            print("Manette #" + str(idManette) + " => " + VAR.manettes[idManette].get_name() + " => "+ VAR.manettes[idManette].get_guid())
        VAR.nbBoutons = VAR.manettes[0].get_numbuttons()
        
        CControle.initialiser_les_dimensions()

    def initialiser_les_dimensions():
        j = 0
        if VAR.joueur_clavier: j = 1

        if VAR.nbManettes+j == 9: VAR.TAILLE, VAR.ECARTX = 18, 33
        if VAR.nbManettes+j == 8: VAR.TAILLE, VAR.ECARTX = 20, 40
        if VAR.nbManettes+j == 7: VAR.TAILLE, VAR.ECARTX = 23, 45
        if VAR.nbManettes+j == 6: VAR.TAILLE, VAR.ECARTX = 25, 70        
        if VAR.nbManettes+j == 5: VAR.TAILLE, VAR.ECARTX = 30, 84        
        if VAR.nbManettes+j == 4: VAR.TAILLE, VAR.ECARTX = 32, 80        
        if VAR.nbManettes+j == 3: VAR.TAILLE, VAR.ECARTX = 32, 120        
        if VAR.nbManettes+j == 2: VAR.TAILLE, VAR.ECARTX = 32, 300
        if VAR.nbManettes+j == 1: VAR.TAILLE, VAR.ECARTX = 38, 0
        
        if VAR.MODE_ECRAN == DOUBLEBUF: VAR.TAILLE, VAR.ECARTX = 20, 80

    def initialiser_les_joueurs():
        j = 0
        if VAR.joueur_clavier: j = 1        
                
        VAR.tetris_joueurs = {}
        if VAR.joueur_clavier:
            VAR.tetris_joueurs[0] = moteur.CMoteur(0, -1)
            VAR.tetris_joueurs[0].initialiser()

        for i in range(VAR.nbManettes):
            VAR.tetris_joueurs[i+j] = moteur.CMoteur(i+j, i)
            VAR.tetris_joueurs[i+j].initialiser()
        
        VAR.nbJoueurs = len(VAR.tetris_joueurs)
        

    def capture_evements_utilisateurs():
        VAR.evenements = pygame.event.get()

    def controle_fermeture_fenetre():
        
        for event in VAR.evenements:        
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                VAR.boucle = False

    def __init__(self, moteur, idManette):
        print("        + CONTROLE (CLAVIER / MANETTE)")

        self.Moteur = moteur
        self.manetteId = idManette
        self.cyclePoseRapide = pygame.time.get_ticks()
        
        self.direction = 0
        self.chute = False
        self.cycleDirection = pygame.time.get_ticks()
    
    
    
    def action_chute(self):
        self.Moteur.Mecanique.faire_descendre_a_fond_la_piece(self.Moteur.Pieces)
    
    def action_start(self):
        if self.Moteur.Partie.mort == True:
            self.Moteur.Partie.redemarre()
                        
        elif self.Moteur.actif == False:
            if VAR.cycle_partie == -1:
                VAR.cycle_partie = pygame.time.get_ticks()
                VAR.fin_partie = False
            self.Moteur.actif = True
            self.Moteur.Avatar.changer_expression ("NORMAL", -1)

        else:
            self.Moteur.Partie.pause = not self.Moteur.Partie.pause
    
    def action_select(self):
        self.Moteur.Partie.aide = not self.Moteur.Partie.aide

    def action_rotation(self, sens):
        self.Moteur.Pieces.faire_tourner_la_piece(sens)
    
    
    
    def actions(self):
        if pygame.time.get_ticks() - self.cycleDirection > vitesseDeplacement:
            self.Moteur.Pieces.controle_deplacement_lateral(self.direction)
            if self.chute:
                self.Moteur.Mecanique.faire_descendre_la_piece(self.Moteur.Pieces)
            self.cycleDirection = pygame.time.get_ticks()
            
            
    def gestion_manette(self):
        Partie = self.Moteur.Partie

        for event in VAR.evenements:
            if self.manetteId == -1 and VAR.joueur_clavier:
                if event.type == KEYDOWN:  
                    if not (self.pause or not self.actif):
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

                    if event.key == 13:
                        self.action_start()

            elif VAR.manettes[self.manetteId].get_button(CBouton.B_START) == 1:
                    if pygame.time.get_ticks() - self.cyclePoseRapide > VAR.poseRapideDelais: 
                        self.cyclePoseRapide = pygame.time.get_ticks()
                        self.action_start()
            elif VAR.manettes[self.manetteId].get_button(CBouton.B_SELECT) == 1:
                    self.action_select()

            elif not (Partie.pause or not self.Moteur.actif):
                if event.type == pygame.JOYBUTTONDOWN:
                    if VAR.manettes[self.manetteId].get_button(CBouton.B_L) == 1:
                        self.Moteur.Pieces.faire_tourner_la_piece(False)
                    if VAR.manettes[self.manetteId].get_button(CBouton.B_R) == 1:
                        self.Moteur.Pieces.faire_tourner_la_piece(True)
                    if VAR.manettes[self.manetteId].get_button(CBouton.B_A) == 1:
                        self.Moteur.Pieces.faire_tourner_la_piece(True)
                    if VAR.manettes[self.manetteId].get_button(CBouton.B_B) == 1:
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
                            
        self.actions()
                