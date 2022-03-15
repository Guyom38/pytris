
import pygame
from pygame.locals import *

import variables as VAR

class CPieces():
    pieces_couleurs = {}
    pieces_couleurs["O"] = (0, 0, 36)
    pieces_couleurs["I"] = (104, 107, 55)
    pieces_couleurs["S"] = (61,61,125)
    pieces_couleurs["Z"] = (107, 39, 71)
    pieces_couleurs["L"] = (18, 105, 232)
    pieces_couleurs["J"] = (98, 52, 15)
    pieces_couleurs["T"] = (0, 105, 0)

    pieces = {}
    pieces["O"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 0), \
                     (0, 1, 1, 0), \
                     (0, 0, 0, 0) )]

    pieces["I"] = [( (0, 0, 0, 0), \
                     (1, 1, 1, 1), \
                     (0, 0, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 0) )]

    pieces["S"] = [( (0, 0, 0, 0), \
                     (0, 0, 1, 1), \
                     (0, 1, 1, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 1), \
                     (0, 0, 0, 1), \
                     (0, 0, 0, 0) )]

    pieces["Z"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 0), \
                     (0, 0, 1, 1), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 0, 1), \
                     (0, 0, 1, 1), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) )]

    pieces["L"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 1), \
                     (0, 1, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 1), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 0, 1), \
                     (0, 1, 1, 1), \
                     (0, 0, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 1, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) )]

    pieces["J"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 1), \
                     (0, 0, 0, 1), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 1), \
                     (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 1, 0, 0), \
                     (0, 1, 1, 1), \
                     (0, 0, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 1, 1, 0), \
                     (0, 0, 0, 0) )]

    pieces["T"] = [( (0, 0, 0, 0), \
                     (0, 1, 1, 1), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 0, 1, 1), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 1, 1, 1), \
                     (0, 0, 0, 0), \
                     (0, 0, 0, 0) ), \
                   ( (0, 0, 1, 0), \
                     (0, 1, 1, 0), \
                     (0, 0, 1, 0), \
                     (0, 0, 0, 0) )]

