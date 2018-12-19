# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:02:41 2018

@author: Matías
"""

import matplotlib.pyplot as plt
import numpy as np
import funciones_teoria as fteo
from importlib import reload
from decimal import Decimal


#%%

   
dielectrico = 'pvc'

vac = 14e3 /2 # voltaje instantaneo del electrodo activo en volts

vdc = -9.02e3 # voltaje de continua de la malla en volts

r= 3.3e-2 # posición radial en la que se desea evaluar el campo electrico.


campo, cargas, capacidad = fteo.campo(r, vac, vdc, dielectrico)


print('q1, q2 en Coulombs: ', cargas)

'%.2E' % Decimal(campo)

print('Campo electrico en la posicion r en Volt/m: ', '%.3E' % Decimal(campo))

print('Matriz de capacidad en faradios:', capacidad)



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



#%%

#------------------------------Cargar datos del Bolsig---------------------------------


signal = np.loadtxt(r"C:\Users\Matías\Documents\GitHub\Tesis\Mediciones\mobility2.txt", delimiter = '\t', unpack = True)












#nota: para interpolar la funcion G hay que usar el scipy con interpolate por spline.






    
  