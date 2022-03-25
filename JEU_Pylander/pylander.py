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
        V.fps_max = 5

        self.C = c
        self.initialiser_les_joueurs()

    def initialiser_les_joueurs(self):
        j = 0
        if V.joueur_clavier: j = 1    
                        
        VAR.pylander_joueurs = {}
        for i in range(V.nbManettes+j):
            VAR.pylander_joueurs[i] =  CMoteur(V.joueurs[i])
            VAR.pylander_joueurs[i].initialiser()

            barre = (200 / V.nbManettes+j) * i
            pygame.draw.rect(V.fenetre, (255,255,0,255), (0, V.RESOLUTION[1]-30, barre, 30), 0)
            pygame.display.flip()

    def afficher_les_joueurs(self):
        for i, pylander_moteur in VAR.pylander_joueurs.items():
            pylander_moteur.FUSEE_C, pylander_moteur.FUSEE_D, pylander_moteur.FUSEE_G = False, False, False
            pylander_moteur.Manette.gestion_evenements()
            pylander_moteur.afficher()    

    def boucle(self):

        # ---------------------------------------------------------------- BOUCLE DU JEU
        V.boucle = True
        
        while V.boucle:
            CControle.capture_evements_utilisateurs()
             
            self.C.gestion_musique()
            self.C.afficher_fond()
            self.afficher_les_joueurs()

            self.C.afficher_rendu()
            
            
        pygame.quit()