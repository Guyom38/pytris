import pygame
from pygame.locals import *

import time

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
    return time.strftime('%H:%M', time.gmtime(temps))