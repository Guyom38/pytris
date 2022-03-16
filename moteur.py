
import pygame
from pygame.locals import *

from pieces import *
from grille import *
from mecanique import *
from controles import *
from partie import *

import variables as VAR
from variables import *


class CMoteur():
    def __init__(self, id, location, idManette):
        print("    + Moteur # " + str(id))

        self.id = id
        self.idManette = idManette
        self.location = location
        
        self.actif = False

        self.grille = None
        self.Partie = None
        self.Pieces = None
        self.Controle = None
        self.Mecanique = None

        self.initialiser()

    def initialiser(self):
        self.grille = CGrille(self)
        self.Partie = CParties(self)
        self.Pieces = CPieces(self)
        self.Controle = CControle(self, self.idManette)
        self.Mecanique = CMecanique(self)

        self.Partie.demarrer()
        
    def afficher(self):
        self.Controle.gestion_manette()
        self.Mecanique.gravite()

        self.grille.afficher()
        self.Pieces.afficher_piece()      
        self.Pieces.afficher_piece_suivante()  

        self.Partie.afficher_message()
        self.Partie.afficher_score()



    
    
    
    


    


        
        
    
        
        


    
                 
    

    
            
            


        


