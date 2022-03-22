from JEU_Pytris.pytris import *

if __name__ == '__main__':       
    commun = CCommun("Pytris") 
    commun.Salon.boucle()
    
    pytris = CPyTris(commun)
    pytris.jeu_PyTris()