
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

  

    def initialiser(self):
        self.Pieces = CPieces(self, False)
        self.PiecesAide = CPieces(self, True)
        self.grille = CGrille(self)
        self.Partie = CParties(self)
        self.Controle = CControle(self, self.idManette)
        self.Mecanique = CMecanique(self)
        self.Partie.demarrer()

    def gestion_piece_aide(self):
        if self.Partie.aide:
            self.PiecesAide.pieceSelect = self.Pieces.pieceSelect
            self.PiecesAide.pieceRotation = self.Pieces.pieceRotation
            self.PiecesAide.pieceX = self.Pieces.pieceX
            
            self.Mecanique.faire_descendre_a_fond_la_piece(True)
            self.Pieces.afficher_piece(False)  
              
    def afficher(self):
        self.Controle.gestion_manette()
        self.Mecanique.gravite()
        #self.gestion_piece_aide()
        
        self.grille.afficher()
        self.Pieces.afficher_piece(True)   
           
        self.Pieces.afficher_piece_suivante()  

        self.Partie.afficher_message()
        self.Partie.afficher_score()
        
    



    
    
    
    


    


        
        
    
        
        


    
                 
    

    
            
            


        


