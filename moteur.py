
import pygame
from pygame.locals import *

from pieces import *
from grille import *
from mecanique import *
from controles import *
from partie import *
from animation import *
from avatars import *

import variables as VAR
from variables import *


class CMoteur():
    def __init__(self, id, idManette):
        print("    + Moteur # " + str(id))

        self.id = id
        
        alpha = 60
        self.couleur = ((232,147,15,alpha), \
                        (110,68,216,alpha), \
                        (20,163,194,alpha), \
                        (216,78,28,alpha), \
                        (240,212,72,alpha), \
                        (53,53,86,alpha), \
                        (216,68,18,alpha), \
                        (158,57,34,alpha), \
                        (224,224,224,alpha), \
                        (59,59,59,alpha))[id]
        
        self.idManette = idManette

        self.actif = False
        self.grille = None

        self.Partie = None
        self.Pieces = None
        self.Controle = None
        self.Mecanique = None
        self.Animation = None
        self.Avatar = None

    def initialiser(self):
        self.Pieces = CPieces(self, False)
        self.PiecesAide = CPieces(self, True)
        self.grille = CGrille(self)
        self.Partie = CParties(self)
        self.Controle = CControle(self, self.idManette)
        self.Mecanique = CMecanique(self)
        self.Animation = CAnimation(self)
        self.Avatar = CAvatars(self)
        
        self.Partie.demarrer()

    def gestion_piece_aide(self):
        if not self.actif: return

        if self.Partie.aide:
            self.PiecesAide.pieceSelect = self.Pieces.pieceSelect
            self.PiecesAide.pieceRotation = self.Pieces.pieceRotation
            self.PiecesAide.pieceX = self.Pieces.pieceX
            self.PiecesAide.pieceY = -2
            self.Mecanique.faire_descendre_a_fond_la_piece(self.PiecesAide)
            self.PiecesAide.afficher_piece()  
              
    def afficher(self):
        self.Controle.gestion_manette()
        self.Mecanique.gravite()
        
        
        self.grille.afficher()
        self.gestion_piece_aide()

        self.Pieces.afficher_piece()   
        self.Pieces.afficher_piece_suivante()  

        self.Animation.afficher()
        self.Partie.afficher_message()
        self.Partie.afficher_score()
        
        self.Avatar.afficher(self.grille.offX , self.grille.offY + (VAR.TAILLE * VAR.DIMENSION[1]) )

        
    



    
    
    
    


    


        
        
    
        
        


    
                 
    

    
            
            


        


