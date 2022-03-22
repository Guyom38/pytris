import pygame
from pygame.locals import *

import time, os, random

import JEU_Pytris.variables as VAR
import COMMUN.variables as V

def GenereMat2D(dimX, dimY, valeurDefaut):
    return [[valeurDefaut for x in range(dimY)] for i in range(dimX)]

def image_vide(dimx, dimy):
    return pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)

def image_decoupe(img, x, y, dimx, dimy, dimxZ = -1, dimyZ = -1):
    tmp = pygame.Surface((dimx, dimy),pygame.SRCALPHA,32)
    tmp.blit(img, (0,0), (int(x) * dimx, int(y) * dimy, dimx, dimy))
                        
    # --- Colle le decors 
    if dimxZ != -1 and dimyZ != -1:   
        tmp = pygame.transform.scale(tmp, (dimxZ, dimyZ))
    return tmp

def format_temps(temps):
    return time.strftime('%H:%M:%S', time.gmtime(temps))

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds) 

def iif(condition, vrai, faux):
    if condition:
        return vrai
    else:
        return faux


# --- DEPENDANTE DU JEU
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
        

