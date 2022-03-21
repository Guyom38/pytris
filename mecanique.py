
import pygame
from pygame.locals import *

import variables as VAR
from pieces import *
import COMMUN.variables as V
import random

class CMecanique():
    def nbJoueursActifs():
        nb = 0
        for i, j in VAR.tetris_joueurs.items():
            if j.Joueur.actif and not j.Partie.mort: nb +=1
        return nb
    
    def __init__(self, moteur):
        self.Moteur = moteur
        self.lignesADetruire = []
        self.lignesAjouter = 0
    
    def gestion_game_over(self):
        if self.verifier_game_over() and self.Moteur.actif:
            self.Moteur.Joueur.Avatar.changer_expression ("MORT", -1)
            self.Moteur.Animation.meurt()
            self.Moteur.Partie.meurt()
            FCT.jouer_son("game_over")

    def faire_descendre_la_piece(self, piece):
        ancY = piece.pieceY
        piece.pieceY +=1
        if self.controle_choque_piece(piece):
            piece.pieceY = ancY

            if not piece.simulation: self.fixer_piece_sur_la_grille()
                
            return False
        return True
    
   
                    
    def verifier_game_over(self):
        for x in range(VAR.DIMENSION[0]):
            if self.Moteur.grille.zones[x][0] != "": return True
        return False
        
    def faire_descendre_a_fond_la_piece(self, piece):
        while self.faire_descendre_la_piece(piece):
            pass
        self.Moteur.Joueur.Avatar.changer_expression ("CONCENTRE", 200)
        
    def controle_choque_piece(self, piece):
        for y in range(4):
            for x in range(4):
                if CPieces.pieces[piece.pieceSelect][piece.pieceRotation][x][y] == 1:
                    pX, pY = piece.pieceX + x, piece.pieceY + y
                    if pX >= 0 and pX < VAR.DIMENSION[0] and pY < VAR.DIMENSION[1]:
                        if pY < 0: 
                            #return False
                            pass
                        elif self.Moteur.grille.zones[pX][pY] != "": 
                            return True
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

        FCT.jouer_son("block")
        self.rechercher_de_lignes()
        self.Moteur.Pieces.tirer_nouvelle_piece()

    
    def gestion_mecanique_du_jeu(self):
        if not VAR.partie_en_cours() or self.Moteur.Partie.pause or not self.Moteur.actif: return None

        self.traitement_des_lignes_a_ajouter()
        self.gravite()        
        self.gestion_game_over()
    
            
    def gravite(self):
        if pygame.time.get_ticks() - self.Moteur.Partie.cycle > self.Moteur.Partie.vitesse:
            self.faire_descendre_la_piece(self.Moteur.Pieces)
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
            FCT.jouer_son("tetris")

    def rechercher_de_lignes(self):
        liste_lignes = []
        bloc_de_lignes_ref = -1
        bloc_de_lignes_cpt = 0
        bloc_traite = False
        
        for y in range(0, VAR.DIMENSION[1]):                                # --- Parcours chaque ligne dans haut jusqu'en bas
            if self.verifie_la_ligne(y):                                    # --- --- Est ce que c'est une ligne complete ?
                liste_lignes.append(y)                                      # --- --- --- Ajoute la ligne a la liste
                bloc_de_lignes_cpt+=1                                       # --- --- --- Ajoute au bloc +1
                self.Moteur.Partie.nbLignes +=1                             
                self.Moteur.Partie.verifie_changement_de_niveau()
                
                if bloc_de_lignes_ref != -1:                                # --- --- --- Est-ce que c'est la premiere ligne du bloc ?
                    if bloc_de_lignes_ref == y-1:                           # --- --- --- --- Est-ce que la ligne courante (y) touche celle du dessus (ref = y-1) ?+1
                        bloc_traite = True                                  # --- --- --- --- --- C'est toujours un bloc

                    else:                                                   # --- --- --- --- Si il y a rupture avec la ligne precedente
                        self.ajoute_score_lignes(bloc_de_lignes_cpt)        # --- --- --- --- --- Ajoute le score correspondant au bloc
                        bloc_traite = False                                 # --- --- --- --- --- Il ne faut plus traiter le bloc
                        bloc_de_lignes_cpt = 0                              # --- --- --- --- --- Aucune ligne dans le bloc
                bloc_de_lignes_ref = y                                      # --- --- --- --- Met a jour la reference avec la ligne courante
        
        if bloc_traite or bloc_de_lignes_cpt > 0:                          # --- --- --- Le bloc est a traité ou contient plusieurs lignes ?
            self.ajoute_score_lignes(bloc_de_lignes_cpt)                    # --- --- --- --- Ajoute le score correspondant au bloc
        
        if len(liste_lignes) > 0:                                           # --- --- --- Si plusieurs lignes ont été faites ?
            self.lignesADetruire = liste_lignes                             # --- --- --- --- Ajoute les lignes dans la file a détruire
            self.Moteur.Animation.destLignesActif = True                    # --- --- --- --- Active l'animation de destruction
    
    
    def balance_les_lignes(self, nbLignes):
        if self.Moteur.id == VAR.pouvoirId:                 # --- Si le joueur a le pouvoir, il balance a tout le monde
            for id, joueur in VAR.tetris_joueurs.items():
                if VAR.tetris_joueurs[joueur.id].actif:  
                    if joueur.id != self.Moteur.id: joueur.Mecanique.lignesAjouter += nbLignes 
         
        else:                                               # --- Si un autre joueur a le pouvoir, il recoit la malediction
            if VAR.tetris_joueurs[VAR.pouvoirId].actif:  
                VAR.tetris_joueurs[VAR.pouvoirId].Mecanique.lignesAjouter += nbLignes 
                
        if VAR.limiteModeBalance:                           # --- Retire autant de lignes en attente qu'il y a de lignes a ajouter
            self.Moteur.Mecanique.lignesAjouter -= nbLignes
            if self.Moteur.Mecanique.lignesAjouter < 0: self.Moteur.Mecanique.lignesAjouter = 0
    
    
    def traitement_des_lignes_a_ajouter(self):
        if self.lignesAjouter > 0:
            if pygame.time.get_ticks() - VAR.limiteLignesCycle > VAR.limiteLignesFrequence:
                VAR.limiteLignesCycle = pygame.time.get_ticks()
                      
                nbLignesMax = FCT.iif(self.lignesAjouter > VAR.limiteLignesMax, VAR.limiteLignesMax,self.lignesAjouter)
                self.Moteur.Mecanique.ajoute_des_lignes(nbLignesMax)    
                self.lignesAjouter -= nbLignesMax
                                  
    def ajoute_des_lignes(self, nbLignes):
        self.Moteur.Joueur.Avatar.changer_expression("ENERVE", 500)
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

            FCT.jouer_son("ligne")