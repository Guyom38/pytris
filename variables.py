from pygame.locals import *
import COMMUN.fonctions as FCT
import COMMUN.variables as V


import os, random


TITRE = "PyTris"

DIMENSION = (10, 20)
TAILLE = 20
TAILLE_ECRITURE = 20
ECARTX = 40

MODE_MENU = 0
MODE_JEU = 1
MODE_SCORE = 2
MODE_SALON = 3

mode = MODE_SALON












tetris_joueurs = {}
poseRapideDelais = 200
vitesseDeplacement = 50

fonts = {}





mode_bmp = True


nbLignesNiveauSuivant = 10



cycle_partie = 0
duree_partie = 180000
fin_partie = False
partie_demarree = False

pouvoirId = 0
pouvoirCycle = 0
pouvoirDelais = 5000

limitePiecesQuiSeSuivent = 2





compteARebours_cycle = -1
compteARebours_Delais = 5000



limiteModeBalance = True            # Si le joueur fait une ligne, cela baisse le nombre de lignes en attente
limiteLignesEnAttente = 5
limiteLignesMax = 2
limiteLignesCycle = 0
limiteLignesFrequence = 10000

marge = 20

pp = False # recharge les classes
        
animation_cpt = 0       


def partie_en_cours():
    return (partie_demarree)

def partie_en_pause():
    for i, joueur in tetris_joueurs.items():
        if not joueur.pause: return False
    return True 

def partie_terminee():
    for i, joueur in tetris_joueurs.items():
        if not joueur.Partie.mort: return False
    return True

        
   