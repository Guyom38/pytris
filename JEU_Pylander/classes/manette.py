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
    def __init__(self, m, idManette):
        self.M = m
        self.manetteId = self.M.Joueur.id
     
    
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
                #if pygame.time.get_ticks() - self.cyclePoseRapide > VAR.poseRapideDelais: 
                #    self.cyclePoseRapide = pygame.time.get_ticks()
            self.action_start()   
                                   
    
                             
                                       
    def gestion_evenements_joueurs(self, event):
        if not V.partie_demarree or not self.M.Joueur.actif: return  

        manette = self.M.Joueur.Manette
        #if manette.boutonL.get_etat():
        #    pass
        #if manette.boutonR.get_etat():
        #    pass
        if manette.boutonA.get_etat():
            self.M.V_CHUTE = self.M.V_CHUTE-2
            self.M.ESSENCE = self.M.ESSENCE-5
            self.M.FUSEE_C = True

        #if manette.boutonB.get_etat():
        #    pass
        #if manette.boutonX:
        #if manette.boutonY:
           
        #if manette.boutonSelect.get_etat():
        #    pass
        #if manette.boutonStart:    
            
                                
        if manette.axeX > 0.9:
            self.M.V_DECAL = self.M.V_DECAL-2
            self.M.ESSENCE = self.M.ESSENCE-5
            self.M.FUSEE_D = True            
            
        elif manette.axeX < -0.9:
            
            self.M.V_DECAL = self.M.V_DECAL +2
            self.M.ESSENCE = self.M.ESSENCE -5
            self.M.FUSEE_G = True
            
        #else:
        #    pass
            

        #if manette.axeY > 0.9:
        #    pass
        #else:
        #    pass

                            
        