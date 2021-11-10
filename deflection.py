from math import *


class LaserSource:    
    def __init__(self, name = str()):    
        self.name = name
        
    def deltaSource(self, par = dict()):
        alpha = par['laser']['alpha']
        power = par['laser']['power']
        self.g = alpha * power / erf(sqrt(2))
        
    def gaussSource(self, par = dict()):
        pass

def runCalculation(x0, laser, par):
    ##-- shorten the symbol
    k1, k2  = par['mat']['k1'], par['mat']['k2']
    t1, t2  = par['geo']['t1'], par['geo']['t2']
    w, L    = par['geo']['w'], par['geo']['L']
    h = par['mat']['h']
    E1, E2  = par['mat']['E1'], par['mat']['E2']
    gam1, gam2 = par['mat']['gam1'], par['mat']['gam2']
    
    ##-- pre-computing    
    demon = k1 * t1 + k2 * t2
    m2 = (2 * h) / demon
    mm = sqrt(m2)
    rat = h * (t1 + t2) / (mm * demon)
    x0 = x0*L
    rt = t1/t2
    K = 4.0 + 6.0 * rt + 4.0 * rt * rt + (E1 / E2) * rt * rt * rt + (E2 / E1) * (1 / rt)
    N = (6.0 * (gam1 - gam2) * (t1 + t2)) / (t2 * t2 * K) 
    
    ##-- find coefficients
    C = -(1 / mm) * sinh(mm * x0)
    D = -((sinh(mm * L) + rat * cosh(mm * L)) /(cosh(mm * L) + rat * sinh(mm * L))) * C    
    B = (cosh(mm * x0) / sinh(mm * x0)) * C + D
    eta = B * (1 - cosh(mm * x0)) + C * sinh(mm * x0) + D * cosh(mm * x0)
    zeta = (B-D) * (x0*cosh(mm*x0) - sinh(mm * x0) / mm) + C * (cosh(mm * x0)/mm - x0*sinh(mm*x0))    
    ##-- temperature distribution
    genEn = laser.g / (w * demon)    
    Tx = list()
    Zx = list()
    dx = 0.01
    xnor = 0.0
    while xnor <= 1.0:
        x   = xnor*L
        tem, w = 0.0, 0.0
        if x < x0:
            tem = - genEn * B * sinh (mm * x)
            w   = (N * B * genEn / mm) * (x - sinh(mm * x) / mm)
        else:
            tem = - genEn * (C * cosh (mm * x) + D * sinh (mm * x))
            w = (N * genEn / mm) * (eta * x + zeta - (1/ mm) * (C * cosh(mm * x) + D * sinh(mm * x)))
        tempPoint = (xnor,tem)
        wPoint = (xnor, w)
        Tx.append(tempPoint)  
        Zx.append(wPoint)
        xnor += dx            
    return Tx, Zx