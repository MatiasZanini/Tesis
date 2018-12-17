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


    
  