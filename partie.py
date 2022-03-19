from grille import *

import fonctions as FCT
import random

from mecanique import CMecanique

class CParties():
    def controle_fin_de_partie():
        if VAR.partie_en_cours():
            if VAR.duree_partie - CParties.temps_ecoule() <= 0:
                for i in range(VAR.nbJoueurs):
                    VAR.tetris_joueurs[i].actif == False
                    VAR.tetris_joueurs[i].mort = True
                    VAR.tetris_joueurs[i].Mecanique.gestion_game_over()
                    
                VAR.partie_demarree = False
                VAR.fin_partie = True
                FCT.arreter_musique()
                VAR.mode = VAR.MODE_SCORE
                

    def temps_ecoule():
        resultat = pygame.time.get_ticks() - VAR.cycle_partie
        if resultat < 0: resultat = 0
        return resultat

    def gestion_malediction(force = False):
        if VAR.nbJoueurs > 1 and CMecanique.nbJoueursActifs() > 1:
            if (pygame.time.get_ticks() - VAR.pouvoirCycle > VAR.pouvoirDelais) or force:
                VAR.pouvoirId +=1
                if VAR.pouvoirId > VAR.nbJoueurs -1: VAR.pouvoirId = 0
                if not VAR.tetris_joueurs[VAR.pouvoirId].actif: CParties.gestion_malediction()
                VAR.pouvoirCycle = pygame.time.get_ticks()

# -----------------------------------------------------------------------------------------------------------
# -
# -     CLASSE PARTIE
# -
# -----------------------------------------------------------------------------------------------------------
    def __init__(self, moteur):
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
        
    def partie_arretee(self):
        return self.pause or not self.Moteur.actif or self.mort  
    
    def demarrer(self):
        self.Moteur.actif = False
        self.mort = False
        self.pause = False
        
        self.Moteur.Pieces.pieceSuivante = random.choice(["O", "I", "S", "Z", "L", "J", "T"])
        self.Moteur.Pieces.tirer_nouvelle_piece()
        
        VAR.cycle_partie = pygame.time.get_ticks()
        VAR.fin_partie = False
        
        
    def redemarre(self):
        self.score = 0
        self.vitesse = 500
        self.nbLignes = 0
        self.Moteur.grille = CGrille(self.Moteur)

        self.Moteur.Mecanique.lignesADetruire = []
        self.Moteur.Mecanique.lignesAjouter = 0
        self.Moteur.Avatar.changer_expression ("NORMAL", -1)
        VAR.cycle_partie == -1
               
        self.demarrer()
    
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
    
    
    def fige_le_temps(self):
        self.memoireDuTemps = (pygame.time.get_ticks() - self.Moteur.Partie.cycle)
 
    def libere_le_temps(self):
         self.Moteur.Partie.cycle = (pygame.time.get_ticks() + self.memoireDuTemps)
         
         
                            
    def afficher_message(self):
        if self.partie_arretee() or not VAR.partie_en_cours():
            
            if not self.Moteur.actif : 
                texte = "PRESSEZ START"
            elif self.mort: 
                texte = "REJOUER, PRESSEZ START"
            else:
                texte = "PAUSE"
            
            image_pause = VAR.ecritures[VAR.TAILLE_ECRITURE].render(texte, True, (255,255,255,255)) 
            largeur, hauteur = (VAR.DIMENSION[0] * VAR.TAILLE), (VAR.DIMENSION[1] * VAR.TAILLE)
            cX, cY = self.Moteur.grille.offX + ((largeur - image_pause.get_width())/2) , self.Moteur.grille.offY + int((hauteur - image_pause.get_height()) /2 )
            
            couleur = self.Moteur.couleur
            pygame.draw.rect(VAR.fenetre, (0,0,0,255), (self.Moteur.grille.offX, cY-10, largeur+2, image_pause.get_height()+20), 0)
            pygame.draw.rect(VAR.fenetre, couleur, (self.Moteur.grille.offX, cY-10, largeur+2, image_pause.get_height()+20), 2)
            VAR.fenetre.blit(image_pause, (cX, cY))
    
    def afficher_score(self): 
        y=0
        for taille, texte in ((20, "Lignes : "+str(self.nbLignes)), (20, "Niveau : " + str(self.niveau)), (30, "Score : " + str(self.score))) :
            image = VAR.ecritures[taille].render(texte, True, (255,255,255,255)) 
            
            pX = self.Moteur.grille.offX + (VAR.TAILLE * 3) + VAR.marge
            pY = self.Moteur.grille.offY - self.Moteur.grille.cadreHaut[3] + VAR.marge
            VAR.fenetre.blit(image, (pX, pY + y))
            y += image.get_height() 
        
        image_rang = VAR.ecritures[VAR.TAILLE_ECRITURE * 5].render(str(self.rang), True, (255,255,255,255)) 
        pX = self.Moteur.grille.offX + (VAR.DIMENSION[0] * VAR.TAILLE) - image_rang.get_width()
        pY = self.Moteur.grille.offY + (VAR.DIMENSION[1] * VAR.TAILLE) + ((self.Moteur.grille.cadreBas[3] - image_rang.get_height()) //2) + VAR.marge
        VAR.fenetre.blit(image_rang, (pX, pY))
        
    

    
        
    


    
     