from JEU_Pytris.pytris import *
import JEU_Pylander.pylander as PL

if __name__ == '__main__':       
    commun = CCommun("Pytris") 
    commun.Salon.boucle()
    
    #pytris = CPyTris(commun)
    #pytris.boucle()

    pylander = PL.pylander(commun)
    pylander.boucle()