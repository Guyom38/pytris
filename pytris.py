import pygame
from pygame.locals import *

from moteur import *
from partie import *
from init import *
from controles import *

import variables as VAR


           
def afficher_fond():
    if not VAR.fond:
        VAR.fenetre.fill((96,96,96))
    else:
        VAR.fenetre.blit(VAR.IMG_FOND[VAR.idFond], (0,0), (0,0,VAR.RESOLUTION[0], VAR.RESOLUTION[1]))
        VAR.idFond +=1
        if VAR.idFond > len(VAR.IMG_FOND) -1: VAR.idFond = 0

def afficher_tetris():
    liste_scores = []
    for i in range(VAR.nbJoueurs):
        VAR.tetris_joueurs[i].afficher()    
        liste_scores.append((VAR.tetris_joueurs[i].Partie.score, i))
    
    rang = VAR.nbJoueurs
    liste_triee = sorted(liste_scores)
    for score,i in liste_triee:
        VAR.tetris_joueurs[i].rang = rang
        rang-=1

def afficher_temps():
    if not VAR.partie_demarree: return

    couleur_fond_grille = (28, 28, 28, 200)
    couleur_cellule = (16,16,16,255)
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
    pygame.draw.rect(VAR.fenetre, couleur_contour_grille, (pX, pY, largeur_barre, hauteur_barre),4)
    
    image_temps = ecritures[40].render("TEMPS  " + FCT.format_temps((VAR.duree_partie - temps) // 1000) , True, (255,255,255,255)) 
    VAR.fenetre.blit(image_temps, ((VAR.RESOLUTION[0] - image_temps.get_width()) // 2, pY+((hauteur_barre-image_temps.get_height()) //2)))





def gestion_fps():

    if pygame.time.get_ticks() - VAR.fps_cycle > 1000:
        VAR.fps = VAR.fps_cpt
        VAR.fps_cpt = 0
        VAR.fps_cycle = pygame.time.get_ticks()
    VAR.fps_cpt +=1

    image_score = ecritures[20].render("FPS : " + str(VAR.fps), True, (255,255,255,255)) 
    VAR.fenetre.blit(image_score, (0, 0))

def rendu():
    gestion_fps()
    
    pygame.display.update()
    VAR.horloge.tick(0)

def gestion_musique():
    if VAR.partie_demarree:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
    else:
        pygame.mixer.music.stop()
        
def jeu_PyTris():
    CInit.initialiser()

    VAR.horloge = pygame.time.Clock()
  
    VAR.boucle = True
    while VAR.boucle:
        CControle.capture_evements_utilisateurs()
        gestion_musique()
        
        afficher_fond()
        afficher_tetris()
        afficher_temps()
        
        CControle.controle_fermeture_fenetre()
        CParties.gestion_malediction()
        CParties.controle_fin_de_partie()

        rendu()
    pygame.quit() 



if __name__ == '__main__':        
    jeu_PyTris()