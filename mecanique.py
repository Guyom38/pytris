
import pygame
from pygame.locals import *

import variables as VAR
from pieces import *

class CMecanique():
    def __init__(self, moteur):
        print("        + MECANIQUE")
        self.Moteur = moteur

    def faire_descendre_la_piece(self):
        ancY = self.pieceY
        self.pieceY +=1
        if self.controle_choque_piece():
            self.pieceY = ancY
            if self.pieceY != -1:
                self.fixer_piece_sur_la_grille()
            else:
                self.meurt()
            
            
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

        pygame.mixer.Sound.play(VAR.AUDIOS["fixe"])

        self.rechercher_de_lignes()
        self.Moteur.Pieces.tirer_nouvelle_piece()

    
    def gravite(self):
        if self.Moteur.Partie.pause or not self.Moteur.actif: return None

        if pygame.time.get_ticks() - self.cycle > self.vitesse:
            self.faire_descendre_la_piece()
            self.cycle = pygame.time.get_ticks()

    def verifie_la_ligne(self, ligne):
        cpt = 0
        for x in range(VAR.DIMENSION[0]):
            if self.grille.zones[x][ligne] != "": cpt +=1

        if cpt == VAR.DIMENSION[0]:
            return True
        return False

    def ajoute_score_lignes(self, nbLignes):
        if nbLignes == 1:
            self.score += 40 * (self.niveau + 1)
        elif nbLignes == 2:
            self.score += 100 * (self.niveau + 1)
        elif nbLignes == 3:
            self.score += 300 * (self.niveau + 1)
        elif nbLignes == 4:
            self.score += 1200 * (self.niveau + 1)

    def rechercher_de_lignes(self):
        liste_lignes = []
        bloc_de_lignes_ref = -1
        bloc_de_lignes_cpt = 0
        bloc_traite = False

        
        for y in range(-1, VAR.DIMENSION[1]):
            if self.verifie_la_ligne(y):
                liste_lignes.append(y)                      # --- Ajoute la ligne a la liste
                bloc_de_lignes_cpt+=1
                self.Moteur.Partie.nbLignes +=1
                self.Moteur.Partie.verifie_changement_de_niveau()
                 
                if bloc_de_lignes_ref != -1:                # --- premiere ligne traitée
                    if bloc_de_lignes_ref == y+1:           # --- Si les lignes se touchent
                        bloc_traite = True
                    else:                                   # --- Si il y a rupture avec la ligne precedente
                        self.Mecanique.ajoute_score_lignes(bloc_de_lignes_cpt)
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
            
    

            
            
        
            
    def detruire_lignes(self, liste_lignes):
        for ligne in liste_lignes:
            self.detruire_ligne(ligne)
            
    def detruire_ligne(self, ligne):
        for y in range(ligne, 0, -1):
            for x in range(VAR.DIMENSION[0]): 
                if y < VAR.DIMENSION[1]:
                    self.grille.zones[x][y] = self.grille.zones[x][y-1]

            pygame.mixer.Sound.play(VAR.AUDIOS["ligne"])