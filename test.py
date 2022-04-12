# ---------------------------------------------------------------- IMPORTATION DES LIBRAIRIES
import pygame
from pygame import*

from math import*
from random import*

# ---------------------------------------------------------------- INITIALISATION DU MOTEUR PYGAME
init()

# ---------------------------------------------------------------- INITISALISATION DES VARIABLES
SUCCES='REUSSIE'
ECHEC='CRASH'
MESSAGE=AUCUN=''

FUSEE_C=FUSEE_D=FUSEE_G=False

NOIR=(0,0,0)
GRIS=(255,255,255)
ROUGE=(255,0,0)
BLANC=(255,255,255)

ALT=400
MX_ALT=ALT/20
V_MAX_ATT = 30
ESSENCE=ALT

LG_BASE=14
BASE=20

PAS=10
x=randint(PAS,ALT-PAS)
y=PAS

V_DECAL=V_CHUTE=0
T_VAISS=5
T_BOOM=255

NB_DECORS=40
mx=[]
my=[]
mz=[]

# ---------------------------------------------------------------- CREATION DU RELIEF
ref=randint(0,ALT)
for i in range(NB_DECORS+1):
    mx.append(PAS*i)
    my.append(int(randint(-MX_ALT,0)+(ALT/5)*(4-sin((i+(ref))/5.)))-(ALT/32))

# ---------------------------------------------------------------- INSTALLATION DE LA BASE
mx.append(ALT)
my.append(randint(ALT-MX_ALT,ALT))
mz.append(randint(1, 8))

mx[BASE]=mx[BASE-1]+LG_BASE
my[BASE]=my[BASE-1]

# ---------------------------------------------------------------- CREE LA FENETRE, ET BLOC LE CLAVIER A UNE TOUCHE TOUTES LES 100ms
fenetre=display.set_mode((ALT,ALT))
horloge=time.Clock()
key.set_repeat(100,100)

# ---------------------------------------------------------------- INITIALISE L'ECRITURE POUR LE TEXTE
pygame.font.init()
ECRITURE=pygame.font.SysFont('arial',int(ALT/32))

