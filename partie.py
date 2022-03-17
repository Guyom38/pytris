from grille import *

import fonctions as FCT
import random

class CParties():
    def controle_fin_de_partie():
        if VAR.partie_demarree:
            if VAR.duree_partie - CParties.temps_ecoule() <= 0:
                pygame.mixer.music.stop()
                for i in range(VAR.nbJoueurs):
                    VAR.tetris_joueurs[i].mort = True
                VAR.cycle_partie = -1

    def temps_ecoule():
        return pygame.time.get_ticks() - VAR.cycle_partie

    def gestion_malediction():
        if pygame.time.get_ticks() - VAR.pouvoirCycle > VAR.pouvoirDelais:
            VAR.pouvoirId +=1
            if VAR.pouvoirId > VAR.nbJoueurs -1: VAR.pouvoirId = 0
            VAR.pouvoirCycle = pygame.time.get_ticks()

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
        self.aide = False
        self.ligneNiveau = 0
        self.pause = False
        self.mort = False
        self.cycle = 0
        self.vitesse = 500

        VAR.cycle_partie = -1
        self.memoireDuTemps = 0
        
    def demarrer(self):
        self.Moteur.actif = False
        
        self.Moteur.Pieces.pieceSuivante = random.choice(["O", "I", "S", "Z", "L", "J", "T"])
        self.Moteur.Pieces.tirer_nouvelle_piece()
        
    def afficher_message(self):
        if self.pause or not self.Moteur.actif or self.mort:
            texte = "PAUSE"
            if not self.Moteur.actif : texte = "PRESSEZ START"
            if self.mort: texte = "REJOUER, PRESSEZ START"
            

            image_pause = VAR.ecritures[20].render(texte, True, (255,255,255,255)) 
            largeur, hauteur = (VAR.DIMENSION[0] * VAR.TAILLE), (VAR.DIMENSION[1] * VAR.TAILLE)
            cX, cY = self.Moteur.grille.offX + ((largeur - image_pause.get_width())/2) , self.Moteur.grille.offY + int((hauteur - image_pause.get_height()) /2 )
            pygame.draw.rect(VAR.fenetre, (0,0,0,255), (self.Moteur.grille.offX, cY-10, largeur, image_pause.get_height()+20), 0)
            pygame.draw.rect(VAR.fenetre, (64,64,64,255), (self.Moteur.grille.offX, cY-10, largeur, image_pause.get_height()+20), 2)
            VAR.fenetre.blit(image_pause, (cX, cY))
    
    def afficher_score(self): 
        y=50
        for texte in ("Score : " + str(self.score), "Lignes : "+str(self.nbLignes), "Niveau : " + str(self.niveau)) :
            image = VAR.ecritures[20].render(texte, True, (0,0,0,255)) 
            VAR.fenetre.blit(image, (self.Moteur.grille.offX +98, self.Moteur.grille.offY - y-2))
            
            image = VAR.ecritures[20].render(texte, True, (255,255,255,255)) 
            VAR.fenetre.blit(image, (self.Moteur.grille.offX +100, self.Moteur.grille.offY - y))
            y += image.get_height() +5
        
        image_rang = VAR.ecritures[80].render(str(self.rang), True, (255,255,255,255)) 
        VAR.fenetre.blit(image_rang, (self.Moteur.grille.offX + (VAR.DIMENSION[0] * VAR.TAILLE) - image_rang.get_width(), self.Moteur.grille.offY - (image_rang.get_height()+20)))
        
    def verifie_changement_de_niveau(self):
        self.ligneNiveau +=1
        if self.ligneNiveau == VAR.nbLignesNiveauSuivant:
            self.niveau +=1
            self.vitesse -= 50
            self.ligneNiveau = 0
            self.Moteur.Animation.nivSupActif = True
            FCT.jouer_son("level_up")

    def meurt(self):
        self.Moteur.actif = False
        self.mort = True

    
        
    def game_over(self):
        self.Moteur.actif = True
        self.mort = False
        self.score = 0
        self.vitesse = 500
        self.nbLignes = 0
        self.Moteur.grille = CGrille(self.Moteur)
        self.Moteur.Pieces.tirer_nouvelle_piece()
        self.Moteur.Mecanique.lignesADetruire = []


    def fige_le_temps(self):
        self.memoireDuTemps = (pygame.time.get_ticks() - self.Moteur.Partie.cycle)
 
    def libere_le_temps(self):
         self.Moteur.Partie.cycle = (pygame.time.get_ticks() + self.memoireDuTemps)
     