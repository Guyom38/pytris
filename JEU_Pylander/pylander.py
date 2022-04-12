# ---------------------------------------------------------------- IMPORTATION DES LIBRAIRIES
import pygame
from pygame import *

import math, random

import JEU_Pylander.variables as VAR
import COMMUN.classes.fonctions as FCT
import COMMUN.variables as V

from JEU_Pylander.classes.moteur import *
from COMMUN.classes.controles import *

class pylander:
    def __init__(self, c):
        V.fps_max = 0

        self.C = c
        self.initialiser_les_joueurs()

    def initialiser_les_joueurs(self):
        j = 0
        if V.joueur_clavier: j = 1    
                        
        V.moteurs = {}
        for i in range(V.nbManettes+j):
            V.moteurs[i] =  CMoteur(V.joueurs[i])
            V.moteurs[i].initialiser()
            V.moteurs[i].offX = (V.moteurs[i].image.get_width() + 10 ) * i
            
            barre = (200 / V.nbManettes+j) * i
            pygame.draw.rect(V.fenetre, (255,255,0,255), (0, V.RESOLUTION[1]-30, barre, 30), 0)
            pygame.display.flip()

    def afficher_les_joueurs(self):
        for i, moteur in V.moteurs.items():
            moteur.propulseur_central, moteur.propulseur_droit, moteur.propulseur_gauche = False, False, False
            moteur.Manette.gestion_evenements()
            moteur.afficher()    

    def boucle(self):

        # ---------------------------------------------------------------- BOUCLE DU JEU
        V.boucle = True
        
        while V.boucle:
            CControle.capture_evements_utilisateurs()
             
            self.C.gestion_musique()
            self.C.afficher_fond()
            self.afficher_les_joueurs()

            if self.C.compte_a_rebours_partie():
                V.partie_demarree = True
                
            self.C.afficher_rendu()
            
            
        pygame.quit()