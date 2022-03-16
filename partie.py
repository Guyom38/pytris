from grille import *

import fonctions as FCT
import random

class CParties():
    def controle_fin_de_partie():
        if VAR.partie_demarree:
            if CParties.temps_restant() <= 0:
                pygame.mixer.music.stop()
                for i in range(VAR.nbJoueurs):
                    VAR.tetris_joueurs[i].mort = True
                VAR.cycle_partie = -1

    def temps_restant():
        return pygame.time.get_ticks() - VAR.cycle_partie

# -----------------------------------------------------------------------------------------------------------
# -
# -     CLASSE PARTIE
# -
# -----------------------------------------------------------------------------------------------------------
    def __init__(self, moteur):
        print("        + PARTIE")
        self.Moteur = moteur

        self.score = 0
        self.nom = ""
        self.nbLignes = 0
        self.niveau = 0
        self.rang = 0
        self.aide = True
        self.ligneNiveau = 0
        self.pause = False
        self.mort = False
        self.cycle = 0
        self.vitesse = 500

        VAR.cycle_partie = -1
        

    def afficher_message(self):
        if self.pause or not self.actif or self.mort:
            texte = "PAUSE"
            if not self.actif : texte = "PRESSEZ START"
            if self.mort: texte = "REJOUER, PRESSEZ START"
            

            image_pause = VAR.ecritures[20].render(texte, True, (255,255,255,255)) 
            largeur, hauteur = (VAR.DIMENSION[0] * VAR.TAILLE), (VAR.DIMENSION[1] * VAR.TAILLE)
            cX, cY = self.grille.offX + ((largeur - image_pause.get_width())/2) , self.grille.offY + int((hauteur - image_pause.get_height()) /2 )
            pygame.draw.rect(VAR.fenetre, (0,0,0,255), (self.grille.offX, cY-10, largeur, image_pause.get_height()+20), 0)
            pygame.draw.rect(VAR.fenetre, (64,64,64,255), (self.grille.offX, cY-10, largeur, image_pause.get_height()+20), 2)
            VAR.fenetre.blit(image_pause, (cX, cY))
    
    def afficher_score(self): 
        y=50
        for texte in ("Score : " + str(self.score), "Lignes : "+str(self.nbLignes), "Niveau : " + str(self.niveau)) :
            image = VAR.ecritures[20].render(texte, True, (255,255,255,255)) 
            VAR.fenetre.blit(image, (self.grille.offX +100, self.grille.offY - y))
            y += image.get_height() +5
        
        image_rang = VAR.ecritures[80].render(str(self.rang), True, (255,255,255,255)) 
        VAR.fenetre.blit(image_rang, (self.grille.offX + (VAR.DIMENSION[0] * VAR.TAILLE) - image_rang.get_width(), self.grille.offY - (image_rang.get_height()+20)))
        
    def verifie_changement_de_niveau(self):
        self.ligneNiveau +=1
        if self.Moteur.ligneNiveau == 10:
            self.niveau +=1
            self.vitesse -= 50
            self.Moteur.ligneNiveau = 0

    def meurt(self):
        self.actif = False
        self.mort = True

    def demarrer(self):
        self.actif = False
        
        self.pieceSuivante = random.choice(["O", "I", "S", "Z", "L", "J", "T"])
        self.Moteur.Pieces.tirer_nouvelle_piece()
        
    def game_over(self):
        self.Moteur.actif = True
        self.Moteur.mort = False
        self.score = 0
        self.Moteur.vitesse = 500
        self.nbLignes = 0
        self.Moteur.grille = CGrille(self)
