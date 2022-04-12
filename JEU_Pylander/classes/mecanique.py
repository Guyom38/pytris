
import pygame
from pygame.locals import *

import JEU_Pylander.variables as VAR

import COMMUN.variables as V
import COMMUN.classes.fonctions as FCT


class CMecanique:   
    def __init__(self, m):
        self.M = m
        self.cycle = pygame.time.get_ticks()   
        self.frequence = 70 

    def gravite(self):
        if not V.partie_demarree: return
        if pygame.time.get_ticks() - self.cycle < self.frequence: return
        self.cycle = pygame.time.get_ticks()   

        self.M.vitesse_de_chute = self.M.vitesse_de_chute + 1
        self.M.x = (10 * self.M.x + self.M.deport_lateral) / 10
        self.M.y = (10 * self.M.y + self.M.vitesse_de_chute) / 10
 
    def controle_sortie_de_lecran(self):
        if  (self.M.x < 0 or self.M.x > VAR.altitude):
            self.M.x = self.M.x - (abs(self.M.x) / self.M.x) * VAR.altitude
         
    def controle_collision_decors(self):
        for i in range(VAR.nombre_decors):
            
            
            if self.M.Decors.mx[i] <= self.M.x and self.M.Decors.mx[i+1] >= self.M.x and (self.M.Decors.my[i] <= self.M.y or self.M.Decors.my[i+1] <= self.M.y):
                self.M.etat = VAR.ENUM_ETAT.ECHEC
        
    def controle_atterissage(self):
        if (self.M.y+8) >= self.M.Decors.my[self.M.base] and self.M.x > self.M.Decors.mx[self.M.base-1] and self.M.x<self.M.Decors.mx[self.M.base] and self.M.vitesse_de_chute<self.M.vitesse_max_altitude:
            self.M.etat = VAR.ENUM_ETAT.SUCCES
    
    def gestion_explosion(self):
        if self.M.taille_explosion > 10 and self.M.etat == VAR.ENUM_ETAT.ECHEC:
            self.M.taille_vaisseau = self.M.taille_vaisseau + VAR.pas
            self.M.taille_explosion = self.M.taille_explosion - VAR.pas