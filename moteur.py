from email.mime import image
from operator import truediv
import pygame
from pygame.locals import *

from pieces import *
from grille import *

import variables as VAR
from variables import *

import random

class CMoteur():
    def __init__(self, id, location):
        print("Initia")
        self.id = id
        self.location = location

        self.grille = CGrille(self)
        self.actif = True
        self.pause = False
        self.manetteId = 0

        self.pieceSelect = None
        self.pieceRotation = 0

        self.pieceSuivante = None

        self.pieceX, self.pieceY = -1, -1
        self.cycle = 0
        self.vitesse = 1000

    def demarrer(self):
        self.actif = False
        self.tirer_nouvelle_piece()

    def tirer_nouvelle_piece(self):
        self.pieceSelect = random.choice(["O", "I", "S", "Z", "L", "J", "T"])
        self.pieceX = int( ( VAR.DIMENSION[0]-2 ) / 2 )
        self.pieceY = -2
        self.pieceRotation = 0

    def afficher(self):
        self.gestion_manette()
        self.gravite()
        self.grille.afficher()
        self.afficher_piece()

        if self.pause:
            ecriture = pygame.font.SysFont('arial', 20) 
            image_pause = ecriture.render("PAUSE", True, (255,255,255,255)) 
            largeur, hauteur = (VAR.DIMENSION[0] * VAR.TAILLE), (VAR.DIMENSION[1] * VAR.TAILLE)
            cX, cY = self.grille.offX + ((largeur - image_pause.get_width())/2) , self.grille.offY + int((hauteur - image_pause.get_height()) /2 )
            pygame.draw.rect(VAR.fenetre, (0,0,0,255), (self.grille.offX, cY-10, largeur, image_pause.get_height()+20), 0)
            pygame.draw.rect(VAR.fenetre, (64,64,64,255), (self.grille.offX, cY-10, largeur, image_pause.get_height()+20), 2)
            VAR.fenetre.blit(image_pause, (cX, cY))

    

    def afficher_piece(self):
        piece = CPieces.pieces[self.pieceSelect][self.pieceRotation]
        couleur = CPieces.pieces_couleurs[self.pieceSelect]
        t = VAR.TAILLE

        for y in range(4):
            for x in range(4):
                if piece[x][y] == 1:
                    pygame.draw.rect(VAR.fenetre, couleur, (self.grille.offX + ((x+self.pieceX)*t), self.grille.offY + (((y+self.pieceY)*t)), t, t), 0)

    def gravite(self):
        if self.pause: return None

        if pygame.time.get_ticks() - self.cycle > self.vitesse:
            self.faire_descendre_la_piece()
            self.cycle = pygame.time.get_ticks()

    def faire_descendre_la_piece(self):
        ancX, ancY = self.pieceX, self.pieceY
        self.pieceY +=1
        if self.controle_choque_piece():
            self.pieceX, self.pieceY = ancX, ancY
            self.fixer_piece_sur_la_grille()
            return False
        return True

    def controle_choque_piece(self):
        for y in range(4):
            for x in range(4):
                if CPieces.pieces[self.pieceSelect][self.pieceRotation][x][y] == 1:
                    pX, pY = self.pieceX + x, self.pieceY + y
                    if pX >= 0 and pX < VAR.DIMENSION[0] and pY < VAR.DIMENSION[1]:
                        if self.grille.zones[pX][pY] != "": return True
                    else:
                        return True
        return False

    def fixer_piece_sur_la_grille(self):
        for y in range(4):
            for x in range(4):
                if CPieces.pieces[self.pieceSelect][self.pieceRotation][x][y] == 1:
                    pX, pY = self.pieceX + x, self.pieceY + y
                    if pX >= 0 and pX < VAR.DIMENSION[0] and pY >= 0 and pY < VAR.DIMENSION[1]:
                        self.grille.zones[pX][pY] = self.pieceSelect

        self.rechercher_de_lignes()
        self.tirer_nouvelle_piece()

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

        if self.controle_choque_piece():
            self.pieceRotation = ancRot


    def gestion_manette(self):
        
        for event in VAR.evenements: 
            if VAR.manettes[self.manetteId].get_button(CBouton.B_START) == 1:
                    if self.actif == False:
                        self.actif = True
                    else:
                        self.pause = not self.pause

        if not self.pause:
            for event in VAR.evenements: 
                if event.type == pygame.JOYBUTTONDOWN:
                    if VAR.manettes[self.manetteId].get_button(CBouton.B_L) == 1:
                        self.faire_tourner_la_piece(False)
                    if VAR.manettes[self.manetteId].get_button(CBouton.B_R) == 1:
                        self.faire_tourner_la_piece(True)
                elif event.type == pygame.JOYAXISMOTION:
                    if event.joy == self.manetteId:
                        if event.axis == 0 and event.value > 0.9:
                            self.controle_deplacement_lateral(1)
                        elif event.axis == 0 and event.value < -0.9:
                            self.controle_deplacement_lateral(-1)
                        elif event.axis == 1 and event.value > 0.9:
                            self.faire_descendre_la_piece()
                        elif event.axis == 1 and event.value < -0.9: #HAUT
                            self.faire_descendre_a_fond_la_piece()
                 
    def controle_deplacement_lateral(self, valeur):
        ancX, ancY = self.pieceX, self.pieceY
        self.pieceX +=valeur
        if self.controle_choque_piece():
            self.pieceX, self.pieceY = ancX, ancY
            return True
        return False

    def faire_descendre_a_fond_la_piece(self):
        while self.faire_descendre_la_piece():
            pass

    def rechercher_de_lignes(self):
        for y in range(VAR.DIMENSION[1]-1, 0, -1):
            if self.verifie_la_ligne(y):
                print ("Ligne")

    def verifie_la_ligne(self, ligne):
        cpt = 0
        for x in range(VAR.DIMENSION[0]):
            if self.grille.zones[x][ligne] != "": cpt +=1

        if cpt == VAR.DIMENSION[0]:
            return True

        return False

