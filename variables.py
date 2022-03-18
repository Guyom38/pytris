from pygame.locals import *

RESOLUTION = ((1280, 800),(1920, 1080))[0]
MODE_ECRAN = (DOUBLEBUF,FULLSCREEN)[0]
DIMENSION = (10, 20)
TAILLE = 20
TAILLE_ECRITURE = 20
ECARTX = 40

fenetre = None
evenements = None
nbJoueurs = 0
boucle = True

nbManettes = 0
manettes = {}
nbBoutons = 0
tetris_joueurs = {}
poseRapideDelais = 300
vitesseDeplacement = 100

fonts = {}
ecritures = {}

idFond = 0
IMG_FOND = []


fond = True
mode_bmp = True
audio = True
musique = True
joueur_clavier = False

nbLignesNiveauSuivant = 1

AUDIOS = {}
IMAGES = {}

cycle_partie = 0
duree_partie = 5*60000
fin_partie = False
partie_demarree = False

pouvoirId = 0
pouvoirCycle = 0
pouvoirDelais = 7000

limitePiecesQuiSeSuivent = 3
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


fondVideo_cycle = 0
fondVideo_frequence =  35

