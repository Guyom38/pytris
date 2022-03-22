
import pygame
from pygame.locals import *

import COMMUN.variables as V
from COMMUN.classes.controles import *
from COMMUN.classes.avatars import *
from COMMUN.classes.joueur import *
from COMMUN.salon import *

import COMMUN.classes.fonctions as FCT
import os, random

class CCommun:
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
    def __init__(self, titre):
        pygame.init()
         
        V.fenetre = pygame.display.set_mode(V.RESOLUTION, V.MODE_ECRAN, 32) #: DOUBLEBUF
        pygame.display.set_caption(titre)
        
        random.shuffle(CAvatars.LISTE_NOMS)

        self.Salon = CSalon()
        
        
        
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
    def get_nbJoueurs():
        return len(CControle.manettes)
    
    def add_ecriture(self, nom, police, taille):
        V.ecritures[nom] = pygame.font.SysFont(police, taille)    
        
     
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
    def initialiser(self):
        CControle.initialiser_manettes()
        CAvatars.chargement_fichiers_sprites()
        
        self.initialiser_joueurs()
        self.initialiser_fond()
        self.initialiser_musiques()
        
        V.horloge = pygame.time.Clock()
          
    def initialiser_joueurs(self):
        for i in range(V.nbManettes):
            V.joueurs[i] = CJoueur(i)
                    
    def initialiser_ecritures(self, liste_polices):
        for taille in liste_polices:
            self.add_ecriture(taille, "arial", taille)
    
    def initialiser_musiques(self, chemin = ""):
        if V.musique:
            pygame.mixer.init()
            #fichier = random.choice(os.listdir("JEU_Pytris\\audios\\musics\\" + chemin))
            #FCT.charger_musique("musics\\" + chemin + fichier)    
            
    def initialiser_fond(self, chemin = ""):
        if not V.fond: return 

        V.IMG_FOND = []
        V.idFond = 0

        i = 0
        dossiers = os.listdir("JEU_Pytris\\fonds" + chemin)
        #for dossier in dossiers:
        if 1 == 1:
            dossier = random.choice(dossiers)
            fichiers = os.listdir("JEU_Pytris\\fonds\\"+chemin + dossier)

            for fichier in fichiers:
                tmpImage = pygame.image.load("JEU_Pytris\\fonds\\"+chemin + dossier+"\\"+fichier)
                tmpImage = pygame.transform.scale(tmpImage, (V.RESOLUTION[0], V.RESOLUTION[1]))
                V.IMG_FOND.append(tmpImage)   
                barre = ((V.RESOLUTION[0]-200) / (len(fichiers))) * i
                i += 1
                
                pygame.draw.rect(V.fenetre, (255,255,0,255), (0, V.RESOLUTION[1]-30, barre, 30), 0)
                pygame.display.flip()
        
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
    def afficher_fond(self):
        if not V.fond:
            V.fenetre.fill((96,96,96))
        else:
            V.fenetre.blit(V.IMG_FOND[V.idFond], (0,0), (0,0,V.RESOLUTION[0], V.RESOLUTION[1]))
            if pygame.time.get_ticks() - V.fondVideo_cycle > V.fondVideo_frequence:
                V.idFond +=1
                if V.idFond > len(V.IMG_FOND) -1: V.idFond = 0
                V.fondVideo_cycle = pygame.time.get_ticks()
                
    def afficher_fps(self):
        if pygame.time.get_ticks() - V.fps_cycle > 1000:
            V.fps = V.fps_cpt
            V.fps_cpt = 0
            V.fps_cycle = pygame.time.get_ticks()
        V.fps_cpt +=1
    
        image_score = V.ecritures[20].render("FPS : " + str(V.fps), True, (255,255,255,255)) 
        V.fenetre.blit(image_score, (0, 0))
        
    def afficher_rendu(self):
        self.afficher_fps()
        
        pygame.display.update()
        V.horloge.tick(0)
        
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
    def gestion_musique(self):
        FCT.jouer_musique()
    
    