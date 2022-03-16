
import pygame
from pygame.locals import *

import variables as VAR
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

    def __init__(self, moteur):
        print("        + PIECES")
        self.Moteur = moteur

        self.pieceSelect = None
        self.pieceRotation = 0
        self.pieceSuivante = None
        self.pieceX, self.pieceY = -1, -1

    def afficher_piece(self):
        piece = CPieces.pieces[self.pieceSelect][self.pieceRotation]
        couleur = CPieces.pieces_couleurs[self.pieceSelect]
        t = VAR.TAILLE

        for y in range(4):
            for x in range(4):
                if piece[x][y] == 1:
                    pX, pY =x+self.pieceX, y+self.pieceY
                    if pY >= 0:
                        if VAR.mode_bmp:
                            VAR.fenetre.blit(VAR.IMAGES[self.pieceSelect][1], (self.grille.offX + ((pX)*t), self.grille.offY + (pY*t)))
                        else:
                            pygame.draw.rect(VAR.fenetre, couleur, (self.grille.offX + ((pX)*t), self.grille.offY + (pY*t), t, t), 0)

    def afficher_piece_suivante(self):
        piece = CPieces.pieces[self.pieceSuivante][0]
        couleur = CPieces.pieces_couleurs[self.pieceSuivante]
        t = VAR.TAILLE

        for y in range(4):
            for x in range(4):
                if piece[x][y] == 1:
                    pX, pY = self.grille.offX + (x*t), self.grille.offY + (y*t) - 120
                    if VAR.mode_bmp:
                        VAR.fenetre.blit(VAR.IMAGES[self.pieceSuivante][0], (pX, pY))
                    else:
                        pygame.draw.rect(VAR.fenetre, couleur, (pX, pY , t, t), 0)

    def tirer_nouvelle_piece(self):
        self.pieceSelect = self.pieceSuivante
        self.pieceSuivante = random.choice(["O", "I", "S", "Z", "L", "J", "T"])
        self.pieceX = int( ( VAR.DIMENSION[0]-2 ) / 2 )
        self.pieceY = -1
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

        if self.MOTEUR.PIECES.controle_choque_piece():
            self.pieceRotation = ancRot
        else:
            pygame.mixer.Sound.play(VAR.AUDIOS["rotation"])

    def controle_deplacement_lateral(self, valeur):
        ancX, ancY = self.pieceX, self.pieceY
        self.pieceX +=valeur
        if self.MOTEUR.PIECES.controle_choque_piece():
            self.pieceX, self.pieceY = ancX, ancY
            return True
        return False

    def faire_descendre_a_fond_la_piece(self):
        while self.faire_descendre_la_piece():
            pass