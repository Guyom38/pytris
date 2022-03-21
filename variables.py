<<<<<<< HEAD
=======

from pygame.locals import *
import fonctions as FCT
import os, random
>>>>>>> 2aa68738f3a301ac17aed6b1c71fcb8030054908

from pygame.locals import *
import fonctions as FCT
import os, random

RESOLUTION = ((1280, 800),(1920, 1080))[1]
MODE_ECRAN = (DOUBLEBUF,FULLSCREEN)[1]
DIMENSION = (10, 20)
TAILLE = 20
TAILLE_ECRITURE = 20
ECARTX = 40

MODE_MENU = 0
MODE_JEU = 1
MODE_SCORE = 2
MODE_SALON = 3

mode = MODE_SALON


LISTE_NOMS = ["Groun", "Kazek", "Thinuf", "Vonog", "Grodron", "Dronbok", "Kazdre", "Azgan", "Vondur", "Waelg", "Damval", "Kroncae", "Dronkar", "Ginuf", \
              "Gilsko", "Bokskrarag", "Agcae", "Riltha", "Darnog", "Dron", "Zornthron", "Grogor", "Mingin", "Ekskre", "Golskre", "Kruag", "Throngrin", \
              "Griaz", "Anag", "Zornmin", "Kaz", "Trolrhun", "Unthron", "Elgril", "Stogriki", "Galag", "Agsko", "Gurfron", "Ginril", "Grinthron", "Rilthin", \
              "Rhunril", "Caeskra", "Ekgin", "Gurnog", "Ufdam", "Gorgur", "Kazgru", "Zornuz", "Fronelg", "Uzganrin", "Rikgar", "Krukul", "Rilcaeril", "Skogin", \
              "Lokgil", "Grudag", "Skouf", "Rikdag", "Ogur", "Dregan", "Agval", "Makkim", "Ekazril", "Gardun", "Throngin", "Thronzorn", "Kulum", "Skraag", "Krontol", \
              "Makril", "Okgan", "Karrag", "Stouz", "Duntha"]

fenetre = None
evenements = None


nbJoueurs = 0
boucle = True

nbManettes = 0
manettes = {}
nbBoutons = 0
tetris_joueurs = {}
poseRapideDelais = 200
vitesseDeplacement = 50

fonts = {}
ecritures = {}

idFond = 0
IMG_FOND = []


fond = True
mode_bmp = True
audio = True
musique = True
joueur_clavier = False

nbLignesNiveauSuivant = 10

AUDIOS = {}
IMAGES = {}

cycle_partie = 0
duree_partie = 180000
fin_partie = False
partie_demarree = False

pouvoirId = 0
pouvoirCycle = 0
pouvoirDelais = 5000

limitePiecesQuiSeSuivent = 2
class CBouton:
    B_X = 0
    B_A = 1
    B_B = 2
    B_Y = 3
    B_L = 4
    B_R = 5
    B_START = 9
    B_SELECT = 8

horloge = None
cycle = 0
fps = 0
fps_cpt = 0
fps_cycle = 0
animation_cpt = 0

compteARebours_cycle = -1
compteARebours_Delais = 5000

fondVideo_cycle = 0
fondVideo_frequence =  35

limiteModeBalance = True            # Si le joueur fait une ligne, cela baisse le nombre de lignes en attente
limiteLignesEnAttente = 5
limiteLignesMax = 2
limiteLignesCycle = 0
limiteLignesFrequence = 10000

marge = 20

pp = False # recharge les classes
        
        
def joueurs_actifs():
    for i, joueur in tetris_joueurs.items():
        if joueur.actif: return True
    return False

def joueurs_prets():
    for i, joueur in tetris_joueurs.items():
        if not joueur.actif: return False
    return True

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

        
   