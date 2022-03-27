
import pygame
from pygame.locals import *
from COMMUN.highscore import CHighscore

import COMMUN.variables as V
from COMMUN.classes.controles import *
from COMMUN.classes.avatars import *
from COMMUN.classes.joueur import *
from COMMUN.salon import *

from COMMUN.classes.fonctions import *
import os, random

from JEU_Pytris.init import CInit

class CCommun:
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
    def __init__(self, titre):
        pygame.init()
         
        V.fenetre = pygame.display.set_mode(V.RESOLUTION, V.MODE_ECRAN, 32) #: DOUBLEBUF
        pygame.display.set_caption(titre)
        
        self.page_chargement()
        random.shuffle(CAvatars.LISTE_NOMS)
        
        self.compte_a_rebours = FCT.GTEMPS.chrono(V.compte_a_rebours_delais, -1)
        
        self.Salon = CSalon(self)
        self.Highscore = CHighscore(self)
        
    def page_chargement(self):
        # --- initialisation du moteur Pygame
        titre = pygame.image.load("JEU_Pytris\\images\\titre.jpg")
        titre = pygame.transform.scale(titre, V.RESOLUTION)
        V.fenetre.blit(titre, (0,0))
        pygame.display.flip()   
        
        self.initialiser()
        
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
    def get_nbJoueurs():
        return len(CControle.manettes)
    
    
        
     
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
    def initialiser(self):
        CControle.initialiser_manettes()
        CInit.afficher_nombres_manettes()
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
            GFONT.add_ecriture(taille, "arial", taille)
    
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


    def compte_a_rebours_partie(self):
        relance_partie = False
        if not V.partie_demarree:
            if self.compte_a_rebours.cycle == -1:     # --- Initialise le compte a rebours de debut de partie  
                self.compte_a_rebours.reset()        
                
            if self.compte_a_rebours.controle():      # --- Demarre la partie en fin de compte a rebours
                self.compte_a_rebours.reset(-1)
                
                V.partie_demarree = True
                relance_partie = True
                
                for i, moteur in V.moteurs.items():
                    moteur.Joueur.actif = True

            else:
                self.afficher_compte_a_rebours()    
        return relance_partie          
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------

    # ---
    # --- Affichage du compte a rebours de début de partie
    def afficher_compte_a_rebours(self):
        reste = (self.compte_a_rebours.frequence // 1000) - (self.compte_a_rebours.get_temps_restant()) // 1000
        image_temps = FCT.GFONT.get_image_texte(str(reste), 200, (0,0,0,255)) 
        pX, pY = (V.RESOLUTION[0] - image_temps.get_width()) //2, (V.RESOLUTION[1] - image_temps.get_height()) //2
        V.fenetre.blit(image_temps, (pX-10, pY+10))
        image_temps = FCT.GFONT.get_image_texte(str(reste), 200, (255,255,255,255)) 
        V.fenetre.blit(image_temps, (pX, pY))
        
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
    
        image_score = GFONT.get_image_texte("FPS : " + str(V.fps), 20, (255,255,255,255)) 
        V.fenetre.blit(image_score, (0, 0))
        
    def afficher_rendu(self):
        self.afficher_fps()
        
        pygame.display.update()
        V.horloge.tick(V.fps_max)
        
# ---------------------------------------------------------------------------------------------------------------
# -
# ---------------------------------------------------------------------------------------------------------------
    def gestion_musique(self):
        GAUDIO.jouer_musique()
    
    