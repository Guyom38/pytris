
from JEU_Pylander.variables import *
import JEU_Pylander.variables as VAR

import math, random

class CDecors:
    def __init__(self, m):
        self.M = m
        self.mx = []
        self.my = []

    def creation_du_relief(self):                   # ---------------------------------------------------------------- CREATION DU RELIEF
        ref = random.randint(0, VAR.altitude)
        for i in range(VAR.nombre_decors + 1):
            self.mx.append(VAR.pas * i)
            self.my.append(int(random.randint(-self.M.max_altitude, 0)+(VAR.altitude / 5) * (4 - math.sin((i+ (ref)) /5.)))-(VAR.altitude / 32))

    def installation_de_la_base(self):              # ---------------------------------------------------------------- INSTALLATION DE LA base
        self.mx.append(VAR.altitude)
        self.my.append(random.randint(VAR.altitude - self.M.max_altitude, VAR.altitude))
        self.mx[self.M.base] = self.mx[self.M.base -1] + self.M.longueur_base
        self.my[self.M.base] = self.my[self.M.base -1]

   