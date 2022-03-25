import pygame
from pygame.locals import *

from COMMUN.classes.controles import CBouton

import COMMUN.variables as V
import JEU_Pylander.variables as VAR
from JEU_Pylander.variables import *

class CManette:
    # ---------------------------------------------------------------------------------------------------------------
    # -
    # ---------------------------------------------------------------------------------------------------------------
    def __init__(self, moteur, idManette):
        self.Moteur = moteur
        self.manetteId = self.Moteur.Joueur.id
      

            
            
    
    
    
    
    
    def executer_actions(self):
        pass    
    
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
        if not VAR.partie_en_cours() or not self.Moteur.Joueur.actif: return  

        manette = self.Moteur.Joueur.Manette
        if manette.boutonL:
            pass
        if manette.boutonR:
            pass
        if manette.boutonA:
            self.V_CHUTE = self.V_CHUTE-2
            self.ESSENCE = self.ESSENCE-5
            self.FUSEE_C = True

        if manette.boutonB:
            pass
        #if manette.boutonX:
        #if manette.boutonY:
           
        if manette.boutonSelect:
            pass
        #if manette.boutonStart:    
            
                                
        if manette.axeX > 0.9:
            self.V_DECAL = self.V_DECAL +2
            self.ESSENCE = self.ESSENCE -5
            self.FUSEE_G = True
            
        elif manette.axeX < -0.9:
            self.V_DECAL = self.V_DECAL-2
            self.ESSENCE = self.ESSENCE-5
            self.FUSEE_D = True
            
        else:
            pass
            

        if manette.axeY > 0.9:
            pass
        else:
            pass

                            
        