
import pygame
from pygame.locals import *

from COMMUN.classes.controles import *
from COMMUN.salon import *
from COMMUN.commun import *
import COMMUN.variables as V

from JEU_Pytris.classes.moteur import *
from JEU_Pytris.classes.partie import *
from JEU_Pytris.init import *
from COMMUN.highscore import * 

import JEU_Pytris.variables as VAR
from JEU_Pytris.variables import *

# █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
# █  Classe principale du jeu PYTRIS                                        █
# █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

class CPyTris:
    def __init__(self, c, websocket):
        self.C = c
        self.actions_websocket = websocket
        
        CInit.page_chargement()
        CInit.initialiser()
    
    # █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
    # █  Fonctions                                                              █
    # █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

    def calcul_du_rang(self):
        liste_scores = []
        for id in range(V.get_nb_joueurs()):
            liste_scores.append((V.moteurs[id].Partie.score, id))
        
        rang = V.get_nb_joueurs()
        liste_triee = sorted(liste_scores)
        for score, id in liste_triee:
            V.moteurs[id].Partie.rang = rang
            rang-=1

    

    def gestion_manettes_minimum(self):
        for i, moteur in V.moteurs.items():
            moteur.Manette.gestion_evenements_start()
    
    def relance_la_partie(self):
        VAR.relancePartie = False       

        self.C.initialiser_fond()
                    
        for i, moteur in V.moteurs.items():                                        
            moteur.initialiser()
        
        VAR.temps_de_partie.reset(-1)
        V.fin_partie = False  
        #self.changer_musique()
        

    # █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
    # █  Gestion de l'affichage                                                 █
    # █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

    # ---
    # --- Traitement des actions joueurs et affichage des joueurs
    def afficher_les_joueurs(self):
        for i, moteur in V.moteurs.items():
            moteur.Manette.gestion_evenements()
            moteur.afficher()    

    # ---
    # --- Affichage du temps restant de la partie
    def afficher_temps(self):
        if not V.partie_demarree: return
        
        temps = VAR.temps_de_partie.get_temps_restant()
        if temps <=0: temps = 0

        couleur_fond_grille = (28, 28, 28, 200)
        couleur_contour_grille = (128,128,128,200)

        largeur_barre = int(V.RESOLUTION[0] * 0.66)
        hauteur_barre = int(V.RESOLUTION[1] * 0.05)
        pX = int((V.RESOLUTION[0] - largeur_barre) / 2)
        pY = V.RESOLUTION[1] - hauteur_barre - 20
        barre = (largeur_barre / VAR.duree_partie) * temps
        
        pygame.draw.rect(V.fenetre, couleur_fond_grille, (pX, pY, largeur_barre, hauteur_barre),0)
        pygame.draw.rect(V.fenetre, (128,128,128,200), (pX, pY, barre, hauteur_barre),0)
        pygame.draw.rect(V.fenetre, couleur_contour_grille, (pX, pY, largeur_barre, hauteur_barre),2)
        
        image_temps = FCT.GFONT.get_image_texte("TEMPS  RESTANT   " + GTEMPS.format_temps((VAR.duree_partie - temps) // 1000) , 40, (255,255,255,255)) 
        V.fenetre.blit(image_temps, ((V.RESOLUTION[0] - image_temps.get_width()) // 2, pY+((hauteur_barre-image_temps.get_height()) //2)))

    
        
        
    # █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
    # █  Boucle du jeu                                                          █
    # █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

    def boucle_score(self):
        self.gestion_manettes_minimum()
        self.C.Highscore.afficher()


    def boucle_jeu(self):
        if VAR.relancePartie:
            self.relance_la_partie()
               
        self.calcul_du_rang()
        self.afficher_les_joueurs()
        self.afficher_temps()
        
        if self.C.compte_a_rebours_partie():
            VAR.temps_de_partie.reset(-1)

        CParties.gestion_malediction()
        CParties.controle_fin_de_partie()

    def changer_musique(self):
        fichier = random.choice(os.listdir("JEU_Pytris\\audios\\musics" ))
        FCT.GAUDIO.charger_musique("JEU_Pytris\\audios\\musics\\" + fichier)    
        
    def boucle(self):
        self.changer_musique()
            
        V.boucle = True
        while V.boucle:
            CControle.capture_evements_utilisateurs()
             
            self.C.gestion_musique()
            self.C.afficher_fond()
            
            if VAR.mode == VAR.ENUM_MODE.MODE_SCORE:    self.boucle_score()                
            elif VAR.mode == VAR.ENUM_MODE.MODE_JEU:    self.boucle_jeu()
    
            self.C.afficher_rendu()
        pygame.quit() 
