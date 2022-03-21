from COMMUN.avatars import *
from COMMUN.controles import *
from avatars import *

class CJoueur:
    def __init__(self, id):
        
        self.id = id
        self.nom =  CAvatars.LISTE_NOMS[id]
        self.couleur = CAvatars.COULEUR[id]
        
        self.Manette = CControle(self, id - FCT.iif(V.joueur_clavier, 1, 0))
        self.Avatar = CAvatars(self)
        self.actif = False
        
    