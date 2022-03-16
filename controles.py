
import pygame
from pygame.locals import *

import moteur

import variables as VAR
from variables import *


class CControle():
    def initialiser_manettes():
        pygame.joystick.init()
        VAR.nbManettes = pygame.joystick.get_count()
        if VAR.nbManettes == 0: return False

        VAR.manettes = {}
        for idManette in range(VAR.nbManettes):
            VAR.manettes[idManette] = pygame.joystick.Joystick(idManette) 
            VAR.manettes[idManette].init()
        VAR.nbBoutons = VAR.manettes[0].get_numbuttons()

    def initialiser_les_joueurs():
        j = 0
        if VAR.joueur_clavier: j = 1

        if VAR.nbManettes+j == 5: VAR.TAILLE, VAR.ECARTX = 32, 50
        if VAR.nbManettes+j == 4: VAR.TAILLE, VAR.ECARTX = 32, 80
        if VAR.nbManettes+j == 3: VAR.TAILLE, VAR.ECARTX = 32, 120
        if VAR.nbManettes+j == 2: VAR.TAILLE, VAR.ECARTX = 32, 200
        if VAR.nbManettes+j == 1: VAR.TAILLE, VAR.ECARTX = 32, 0


        largeur_grilles = (VAR.nbManettes +j) * ((VAR.DIMENSION[0] * VAR.TAILLE)+VAR.ECARTX) -VAR.ECARTX
        hauteur = (VAR.DIMENSION[1] * VAR.TAILLE)
        offsetX = int((VAR.RESOLUTION[0] - largeur_grilles) /2)
        offsetY = int((VAR.RESOLUTION[1] - hauteur) /2 ) + 50
        
        x = 0
        
        VAR.tetris_joueurs = {}

        if VAR.joueur_clavier:
            VAR.tetris_joueurs[0] = moteur.CMoteur(0, (offsetX+x, offsetY), -1)
            VAR.tetris_joueurs[0].demarrer()
            j = 1

        for i in range(VAR.nbManettes):
            x = (i+j) * ((VAR.DIMENSION[0] * VAR.TAILLE)+VAR.ECARTX)
            VAR.tetris_joueurs[i+j] = moteur.CMoteur(i+j, (offsetX+x, offsetY), i)
            #VAR.tetris_joueurs[i+j].demarrer()
        
        
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

    def gestion_manette(self):
        Partie = self.Moteur.Partie

        for event in VAR.evenements:
            if self.manetteId == -1 and VAR.joueur_clavier:
                if event.type == KEYDOWN:  
                    if not (self.pause or not self.actif):
                        if event.key == K_DOWN: 
                            self.faire_descendre_la_piece()
                        elif event.key == K_LEFT: 
                            self.controle_deplacement_lateral(-1)
                        elif event.key == K_RIGHT: 
                            self.controle_deplacement_lateral(1)
                        elif event.key == K_UP: 
                            self.faire_descendre_a_fond_la_piece()
                        elif event.key == K_SPACE:
                            self.faire_tourner_la_piece(True)

                    if event.key == 13:
                        if Partie.mort == True:
                            Partie.game_over()
                            
                        elif self.actif == False:
                            VAR.partie_demarree = True
                            if VAR.cycle_partie == -1:
                                VAR.cycle_partie = pygame.time.get_ticks()
                            self.Moteur.actif = True
                        else:
                            Partie.pause = not Partie.pause

            elif VAR.manettes[self.manetteId].get_button(CBouton.B_START) == 1:
                    if Partie.mort == True:
                        Partie.game_over()
                        
                    elif self.Moteur.actif == False:
                        VAR.partie_demarree = True
                        if VAR.cycle_partie == -1:
                            VAR.cycle_partie = pygame.time.get_ticks()
                        self.Moteur.actif = True
                    else:
                        Partie.pause = not Partie.pause
                        
            elif VAR.manettes[self.manetteId].get_button(CBouton.B_SELECT) == 1:
                    Partie.aide = not Partie.aide

            elif not (Partie.pause or not self.Moteur.actif):
                if event.type == pygame.JOYBUTTONDOWN:
                    if VAR.manettes[self.manetteId].get_button(CBouton.B_L) == 1:
                        self.faire_tourner_la_piece(False)
                    if VAR.manettes[self.manetteId].get_button(CBouton.B_R) == 1:
                        self.faire_tourner_la_piece(True)
                    if VAR.manettes[self.manetteId].get_button(CBouton.B_B) == 1:
                        self.faire_descendre_a_fond_la_piece()
                elif event.type == pygame.JOYAXISMOTION:
                    
                    if event.joy == self.manetteId:
                        if event.axis == 0 and event.value > 0.9:
                            self.controle_deplacement_lateral(1)
                        elif event.axis == 0 and event.value < -0.9:
                            self.controle_deplacement_lateral(-1)
                        elif event.axis == 1 and event.value > 0.9:
                            self.faire_descendre_la_piece()
                        #elif event.axis == 1 and event.value < -0.9: #HAUT
                            #self.faire_descendre_a_fond_la_piece()