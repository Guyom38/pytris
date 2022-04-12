from enum import *
class ENUM_ETAT(Enum):
    SUCCES = 1
    ECHEC = -1   
    AUCUN = 0

NOIR=(0,0,0)
GRIS=(255,255,255)
ROUGE=(255,0,0)
BLANC=(255,255,255)

partie_en_cours = True

nombre_decors = 40
altitude = 400
pas = 10