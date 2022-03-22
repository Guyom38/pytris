import pygame
from pygame.locals import *

import time, os, random

import JEU_Pytris.variables as VAR
import COMMUN.variables as V


class GBASE:
    def GenereMat2D(dimX, dimY, valeurDefaut):
        return [[valeurDefaut for x in range(dimY)] for i in range(dimX)]

    def iif(condition, vrai, faux):
        if condition:
            return vrai
        else:
            return faux
    
class GTEMPS:
    def init(nom):
        V.temps[nom] = [pygame.time.get_ticks(), 0]
    
    def est_il_temps(nom):
        if pygame.time.get_ticks() - V.temps[nom][0] > V.temps[nom][1] :
            V.temps[nom][0] = pygame.time.get_ticks()
            return True
        return False
    
    def format_temps(temps):
        return time.strftime('%H:%M:%S', time.gmtime(temps))     
    
    def convert(seconds): 
        seconds = seconds % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        
        return "%d:%02d:%02d" % (hour, minutes, seconds) 
           
class GIMAGE:
    def image_vide(dimx, dimy):
        return pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)

    def image_decoupe(img, x, y, dimx, dimy, dimxZ = -1, dimyZ = -1):
        tmp = pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)
        tmp.blit(img, (0,0), (int(x) * dimx, int(y) * dimy, dimx, dimy))
                            
        # --- Colle le decors 
        if dimxZ != -1 and dimyZ != -1:   
            tmp = pygame.transform.scale(tmp, (dimxZ, dimyZ))
        return tmp

class GFONT:
    def add_ecriture( nom, police, taille):
        V.ecritures[nom] = pygame.font.SysFont(police, taille)    

    @classmethod    
    def get_image_texte(cls, message, taille, couleur = (255,255,255,255)):
        if not taille in V.ecritures:
            cls.add_ecriture(taille, V.ECRITURE_PAR_DEFAULT, taille)
        return V.ecritures[taille].render(message, True, couleur)







# --- DEPENDANTE DU JEU
class GAUDIO:
    def jouer_musique():
        if V.audio and V.musique:
            try:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
            except Exception:
                print("Erreur")

    def charger_musique(fichier):
        pygame.mixer.music.load(fichier)


    def arreter_musique():
        if V.audio and V.musique:
            pygame.mixer.music.stop()


    def jouer_son(son):
        if V.audio:
            pygame.mixer.Sound.play(V.AUDIOS[son])
        

