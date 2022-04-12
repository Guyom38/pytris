import COMMUN.classes.avatars as CA
import COMMUN.classes.controles as CC

class CJoueur:
    def __init__(self, id):
        
        self.id = id
        self.nom =  CA.CAvatars.LISTE_NOMS[id]
        self.couleur = CA.CAvatars.COULEUR[id]
        self.Avatar = CA.CAvatars(self)        
        self.Manette = CC.CControle(self)

        self.actif = False
        
    