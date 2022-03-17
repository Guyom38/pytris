
import pygame
from pygame.locals import *

from pieces import *
from grille import *
from mecanique import *
from controles import *
from partie import *
from animation import *


import variables as VAR
from variables import *


class CMoteur():
    def __init__(self, id, idManette):
        print("    + Moteur # " + str(id))

        self.id = id
        
        alpha = 60
        self.couleur = ((210,0,0,alpha),(173,212,0,alpha),(212,194,0,alpha),(210,140,0,alpha),(0,106,203,alpha),(0,212,57,alpha),(0,188,210,alpha),(245,130,244,alpha),(20,81,16,alpha) )[id]
        
        self.idManette = idManette

        self.actif = False
        self.grille = None

        self.Partie = None
        self.Pieces = None
        self.Controle = None
        self.Mecanique = None
        self.Animation = None
  

    def initialiser(self):
        self.Pieces = CPieces(self, False)
        self.PiecesAide = CPieces(self, True)
        self.grille = CGrille(self)
        self.Partie = CParties(self)
        self.Controle = CControle(self, self.idManette)
        self.Mecanique = CMecanique(self)
        self.Animation = CAnimation(self)
        self.Partie.demarrer()

    def gestion_piece_aide(self):
        if not self.actif: return

        if self.Partie.aide:
            self.PiecesAide.pieceSelect = self.Pieces.pieceSelect
            self.PiecesAide.pieceRotation = self.Pieces.pieceRotation
            self.PiecesAide.pieceX = self.Pieces.pieceX
            
            self.Mecanique.faire_descendre_a_fond_la_piece(self.PiecesAide)
            self.PiecesAide.afficher_piece()  
              
    def afficher(self):
        self.Controle.gestion_manette()
        self.Mecanique.gravite()
        self.gestion_piece_aide()

        
        self.grille.afficher()
        self.Pieces.afficher_piece()   
        self.Pieces.afficher_piece_suivante()  

        self.Animation.afficher()
        self.Partie.afficher_message()
        self.Partie.afficher_score()

        
    



    
    
    
    


    


        
        
    
        
        


    
                 
    

    
            
            


        


