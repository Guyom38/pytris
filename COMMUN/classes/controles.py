
import pygame
from pygame.locals import *

import COMMUN.variables as V
import JEU_Pytris.variables as VAR
from JEU_Pytris.variables import *
import COMMUN.classes.fonctions as FCT

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
    

class CTouche:
    def __init__(self):
        #self.cycle = FCT.GTEMPS.chrono(100)
        self.etat = False
    
    def pression(self):
        self.etat = True
        
    def relache(self):
        self.etat = False
        
    def get_etat(self):
        etat = self.etat
        if etat: self.etat = False
        return etat
        
        
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
        for i, moteur in V.moteurs.items():
            moteur.Manette.initialiser()


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

                if event.button == CBouton.B_A: V.joueurs[idManette].Manette.boutonA.pression()
                if event.button == CBouton.B_B: V.joueurs[idManette].Manette.boutonB.pression()
                if event.button == CBouton.B_X: V.joueurs[idManette].Manette.boutonX.pression()
                if event.button == CBouton.B_Y: V.joueurs[idManette].Manette.boutonY.pression()
                if event.button == CBouton.B_L: V.joueurs[idManette].Manette.boutonL.pression()
                if event.button == CBouton.B_R: V.joueurs[idManette].Manette.boutonR.pression()
                if event.button == CBouton.B_START: V.joueurs[idManette].Manette.boutonStart.pression()
                if event.button == CBouton.B_SELECT: V.joueurs[idManette].Manette.boutonSelect.pression() 

 
            elif event.type == pygame.JOYBUTTONUP:
                idManette = event.joy

                if event.button == CBouton.B_A: V.joueurs[idManette].Manette.boutonA.relache()
                if event.button == CBouton.B_B: V.joueurs[idManette].Manette.boutonB.relache()
                if event.button == CBouton.B_X: V.joueurs[idManette].Manette.boutonX.relache()
                if event.button == CBouton.B_Y: V.joueurs[idManette].Manette.boutonY.relache()
                if event.button == CBouton.B_L: V.joueurs[idManette].Manette.boutonL.relache()
                if event.button == CBouton.B_R: V.joueurs[idManette].Manette.boutonR.relache()
                if event.button == CBouton.B_START: V.joueurs[idManette].Manette.boutonStart.relache()
                if event.button == CBouton.B_SELECT: V.joueurs[idManette].Manette.boutonSelect.relache()
   


    def __init__(self, joueur):
        self.Joueur = joueur
        self.initialiser()
    
    def initialiser(self):
        self.boutonA = CTouche()
        self.boutonB = CTouche()
        self.boutonX = CTouche()
        self.boutonY = CTouche()
        self.boutonL = CTouche()
        self.boutonR = CTouche()
        self.boutonStart = CTouche()
        self.boutonSelect = CTouche()
        self.axeX = 0.0
        self.axeY = 0.0

    




    
    
                            
        
                