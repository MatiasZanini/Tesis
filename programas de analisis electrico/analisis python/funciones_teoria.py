# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:21:28 2018

@author: Matías
"""

import scipy.special as special
import scipy.integrate as integrate
import scipy.constants as ctes
import numpy as np

#%%

# Integral util para el calculo del potencial en el electrodo. r y z son los puntos donde se 
# evalua el campo (cilindricas) y zd es la posicion axial del anillo conductor. k es el numero de onda sobre el cual se integra.

def func_int_potencial(k, r, z, zd):
    
    r_cond = 1e-3 #radio del anillo conductor en metros.
    
    r_malla = 3e-3 #radio de la malla conductora externa en metros.
    
    f = special.i0(k*r_cond) * np.cos(k*(z-zd)) * (special.k0(k*r) - 
        special.i0(k *r)*special.k0(k*r_malla)/special.i0(k*r_malla))
    
    return f



def int_potencial(r, z, zd):
    
    return integrate.quad(func_int_potencial, 0, np.inf, args = (r, z, zd))[0]


def coef_potencial(r, z, er, zd1 = 0, zd2 = 1e-3):

# calcula los coeficientes del sistema de ecuaciones para hallar las cargas de cada electrodo    
    
    cte = 1/ (2*np.pi**2 * ctes.epsilon_0 * er)
    
    coef1 = int_potencial(r, z, zd1)
    
    coef2 = int_potencial(r, z, zd2)
    
    coefs = np.array([cte*coef1, cte*coef2])
    
    return coefs


#%%

ctes_diel = {'pvc': 3.2 , 'teflon': 2.1}
    
#sitema para hallar qd1 y qd2 en funcion de Vac


    
dielectrico = 'pvc'

r_cond = 1e-3 # radio del anillo conductor en metros

vac = 14e3 # voltaje pico a pico de alterna en volts.

zd1 = 0

zd2 = 1e-3 #distancia entre los conductores en metros

er = ctes_diel[dielectrico]
    
coefs1 = coef_potencial(r_cond, zd1, er)

coefs2 = coef_potencial(r_cond, zd2, er)

coefs = np.array([coefs1, coefs2])

voltajes = np.array([vac, 0])

cargas = np.linalg.solve(coefs, voltajes)

chequeo = np.allclose(np.dot(coefs, cargas), voltajes)

if chequeo:
    print('q1, q2 en coulombs:', cargas)
    
else:
    print('ERROR: El sistema no pudo resolverse')
    
    
#%%

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    