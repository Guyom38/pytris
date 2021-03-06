
from COMMUN.classes.fonctions import * 
from enum import *
import random, os

# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
# █  PARAMETRES DU JEU                                                      █
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

TITRE = "PyTris"
DIMENSION = (10, 20)
TAILLE = 20

# TODO : Reformuler le nom des variables
ECARTX = 40
TAILLE_ECRITURE = 20

poseRapideDelais = 200
vitesseDeplacement = 50
mode_bmp = True
nbLignesNiveauSuivant = 10
limitePiecesQuiSeSuivent = 2

mode_balance = True            # Si le joueur fait une ligne, cela baisse le nombre de lignes en attente
lignes_en_attente = 5
lignes_ajout_max = 2

lignes_ajout_delais = 10000
duree_partie = 180000

vitesse_par_defaut = 500
pouvoir_delais = 7000

marge = 20

# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
# █  ENUMERATIONS                                                           █
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

class ENUM_MODE(Enum):
    MODE_MENU = 0
    MODE_JEU = 1
    MODE_SCORE = 2
    MODE_SALON = 3

# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
# █  CLASSES DE PROPRIETES                                                  █
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█


    
    
# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
# █  VARIABLES DU JEU                                                       █
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█


mode = ENUM_MODE.MODE_JEU

temps_de_partie = GTEMPS.chrono(duree_partie)

temps_ajout_de_lignes = GTEMPS.chrono(lignes_ajout_delais)
temps_pouvoir = GTEMPS.chrono(pouvoir_delais)


LISTE_DES_PIECES = ["O", "I", "S", "Z", "L", "J", "T"]

pouvoirId = 0


#pouvoirCycle = 0
#limiteLignesCycle = 0

relancePartie = False # recharge les classes
        
animation_cpt = 0  



# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
# █  METHODES DU JEU                                                        █
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█



def nbJoueursActifs():
        nb = 0
        for i, moteur in V.moteurs.items():
            if moteur.Joueur.actif and not moteur.Partie.mort: nb +=1
        return nb

def partie_en_pause():
    for i, moteur in V.moteurs.items():
        if not moteur.pause: return False
    return True 

def partie_terminee():
    for i, moteur in V.moteurs.items():
        if not moteur.Partie.mort: return False
    return True

def changer_de_mode(x):
    global mode
    mode = x
        
    if x == ENUM_MODE.MODE_JEU:
        fichier = random.choice(os.listdir("JEU_Pytris\\audios\\musics"))
        GAUDIO.charger_musique("JEU_Pytris\\audios\\musics\\" + fichier)
    else:
        GAUDIO.arreter_musique()   

        
   