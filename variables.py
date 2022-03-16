from pygame.locals import *

RESOLUTION = (1280, 768)
MODE_ECRAN = DOUBLEBUF
DIMENSION = (10, 20)
TAILLE = 32
ECARTX = 50

fenetre = None
evenements = None
nbJoueurs = 0
boucle = True

nbManettes = 0
manettes = {}
nbBoutons = 0
tetris_joueurs = {}

fonts = {}
ecritures = {}

idFond = 0
IMG_FOND = []


fond = False
mode_bmp = True
musique = True
joueur_clavier = False


AUDIOS = {}
IMAGES = {}

cycle_partie = 0
duree_partie = 180000
fin_partie = False
partie_demarree = False


class CBouton:
    B_X = 0
    B_A = 1
    B_B = 2
    B_Y = 3
    B_L = 4
    B_R = 5
    B_START = 9
    B_SELECT = 8
