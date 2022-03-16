
import pygame
from pygame.locals import *

from moteur import *
from partie import *
from controles import *

import time
import variables as VAR

class CInit():
    def initialiser():
        print("+ TETRIS")

        # --- initialisation du moteur Pygame
        pygame.init()

        # --- création de la fenetre
        VAR.fenetre = pygame.display.set_mode(VAR.RESOLUTION, MODE_ECRAN, 32) #: DOUBLEBUF
        pygame.display.set_caption("PyTris")
        


        VAR.fenetre.blit(pygame.image.load("fonds\\titre.jpg"), (0,0))
        pygame.display.flip()

        CInit.initialiser_ecritures()
        CControle.initialiser_manettes()
        CInit.initialiser_decors()
        CInit.initialiser_fond()
        CInit.initialiser_musique()
        CControle.initialiser_les_joueurs()

    def initialiser_musique():
        if musique:
            pygame.mixer.init()
            pygame.mixer.music.load("audios\\music00.mp3")
            pygame.mixer.music.play()

            VAR.AUDIOS["fixe"] = pygame.mixer.Sound("audios\\fall.wav")
            VAR.AUDIOS["ligne"] = pygame.mixer.Sound("audios\\line.wav")
            VAR.AUDIOS["rotation"] = pygame.mixer.Sound("audios\\selection.wav")

    def initialiser_decors():   
        imgTmp = pygame.image.load("blocs.png")
        VAR.IMAGES["Z"] = (FCT.image_decoupe(imgTmp, 0, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 0, 1, 25, 25, VAR.TAILLE, VAR.TAILLE))
        VAR.IMAGES["T"] = (FCT.image_decoupe(imgTmp, 1, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 1, 1, 25, 25, VAR.TAILLE, VAR.TAILLE))
        VAR.IMAGES["O"] = (FCT.image_decoupe(imgTmp, 2, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 2, 1, 25, 25, VAR.TAILLE, VAR.TAILLE))
        VAR.IMAGES["L"] = (FCT.image_decoupe(imgTmp, 3, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 3, 1, 25, 25, VAR.TAILLE, VAR.TAILLE))
        VAR.IMAGES["J"] = (FCT.image_decoupe(imgTmp, 4, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 4, 1, 25, 25, VAR.TAILLE, VAR.TAILLE))
        VAR.IMAGES["S"] = (FCT.image_decoupe(imgTmp, 5, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 5, 1, 25, 25, VAR.TAILLE, VAR.TAILLE))
        VAR.IMAGES["I"] = (FCT.image_decoupe(imgTmp, 6, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 6, 1, 25, 25, VAR.TAILLE, VAR.TAILLE))
        
        VAR.IMAGES["X"] = (FCT.image_decoupe(imgTmp, 8, 0, 27, 27, VAR.TAILLE+2, VAR.TAILLE+2), FCT.image_decoupe(imgTmp, 8, 1, 27, 27, VAR.TAILLE+2, VAR.TAILLE+2))

    def initialiser_fond():
        if not fond: return 

        for i in range(102):
            id = str(i)
            if i<10:
                id = "00" + id
            elif i<100:
                id = "0" + id

            tmpImage = pygame.image.load("fonds\\darkCinematic_"+ id + ".jpg")
            tmpImage = pygame.transform.scale(tmpImage, (VAR.RESOLUTION[0], VAR.RESOLUTION[1]))
            VAR.IMG_FOND.append(tmpImage)

            barre = (VAR.RESOLUTION[0] / 100) * i
            pygame.draw.rect(VAR.fenetre, (255,255,0,255), (0, VAR.RESOLUTION[1]-30, barre, 30), 0)
            pygame.display.flip()

    def initialiser_ecritures():
        for taille in (10, 20, 30, 40, 50, 60, 80):
            VAR.ecritures[taille] = pygame.font.SysFont('arial', taille)    