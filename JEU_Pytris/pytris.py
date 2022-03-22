
import pygame
from pygame.locals import *

from COMMUN.classes.controles import *
from COMMUN.salon import *
from COMMUN.commun import *
import COMMUN.variables as V

from JEU_Pytris.classes.moteur import *
from JEU_Pytris.classes.partie import *
from JEU_Pytris.classes.init import *
from JEU_Pytris.classes.highscore import * 
import JEU_Pytris.variables as VAR


class CPyTris:
    def __init__(self, c):
        self.C = c
    
        
        CInit.page_chargement()
        self.C.initialiser_ecritures ([10, 20, 30, 40, 50, 60, 80, 100, 120, 200])
        CInit.initialiser()
        
    
    def surveille_demarrage(self):
        
        if not VAR.partie_demarree and not VAR.fin_partie:
            pret = False
            for i, joueur in V.joueurs.items():
                if joueur.actif: pret = True

            if pret:
                for i, joueur in V.Joueurs.items():
                    joueur.actif == True
                VAR.partie_demarree = True

            
    
                

    def afficher(self):
        liste_scores = []
        for i in range(V.nbJoueurs):
            VAR.tetris_joueurs[i].Manette.gestion_evenements()
            VAR.tetris_joueurs[i].afficher()    
            liste_scores.append((VAR.tetris_joueurs[i].Partie.score, i))
        
        rang = V.nbJoueurs
        liste_triee = sorted(liste_scores)
        for score,i in liste_triee:
            VAR.tetris_joueurs[i].Partie.rang = rang
            rang-=1

    def afficher_temps(self):
        if not VAR.partie_en_cours(): return

        couleur_fond_grille = (28, 28, 28, 200)
        couleur_contour_grille = (128,128,128,200)

        largeur_barre = int(V.RESOLUTION[0] * 0.66)
        hauteur_barre = int(V.RESOLUTION[1] * 0.05)
        pX = int((V.RESOLUTION[0] - largeur_barre) / 2)
        pY = V.RESOLUTION[1] - hauteur_barre - 20
        temps = CParties.temps_ecoule()
        if temps <=0: temps = 0
        barre = (largeur_barre / VAR.duree_partie) * temps
        
        pygame.draw.rect(V.fenetre, couleur_fond_grille, (pX, pY, largeur_barre, hauteur_barre),0)
        pygame.draw.rect(V.fenetre, (128,128,128,200), (pX, pY, barre, hauteur_barre),0)
        pygame.draw.rect(V.fenetre, couleur_contour_grille, (pX, pY, largeur_barre, hauteur_barre),2)
        
        image_temps = V.ecritures[40].render("TEMPS  RESTANT   " + GTEMPS.format_temps((VAR.duree_partie - temps) // 1000) , True, (255,255,255,255)) 
        V.fenetre.blit(image_temps, ((V.RESOLUTION[0] - image_temps.get_width()) // 2, pY+((hauteur_barre-image_temps.get_height()) //2)))








   



 
            
            
    def gestion_manettes_minimum(self):
        for i, joueur in VAR.tetris_joueurs.items():
            joueur.Controle.gestion_evenements()
            


    def compte_a_rebours_partie(self):
        if not VAR.partie_demarree:
            if VAR.compteARebours_cycle == -1:
                VAR.compteARebours_cycle = pygame.time.get_ticks()
                
            if pygame.time.get_ticks() - VAR.compteARebours_cycle > VAR.compteARebours_Delais:
                VAR.partie_demarree = True
                VAR.cycle_partie = pygame.time.get_ticks()
                VAR.compteARebours_cycle = -1
                
                for i, joueur in VAR.tetris_joueurs.items():
                    joueur.actif = True

            else:
                
                reste = (VAR.compteARebours_Delais // 1000) - (pygame.time.get_ticks() - VAR.compteARebours_cycle) // 1000
                image_temps = V.ecritures[200].render(str(reste), True, (0,0,0,255)) 
                pX, pY = (V.RESOLUTION[0] - image_temps.get_width()) //2, (V.RESOLUTION[1] - image_temps.get_height()) //2
                V.fenetre.blit(image_temps, (pX-10, pY+10))
                image_temps = V.ecritures[200].render(str(reste), True, (255,255,255,255)) 
                V.fenetre.blit(image_temps, (pX, pY))
                
    def jeu_PyTris(self):
        
        
        V.boucle = True
        while V.boucle:
            CControle.capture_evements_utilisateurs()
             
            self.C.gestion_musique()
            self.C.afficher_fond()
            
            if VAR.mode == VAR.MODE_SCORE:
                CHighscore.afficher()
                self.gestion_manettes_minimum()
                
            elif VAR.mode == VAR.MODE_JEU:
                if VAR.pp:
                    
                    CInit.initialiser_fond()
                    
                    j = 0
                    for i in range(VAR.nbManettes):                                        
                        VAR.tetris_joueurs[i+j].initialiser(False)
                    VAR.cycle_partie == -1
                    VAR.fin_partie = False  
                    VAR.pp = False
                    
                self.afficher()
                self.afficher_temps()
                            
                CParties.gestion_malediction()
                CParties.controle_fin_de_partie()

                self.compte_a_rebours_partie()
                #surveille_demarrage()
    
            self.C.afficher_rendu()
        pygame.quit() 



if __name__ == '__main__':        
    pytris = CPyTris()
    pytris.jeu_PyTris()