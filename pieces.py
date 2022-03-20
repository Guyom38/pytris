

import pygame
from pygame.locals import *

import variables as VAR
import fonctions as FCT

import random


class CPieces():
    pieces_couleurs = {}
    pieces_couleurs["O"] = (0, 0, 36)
    pieces_couleurs["I"] = (104, 107, 55)
    pieces_couleurs["S"] = (61,61,125)
    pieces_couleurs["Z"] = (107, 39, 71)
    pieces_couleurs["L"] = (18, 105, 232)
    pieces_couleurs["J"] = (98, 52, 15)
    pieces_couleurs["T"] = (0, 105, 0)
    pieces_couleurs["#"] = (128, 128, 128, 200)

    pieces = {}
    pieces["O"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 0), \
                     (0, 1, 1, 0), \
                     (0, 0, 0, 0) )]

    pieces["I"] = [( (0, 0, 0, 0), \
                     (1, 1, 1, 1), \
                     (0, 0, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 0) )]

    pieces["S"] = [( (0, 0, 0, 0), \
                     (0, 0, 1, 1), \
                     (0, 1, 1, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 1), \
                     (0, 0, 0, 1), \
                     (0, 0, 0, 0) )]

    pieces["Z"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 0), \
                     (0, 0, 1, 1), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 0, 1), \
                     (0, 0, 1, 1), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) )]

    pieces["L"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 1), \
                     (0, 1, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 1), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 0, 1), \
                     (0, 1, 1, 1), \
                     (0, 0, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 1, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) )]

    pieces["J"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 1), \
                     (0, 0, 0, 1), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 1), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 1, 0, 0), \
                     (0, 1, 1, 1), \
                     (0, 0, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 1, 1, 0), \
                     (0, 0, 0, 0) )]

    pieces["T"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 1), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 1), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 1, 1, 1), \
                     (0, 0, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 1, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) )]

    def __init__(self, moteur, simulation):
        self.Moteur = moteur

        self.pieceSelect = None
        self.pieceRotation = 0
        self.pieceSuivante = None
        self.pieceX, self.pieceY = -1, -1

        self.pieceRepetition = 0
        self.simulation = simulation
      
    def afficher_piece(self):
        if self.Moteur.Partie.mort: return 

        t = VAR.TAILLE
        piece = CPieces.pieces[self.pieceSelect][self.pieceRotation]
        couleur = CPieces.pieces_couleurs[FCT.iif(self.simulation, "#", self.pieceSelect)]
        pImg = FCT.iif(self.simulation, "#", self.pieceSelect)
        
        for y in range(4):
            for x in range(4):
                if piece[x][y] == 1:
                    pX, pY =x+self.pieceX, y+ self.pieceY
                    if pY >= 0:
                        if VAR.mode_bmp:
                            VAR.fenetre.blit(VAR.IMAGES[pImg][1], (self.Moteur.grille.offX + ((pX)*t), self.Moteur.grille.offY + (pY*t)  ))
                        else:
                            pygame.draw.rect(VAR.fenetre, couleur, (self.Moteur.grille.offX + ((pX)*t), self.Moteur.grille.offY + (pY*t), t, t), 0)


    def afficher_piece_suivante(self):
        if self.Moteur.Partie.mort: return 0

        piece = CPieces.pieces[self.pieceSuivante][0]
        couleur = CPieces.pieces_couleurs[self.pieceSuivante]
        t = VAR.TAILLE
    
        for y in range(4):
            for x in range(4):
                if piece[x][y] == 1:
                    pX = self.Moteur.grille.offX + self.Moteur.grille.cadreHaut[0] + (x * VAR.TAILLE) - VAR.marge
                    pY = self.Moteur.grille.offY + self.Moteur.grille.cadreHaut[1] + (y * VAR.TAILLE) - self.Moteur.grille.cadreHaut[3] - VAR.marge  
                    if VAR.mode_bmp:
                        VAR.fenetre.blit(VAR.IMAGES[self.pieceSuivante][0], (pX, pY))
                    else:
                        pygame.draw.rect(VAR.fenetre, couleur, (pX, pY , t, t), 0)


    def hasard(self, forceDifference = ""):
        self.pieceSuivante = random.choice(["O", "I", "S", "Z", "L", "J", "T"])

        if self.pieceSelect == self.pieceSuivante:
            self.pieceRepetition += 1
        else:
            self.pieceRepetition = 0

        if self.pieceRepetition > (VAR.limitePiecesQuiSeSuivent+1) or (forceDifference == self.pieceSuivante):
            self.hasard(self.pieceSuivante)
            self.pieceRepetition = 0


    def tirer_nouvelle_piece(self):
        self.pieceSelect = self.pieceSuivante
        self.hasard()
        
        self.pieceX = int( ( VAR.DIMENSION[0]-2 ) / 2 )
        self.pieceY = -3
        self.pieceRotation = 0

    

    

    def faire_tourner_la_piece(self, sensAiguille):
        
        ancRot = self.pieceRotation

        if sensAiguille:
            self.pieceRotation +=1
            if self.pieceRotation > len(CPieces.pieces[self.pieceSelect]) -1:
                self.pieceRotation = 0
     
        else:
            self.pieceRotation -=1
            if self.pieceRotation < 0:
                self.pieceRotation = len(CPieces.pieces[self.pieceSelect]) -1

        if self.Moteur.Mecanique.controle_choque_piece(self):
            self.pieceRotation = ancRot
        else:
            FCT.jouer_son("rotation")


    def controle_deplacement_lateral(self, valeur):
        if valeur == 0: return False
      
        ancX, ancY = self.pieceX, self.pieceY
        self.pieceX +=valeur
        if self.Moteur.Mecanique.controle_choque_piece(self):
            self.pieceX, self.pieceY = ancX, ancY
            return True
        return False

