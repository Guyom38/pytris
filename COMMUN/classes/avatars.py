import pygame
from pygame.locals import *
 
import JEU_Pytris.variables as VAR
from COMMUN.classes.fonctions import *
import COMMUN.variables as V
#from JEU_Pytris.grille import *

import csv, math, random, os

class CAvatars:
    DOSSIER = "COMMUN\\"
    COLLECTION = {"yeux" :   {"MORT" : ["15"], "NORMAL" : ["03"], "CONTENT" : ["27"], "ENERVE" : ["17"], "CONCENTRE" : ["18"], "EPUISE" : ["25"], "DORT" : ["14"], "POUVOIR" : ["16"], "BISOUS" : ["33"]}, \
                  "bouche" : {"MORT" : ["50"], "NORMAL" : ["55"], "CONTENT" : ["20"], "ENERVE" : ["33"], "CONCENTRE" : ["07"], "EPUISE" : ["24"], "DORT" : ["18"], "POUVOIR" : ["33"], "BISOUS" : ["10"]}}
   


    ALPHA = 60
    COULEUR = ( (232,147,15,ALPHA), \
                (110,68,216,ALPHA), \
                (20,163,194,ALPHA), \
                (216,78,28,ALPHA), \
                (240,212,72,ALPHA), \
                (53,53,86,ALPHA), \
                (216,68,18,ALPHA), \
                (158,57,34,ALPHA), \
                (224,224,224,ALPHA), \
                (59,59,59,ALPHA) )
    
    LISTE_NOMS = ["Groun", "Kazek", "Thinuf", "Vonog", "Grodron", "Dronbok", "Kazdre", "Azgan", "Vondur", "Waelg", "Damval", "Kroncae", "Dronkar", "Ginuf", \
              "Gilsko", "Bokskrarag", "Agcae", "Riltha", "Darnog", "Dron", "Zornthron", "Grogor", "Mingin", "Ekskre", "Golskre", "Kruag", "Throngrin", \
              "Griaz", "Anag", "Zornmin", "Kaz", "Trolrhun", "Unthron", "Elgril", "Stogriki", "Galag", "Agsko", "Gurfron", "Ginril", "Grinthron", "Rilthin", \
              "Rhunril", "Caeskra", "Ekgin", "Gurnog", "Ufdam", "Gorgur", "Kazgru", "Zornuz", "Fronelg", "Uzganrin", "Rikgar", "Krukul", "Rilcaeril", "Skogin", \
              "Lokgil", "Grudag", "Skouf", "Rikdag", "Ogur", "Dregan", "Agval", "Makkim", "Ekazril", "Gardun", "Throngin", "Thronzorn", "Kulum", "Skraag", "Krontol", \
              "Makril", "Okgan", "Karrag", "Stouz", "Duntha"]
    
    LISTE_CHEVEUX = []
    LISTE_BARBES = []
    LISTE_CILS = []    
    
    DONNEES = {}
    LISTE_FICHIER = {}
    
    
    def chargement_fichiers_sprites():
        with open(CAvatars.DOSSIER + 'avatars\\avatars.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                CAvatars.DONNEES[row['dossier'] + row['fichier']] = (int(row['x']), int(row['y']))
              
                if row['dossier'] == "cils":
                    CAvatars.LISTE_CILS.append(row['fichier'])
                elif row['dossier'] == "barbes":
                    CAvatars.LISTE_BARBES.append(row['fichier'])
                elif row['dossier'] == "cheveux":
                    CAvatars.LISTE_CHEVEUX.append(row['fichier'])
               
                
    def charger_textures(couleur, dossier, fichier, ratio):
        chemin = CAvatars.DOSSIER + "avatars"
        
        if couleur == "":
            chemin = chemin + "\\"+dossier+"\\"+fichier+".png"
        elif dossier == "corps":
            chemin = chemin + "\\"+dossier+"\\"+couleur + "\\"+fichier+".png"
        elif dossier in ("barbes", "cheveux"):
            chemin = chemin + "\\"+dossier+"\\"+couleur + "\\"+couleur+" "+fichier+".png"
        else:
            chemin = chemin + "\\"+dossier+"\\"+couleur + "\\"+fichier+".png"
            
        img = pygame.image.load(chemin).convert_alpha()
        img = pygame.transform.scale(img, (int(img.get_width() * ratio[0]), int(img.get_height() * ratio[1])))
        
        if not dossier == "nez":
            x, y = CAvatars.DONNEES[dossier+fichier]
        else:
            x, y = CAvatars.DONNEES[dossier+"01"]
        x, y = int(x * ratio[0]), int(y * ratio[1])
        
        return dossier, img, x, y 
    
    # ----------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self, joueur):
        self.Joueur = joueur
        #self.IMG_AVATARS = {}
        self.image = None
        
        self.offY = 0
        self.chemin = CAvatars.DOSSIER + "avatars"
        
        self.animation_cycle = 0
        self.animation_frequence = 50
        self.animation_cpt = 0
        
        self.animation_flip_cycle = 0
        self.animation_flip_frequence = 3000
        self.animation_flip = False
        
        self.expression = "DORT"
        self.expressionOld = "DORT"
        
        self.expression_actif = {"yeux" : False, "bouche" : False}
        self.expression_liste = {"yeux" : [], "bouche" : []}
        self.expression_id = {"yeux" : 0, "bouche" : 0}
        self.expression_cycle = {"global" : 0, "yeux" : 0, "bouche" : 0}
        self.expression_frequence = {"global" : 0, "yeux" : 0, "bouche" : 0}    

        self.ratioX, self.ratioY = VAR.TAILLE * 0.007, VAR.TAILLE * 0.007
        self.maxX, self.maxY = 0, 0
        
        self.salonX, self.salonY = 0, 0
        
        liste_corps = []
        for i in range(1, 33):
            if i<10:
                liste_corps.append("0"+str(i))
            else:
                liste_corps.append(str(i))
                
        liste_poiles = []
        for i in range(1, 11):
            if i<10:
                liste_poiles.append("0"+str(i))
            else:
                liste_poiles.append(str(i))

        self.ratioY += (random.randint(0, 15) / 1000)       
        self.charger_personnage()
            
        
    
    def remet_expression_precedent(self):
        self.changer_expression(self.expressionOld, -1)
        
        
    def changer_expression(self, expression, delais):
        self.expression_cycle["global"] = pygame.time.get_ticks()
        self.expression_frequence["global"] = delais
        
        self.expressionOld = self.expression
        self.expression = expression
        self.expression_liste = {"yeux" : CAvatars.COLLECTION["yeux"][self.expression], \
                                 "bouche" : CAvatars.COLLECTION["bouche"][self.expression]}
        
       
        
        
    def charger_expression(self):
        self.expression_liste = {"yeux" : CAvatars.COLLECTION["yeux"][self.expression], \
                                 "bouche" : CAvatars.COLLECTION["bouche"][self.expression]}
        self.expression_id = {"global" : 0, "yeux" : 0, "bouche" : 0}
        self.expression_frequence = {"global" : 3000, "yeux" : 5000, "bouche" : 7000}
        
   
       
    def charger_personnage(self, couleurCorps = "", couleurPoiles = "", cheveux = "", cils = "", barbe = "", ratio = ""):
        couleur = self.Joueur.id +1
        if couleur < 10: couleur = "0" + str(couleur)
        
        if couleurCorps == "":   couleurCorps = random.choice(("01", "02", "03", "04", "05", "06", "07", "08", "09", "10"))
        if couleurPoiles == "":  couleurPoiles = couleur
        if cheveux == "": cheveux = random.choice(CAvatars.LISTE_CHEVEUX)
        if cils == "": cils = random.choice(CAvatars.LISTE_CILS)
        if barbe == "": barbe = random.choice(CAvatars.LISTE_BARBES)
        if ratio == "": ratio = (self.ratioX, self.ratioY)
                                
        # --- COMMUN
        self.yeux = {"yeux" : {}}
        for i in os.listdir(self.chemin + "\\yeux\\"):
            index = i.replace(".png","")
            self.yeux["yeux"][index] = CAvatars.charger_textures("", "yeux", index, ratio)
        
        self.bouche = {"bouche": {}} #    self.charger_textures("", "bouches", "17", ratio)
        for i in os.listdir(self.chemin + "\\bouches\\"):
            index = i.replace(".png","")
            self.bouche["bouche"][index] = CAvatars.charger_textures("", "bouches", index, ratio)
            
        # --- SPECIFIQUE   
        self.tete = CAvatars.charger_textures(couleurCorps, "corps", "Head",ratio)
        self.nez = CAvatars.charger_textures("01", "nez", couleurCorps,ratio)
        self.oreille = CAvatars.charger_textures(couleurCorps, "corps", "Ear", ratio)
        self.corps = CAvatars.charger_textures(couleurCorps, "corps", "Body", ratio)
        self.bras_droit = CAvatars.charger_textures(couleurCorps, "corps", "Arm", ratio)
        self.bras_gauche = CAvatars.charger_textures(couleurCorps, "corps", "ArmBack", ratio)
        self.pied_droit = CAvatars.charger_textures(couleurCorps, "corps", "Leg", ratio)
        self.pied_gauche = CAvatars.charger_textures(couleurCorps, "corps", "LegBack", ratio)
        
        self.cheveux = CAvatars.charger_textures(couleurPoiles, "cheveux", cheveux, ratio)
                
        self.cils = CAvatars.charger_textures(couleurPoiles, "cils", cils, ratio)
        self.barbe = CAvatars.charger_textures(couleurPoiles, "barbes", barbe, ratio)
        
        self.charger_expression()  
 
        
    
    
         
    def afficher_membres(self, liste_membres, x, y):
        for d in (liste_membres):
            if ("bouche" in d) or ("yeux" in d):
                element = []
                
                for el in ("yeux", "bouche"):
                    if el in d:
                        if self.expression_actif[el]:
                            key = self.expression_liste[el][self.expression_id[el]]
                        else:
                            key = self.expression_liste[el][0]
                            
                        element = d[el][key]
            else:    
                element = d
                
            xP = x + element[2]
            yP = y + element[3]
            image = element[1]


            self.image.blit(image, (xP, yP))
            maxX, maxY = xP + image.get_width(), yP + image.get_height()
            if maxX > self.maxX: self.maxX = maxX
            if maxY > self.maxY: self.maxY = maxY
            
            
        

    def dessiner(self, x, y):
        self.image = GIMAGE.image_vide(680 * self.ratioX, 720 * self.ratioY)
        self.afficher_membres((self.bras_gauche, self.pied_gauche, self.corps, self.pied_droit, self.bras_droit), 0, 0 )
        
        # --- Animation et affichage des différents élements de la tete   
        yP = (math.cos(self.animation_cpt) * 1) 
        self.afficher_membres((self.tete, self.oreille, self.yeux, self.cheveux, self.cils, self.barbe, self.bouche, self.nez), 0, yP)
        
        if self.animation_flip:
            self.image = pygame.transform.flip(self.image, True, False) 
            
        
        V.fenetre.blit(self.image, (x, y))
        
    
    def gestion_pouvoir(self):
        if VAR.pouvoirId == self.Joueur.id:
            if self.expression != "POUVOIR": self.changer_expression("POUVOIR", -1)
            return True
        elif self.expression == "POUVOIR" :
            if self.expressionOld == "POUVOIR": self.expressionOld = "NORMAL"
            self.remet_expression_precedent()         
            return False
    
    def gestion_expression(self):
        if self.expression_cycle["global"] > 0 and self.expression_cycle["global"] != -1:
            if pygame.time.get_ticks() - self.expression_cycle["global"] > self.expression_frequence["global"]:
                self.expression_cycle["global"] = 0
                self.remet_expression_precedent()    
                
    def gestion_sens(self):
         # --- Rythme d'animation du flip
        if pygame.time.get_ticks() - self.animation_flip_cycle > self.animation_flip_frequence:
            self.animation_flip = not self.animation_flip
            self.animation_flip_frequence = random.randint(2000, 30000)
            self.animation_flip_cycle = pygame.time.get_ticks()
     
    def gestion_animation(self):
        # --- Rythme d'animation
        if pygame.time.get_ticks() - self.animation_cycle > self.animation_frequence:
            self.animation_cpt +=1
            self.animation_cycle = pygame.time.get_ticks()
    
    def gestion_visage(self):
        # --- Changement d'expressions du visage
        for element in ("yeux", "bouche"):
            if pygame.time.get_ticks() - self.expression_cycle[element] > GBASE.iif(self.expression_actif, self.expression_frequence[element], 300):
                self.expression_actif[element] = not self.expression_actif[element]
                
                if self.expression_actif[element]: 
                    self.expression_id[element] +=1
                    if self.expression_id[element] > len(self.expression_liste[element])-1: self.expression_id[element] = 0
                    
                self.expression_cycle[element] = pygame.time.get_ticks()
    
    def gestion_personnage(self):
        if self.Joueur.actif:
            if not self.gestion_pouvoir():
                self.gestion_expression()
            self.gestion_sens()
            self.gestion_animation()
            self.gestion_visage()    
    
                                         
    def afficher(self, x, y):
        self.gestion_personnage()

        
        # --- Affichage des différents élements du corps   
        
        self.offY = self.pied_droit[3] + self.pied_droit[1].get_height() 
        self.dessiner(x, y - self.offY)
        
        
        

       