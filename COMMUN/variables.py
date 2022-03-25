from pygame.locals import *

RESOLUTION = ((1280, 800),(1920, 1080))[0]
MODE_ECRAN = (DOUBLEBUF,FULLSCREEN)[0]
ECRITURE_PAR_DEFAULT = "Arial"

horloge = None
fenetre = None
boucle = True
    
ecritures = {}
moteurs = {}

fond = True
idFond = 0
IMG_FOND = []
fondVideo_cycle = 0
fondVideo_frequence =  35

joueur_clavier = False


AUDIOS = {}
audio = True
musique = True

IMAGES = {}
temps = {}

cycle = 0
fps = 0
fps_cpt = 0
fps_cycle = 0
fps_max = 50

joueurs = {}
nbManettes = 0
nbBoutons = 0
manettes = {}
    
evenements = None
partie_demarree = False
fin_partie = False

def joueurs_actifs():
    for i, joueur in joueurs.items():
        if joueur.actif: return True
    return False

def joueurs_prets():
    for i, joueur in joueurs.items():
        if not joueur.actif: return False
    return True

def get_nb_joueurs():
    return (len(moteurs))


