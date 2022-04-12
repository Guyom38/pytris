import pygame
from pygame.locals import *

import time, os, random
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
    
    class chrono:
        def __init__(self, _frequence, _cycle = None, _defaut_cycle = None):
            #print("Initialisation " + str(_frequence) + str(_cycle) + str(_defaut_cycle))
            self.defaut = _defaut_cycle
            self.cycle = 0
            self.frequence = _frequence
            self.bascule = False

            self.reset(_cycle)


        def reset(self, _cycle = None):
            #print("Reset "+str(_cycle))
            if _cycle == None:
                self.cycle = pygame.time.get_ticks()   
            else:
                self.cycle = _cycle

        def controle(self):
            #print("Controle")
            return self.verification(self.frequence)
        
        def verification(self, _frequence):
            if pygame.time.get_ticks() - self.cycle > _frequence:
                self.bascule = not self.bascule

                if self.defaut == None :
                    self.cycle = pygame.time.get_ticks()
                else:
                    self.cycle = self.defaut

                return True
            return False

        def get_temps_restant(self):
            #print("Restant : " + str(pygame.time.get_ticks() - self.cycle) )
            return (pygame.time.get_ticks() - self.cycle)

        



   
    
    def format_temps(temps):
        return time.strftime('%H:%M:%S', time.gmtime(temps))     
    
    def convert(seconds): 
        seconds = seconds % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        
        return "%d:%02d:%02d" % (hour, minutes, seconds) 
           


class GFONT:
    def add_ecriture( nom, police, taille):
        V.ecritures[nom] = pygame.font.SysFont(police, taille)    

    @classmethod    
    def get_image_texte(cls, message, taille, couleur = (255,255,255,255), police = ""):
        if police == "": police = V.ECRITURE_PAR_DEFAULT
        if not taille in V.ecritures:
            cls.add_ecriture(police+str(taille), police, taille)
        return V.ecritures[police+str(taille)].render(str(message), True, couleur)



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

    class point:
        def __init__(self, x, y):
            self.x, self.y = x, y

    class rectangle:
        def __init__(self, x, y, largeur, hauteur):
            self.x, self.y, self.largeur, self.hauteur = x, y, largeur, hauteur
        
        def get_x2(self):
            return self.x + self.largeur
        
        def get_y2(self):
            return self.y + self.hauteur


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
        

