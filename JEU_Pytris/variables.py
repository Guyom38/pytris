
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
pouvoir_delais = 5000
vitesse_par_defaut = 500

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

partie_demarree = False
mode = ENUM_MODE.MODE_JEU

tetris_joueurs = {}
fonts = {}


temps_de_partie = GTEMPS.chrono(duree_partie)
compte_a_rebours = GTEMPS.chrono(pouvoir_delais, -1)
temps_ajout_de_lignes = GTEMPS.chrono(lignes_ajout_delais)

fin_partie = False

LISTE_DES_PIECES = ["O", "I", "S", "Z", "L", "J", "T"]

pouvoirId = 0

temps_pouvoir = GTEMPS.chrono(duree_partie)
#pouvoirCycle = 0
#limiteLignesCycle = 0

relancePartie = False # recharge les classes
        
animation_cpt = 0  



# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
# █  METHODES DU JEU                                                        █
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

def get_nb_joueurs():
    return (len(tetris_joueurs))

def nbJoueursActifs():
        nb = 0
        for i, m in tetris_joueurs.items():
            if m.Joueur.actif and not m.Partie.mort: nb +=1
        return nb

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

def changer_de_mode(x):
    global mode
    mode = x
        
    if x == ENUM_MODE.MODE_JEU:
        fichier = random.choice(os.listdir("JEU_Pytris\\audios\\musics"))
        GAUDIO.charger_musique("JEU_Pytris\\audios\\musics\\" + fichier)
    else:
        GAUDIO.arreter_musique()   

        
   