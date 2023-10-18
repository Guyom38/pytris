from COMMUN.classes.fonctions import *
import COMMUN.classes.fonctions as FCT

import COMMUN.variables as V
from COMMUN.classes.controles import *

from JEU_Pytris.classes.mecanique import CMecanique
from JEU_Pytris.classes.grille import *

import random

class CParties:
    def controle_fin_de_partie():
        if V.partie_demarree :
            if (VAR.temps_de_partie.get_temps_restant() <= 0) or VAR.partie_terminee():
                for i, moteur in V.moteurs.items():
                    moteur.mort = True
                    moteur.Mecanique.action_a_entreprendre_si_le_joueur_a_perdu()
                    
                V.partie_demarree = False
                V.fin_partie = True
                
                VAR.changer_de_mode(VAR.ENUM_MODE.MODE_SCORE)
                FCT.GAUDIO.charger_musique("JEU_Pytris\\audios\\score.mp3")
                

    def gestion_malediction(force = False):
     
        if V.partie_demarree and V.get_nb_joueurs() > 1 and VAR.nbJoueursActifs() > 1:
            if VAR.temps_pouvoir.controle() or force:
                VAR.pouvoirId +=1
                if VAR.pouvoirId > V.get_nb_joueurs() -1: VAR.pouvoirId = 0
                if not V.moteurs[VAR.pouvoirId].Joueur.actif: CParties.gestion_malediction()

        for i, moteur in V.moteurs.items():
            if moteur.Joueur.id > VAR.pouvoirId:
                moteur.Joueur.Avatar.animation_flip.bascule = False
            elif moteur.Joueur.id < VAR.pouvoirId:
                moteur.Joueur.Avatar.animation_flip.bascule = True
# -----------------------------------------------------------------------------------------------------------
# -
# -     CLASSE PARTIE
# -
# -----------------------------------------------------------------------------------------------------------
    def __init__(self, moteur):
        self.Moteur = moteur

        self.score, self.niveau, self.rang = 0, 0, 0
        self.nbLignes, self.ligneNiveau = 0, 0

        self.aide = False
        self.pause = False
        self.mort = True
        
        self.vitesse_partie = GTEMPS.chrono(VAR.vitesse_par_defaut, -1)       
        self.memoireDuTemps = 0
                
        
    def reinitialisation_de_la_vitesse(self):
        self.vitesse_partie.frequence = VAR.vitesse_par_defaut
    def accelerer_la_vitesse_de_la_partie(self):
        self.vitesse_partie.frequence -= 50
    def fige_le_temps(self):
        self.memoireDuTemps = self.vitesse_partie.get_temps_restant() 
    def libere_le_temps(self):
        self.vitesse_partie.cycle = (pygame.time.get_ticks() + self.memoireDuTemps)


    def demarrer(self):
        self.mort, self.pause = False, False
        self.Moteur.Pieces.pieceSuivante = random.choice(VAR.LISTE_DES_PIECES)
        self.Moteur.Pieces.tirer_nouvelle_piece()

    def redemarre(self):
        self.demarrer()

        self.Moteur.Joueur.Avatar.changer_expression ("NORMAL", -1)
        self.Moteur.Joueur.actif = True
        self.reinitialisation_de_la_vitesse()
        self.score, self.nbLignes = 0, 0

        self.Moteur.grille = CGrille(self.Moteur)
        self.Moteur.Mecanique.lignesADetruire = []
        self.Moteur.Mecanique.lignesAjouter = 0
        
    def partie_arretee(self):
        return self.pause or not self.Moteur.Joueur.actif or self.mort          


    def verifie_changement_de_niveau(self):
        self.ligneNiveau +=1
        if self.ligneNiveau == VAR.nbLignesNiveauSuivant:
            
            self.accelerer_la_vitesse_de_la_partie()
            self.niveau +=1
            self.ligneNiveau = 0
            
            self.Moteur.Animation.nivSupActif = True
            GAUDIO.jouer_son("level_up")


    def meurt(self):
        self.Moteur.Joueur.actif = False
        self.mort = True
         
                            
    def afficher_message(self):
        if self.pause:
            texte = "PAUSE"
        elif self.mort:
            texte = "GAME OVER"
        else:
            return
            
        image_pause = FCT.GFONT.get_image_texte(texte, VAR.TAILLE_ECRITURE, (255,255,255,255)) 
        largeur, hauteur = (VAR.DIMENSION[0] * VAR.TAILLE), (VAR.DIMENSION[1] * VAR.TAILLE)
        cX, cY = self.Moteur.grille.offX + ((largeur - image_pause.get_width())/2) , self.Moteur.grille.offY + int((hauteur - image_pause.get_height()) /2 )
            
        couleur = self.Moteur.Joueur.couleur
        pygame.draw.rect(V.fenetre, (0,0,0,255), (self.Moteur.grille.offX, cY-10, largeur+2, image_pause.get_height()+20), 0)
        pygame.draw.rect(V.fenetre, couleur, (self.Moteur.grille.offX, cY-10, largeur+2, image_pause.get_height()+20), 2)
        V.fenetre.blit(image_pause, (cX, cY))
        
    
    def afficher_score(self): 
        liste_images = []
        hauteur = 0
        imageScore = FCT.GFONT.get_image_texte(str(self.score), 30, (255,255,255,255)) 
        for taille, texte in ((20, "Score : " ), (20, "Lignes : "+str(self.nbLignes)), (20, "Niveau : " + str(self.niveau))) : #+ str(self.score)
            image = FCT.GFONT.get_image_texte(texte, taille, (255,255,255,255)) 
            liste_images.append(image)
            hauteur += image.get_height()
        
        y=0    
        for image in liste_images:
            pX = self.Moteur.grille.offX + (VAR.TAILLE * 3) + VAR.marge
            pY = self.Moteur.grille.offY - self.Moteur.grille.cadreHaut[3]  - VAR.marge + ((self.Moteur.grille.cadreHaut[3] - hauteur) //2)
            
            if y == 0:
                V.fenetre.blit(imageScore, (pX + image.get_width(), pY + y))
                
            V.fenetre.blit(image, (pX, pY + y))
            y += image.get_height() 
        
        
        image_rang = FCT.GFONT.get_image_texte(str(self.rang), (VAR.TAILLE_ECRITURE * 5), (255,255,255,255)) 
        pX = self.Moteur.grille.offX + (VAR.DIMENSION[0] * VAR.TAILLE) - image_rang.get_width()
        pY = self.Moteur.grille.offY + (VAR.DIMENSION[1] * VAR.TAILLE) + ((self.Moteur.grille.cadreBas[3] - image_rang.get_height()) //2) + VAR.marge
        V.fenetre.blit(image_rang, (pX, pY))
        
        image_nom = FCT.GFONT.get_image_texte(self.Moteur.Joueur.nom, 30, (255,255,255,255)) 
        V.fenetre.blit(image_nom, (self.Moteur.grille.offX + self.Moteur.Joueur.Avatar.maxX, pY + VAR.marge))
       

    
        
    


    
     