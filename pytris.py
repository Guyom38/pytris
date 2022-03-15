import pygame
from pygame.locals import *

from moteur import *

import variables as VAR

def initialiser_manettes():
    pygame.joystick.init()
    VAR.nbManettes = pygame.joystick.get_count()
    if VAR.nbManettes == 0: return False

    VAR.manettes = {}
    for idManette in range(VAR.nbManettes):
        VAR.manettes[idManette] = pygame.joystick.Joystick(idManette) 
        VAR.manettes[idManette].init()
    
    VAR.nbBoutons = VAR.manettes[0].get_numbuttons()

def lancer():
    # --- initialisation du moteur Pygame
    pygame.init()

    # --- création de la fenetre
    VAR.fenetre = pygame.display.set_mode(VAR.RESOLUTION, pygame.DOUBLEBUF, 32)
    pygame.display.set_caption("PyTris")
    initialiser_manettes()

   
    # --- création d'un horloge pour limiter le raffraichissement
    horloge = pygame.time.Clock()
    boucle = True

    tetris_joueur1 = CMoteur(1, (32, 32))
    tetris_joueur1.demarrer()

    while boucle:
        VAR.evenements = pygame.event.get()
        # --- récupére l'ensemble des évènements
        for event in VAR.evenements:        
            # --- si l'utilisateur clic sur la croix, ou appuie sur la touche ESCAPE
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                boucle = False


        # --- remplissage de la fenetre avec une couleur proche du noir
        VAR.fenetre.fill((96,96,96))
        
        tetris_joueur1.afficher()
            


        # --- afficher le résultat
        pygame.display.update()
        horloge.tick(60)

    # --- en sortie de boucle, quitte le programme
    pygame.quit() 

lancer()