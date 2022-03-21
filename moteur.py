
import pygame
from pygame.locals import *

from pieces import *
from grille import *
from mecanique import *
from COMMUN.controles import *
from partie import *
from animation import *
from COMMUN.avatars import *

import variables as VAR
from variables import *
import COMMUN.variables as V

class CMoteur():
    def __init__(self, joueur):
        self.Joueur = joueur

        self.grille = None
        self.Partie = None
        self.Pieces = None
        self.Mecanique = None
        self.Animation = None

        
    def initialiser(self):
        self.Pieces = CPieces(self, False)
        self.PiecesAide = CPieces(self, True)
        self.grille = CGrille(self)
        self.Partie = CParties(self)
        
        self.Mecanique = CMecanique(self)
        self.Animation = CAnimation(self)
        
               #self.Controle = CControle(self, self.idManette)
        #if nouveau_perso:
        #    self.Avatar = CAvatars(self)
        
        self.Partie.demarrer()

    def gestion_piece_aide(self):
        if not self.Joueur.actif: return

        if self.Partie.aide:
            self.PiecesAide.pieceSelect = self.Pieces.pieceSelect
            self.PiecesAide.pieceRotation = self.Pieces.pieceRotation
            self.PiecesAide.pieceX = self.Pieces.pieceX
            self.PiecesAide.pieceY = -2
            self.Mecanique.faire_descendre_a_fond_la_piece(self.PiecesAide)
            self.PiecesAide.afficher_piece()  
              
    def afficher(self):
        
        self.Mecanique.gestion_mecanique_du_jeu()
                
        self.grille.afficher()
        self.gestion_piece_aide()

        self.Pieces.afficher_piece()   
        self.Pieces.afficher_piece_suivante()  

        self.Animation.afficher()
        self.Partie.afficher_message()
        self.Partie.afficher_score()
        
        # --- Les mets au meme niveau
        x = self.grille.offX + self.grille.cadreBas[0] - VAR.marge
        y = self.grille.offY + (VAR.DIMENSION[1] * VAR.TAILLE) + self.grille.cadreBas[3] + VAR.marge
        self.Joueur.Avatar.afficher(x, y)

        
    



    
    
    
    


    


        
        
    
        
        


    
                 
    

    
            
            


        


