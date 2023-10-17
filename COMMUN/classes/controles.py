
import pygame
from pygame.locals import *

import COMMUN.variables as V
import COMMUN.classes.fonctions as FCT
import COMMUN.classes.joueur as CJ
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

    def capture_evenements_websockets(actions_websocket):
        if not V.web_socket: return 0
    
        while not actions_websocket.empty():
            try:                    
                data = actions_websocket.get_nowait()
                if 'playerId' in data:                                            
                    idJoueurWS = int(data['playerId'])
                        
                    if idJoueurWS not in V.JOUEURS_WEBSOCKET:
                        V.JOUEURS_WEBSOCKET[idJoueurWS] = len(V.JOUEURS_WEBSOCKET) 
                        print("Nouveau Joueur #"+str(idJoueurWS)+" => id:" + str(V.JOUEURS_WEBSOCKET[idJoueurWS]))
                        i =  V.JOUEURS_WEBSOCKET[idJoueurWS]
                        V.joueurs[i] = CJ.CJoueur(i)
                        
                    idJoueur = V.JOUEURS_WEBSOCKET[idJoueurWS]
                        
                        
                    #axis_x, axis_y, mouvementJoy = 0.0, 0.0, False                
                    if 'joystick' in data['data']:
                        if 'direction' in data['data']['joystick']:                        
                            if data['data']['joystick']['direction']['angle'] == "left":
                                V.joueurs[idJoueur].Manette.axeX = -1
                            elif data['data']['joystick']['direction']['angle'] == "right":
                                V.joueurs[idJoueur].Manette.axeX = 1
                            elif data['data']['joystick']['direction']['angle'] == "up":
                                V.joueurs[idJoueur].Manette.axeY = -1
                            elif data['data']['joystick']['direction']['angle'] == "down":
                                V.joueurs[idJoueur].Manette.axeX = 1
                            
                        if 'state' in data['data']['joystick']:                     
                            if ( data['data']['joystick']['state']) == 'end':   
                                print("Relache"+ str(idJoueur))
  
                        if 'button' in data['data']: 
                            if (data['data']['button'] == 'B'):
                                V.joueurs[idJoueur].Manette.boutonB.pression()
                            if (data['data']['button'] == 'A'):
                                V.joueurs[idJoueur].Manette.boutonA.pression()
                            if (data['data']['button'] == 'start'):
                                V.joueurs[idJoueur].Manette.boutonStart.pression()
                            if (data['data']['button'] == 'select'):
                                V.joueurs[idJoueur].Manette.boutonSelect.pression()
                            
                                     
            except Exception as e:
                print(f"Erreur: {e}")
                
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

    




    
    
                            
        
                