
import pygame
from pygame.locals import *

from COMMUN.classes.controles import *
from COMMUN.classes.avatars import *
import COMMUN.variables as V

from JEU_Pytris.classes.moteur import *
from JEU_Pytris.classes.partie import *
import JEU_Pytris.variables as VAR



class CInit:
    
    def page_chargement():
        # --- initialisation du moteur Pygame
        titre = pygame.image.load("JEU_Pytris\\images\\titre.jpg")
        titre = pygame.transform.scale(titre, V.RESOLUTION)
        V.fenetre.blit(titre, (0,0))
        pygame.display.flip()
        
    def initialiser():
        print("+ TETRIS")
        
        CInit.initialiser_les_dimensions()
         
        V.ecriture = int((150 / 720) * V.RESOLUTION[1]) 
        pX = int((510 / 1920) * V.RESOLUTION[0]) + 30
        pY = int((700 / 1080) * V.RESOLUTION[1]) 
        
        V.ecritures[200] = pygame.font.SysFont('arial black', V.ecriture)   
        V.fenetre.blit(V.ecritures[200].render("x" + str(V.nbManettes), True, (0,0,0,255)) , (pX-20, pY+20))
        V.fenetre.blit(V.ecritures[200].render("x" + str(V.nbManettes), True, (255,255,255,255)) , (pX, pY))
   
        CInit.initialiser_decors()
        CInit.initialiser_audios()
        CInit.initialiser_les_joueurs()

        #FCT.charger_musique("attente.mp3")
        
        
        
        
    def initialiser_les_joueurs():
        j = 0
        if V.joueur_clavier: j = 1    
                        
        V.moteurs = {}
        for i in range(V.nbManettes+j):
            V.moteurs[i] =  CMoteur(V.joueurs[i])
            V.moteurs[i].initialiser()
            V.moteurs[i].Joueur.Avatar.ratioX, V.moteurs[i].Joueur.Avatar.ratioY = VAR.TAILLE * 0.007, VAR.TAILLE * 0.007

            barre = (200 / V.nbManettes+j) * i
            pygame.draw.rect(V.fenetre, (255,255,0,255), (0, V.RESOLUTION[1]-30, barre, 30), 0)
            pygame.display.flip()
        
        V.nbJoueurs = len(V.moteurs)
        
        
    def initialiser_les_dimensions():
        j = 0
        if V.joueur_clavier: j = 1

        if V.nbManettes+j == 9: VAR.TAILLE, VAR.ECARTX = 18, 33
        if V.nbManettes+j == 8: VAR.TAILLE, VAR.ECARTX = 20, 40
        if V.nbManettes+j == 7: VAR.TAILLE, VAR.ECARTX = 23, 45
        if V.nbManettes+j == 6: VAR.TAILLE, VAR.ECARTX = 25, 70        
        if V.nbManettes+j == 5: VAR.TAILLE, VAR.ECARTX = 30, 84        
        if V.nbManettes+j == 4: VAR.TAILLE, VAR.ECARTX = 32, 80        
        if V.nbManettes+j == 3: VAR.TAILLE, VAR.ECARTX = 32, 120        
        if V.nbManettes+j == 2: VAR.TAILLE, VAR.ECARTX = 32, 300
        if V.nbManettes+j == 1: VAR.TAILLE, VAR.ECARTX = 38, 0
            
        if V.MODE_ECRAN == DOUBLEBUF: VAR.TAILLE, VAR.ECARTX = 20, 80    
        

            
    def initialiser_audios():
        V.AUDIOS["fixe"] = pygame.mixer.Sound("JEU_Pytris\\audios\\fall.wav")
        V.AUDIOS["ligne"] = pygame.mixer.Sound("JEU_Pytris\\audios\\full_line.wav")
        V.AUDIOS["rotation"] = pygame.mixer.Sound("JEU_Pytris\\audios\\rotate_block.wav")
        V.AUDIOS["tetris"] = pygame.mixer.Sound("JEU_Pytris\\audios\\tetris.wav")
        V.AUDIOS["game_over"] = pygame.mixer.Sound("JEU_Pytris\\audios\\game_over.wav")
        V.AUDIOS["level_up"] = pygame.mixer.Sound("JEU_Pytris\\audios\\level_up.wav")
        V.AUDIOS["block"] = pygame.mixer.Sound("JEU_Pytris\\audios\\place_block.wav")
    
    def initialiser_decors():  
        if VAR.TAILLE >= 25: 
            imgTmp = pygame.image.load("JEU_Pytris\\images\\blocs.png")
            V.IMAGES["Z"] = (GIMAGE.image_decoupe(imgTmp, 0, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 0, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["T"] = (GIMAGE.image_decoupe(imgTmp, 1, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 1, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["O"] = (GIMAGE.image_decoupe(imgTmp, 2, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 2, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["L"] = (GIMAGE.image_decoupe(imgTmp, 3, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 3, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["J"] = (GIMAGE.image_decoupe(imgTmp, 4, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 4, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["S"] = (GIMAGE.image_decoupe(imgTmp, 5, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 5, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["I"] = (GIMAGE.image_decoupe(imgTmp, 6, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 6, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["#"] = (GIMAGE.image_decoupe(imgTmp, 7, 0, 25, 25, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 7, 2, 25, 25, VAR.TAILLE, VAR.TAILLE))
            
            V.IMAGES["X"] = (FCT.image_decoupe(imgTmp, 8, 1, 27, 27, VAR.TAILLE+2, VAR.TAILLE+2), GIMAGE.image_decoupe(imgTmp, 8, 1, 27, 27, VAR.TAILLE+2, VAR.TAILLE+2))
        else:
            imgTmp = pygame.image.load("JEU_Pytris\\images\\blocs-mini.png")
            V.IMAGES["Z"] = (GIMAGE.image_decoupe(imgTmp, 0, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 0, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["T"] = (GIMAGE.image_decoupe(imgTmp, 1, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 1, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["O"] = (GIMAGE.image_decoupe(imgTmp, 2, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 2, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["L"] = (GIMAGE.image_decoupe(imgTmp, 3, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 3, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["J"] = (GIMAGE.image_decoupe(imgTmp, 4, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 4, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["S"] = (GIMAGE.image_decoupe(imgTmp, 5, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 5, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["I"] = (GIMAGE.image_decoupe(imgTmp, 6, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 6, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            V.IMAGES["#"] = (GIMAGE.image_decoupe(imgTmp, 7, 0, 20, 20, VAR.TAILLE, VAR.TAILLE), GIMAGE.image_decoupe(imgTmp, 7, 2, 20, 20, VAR.TAILLE, VAR.TAILLE))
            
            V.IMAGES["X"] = (GIMAGE.image_decoupe(imgTmp, 8, 1, 22, 22, VAR.TAILLE+2, VAR.TAILLE+2), GIMAGE.image_decoupe(imgTmp, 8, 1, 22, 22, VAR.TAILLE+2, VAR.TAILLE+2))

    

            


    