import pygame
from pygame import *

from JEU_Pylander.classes.manette import CManette
from JEU_Pylander.classes.mecanique import CMecanique
from JEU_Pylander.classes.decors import CDecors

import JEU_Pylander.variables as VAR
from JEU_Pylander.variables import *

import COMMUN.variables as V
import COMMUN.classes.fonctions as FCT

import math, random

class CMoteur:
    def __init__(self, joueur):
        self.Joueur = joueur    

        self.Manette = None
        self.Mecanique = CMecanique(self)
        self.Decors = CDecors(self)

        self.offX, self.offY = 0, 0

        self.image = FCT.GIMAGE.image_vide(400, 800)
        


    def initialiser(self):     
        self.Manette = CManette(self, self.Joueur.id)
        
        self.propulseur_central = False
        self.propulseur_droit = False
        self.propulseur_gauche = False
        
        self.max_altitude = VAR.altitude / 20
        self.vitesse_max_altitude = 30
        self.carburant = VAR.altitude

        self.longueur_base = 14
        self.base = 20

  
        self.x = random.randint(VAR.pas, VAR.altitude - VAR.pas)
        self.y = VAR.pas

        self.deport_lateral = 0
        self.vitesse_de_chute = 0
        self.taille_vaisseau = 5
        self.taille_explosion = 255

        
        
        
        
        self.etat = ENUM_ETAT.AUCUN

        #key.set_repeat(100,100)

        self.Decors.creation_du_relief()
        self.Decors.installation_de_la_base()
     
    def redemarre(self):
        self.x = math.randint(VAR.pas, VAR.altitude - VAR.pas)
        self.y = VAR.pas
        self.deport_lateral = 0
        self.vitesse_de_chute = 0
        self.taille_vaisseau = 5
        self.taille_explosion = 255
        self.carburant = VAR.altitude
        self.etat = ENUM_ETAT.AUCUN

    
    
    def dessiner_vaisseau(self):
        for i in range(50):
            ax = self.x + self.taille_vaisseau * math.sin( i / 8.)
            ay = self.y + self.taille_vaisseau * math.cos( i / 8.)
            couleur_explosion = (self.taille_explosion, self.taille_explosion, self.taille_explosion)
            draw.line(self.image, couleur_explosion,(ax, ay), (ax, ay))

        # ---------------------------------------------------------------- DESSINE LE PROPULSEUR PRINCIPAL
        if self.propulseur_central == True:
            draw.line(self.image, VAR.ROUGE, (self.x +3, self.y +3), (self.x +4, self.y +6))
            draw.line(self.image, VAR.ROUGE, (self.x -3, self.y +3), (self.x -4, self.y +6))

        # ---------------------------------------------------------------- DESSINE LES PROPULSEURS GAUCHE ET DROITE 
        if self.propulseur_gauche == True:
            draw.line(self.image, VAR.ROUGE,(self.x + 2, self.y + 5), (self.x, self.y + 9))
        if self.propulseur_droit == True:
            draw.line(self.image, VAR.ROUGE,(self.x - 2, self.y + 5), (self.x, self.y + 9))
    
    def dessiner_decors(self):
        for i in range(VAR.nombre_decors):
            draw.line(self.image, VAR.BLANC, (self.Decors.mx[i], self.Decors.my[i]), (self.Decors.mx[i+1], self.Decors.my[i+1]))               
    
    def dessiner_base(self):
        draw.line(self.image, VAR.ROUGE, (self.Decors.mx[self.base-1], self.Decors.my[self.base-1]), (self.Decors.mx[self.base], self.Decors.my[self.base]), 3)  
         
    def afficher_infos(self):
        if self.etat == ENUM_ETAT.SUCCES: 
            txt = "Victoire"
        elif self.etat == ENUM_ETAT.SUCCES: 
            txt = "Echec de la mission"
        else:
            txt = 'Carburant %3d     Altitude %3d     Vitesse Vertic. %3d     Vit. Horiz. %3d'%(self.carburant, VAR.altitude - self.y, self.vitesse_de_chute, self.deport_lateral)
                
        text=FCT.GFONT.get_image_texte(txt, 20, VAR.GRIS)
        self.image.blit(text, (16, self.offY + self.image.get_height()-30))       

        
        
        
    def afficher(self):
            self.image.fill(self.Joueur.couleur)
            
            if self.etat == ENUM_ETAT.AUCUN:
                self.Mecanique.controle_sortie_de_lecran()
                self.Mecanique.gravite()
                self.Mecanique.controle_collision_decors()

            self.Mecanique.controle_atterissage()
            self.Mecanique.gestion_explosion()

            self.dessiner_vaisseau()
            self.dessiner_decors()
            self.dessiner_base()

            self.afficher_infos()

            V.fenetre.blit(self.image, (self.offX, self.offY))
            self.Joueur.Avatar.gestion_personnage()
            self.Joueur.Avatar.dessiner(self.offX, self.offY + self.image.get_height() - self.Joueur.Avatar.maxY)
