
import pygame
from pygame.locals import *

from moteur import *
from partie import *
from controles import *

import time, os
import variables as VAR

from avatars import *


class CInit():
    def initialiser():
        print("+ TETRIS")

        # --- initialisation du moteur Pygame
        pygame.init()

        # --- création de la fenetre
        VAR.fenetre = pygame.display.set_mode(VAR.RESOLUTION, MODE_ECRAN, 32) #: DOUBLEBUF
        pygame.display.set_caption("PyTris")
        

        titre = pygame.image.load("images\\titre.jpg")
        titre = pygame.transform.scale(titre, VAR.RESOLUTION)
        VAR.fenetre.blit(titre, (0,0))
        pygame.display.flip()

        CInit.initialiser_ecritures()
        CControle.initialiser_manettes()
        CInit.initialiser_decors()
        CInit.initialiser_fond()
        CInit.initialiser_musique()
        CControle.initialiser_les_joueurs()

        VAR.avatar = CAvatars()
        
    def initialiser_musique():
        if musique:
            pygame.mixer.init()
            fichier = random.choice(os.listdir("audios\\musics"))
            FCT.charger_musique(fichier)
            

            VAR.AUDIOS["fixe"] = pygame.mixer.Sound("audios\\fall.wav")
            VAR.AUDIOS["ligne"] = pygame.mixer.Sound("audios\\full_line.wav")
            VAR.AUDIOS["rotation"] = pygame.mixer.Sound("audios\\rotate_block.wav")
            VAR.AUDIOS["tetris"] = pygame.mixer.Sound("audios\\tetris.wav")
            VAR.AUDIOS["game_over"] = pygame.mixer.Sound("audios\\game_over.wav")
            VAR.AUDIOS["level_up"] = pygame.mixer.Sound("audios\\level_up.wav")
            VAR.AUDIOS["block"] = pygame.mixer.Sound("audios\\place_block.wav")

    
    def initialiser_decors():  
        if VAR.TAILLE >= 25: 
            imgTmp = pygame.image.load("images\\blocs.png")
            VAR.IMAGES["Z"] = (FCT.image_decoupe(imgTmp, 0, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 0, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["T"] = (FCT.image_decoupe(imgTmp, 1, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 1, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["O"] = (FCT.image_decoupe(imgTmp, 2, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 2, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["L"] = (FCT.image_decoupe(imgTmp, 3, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 3, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["J"] = (FCT.image_decoupe(imgTmp, 4, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 4, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["S"] = (FCT.image_decoupe(imgTmp, 5, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 5, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["I"] = (FCT.image_decoupe(imgTmp, 6, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 6, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["#"] = (FCT.image_decoupe(imgTmp, 7, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 7, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            
            VAR.IMAGES["X"] = (FCT.image_decoupe(imgTmp, 8, 1, 27, 27, VAR.TAILLE+2, VAR.TAILLE+2), FCT.image_decoupe(imgTmp, 8, 1, 27, 27, VAR.TAILLE+2, VAR.TAILLE+2))
        else:
            imgTmp = pygame.image.load("images\\blocs-mini.png")
            VAR.IMAGES["Z"] = (FCT.image_decoupe(imgTmp, 0, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 0, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["T"] = (FCT.image_decoupe(imgTmp, 1, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 1, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["O"] = (FCT.image_decoupe(imgTmp, 2, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 2, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["L"] = (FCT.image_decoupe(imgTmp, 3, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 3, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["J"] = (FCT.image_decoupe(imgTmp, 4, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 4, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["S"] = (FCT.image_decoupe(imgTmp, 5, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 5, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["I"] = (FCT.image_decoupe(imgTmp, 6, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 6, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            VAR.IMAGES["#"] = (FCT.image_decoupe(imgTmp, 7, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), FCT.image_decoupe(imgTmp, 7, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            
            VAR.IMAGES["X"] = (FCT.image_decoupe(imgTmp, 8, 1, 22, 22, VAR.TAILLE+2, VAR.TAILLE+2), FCT.image_decoupe(imgTmp, 8, 1, 22, 22, VAR.TAILLE+2, VAR.TAILLE+2))

    def initialiser_fond():
        if not fond: return 

        VAR.IMG_FOND = []

        i = 0
        dossiers = os.listdir("fonds")
        #for dossier in dossiers:
        if 1 == 1:
            dossier = random.choice(dossiers)
            fichiers = os.listdir("fonds\\"+dossier)
            print("FOND : " + dossier)
            for fichier in fichiers:
                tmpImage = pygame.image.load("fonds\\"+dossier+"\\"+fichier)
                tmpImage = pygame.transform.scale(tmpImage, (VAR.RESOLUTION[0], VAR.RESOLUTION[1]))
                VAR.IMG_FOND.append(tmpImage)   
                barre = (VAR.RESOLUTION[0] / (len(fichiers))) * i
                i += 1
                
                pygame.draw.rect(VAR.fenetre, (255,255,0,255), (0, VAR.RESOLUTION[1]-30, barre, 30), 0)
                pygame.display.flip()

            


    def initialiser_ecritures():
        for taille in (10, 20, 30, 40, 50, 60, 80):
            VAR.ecritures[taille] = pygame.font.SysFont('arial', taille)    