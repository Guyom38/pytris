import pygame
from pygame.locals import *

from moteur import *
from partie import *
from init import *
from controles import *

from highscore import * 
from salon import *

import variables as VAR
import avatars

def surveille_demarrage():
    
    if not VAR.partie_demarree and not VAR.fin_partie:
        pret = False
        for i, joueur in VAR.tetris_joueurs.items():
            if joueur.actif: pret = True

        if pret:
            for i, joueur in VAR.tetris_joueurs.items():
                joueur.actif == True
            VAR.partie_demarree = True

           
def afficher_fond():
    if not VAR.fond:
        VAR.fenetre.fill((96,96,96))
    else:
        VAR.fenetre.blit(VAR.IMG_FOND[VAR.idFond], (0,0), (0,0,VAR.RESOLUTION[0], VAR.RESOLUTION[1]))
        if pygame.time.get_ticks() - VAR.fondVideo_cycle > VAR.fondVideo_frequence:
            VAR.idFond +=1
            if VAR.idFond > len(VAR.IMG_FOND) -1: VAR.idFond = 0
            VAR.fondVideo_cycle = pygame.time.get_ticks()
            

def afficher_tetris():
    liste_scores = []
    for i in range(VAR.nbJoueurs):
        VAR.tetris_joueurs[i].afficher()    
        liste_scores.append((VAR.tetris_joueurs[i].Partie.score, i))
    
    rang = VAR.nbJoueurs
    liste_triee = sorted(liste_scores)
    for score,i in liste_triee:
        VAR.tetris_joueurs[i].Partie.rang = rang
        rang-=1

def afficher_temps():
    if not VAR.partie_en_cours(): return

    couleur_fond_grille = (28, 28, 28, 200)
    couleur_contour_grille = (128,128,128,200)

    largeur_barre = int(VAR.RESOLUTION[0] * 0.66)
    hauteur_barre = int(VAR.RESOLUTION[1] * 0.05)
    pX = int((VAR.RESOLUTION[0] - largeur_barre) / 2)
    pY = VAR.RESOLUTION[1] - hauteur_barre - 20
    temps = CParties.temps_ecoule()
    if temps <=0: temps = 0
    barre = (largeur_barre / VAR.duree_partie) * temps
    
    pygame.draw.rect(VAR.fenetre, couleur_fond_grille, (pX, pY, largeur_barre, hauteur_barre),0)
    pygame.draw.rect(VAR.fenetre, (128,128,128,200), (pX, pY, barre, hauteur_barre),0)
    pygame.draw.rect(VAR.fenetre, couleur_contour_grille, (pX, pY, largeur_barre, hauteur_barre),2)
    
    image_temps = ecritures[40].render("TEMPS  RESTANT   " + FCT.format_temps((VAR.duree_partie - temps) // 1000) , True, (255,255,255,255)) 
    VAR.fenetre.blit(image_temps, ((VAR.RESOLUTION[0] - image_temps.get_width()) // 2, pY+((hauteur_barre-image_temps.get_height()) //2)))





def gestion_fps():
    if pygame.time.get_ticks() - VAR.fps_cycle > 1000:
        VAR.fps = VAR.fps_cpt
        VAR.fps_cpt = 0
        VAR.fps_cycle = pygame.time.get_ticks()
    VAR.fps_cpt +=1
  
    image_score = ecritures[VAR.TAILLE_ECRITURE].render("FPS : " + str(VAR.fps), True, (255,255,255,255)) 
    VAR.fenetre.blit(image_score, (0, 0))


def rendu():
    gestion_fps()
    
    pygame.display.update()
    VAR.horloge.tick(0)


def gestion_musique():
    #if VAR.partie_en_cours() or V:
        FCT.jouer_musique()
    #else:
    #    FCT.arreter_musique()
        
        
def gestion_manettes_minimum():
    for i, joueur in VAR.tetris_joueurs.items():
        joueur.Controle.gestion_evenements()
          


def compte_a_rebours_partie():
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
            image_temps = ecritures[200].render(str(reste), True, (0,0,0,255)) 
            pX, pY = (VAR.RESOLUTION[0] - image_temps.get_width()) //2, (VAR.RESOLUTION[1] - image_temps.get_height()) //2
            VAR.fenetre.blit(image_temps, (pX-10, pY+10))
            image_temps = ecritures[200].render(str(reste), True, (255,255,255,255)) 
            VAR.fenetre.blit(image_temps, (pX, pY))
              
def jeu_PyTris():
    print("jeuPytris")
    CInit.initialiser()
    VAR.horloge = pygame.time.Clock()
    
    VAR.boucle = True
    while VAR.boucle:
        CControle.capture_evements_utilisateurs()
        CControle.controle_fermeture_fenetre()
        
        gestion_musique()
        afficher_fond()
        
        
        if VAR.mode == VAR.MODE_SCORE:
            CHighscore.afficher()
            gestion_manettes_minimum()
        
        elif VAR.mode == VAR.MODE_SALON:
            CSalon.afficher()
            
            
                
        elif VAR.mode == VAR.MODE_JEU:
            
            if VAR.pp:
                
                CInit.initialiser_fond()
                CInit.initialiser_musique()
                #CControle.initialiser_les_joueurs()
                
                j = 0
                for i in range(VAR.nbManettes):                                        
                    VAR.tetris_joueurs[i+j].initialiser(False)
                VAR.cycle_partie == -1
                VAR.fin_partie = False  
                VAR.pp = False
                
            afficher_tetris()
            afficher_temps()
                        
            CParties.gestion_malediction()
            CParties.controle_fin_de_partie()

            compte_a_rebours_partie()
            #surveille_demarrage()
  
        rendu()
    pygame.quit() 



if __name__ == '__main__':        
    jeu_PyTris()