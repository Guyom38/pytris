from COMMUN.classes.avatars import *
from COMMUN.classes.controles import *

class CJoueur:
    def __init__(self, id):
        
        self.id = id
        self.nom =  CAvatars.LISTE_NOMS[id]
        self.couleur = CAvatars.COULEUR[id]
        
        self.Manette = CControle(self)
        self.Avatar = CAvatars(self)
        self.actif = False
        
    