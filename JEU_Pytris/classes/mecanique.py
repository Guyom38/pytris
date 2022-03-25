
import pygame
from pygame.locals import *

import JEU_Pytris.variables as VAR
from JEU_Pytris.classes.pieces import *
import COMMUN.variables as V
from COMMUN.classes.fonctions import *
import random

class CMecanique:
    
    
    def __init__(self, m):
        self.M = m
        self.lignesADetruire = []
        self.lignesAjouter = 0

    def action_a_entreprendre_si_le_joueur_a_perdu(self):
        if (self.M.Joueur.actif and self.le_joueur_a_til_perdu()) \
            or self.M.Partie.mort:
                
            self.M.Joueur.Avatar.changer_expression ("MORT", -1)
            self.M.Animation.meurt()
            self.M.Partie.meurt()
            GAUDIO.jouer_son("game_over")
    
    def le_joueur_a_til_perdu(self):
        for x in range(VAR.DIMENSION[0]):
            if self.M.grille.zones[x][0] != "": return True
        return False
    
    
    def faire_descendre_la_piece(self, piece):
        ancY = piece.pieceY
        piece.pieceY +=1
        if self.la_piece_est_elle_bloquee(piece):
            piece.pieceY = ancY

            if not piece.simulation: 
                self.fixer_piece_sur_la_grille()
                
            return False
        return True
                    
    
        
    def faire_descendre_a_fond_la_piece(self, piece):
        while self.faire_descendre_la_piece(piece):
            pass
        self.M.Joueur.Avatar.changer_expression ("CONCENTRE", 200)
        
    def la_piece_est_elle_bloquee(self, piece):
        for y in range(4):
            for x in range(4):
                if CPieces.pieces[piece.pieceSelect][piece.pieceRotation][x][y] == 1:
                    pX, pY = piece.pieceX + x, piece.pieceY + y
                    if pX >= 0 and pX < VAR.DIMENSION[0] and pY < VAR.DIMENSION[1]:
                        if pY < 0: 
                            #return False
                            pass
                        elif self.M.grille.zones[pX][pY] != "": 
                            return True
                    else:
                        return True
        return False

    def fixer_piece_sur_la_grille(self):
        for y in range(4):
            for x in range(4):
                if CPieces.pieces[self.M.Pieces.pieceSelect][self.M.Pieces.pieceRotation][x][y] == 1:
                    pX, pY = self.M.Pieces.pieceX + x, self.M.Pieces.pieceY + y
                    if pX >= 0 and pX < VAR.DIMENSION[0] and pY >= 0 and pY < VAR.DIMENSION[1]:
                        self.M.grille.zones[pX][pY] = self.M.Pieces.pieceSelect

        GAUDIO.jouer_son("block")
        self.rechercher_de_lignes()
        self.M.Pieces.tirer_nouvelle_piece()

    
    def gestion_mecanique_du_jeu(self):
        partie_arretee = not VAR.partie_en_cours()
        partie_en_pause = self.M.Partie.pause
        joueur_inactif = not self.M.Joueur.actif
       
        if not(partie_arretee or partie_en_pause or joueur_inactif):
            self.gravite() 
            self.traitement_des_lignes_a_ajouter()
            self.action_a_entreprendre_si_le_joueur_a_perdu()
    
            
    def gravite(self):
        if self.M.Partie.vitesse_partie.controle():
            self.faire_descendre_la_piece(self.M.Pieces)
            self.M.Partie.vitesse_partie.reset()
                   
    def verifie_la_ligne(self, ligne):
        cpt = 0
        for x in range(VAR.DIMENSION[0]):
            if self.M.grille.zones[x][ligne] != "": cpt +=1

        if cpt == VAR.DIMENSION[0]:
            return True
        return False

    def ajoute_score_lignes(self, nbLignes):
        if nbLignes == 1:
            self.M.Partie.score += 40 * (self.M.Partie.niveau + 1)
        elif nbLignes == 2:
            self.M.Partie.score += 100 * (self.M.Partie.niveau + 1)
        elif nbLignes == 3:
            self.M.Partie.score += 300 * (self.M.Partie.niveau + 1)
        elif nbLignes == 4:
            self.M.Partie.score += 1200 * (self.M.Partie.niveau + 1)
            GAUDIO.jouer_son("tetris")

    def rechercher_de_lignes(self):
        liste_lignes = []
        bloc_de_lignes_ref = -1
        bloc_de_lignes_cpt = 0
        bloc_traite = False
        
        for y in range(0, VAR.DIMENSION[1]):                                # --- Parcours chaque ligne dans haut jusqu'en bas
            if self.verifie_la_ligne(y):                                    # --- --- Est ce que c'est une ligne complete ?
                liste_lignes.append(y)                                      # --- --- --- Ajoute la ligne a la liste
                bloc_de_lignes_cpt+=1                                       # --- --- --- Ajoute au bloc +1
                self.M.Partie.nbLignes +=1                             
                self.M.Partie.verifie_changement_de_niveau()
                
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
            self.M.Animation.destLignesActif = True                    # --- --- --- --- Active l'animation de destruction
    
    
    def balance_les_lignes(self, nbLignes):
        if self.M.Joueur.id == VAR.pouvoirId:                 # --- Si le joueur a le pouvoir, il balance a tout le monde
            for id, moteur in VAR.tetris_joueurs.items():
                if VAR.tetris_joueurs[moteur.Joueur.id].Joueur.actif:  
                    if moteur.Joueur.id != self.M.Joueur.id: moteur.Mecanique.lignesAjouter += nbLignes 
         
        else:                                               # --- Si un autre joueur a le pouvoir, il recoit la malediction
            if VAR.tetris_joueurs[VAR.pouvoirId].Joueur.actif:  
                VAR.tetris_joueurs[VAR.pouvoirId].Mecanique.lignesAjouter += nbLignes 
                
        if VAR.mode_balance:                           # --- Retire autant de lignes en attente qu'il y a de lignes a ajouter
            self.M.Mecanique.lignesAjouter -= nbLignes
            if self.M.Mecanique.lignesAjouter < 0: self.M.Mecanique.lignesAjouter = 0
    
    
    def traitement_des_lignes_a_ajouter(self):
        if self.lignesAjouter > 0:
            if VAR.temps_ajout_de_lignes.controle():
                nbLignesMax = GBASE.iif(self.lignesAjouter > VAR.lignes_ajout_max, VAR.lignes_ajout_max,self.lignesAjouter)
                self.M.Mecanique.ajoute_des_lignes(nbLignesMax)    
                self.lignesAjouter -= nbLignesMax


    def ajoute_des_lignes(self, nbLignes):
        self.M.Joueur.Avatar.changer_expression("ENERVE", 500)                                                          # Change l'expression de l'avatar
        
        for i in range(nbLignes):
            self.M.Pieces.pieceY -=1                                                                                    # Remonte la piece autnat de fois que des lignes sont ajoutées
            
            for y in range(1, VAR.DIMENSION[1]):                                                                        # parcours de la seconde ligne jusqu'a l'avant dernière
                for x in range(VAR.DIMENSION[0]):                                                                       # remplace la ligne du dessus par celle de dessous
                    self.M.grille.zones[x][y-1] = self.M.grille.zones[x][y]                                             
                    
            for x in range(VAR.DIMENSION[0]):                                                                           # remplit aléatoirement la derniere ligne de blocs                             
                self.M.grille.zones[x][VAR.DIMENSION[1]-1] = random.choice(("", "#"))
        
            
    def detruire_lignes(self, liste_lignes):
        for ligne in liste_lignes:
            self.detruire_ligne(ligne)
            
    def detruire_ligne(self, ligne):
        for y in range(ligne, 0, -1):
            for x in range(VAR.DIMENSION[0]): 
                if y < VAR.DIMENSION[1]:
                    self.M.grille.zones[x][y] = self.M.grille.zones[x][y-1]

            GAUDIO.jouer_son("ligne")