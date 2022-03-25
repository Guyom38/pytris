import pygame
from pygame import *

from JEU_Pylander.classes.manette import *

import JEU_Pylander.variables as VAR
from JEU_Pylander.variables import *

import COMMUN.variables as V
import COMMUN.classes.fonctions as FCT

import math

class CMoteur:
    def __init__(self, joueur):
        self.Joueur = joueur        
        self.Manette = None

        
    def initialiser(self):     
        self.Manette = CManette(self, self.Joueur.id)
        self.FUSEE_C, self.FUSEE_D, self.FUSEE_G = False, False, False
        self.ALT = 400
        self.MX_ALT = self.ALT/20
        self.V_MAX_ATT = 30
        self.ESSENCE = self.ALT

        self.LG_BASE = 14
        self.BASE = 20

        self.PAS = 10


        self.V_DECAL, self.V_CHUTE = 0, 0
        self.T_VAISS = 5
        self.T_BOOM = 255

        self.NB_DECORS = 40
        self.mx = []
        self.my = []
        self.x = random.randint(self.PAS, self.ALT - self.PAS)
        self.y = self.PAS

        #key.set_repeat(100,100)

        
        
      

        self.creation_du_relief()
        self.installation_de_la_base()
     
    def creation_du_relief(self):                   # ---------------------------------------------------------------- CREATION DU RELIEF
        ref = random.randint(0, self.ALT)
        for i in range(self.NB_DECORS + 1):
            self.mx.append(self.PAS * i)
            self.my.append(int(random.randint(-self.MX_ALT, 0)+(self.ALT / 5) * (4 - math.sin((i+ (ref)) /5.)))-(self.ALT / 32))

    def installation_de_la_base(self):              # ---------------------------------------------------------------- INSTALLATION DE LA BASE
        self.mx.append(self.ALT)
        self.my.append(random.randint(self.ALT-self.MX_ALT,self.ALT))
        self.mx[self.BASE]=self.mx[self.BASE-1]+self.LG_BASE
        self.my[self.BASE]=self.my[self.BASE-1]

    def redemarre(self):
        self.x=math.randint(self.PAS, self.ALT - self.PAS)
        self.y=self.PAS
        self.V_DECAL, V_CHUTE = 0, 0
        self.T_VAISS = 5
        self.T_BOOM = 255
        self.ESSENCE = self.ALT
        VAR.MESSAGE = VAR.AUCUN

    def afficher(self):
            if VAR.MESSAGE == VAR.AUCUN:
                # ---------------------------------------------------------------- EMPECHE LA FUSEE DE SORTIR DE L'ECRAN (SUR LES COTES)
                if  (self.x<0 or self.x> self.ALT):
                    self.x = self.x-(abs(self.x)/ self.x)* VAR.ALT

                # ---------------------------------------------------------------- TIRE LA FUSEE VERS LE BAS
                self.V_CHUTE= self.V_CHUTE+1
                self.x=(10*self.x+ self.V_DECAL)/10
                self.y=(10*self.y+ self.V_CHUTE)/10

                # ---------------------------------------------------------------- VERIFIE QUE LA FUSEE N'A PAS TOUCHE LE DECORS 
                for i in range(self.NB_DECORS):
                    if self.mx[i]<=self.x and self.mx[i+1]>=self.x and (self.my[i]<=self.y or self.my[i+1]<=self.y):
                        VAR.MESSAGE=VAR.ECHEC

            # ---------------------------------------------------------------- VERIFIE QUE LA FUSEE SE POSE SUR LA BASE
            if (self.y+8)>=self.my[self.BASE] and self.x>self.mx[self.BASE-1] and self.x<self.mx[self.BASE] and self.V_CHUTE<self.V_MAX_ATT:
                VAR.MESSAGE=VAR.SUCCES
            
            # ---------------------------------------------------------------- EFFACE L'ECRAN
            V.fenetre.fill(VAR.NOIR)
            
            # ---------------------------------------------------------------- GESTION DU VAISSEAU
            if self.T_BOOM>10 and VAR.MESSAGE==VAR.ECHEC:
                self.T_VAISS=self.T_VAISS+self.PAS
                self.T_BOOM=self.T_BOOM-self.PAS
            
            # ---------------------------------------------------------------- DESSINE LE VAISSEAU
            for i in range(50):
                ax= self.x+ self.T_VAISS*math.sin(i/8.)
                ay= self.y+ self.T_VAISS*math.cos(i/8.)
                couleur_explosion = (self.T_BOOM, self.T_BOOM,self.T_BOOM)
                draw.line(V.fenetre, couleur_explosion,(ax,ay), (ax,ay))

            # ---------------------------------------------------------------- DESSINE LE PROPULSEUR PRINCIPAL
            if self.FUSEE_C == True:
                draw.line(V.fenetre, VAR.ROUGE,(self.x+3,self.y+3), (self.x+4,self.y+6))
                draw.line(V.fenetre, VAR.ROUGE,(self.x-3,self.y+3), (self.x-4,self.y+6))

            # ---------------------------------------------------------------- DESSINE LES PROPULSEURS GAUCHE ET DROITE 
            if self.FUSEE_G == True:
                draw.line(V.fenetre, VAR.ROUGE,(self.x+2,self.y+5), (self.x,self.y+9))
            if self.FUSEE_D == True:
                draw.line(V.fenetre, VAR.ROUGE,(self.x-2,self.y+5), (self.x,self.y+9))

            # ---------------------------------------------------------------- DESSINE LE RELIEF
            for i in range(self.NB_DECORS):
                draw.line(V.fenetre, VAR.BLANC,(self.mx[i],self.my[i]), (self.mx[i+1],self.my[i+1]))   

            # ---------------------------------------------------------------- DESSINE LA BASE
            draw.line(V.fenetre, VAR.ROUGE,(self.mx[self.BASE-1],self.my[self.BASE-1]),(self.mx[self.BASE],self.my[self.BASE]),3)  

            # ---------------------------------------------------------------- AFFICHE LES INFOS DU JEU
            txt = VAR.MESSAGE
            if VAR.MESSAGE == VAR.AUCUN:
                txt='ESSENCE %3d     ALTITUDE %3d     VERT VITESSE %3d     HORZ VITESSE %3d'%(self.ESSENCE,self.ALT-self.y,self.V_CHUTE,self.V_DECAL)
                
            text=FCT.GFONT.get_image_texte(txt,20,VAR.GRIS)
            V.fenetre.blit(text,(0,self.ALT-12))