# ---------------------------------------------------------------- BOUCLE DU JEU
boucle_jeu=False
while boucle_jeu == False:
    # ---------------------------------------------------------------- ETEINT LES PROPULSEURS
    FUSEE_C=FUSEE_D=FUSEE_G=False

    for event in pygame.event.get():
        # ---------------------------------------------------------------- LA CROIX = SORT DU JEU
        if event.type==QUIT:
            boucle_jeu=True

        if event.type==KEYDOWN:
            # ---------------------------------------------------------------- ESC = SORT DU JEU
            if event.key==K_ESCAPE:
                boucle_jeu=True

            # ---------------------------------------------------------------- R = RELANCE LA PARTIE
            if event.key==K_r:
                x=randint(PAS,ALT-PAS)
                y=PAS
                V_DECAL=V_CHUTE=0
                T_VAISS=5
                T_BOOM=255
                ESSENCE=ALT
                MESSAGE=AUCUN

            # ---------------------------------------------------------------- POUR DEPLACER LA FUSEE, IL FAUT DE L'ESSENCE  
            if ESSENCE>0:
                # ---------------------------------------------------------------- ESPACE = REMONTE DE 2, UTILISE 5 D'ESSENCE, ACTIVE PROPULSEUR CENTRALE 
                if event.key==K_SPACE :
                    V_CHUTE=V_CHUTE-2
                    ESSENCE=ESSENCE-5
                    FUSEE_C = True

                # ---------------------------------------------------------------- GAUCHE = POUSSE A DROITE, SE DECALE DE 2, ACTIVE PROPULSEUR GAUCHE
                if event.key==K_LEFT :
                    V_DECAL=V_DECAL+2
                    ESSENCE=ESSENCE-5
                    FUSEE_G = True

                # ---------------------------------------------------------------- DROITE = POUSSE A GAICHE, SE DECALE DE 2, ACTIVE PROPULSEUR DROIT
                if event.key==K_RIGHT:
                    V_DECAL=V_DECAL-2
                    ESSENCE=ESSENCE-5
                    FUSEE_D = True
            
    if MESSAGE==AUCUN:
        # ---------------------------------------------------------------- EMPECHE LA FUSEE DE SORTIR DE L'ECRAN (SUR LES COTES)
        if  (x<0 or x>ALT):
            x=x-(abs(x)/x)*ALT

        # ---------------------------------------------------------------- TIRE LA FUSEE VERS LE BAS
        V_CHUTE=V_CHUTE+1
        x=(10*x+V_DECAL)/10
        y=(10*y+V_CHUTE)/10

        # ---------------------------------------------------------------- VERIFIE QUE LA FUSEE N'A PAS TOUCHE LE DECORS 
        for i in range(NB_DECORS):
            if mx[i]<=x and mx[i+1]>=x and (my[i]<=y or my[i+1]<=y):
                MESSAGE=ECHEC

    # ---------------------------------------------------------------- VERIFIE QUE LA FUSEE SE POSE SUR LA BASE
    if (y+8)>=my[BASE] and x>mx[BASE-1] and x<mx[BASE] and V_CHUTE<V_MAX_ATT:
        MESSAGE=SUCCES
    
    # ---------------------------------------------------------------- EFFACE L'ECRAN
    fenetre.fill(NOIR)
    
    # ---------------------------------------------------------------- GESTION DU VAISSEAU
    if T_BOOM>10 and MESSAGE==ECHEC:
        T_VAISS=T_VAISS+PAS
        T_BOOM=T_BOOM-PAS
      
    # ---------------------------------------------------------------- DESSINE LE VAISSEAU
    for i in range(50):
        ax= x+ T_VAISS*sin(i/8.)
        ay= y+ T_VAISS*cos(i/8.)
        couleur_explosion = (T_BOOM, T_BOOM, T_BOOM)
        draw.line(fenetre, couleur_explosion,(ax,ay), (ax,ay))

    # ---------------------------------------------------------------- DESSINE LE PROPULSEUR PRINCIPAL
    if FUSEE_C == True:
        draw.line(fenetre, ROUGE,(x+3,y+3), (x+4,y+6))
        draw.line(fenetre, ROUGE,(x-3,y+3), (x-4,y+6))

    # ---------------------------------------------------------------- DESSINE LES PROPULSEURS GAUCHE ET DROITE 
    if FUSEE_G == True:
        draw.line(fenetre, ROUGE,(x+2,y+5), (x,y+9))
    if FUSEE_D == True:
        draw.line(fenetre, ROUGE,(x-2,y+5), (x,y+9))

    # ---------------------------------------------------------------- DESSINE LE RELIEF
    for i in range(NB_DECORS):
        #draw.line(fenetre, BLANC,(mx[i],my[i]), (mx[i+1],my[i+1]))   
        draw.polygon(fenetre, (0,0,64,255), [(mx[i],my[i]), (mx[i+1],my[i+1]), (mx[i+1],my[i+1]+mz[i+1]), (mx[i],my[i]+mz[i]) ], 0)
    # ---------------------------------------------------------------- DESSINE LA BASE
    draw.line(fenetre, ROUGE,(mx[BASE-1],my[BASE-1]),(mx[BASE],my[BASE]),3)  

    # ---------------------------------------------------------------- AFFICHE LES INFOS DU JEU
    txt = MESSAGE
    if MESSAGE == AUCUN:
        txt='ESSENCE %3d     ALTITUDE %3d     VERT VITESSE %3d     HORZ VITESSE %3d'%(ESSENCE,ALT-y,V_CHUTE,V_DECAL)
        
    text=ECRITURE.render(txt,0,GRIS)
    fenetre.blit(text,(0,ALT-12))

    # ---------------------------------------------------------------- AFFICHE A L'ECRAN LE RESULTAT
    display.flip()
    horloge.tick(5)
    
pygame.quit()