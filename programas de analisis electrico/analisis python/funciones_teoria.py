# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:21:28 2018

@author: Matías
"""

import scipy.special as special
import scipy.integrate as integrate
import scipy.constants as ctes
import scipy.misc as misc
import numpy as np
import matplotlib.pyplot as plt

#%%

# Integral util para el calculo del potencial en el electrodo. r y z son los puntos donde se 
# evalua el campo (cilindricas) y zd es la posicion axial del anillo conductor. k es el numero de onda sobre el cual se integra.

def func_int_potencial(k, r, z, zd, r_cond = 65e-3 /2, r_malla = 113.9e-3 /2):
    
    #r_cond radio del anillo conductor en metros.
    
    #r_malla radio de la malla conductora externa en metros.
    
    f = special.i0(k*r_cond) * np.cos(k*(z-zd)) * (special.k0(k*r) - 
        special.i0(k *r)*special.k0(k*r_malla)/special.i0(k*r_malla))
    
    return f



def int_potencial(r, z, zd):
    
    return integrate.quad(func_int_potencial, 1e-2, 10000, args = (r, z, zd))[0]


def coef_potencial(r, z, er, zd1 = 0, zd2 = 5e-3):

# calcula los coeficientes del sistema de ecuaciones para hallar las cargas de cada electrodo    
    
    cte = 1/ (2*np.pi**2 * ctes.epsilon_0 * er)
    
    coef1 = int_potencial(r, z, zd1)
    
    coef2 = int_potencial(r, z, zd2)
    
    coefs = np.array([cte*coef1, cte*coef2])
    
    return coefs


#%%

#ctes_diel = {'pvc': 3.2 , 'teflon': 2.1}
    
#sitema para hallar qd1 y qd2 en funcion de Vac


#    
#dielectrico = 'pvc'
#
#r_cond = 2e-2 # radio del anillo conductor en metros
#
#vac = 1 # en volts
#
#zd1 = 0 # posicion axial del electrodo activo en metros.
#
#zd2 = 5e-3 # posicion axial del electrodo a tierra en metros.
#
#er = ctes_diel[dielectrico]
#    
#coefs1 = coef_potencial(r_cond, zd1, er)
#
#coefs2 = coef_potencial(r_cond, zd2, er)
#
#coefs = np.array([coefs1, coefs2])
#
#voltajes = np.array([vac, 0])
#
#cargas = np.linalg.solve(coefs, voltajes)
#
#chequeo = np.allclose(np.dot(coefs, cargas), voltajes)
#
#if chequeo:
#    print('q1, q2 en coulombs:', cargas)
#    
#else:
#    print('ERROR: El sistema no pudo resolverse')
#    
    
    
    
    
    
    
    
    
    
    
#%%    

def potencial(r, z, vac, cargas, er, zd1 = 0, zd2 = 5e-3):
    
    cte = 1/ (2*np.pi**2 * ctes.epsilon_0 * er)
    
    qd1, qd2 = cargas
    
    
    v = cte*(qd1*int_potencial(r, z , zd1) + qd2*int_potencial(r, z, zd2))
    
    return v

def campo(r, vac, vdc, permit, r_cond = 65e-3 /2, z0 = 0, zd1 = 0, zd2 = 5e-3):
    
    if permit =='pvc' or permit =='teflon': 
    
        ctes_diel = {'pvc': 3.2 , 'teflon': 2.1}
        
        er = ctes_diel[permit]
        
        coefs1 = coef_potencial(r_cond, zd1, er)
        
        print(coefs1)
    
        coefs2 = coef_potencial(r_cond, zd2, er)
        
        print(coefs2)
        
        coefs = np.array([coefs1 , coefs2])
        
        print(coefs)
        
        voltajes = np.array([vac-vdc, -vdc])
        
        print(voltajes)
        
        capacidad = np.linalg.inv(coefs) #coeficientes de capacidad (Q=C.V)
        
        print(capacidad)
        
        cargas = np.dot(capacidad, voltajes)
        
        print(cargas)
        
        E = -misc.derivative(potencial, r, dx = 1e-7, args=(z0, vac, cargas, er))
    
        return E, cargas, capacidad
    else:
        
        raise ValueError('Dielectrico no reconocido')
    
    
    
#%% pruebas
    
#k = np.linspace(1e-6,1000,10000)
#
#a = func_int_potencial(k, 3e-2, 0, 1e-3)
#    
#plt.plot(a)    
#
#b0=integrate.quad(func_int_potencial, 1e-6, 1000, args=(3e-2,0,1e-3))[0]
#
#b= integrate.quad(func_int_potencial, 1e-6, 2000, args=(3e-2,0,1e-3))[0]
#
#print(b-b0)
#    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    