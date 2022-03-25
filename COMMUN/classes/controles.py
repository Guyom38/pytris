
import pygame
from pygame.locals import *

import COMMUN.variables as V
import JEU_Pytris.variables as VAR
from JEU_Pytris.variables import *

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
class CControle:
    
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

    def remise_a_zero_des_boutons():
        for i, joueur in V.joueurs.items():
            joueur.Manette.initialiser()


    def capture_evements_utilisateurs():
        V.evenements = pygame.event.get()

        for event in V.evenements:        
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                V.boucle = False

            elif event.type == pygame.JOYAXISMOTION:
                idManette = event.joy
                if event.axis == 0: V.joueurs[idManette].Manette.axeX = event.value
                if event.axis == 1: V.joueurs[idManette].Manette.axeY = event.value

            elif event.type == pygame.JOYBUTTONDOWN :
                idManette = event.joy

                if event.button == CBouton.B_A: V.joueurs[idManette].Manette.boutonA = True
                if event.button == CBouton.B_B: V.joueurs[idManette].Manette.boutonB = True
                if event.button == CBouton.B_X: V.joueurs[idManette].Manette.boutonX = True
                if event.button == CBouton.B_Y: V.joueurs[idManette].Manette.boutonY = True
                if event.button == CBouton.B_L: V.joueurs[idManette].Manette.boutonL = True
                if event.button == CBouton.B_R: V.joueurs[idManette].Manette.boutonR = True
                if event.button == CBouton.B_START: V.joueurs[idManette].Manette.boutonStart = True
                if event.button == CBouton.B_SELECT: V.joueurs[idManette].Manette.boutonSelect = True        

 
            elif event.type == pygame.JOYBUTTONUP:
                idManette = event.joy

                if event.button == CBouton.B_A: V.joueurs[idManette].Manette.boutonA = False
                if event.button == CBouton.B_B: V.joueurs[idManette].Manette.boutonB = False
                if event.button == CBouton.B_X: V.joueurs[idManette].Manette.boutonX = False
                if event.button == CBouton.B_Y: V.joueurs[idManette].Manette.boutonY = False
                if event.button == CBouton.B_L: V.joueurs[idManette].Manette.boutonL = False
                if event.button == CBouton.B_R: V.joueurs[idManette].Manette.boutonR = False
                if event.button == CBouton.B_START: V.joueurs[idManette].Manette.boutonStart = False
                if event.button == CBouton.B_SELECT: V.joueurs[idManette].Manette.boutonSelect = False  
   


    def __init__(self, joueur):
        self.Joueur = joueur
        self.initialiser()
    
    def initialiser(self):
        self.boutonA = False
        self.boutonB = False
        self.boutonX = False
        self.boutonY = False
        self.boutonL = False
        self.boutonR = False
        self.boutonStart = False
        self.boutonSelect = False
        self.axeX = 0.0
        self.axeY = 0.0

    




    
    
                            
        
                