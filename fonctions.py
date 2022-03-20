import pygame
from pygame.locals import *

import time, os, random
import variables as VAR

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
    if VAR.audio and VAR.musique:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

def charger_musique(fichier):
        pygame.mixer.music.load("audios\\" + fichier)


def arreter_musique():
    if VAR.audio and VAR.musique:
        pygame.mixer.music.stop()


def jouer_son(son):
    if VAR.audio:
        pygame.mixer.Sound.play(VAR.AUDIOS[son])
        
def changer_de_mode(x):
    VAR.mode = x
    
    if x == VAR.MODE_JEU:
        fichier = random.choice(os.listdir("audios\\musics"))
        charger_musique("musics\\" + fichier)
        
    elif x == VAR.MODE_SALON:
        charger_musique("attente.mp3")
    elif x == VAR.MODE_SCORE:
        charger_musique("score.mp3")
    else:
        arreter_musique()        