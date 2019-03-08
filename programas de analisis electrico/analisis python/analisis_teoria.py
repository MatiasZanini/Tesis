# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:02:41 2018

@author: Mati
"""

import matplotlib.pyplot as plt
import numpy as np
import funciones_teoria as fteo
from importlib import reload
from decimal import Decimal
from scipy import interpolate
import scipy.integrate as integrate
import scipy.constants as ctes

#%%

reload(fteo)

#%%
   
dielectrico = 'pvc'

vac = 14e3 /2 # voltaje instantaneo del electrodo activo en volts

vdc = -9.02e3 # voltaje de continua de la malla en volts

r= 113e-3 /2 # posición radial en la que se desea evaluar el campo electrico.


campo, cargas, capacidad = fteo.campo(r, vac, vdc, dielectrico, entero = True)


print('q1, q2 en Coulombs: ', cargas)

'%.2E' % Decimal(campo)

print('Campo electrico en la posicion r en Volt/m: ', '%.3E' % Decimal(campo))

print('Matriz de capacidad en picofaradios:', capacidad)



#%%

#----------------------------capacidad completa----------------------------------

c11 = capacidad[0][0]

c12 = capacidad[0][1]

c21 = capacidad[1][0]

c22 = capacidad[1][1]

c13 = -c11 -c12  #se usa la propiedad de que la suma de filas y columnas debe dar 0.

c23 = -c21 - c22

c33 = -c13 - c23

capacidad_total = np.array([[c11, c12, c13], [c21, c22, c23], [c13, c23, c33]])

print(capacidad_total)



#%% -------------------------------------------EFICIENCIA TEORICA-------------------------------------------------

#NOTA IMPORTANTE: es importante correr primero la seccion de acondicionamiento de señales en analisis.py para definir idbd, istr y volt
#para evitar esto, despues se puede pasar esto a analisis_teoria.py y llamar a las funciones de este modulo desde analisis_teoria.py.


#%% ---------------------------------INTERPOLACION DE G----------------------------------------------------------
        
        
EN, mob, k_excit, k_disoc  = np.loadtxt(r'C:\Users\Mati\Documents\GitHub\Tesis\Mediciones\Bolsig\20190227\NO\params_NO_100pts.txt', unpack=True)
    
G_excit = k_excit/((EN*1e-21)**2 * mob)*100    #en 1/V

G_disoc = k_disoc/((EN*1e-21)**2 * mob)*100    #en 1/V


#G_excit_params = interpolate.splrep(EN, G_excit, s=0)
#
#G_disoc_params = interpolate.splrep(EN, G_disoc, s=0)

G_excit_suave = interpolate.interp1d(EN*1e-21, G_excit)

G_disoc_suave = interpolate.interp1d(EN*1e-21, G_disoc)


EN_suave = np.arange(1,1000, 0.1)*1e-21

#G_excit_suave = interpolate.splev(EN_suave, G_excit_params, der = 0)
#
#G_disoc_suave = interpolate.splev(EN_suave, G_disoc_params, der = 0)



plt.figure()

plt.semilogy(EN_suave*1e21, G_excit_suave(EN_suave), linewidth=3, label='G(excitación)')    

plt.semilogy(EN_suave*1e21, G_disoc_suave(EN_suave), linewidth=3, linestyle='--', label= 'G(disociación)')

plt.xlabel('E/N (Td)', fontsize= 20)

plt.ylabel('G', fontsize= 20)

plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)
plt.legend(fontsize = 15)
plt.grid(axis='y')   
    


#%%------------------------------------------------CONTRIBUCION CUERPO-----------------------------------------------
N=2.69e25 #en 1/m^3

vdc=-9.02e3

nNO = 510e-6 * N 

Q = np.mean(caudal) * 10e-3/3600

dielectrico = 'pvc'



#iper=2500   #si se trabaja con ventana descomentar esto.


numerador = 0


puntos_interpol = 40

rmin = 72e-3 /2
rmax = 113.9e-3 /2


r_interpol = np.linspace(rmin, rmax, puntos_interpol)

for j in range(iper):

    if istr_aux[j] > 0:
    
    
        volt_inst = volt[j]
        
        E_inst = np.array([])
        
        for l in range(puntos_interpol):
                    
            E_inst = np.append(E_inst, fteo.campo(r_interpol[l], volt_inst, vdc, dielectrico)[0])
            
        
        E_interpol = interpolate.interp1d(r_interpol, E_inst)
            
        def integrando_cuerpo(r):
        
            #N = 2.45e25
        
            E = abs(E_interpol(r)) 
        
            I = E*(2*G_disoc_suave(E/N) + G_excit_suave(E/N))
        
            return I
            
        
        numerador += istr_aux[j] * integrate.quad(integrando_cuerpo, rmin, rmax)[0]
    
    print(j,numerador)

efic_cuerpo = (numerador/(iper+1)) / (100 * ctes.e * Q * nNO)

print('Aporte a la eficiencia del cuerpo en %:' , efic_cuerpo*100)
    

#%% ---------------------------------------------CONTRIBUCION CABEZA----------------------------------------------

N=2.69e25 #en 1/m^3

def Eh(r):

    Ehmax = 120e3/1e-2 # en V/m
    
    rhmax = 9e-4 # en m 

    return Ehmax * rhmax**2 / r**2



def integrando_cabeza(r):
    
    return (2*G_disoc_suave(Eh(r)/(2.69e25)) + G_excit_suave(Eh(r)/(2.69e25)) )*Eh(r)

# 

def efic_cabeza(istr_media, Np, Q):
    
    denom = 100 * ctes.e * Q * Np
    
    return istr_media * (integrate.quad(integrando_cabeza, 9e-4, 19e-3, limit=100))[0] / denom


i_media = cor_media_istr[0]

nNO = 510e-6 * N

Q = np.mean(caudal)*1e-3/ 3600

efic_cabeza_teo = efic_cabeza(i_media, nNO, Q)

print('Aporte a la eficiencia de la cabeza en %:', efic_cabeza_teo*100)
    
#%%------------------------------------Eh vs r----------------------------------------------------------------------------    

dielectrico = 'pvc'

vdc=-9.02*1e3
    
hay_streamer = 364

no_streamer = 150

rmin = 72e-3 /2
rmax = 113.9e-3 /2

puntos = 100

r_dom = np.linspace(rmin, rmax, puntos)


E_str = np.array([])

E_nostr = np.array([])



for k in range(len(r_dom)):

    E_str = np.append(E_str, fteo.campo(r_dom[k], volt[hay_streamer], vdc, dielectrico)[0])

E_str_interpol = interpolate.interp1d(r_dom, E_str)    


for m in range(len(r_dom)):

    E_nostr = np.append(E_nostr, fteo.campo(r_dom[m], volt[no_streamer], vdc, dielectrico)[0])

E_nostr_interpol = interpolate.interp1d(r_dom, E_nostr) 


plt.figure()

plt.plot((r_dom-rmin)*1e2, E_str_interpol(r_dom)*1e-3/1e2, linewidth = 3, label='Se detecta experimentalmente un streamer') 

plt.plot((r_dom-rmin)*1e2, E_nostr_interpol(r_dom)*1e-3/1e2, linewidth = 3, linestyle= '--', label='No se detecta ningún streamer')
    
plt.xlabel('r (cm)', fontsize=20)
plt.ylabel('E (kV/cm)', fontsize=20)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)
plt.legend(fontsize = 15)
plt.grid(True) 
   
    
    





#%%

#esta cuenta es para hallar el máximo r para el cual vamos a integrar el campo de la cabeza
#del streamer. Esto es porque, si bien la integral es hasta infinito, cae rapidamente. Y al
#irnos a un valor muy chico de campo reducido, nos vamos fuera del rango donde está 
#interpolada la G. Entonces truncamos hasta ese r la integral y listo.

rmax = 9e-4
Eredmax = Eh(9e-4)*1e21/N

while Eredmax>1:
    rmax += 1e-4
    Eredmax = Eh(rmax)*1e21/N
    
print('maximo r para integrar=', rmax) 

#El rmax elegido es 19e-3


#%%-------------------------------------------ANALISIS PARA EL CO-------------------------------------------------


EN_co, mob_co, k_disoc_N2, k_disoc_CO, k_disoc_H2O = np.loadtxt(r'C:\Users\Mati\Documents\GitHub\Tesis\Mediciones\Bolsig\20190227\CO\params_CO_100pts.txt', unpack=True)


G_disoc_N2 = k_disoc_N2/((EN_co*1e-21)**2 * mob_co)*100    #en 1/V

G_disoc_CO = k_disoc_CO/((EN_co*1e-21)**2 * mob_co)*100    #en 1/V

G_disoc_H2O = k_disoc_H2O/((EN_co*1e-21)**2 * mob_co)*100    #en 1/V




G_disoc_N2_suave = interpolate.interp1d(EN_co*1e-21, G_disoc_N2)

G_disoc_CO_suave = interpolate.interp1d(EN_co*1e-21, G_disoc_CO)

G_disoc_H2O_suave = interpolate.interp1d(EN_co*1e-21, G_disoc_H2O)


EN_co_suave = np.arange(1,1000, 0.1)*1e-21




plt.semilogy(EN_co_suave*1e21, G_disoc_N2_suave(EN_co_suave), linewidth = 2, label='G(Recombinación)')    

plt.semilogy(EN_co_suave*1e21, G_disoc_CO_suave(EN_co_suave), linewidth = 2, linestyle= '--', label='G(Disociación CO)') 

plt.semilogy(EN_co_suave*1e21, G_disoc_H2O_suave(EN_co_suave), linewidth = 2, linestyle= '-.', label='G(Oxidación)') 

plt.xlabel('E/N (Td)', fontsize=20)

plt.ylabel('G', fontsize=20)

plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)
plt.legend(fontsize = 15)
plt.grid(axis='y')   


#%%------------------------------------------------CONTRIBUCION CUERPO-----------------------------------------------
N=2.69e25 #en 1/m^3

vdc=-9.02e3

nCO = 350e-6 * N 

nH2O = 10e-6 * N





Q = np.mean(caudal) * 10e-3/3600








numerador = 0


puntos_interpol = 40

rmin = 72e-3 /2
rmax = 113.9e-3 /2


r_interpol = np.linspace(rmin, rmax, puntos_interpol)

for j in range(iper):

    if istr_aux[j] > 0:
    
    
        volt_inst = volt[j]
        
        E_inst = np.array([])
        
        for l in range(puntos_interpol):
                    
            E_inst = np.append(E_inst, fteo.campo(r_interpol[l], volt_inst, vdc,'pvc')[0])
            
        
        E_interpol = interpolate.interp1d(r_interpol, E_inst)
            
        def integrando_cuerpo(r):
        
            #N = 2.45e25
        
            E = abs(E_interpol(r)) 
        
            I = E*(nCO/N * G_disoc_CO_suave(E/N) + 0.5 * nH2O/N * G_disoc_H2O_suave(E/N) + 0.7 * G_disoc_N2_suave(E/N))
        
            return I
            
        
        numerador += istr_aux[j] * integrate.quad(integrando_cuerpo, rmin, rmax)[0]
    
    print(j,numerador)

efic_cuerpo = (numerador/(iper+1)) / (100 * ctes.e * Q * nCO)

print('La eficiencia porcentual predicha por el modelo es:', efic_cuerpo*100)
    

#%% ---------------------------------------------CONTRIBUCION CABEZA----------------------------------------------

N=2.69e25 #en 1/m^3

vdc=-9.02e3

nCO = 350e-6 * N 

nH2O = 10e-6 * N

def Eh(r):

    Ehmax = 120e3/1e-2 # en V/m
    
    rhmax = 9e-4 # en m 

    return Ehmax * rhmax**2 / r**2



def integrando_cabeza_co(r):
    
    return ( nCO/N * G_disoc_CO_suave(Eh(r)/N) + 0.5 * nH2O/N * G_disoc_H2O_suave(Eh(r)/N) +  0.7 * G_disoc_N2_suave(Eh(r)/N) )*Eh(r)

#    

def efic_cuerpo(istr_media, Np, Q):
    
    denom = 100 * ctes.e * Q * Np
    
    return istr_media * (integrate.quad(integrando_cabeza_co, 9e-4, 19e-3, limit=200))[0] / denom


i_media = cor_media_istr

nCO = 350e-6 * N

Q = np.mean(caudal)*1e-3/ 3600

efic_cuerpo_teo = efic_cuerpo(i_media, nCO, Q)

print('Aporte a la eficiencia porcentual de la cabeza en %:', efic_cuerpo_teo*100)













    
  