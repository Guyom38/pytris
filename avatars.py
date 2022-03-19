import pygame
from pygame.locals import *

import time, os
import variables as VAR
import fonctions as FCT


import csv, math

class CAvatars:
    def __init__(self):
        self.DONNEES = {}
        self.IMG_AVATARS = {}
        
        self.chemin = "avatars"
        
        self.animation_cycle = 0
        self.animation_frequence = 50
        self.animation_cpt = 0
        
        self.expression_cycle = 0
        self.expression_frequence = 5000
        self.expression = "NORMAL"
        self.expression_liste = ("03", "18")
        self.expression_actif = False
        self.expression_id = 0
        
        self.chargement_fichiers_sprites()
        
    
        self.charger_personnage("04", "02", "(3)", "09", "(4)")
        
    def charger_personnage(self, couleurCorps, couleurPoiles, cheveux, cils, barbe):
        ratio = 0.3
        self.tete = self.charger_textures(couleurCorps, "corps", "Head",ratio)
        self.nez = self.charger_textures("01", "nez", "01",ratio)
        self.oreille = self.charger_textures(couleurCorps, "corps", "Ear", ratio)
        self.corps = self.charger_textures(couleurCorps, "corps", "Body", ratio)
        self.bras_droit = self.charger_textures(couleurCorps, "corps", "Arm", ratio)
        self.bras_gauche = self.charger_textures(couleurCorps, "corps", "ArmBack", ratio)
        self.pied_droit = self.charger_textures(couleurCorps, "corps", "Leg", ratio)
        self.pied_gauche = self.charger_textures(couleurCorps, "corps", "LegBack", ratio)
        
        self.cheveux = self.charger_textures(couleurPoiles, "cheveux", cheveux, ratio)
        
        self.yeux = {}
        for i in self.expression_liste:
            self.yeux[i] = self.charger_textures("", "yeux", i, ratio)
            
        self.cils = self.charger_textures(couleurPoiles, "cils", cils, ratio)
        self.bouche = self.charger_textures("", "bouches", "17", ratio)
        self.barbe = self.charger_textures(couleurPoiles, "barbes", barbe, ratio)
      
    
    def charger_textures(self, couleur, dossier, fichier, ratio):
        if couleur == "":
            chemin = self.chemin + "\\"+dossier+"\\"+fichier+".png"
        elif dossier == "corps":
            chemin = self.chemin + "\\"+dossier+"\\"+couleur + "\\"+fichier+".png"
        elif dossier in ("barbes", "cheveux"):
            chemin = self.chemin + "\\"+dossier+"\\"+couleur + "\\"+couleur+" "+fichier+".png"
        else:
            chemin = self.chemin + "\\"+dossier+"\\"+couleur + "\\"+fichier+".png"
            
        img = pygame.image.load(chemin).convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width() * ratio), int(img.get_height() * ratio)))
        x, y = self.DONNEES[dossier+fichier]
        x, y = int(x * ratio), int(y * ratio)
        
        return dossier, img, x, y
        
    def chargement_fichiers_sprites(self):
        with open('avatars\\avatars.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.DONNEES[row['dossier'] + row['fichier']] = (int(row['x']), int(row['y']))
    
    def afficher_membres(self, liste_membres, x, y):
        for d in (liste_membres):
            if isinstance(d, dict):
                element = []
                if self.expression_actif:
                    key = self.expression_liste[self.expression_id]
                else:
                    key = self.expression_liste[0]
                    
                if d[key][0] == "yeux":
                    element = d[key]
            else:
                element = d
                
            xP = x + element[2]
            yP = y + element[3]
            
            
            VAR.fenetre.blit(element[1], (xP, yP))
            
    def afficher(self, x, y):
        if pygame.time.get_ticks() - self.animation_cycle > self.animation_frequence:
            self.animation_cpt +=1
            self.animation_cycle = pygame.time.get_ticks()
        
        if pygame.time.get_ticks() - self.expression_cycle > FCT.iif(self.expression_actif, self.expression_frequence, 300):
            self.expression_actif = not self.expression_actif
            
            if self.expression_actif: 
                self.expression_id +=1
                if self.expression_id > len(self.expression_liste)-1: self.expression_id = 0
                
            self.expression_cycle = pygame.time.get_ticks()
            
            
        self.afficher_membres((self.bras_gauche, self.pied_gauche, self.corps, self.pied_droit, self.bras_droit), x, y)
        
        yP = y + (math.cos(self.animation_cpt) * 1)
        self.afficher_membres((self.tete, self.oreille, self.yeux, self.cils, self.cheveux, self.barbe, self.bouche, self.nez), x, yP)

       