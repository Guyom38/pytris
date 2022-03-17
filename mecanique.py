
import pygame
from pygame.locals import *

import variables as VAR
from pieces import *

import random

class CMecanique():
    
    
    def __init__(self, moteur):
        print("        + MECANIQUE")
        self.Moteur = moteur

    def faire_descendre_la_piece(self, simulation):
        if not simulation:
            ancY = self.Moteur.Pieces.pieceY
            self.Moteur.Pieces.pieceY +=1
            if self.controle_choque_piece(self.Moteur.Pieces):
                self.Moteur.Pieces.pieceY = ancY
                if self.Moteur.Pieces.pieceY != -1:
                    self.fixer_piece_sur_la_grille()
                else:
                    self.Moteur.Partie.meurt()
                
                return False
            return True
        
        else:
            
            ancY = self.Moteur.PiecesAide.pieceY
            self.Moteur.PiecesAide.pieceY +=1
            if self.controle_choque_piece(self.Moteur.PiecesAide):
                self.Moteur.PiecesAide.pieceY = ancY
    
                return False
            return True            
    
    def faire_descendre_a_fond_la_piece(self, simulation):
        while self.faire_descendre_la_piece(simulation):
            pass
        
    def controle_choque_piece(self, piece):
        for y in range(4):
            for x in range(4):
                if CPieces.pieces[piece.pieceSelect][piece.pieceRotation][x][y] == 1:
                    pX, pY = piece.pieceX + x, piece.pieceY + y
                    if pX >= 0 and pX < VAR.DIMENSION[0] and pY < VAR.DIMENSION[1]:
                        if self.Moteur.grille.zones[pX][pY] != "": return True
                    else:
                        return True
        return False

    def fixer_piece_sur_la_grille(self):

        for y in range(4):
            for x in range(4):
                if CPieces.pieces[self.Moteur.Pieces.pieceSelect][self.Moteur.Pieces.pieceRotation][x][y] == 1:
                    pX, pY = self.Moteur.Pieces.pieceX + x, self.Moteur.Pieces.pieceY + y
                    if pX >= 0 and pX < VAR.DIMENSION[0] and pY >= 0 and pY < VAR.DIMENSION[1]:
                        self.Moteur.grille.zones[pX][pY] = self.Moteur.Pieces.pieceSelect

        pygame.mixer.Sound.play(VAR.AUDIOS["fixe"])

        self.rechercher_de_lignes()
        self.Moteur.Pieces.tirer_nouvelle_piece()

    
    def gravite(self):
        if self.Moteur.Partie.pause or not self.Moteur.actif: return None

        if pygame.time.get_ticks() - self.Moteur.Partie.cycle > self.Moteur.Partie.vitesse:
            self.faire_descendre_la_piece(False)
            self.Moteur.Partie.cycle = pygame.time.get_ticks()

    def verifie_la_ligne(self, ligne):
        cpt = 0
        for x in range(VAR.DIMENSION[0]):
            if self.Moteur.grille.zones[x][ligne] != "": cpt +=1

        if cpt == VAR.DIMENSION[0]:
            return True
        return False

    def ajoute_score_lignes(self, nbLignes):
        if nbLignes == 1:
            self.Moteur.Partie.score += 40 * (self.Moteur.Partie.niveau + 1)
        elif nbLignes == 2:
            self.Moteur.Partie.score += 100 * (self.Moteur.Partie.niveau + 1)
        elif nbLignes == 3:
            self.Moteur.Partie.score += 300 * (self.Moteur.Partie.niveau + 1)
        elif nbLignes == 4:
            self.Moteur.Partie.score += 1200 * (self.Moteur.Partie.niveau + 1)

    def rechercher_de_lignes(self):
        liste_lignes = []
        bloc_de_lignes_ref = -1
        bloc_de_lignes_cpt = 0
        bloc_traite = False

        
        for y in range(0, VAR.DIMENSION[1]):
            if self.verifie_la_ligne(y):
                liste_lignes.append(y)                      # --- Ajoute la ligne a la liste
                bloc_de_lignes_cpt+=1
                self.Moteur.Partie.nbLignes +=1
                self.Moteur.Partie.verifie_changement_de_niveau()
                 
                if bloc_de_lignes_ref != -1:                # --- premiere ligne traitée
                    if bloc_de_lignes_ref == y+1:           # --- Si les lignes se touchent
                        bloc_traite = True
                    else:                                   # --- Si il y a rupture avec la ligne precedente
                        self.ajoute_score_lignes(bloc_de_lignes_cpt)
                        bloc_traite = False
                        bloc_de_lignes_cpt = 0
                        print("BLOC : " + str(bloc_de_lignes_cpt))
                        
                bloc_de_lignes_ref = y
                
        if bloc_traite and bloc_de_lignes_cpt > 0:
            self.ajoute_score_lignes(bloc_de_lignes_cpt)
            print("FIN BLOC : " + str(bloc_de_lignes_cpt))
       
        
        if len(liste_lignes) > 0:
            self.detruire_lignes(liste_lignes)
            print(("A SUPPRIMER", liste_lignes))
            self.balance_les_lignes(len(liste_lignes))
    
    def balance_les_lignes(self, nbLignes):
        if self.Moteur.id == VAR.pouvoirId:                 # --- Si le joueur a le pouvoir, il balance a tout le monde
            for id, joueur in VAR.tetris_joueurs.items():
                if joueur.id != self.Moteur.id: joueur.Mecanique.ajoute_des_lignes(nbLignes)  
        
        else:                                               # --- Si un autre joueur a le pouvoir, il recoit la malediction
            VAR.tetris_joueurs[VAR.pouvoirId].Mecanique.ajoute_des_lignes(nbLignes)    
                          
    def ajoute_des_lignes(self, nbLignes):
        for i in range(nbLignes):
            for y in range(1, VAR.DIMENSION[1]):
                for x in range(VAR.DIMENSION[0]): self.Moteur.grille.zones[x][y-1] = self.Moteur.grille.zones[x][y]
                    
            for x in range(VAR.DIMENSION[0]): 
                self.Moteur.grille.zones[x][VAR.DIMENSION[1]-1] = random.choice(("", "#"))
        
            
    def detruire_lignes(self, liste_lignes):
        for ligne in liste_lignes:
            self.detruire_ligne(ligne)
            
    def detruire_ligne(self, ligne):
        for y in range(ligne, 0, -1):
            for x in range(VAR.DIMENSION[0]): 
                if y < VAR.DIMENSION[1]:
                    self.Moteur.grille.zones[x][y] = self.Moteur.grille.zones[x][y-1]

            pygame.mixer.Sound.play(VAR.AUDIOS["ligne"])