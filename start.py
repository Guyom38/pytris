import COMMUN.commun as C
import COMMUN.variables as V

import JEU_Pytris.pytris as PT
import JEU_Pylander.pylander as PL

if __name__ == '__main__':       
    commun = C.CCommun("Pytris") 
    commun.Salon.boucle()
    
    if V.boucle:
        pytris = PT.CPyTris(commun)
        pytris.boucle()

    #pylander = PL.pylander(commun)
    #pylander.boucle()