# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:21:28 2018

@author: Matías
"""

import scipy.special as special
import scipy.integrate as integrate
import scipy.constants as ctes
import scipy.misc as misc
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

#%%

# Integral util para el calculo del potencial en el electrodo. r y z son los puntos donde se 
# evalua el campo (cilindricas) y zd es la posicion axial del anillo conductor. k es el numero de onda sobre el cual se integra.

def func_int_potencial(k, r, z, zd, r_cond = 70e-3 /2, r_malla = 113.9e-3 /2):
    
    #r_cond radio del anillo conductor en metros.
    
    #r_malla radio de la malla conductora externa en metros.
    
    f = special.i0(k*r_cond) * np.cos(k*(z-zd)) * (special.k0(k*r) - 
        special.i0(k *r)*special.k0(k*r_malla)/special.i0(k*r_malla))
    
    return f



def int_potencial(r, z, zd):
    
    return integrate.quad(func_int_potencial, 1e-2, 10000, args = (r, z, zd))[0]


def coef_potencial(r, z, er, zd1 = 2.5e-3, zd2 = -2.5e-3):

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

def potencial(r, z, cargas, er, zd1 = 2.5e-3, zd2 = -2.5e-3):
    
    cte = 1/ (2*np.pi**2 * ctes.epsilon_0 * er)
    
    qd1, qd2 = cargas
    
    
    v = cte*(qd1*int_potencial(r, z , zd1) + qd2*int_potencial(r, z, zd2))
    
    return v

def campo(r, vac, vdc, permit, r_cond = 70e-3 /2, z0 = 2.5e-3, zd1 = 2.5e-3, zd2 = -2.5e-3, entero= True):
    
    if permit =='pvc' or permit =='teflon': 
    
                
        q1 = np.array([])
        
        q2 = np.array([])
        
        
        ctes_diel = {'pvc': 3.2 , 'teflon': 2.1}
        
        er = ctes_diel[permit]
        
        coefs1 = coef_potencial(r_cond, zd1, er)
        
#        print(coefs1)
    
        coefs2 = coef_potencial(r_cond, zd2, er)
        
#        print(coefs2)
        
        coefs = np.array([coefs1 , coefs2])
        
#        print(coefs)
      
        capacidad = np.linalg.inv(coefs) #coeficientes de capacidad (Q=C.V)
        
        
        if entero:
            
            voltajes = np.array([vac-vdc, -vdc])
        
   
            cargas_instant = np.dot(capacidad, voltajes)
            
            q1 = np.append(q1, cargas_instant[0])
            
            q2 = np.append(q2,cargas_instant[1]) 
            
        else:        
        
            ultimo_vac = len(vac) - 1
            for i in range(ultimo_vac):
            
                voltajes = np.array([vac[i]-vdc, -vdc])
            
       
                cargas_instant = np.dot(capacidad, voltajes)
                
                q1 = np.append(q1, cargas_instant[0])
                
                q2 = np.append(q2,cargas_instant[1])
        
#        print(cargas)
        
        cargas = np.array([q1,q2])
        
        
        E = -misc.derivative(potencial, r, dx = 1e-7, args=(z0, cargas, er))
    
        return E, cargas, capacidad*1e12 
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
        
#%% ---------------------------------INTERPOLACION DE G----------------------------------------------------------
        
        
EN, mob, k_excit, k_disoc  = np.loadtxt(r'C:\Users\Mati\Documents\GitHub\Tesis\Mediciones\Bolsig\NO\params_NO_100pts.txt', unpack=True)
    
G_excit = k_excit/((EN*1e-21)**2 * mob)*100    

G_disoc = k_disoc/((EN*1e-21)**2 * mob)*100


#G_excit_params = interpolate.splrep(EN, G_excit, s=0)
#
#G_disoc_params = interpolate.splrep(EN, G_disoc, s=0)

G_excit_suave = interpolate.interp1d(EN, G_excit)

G_disoc_suave = interpolate.interp1d(EN, G_disoc)


EN_suave = np.arange(1,1000, 0.1)

#G_excit_suave = interpolate.splev(EN_suave, G_excit_params, der = 0)
#
#G_disoc_suave = interpolate.splev(EN_suave, G_disoc_params, der = 0)





plt.semilogy(EN_suave, G_excit_suave(EN_suave), label='G(excitación)')    

plt.semilogy(EN_suave, G_disoc_suave(EN_suave), label= 'G(disociación)')

plt.xlabel('E/N (Td)')

plt.ylabel('G')

plt.legend()

plt.grid()    
    
#%% -------------------------------------------EFICIENCIA TEORICA-------------------------------------------------

#NOTA IMPORTANTE: es importante correr primero la seccion de acondicionamiento de señales en analisis.py para definir idbd, istr y volt
#para evitar esto, despues se puede pasar esto a analisis.py y llamar a las funciones de este modulo desde analisis.py.

i_tot = idbd + istr

vdc=-9.02e3

nNO = 500e-6

Q = np.mean(caudal)

def integrando_cuerpo(r, vac, vdc):
    
    #N = 2.45e25
    
    E = campo(r, vac, vdc, 'pvc')[0] 
    
    I = E*(2*G_disoc_suave(E/2.45 * 10e-4) + G_excit_suave(E/2.45 * 10e-4))
    
    return I


numerador = 0

for j in range(4*iper):

    numerador += i_tot[j] * integrate.quad(integrando_cuerpo, 70e-3 /2, 113.9e-3 /2, args = (volt[j], vdc))[0]
    

efic_cuerpo = (numerador/(4*iper-1)) / (100 * ctes.e * Q * nNO)
    
    
    
    
    
    
    
    
    