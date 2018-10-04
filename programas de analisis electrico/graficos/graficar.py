# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 12:38:02 2018

@author: Matías
"""

import csv
#import sys
import matplotlib.pyplot as plt
import numpy as np

#%%

csv.register_dialect('pycoma', delimiter=';') #PONER ACÁ EL DELIMITADOR DEL ARCHIVO



#%%

#LEER UN ARCHIVO CSV

f = open(r'C:\Users\Matías\Documents\GitHub\Tesis\20180928\Concentracion NO.csv', 'rt')
try:
    reader = csv.reader(f,dialect='pycoma') #si no se pone el dialect es ',' por defecto
    for row in reader:
        print(row)
finally:
    f.close()

#%%

#------------------------GRAFICAR CONCENTRACION DE GASES-------------------------


csv.register_dialect('pycoma', delimiter=';')

#datos = open(r'C:\Users\Matías\Documents\GitHub\Tesis\20180928\Concentracion NO.csv', 'rt')

matriz=[]
NO=np.array([]) #en PPM
NO2=np.array([]) #en PPM
CO=np.array([]) #en PPM
NOx=np.array([]) #en PPM
caudal=np.array([]) #en l/h
#arrcomp=[]

with open(r"C:\Users\Matías\Documents\GitHub\Tesis\20180928\Concentracion NO.csv") as csvfile:
    reader = csv.reader(csvfile,dialect='pycoma', quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # cada fila es una lista
        matriz.append(row)
        #arr=np.append(arr,np.asarray(row))
        #NO=np.append(NO,np.array(float(arr[1])))
    
    for i in range(len(matriz)-2):
        arr=np.asarray(matriz[i+2])
       # arrcomp.append(arr)
        control1=str.find(arr[1],'E-') #chequea que no aparezca el error de medicion 'E-algo'
        control2=str.find(arr[2],'E-')
        control3=str.find(arr[3],'E-')
        control4=str.find(arr[4],'E-')
        control5=str.find(arr[5],'E-')
        if control1 == -1 & control2 == -1 & control3 == -1 & control4 == -1 & control5==-1:
            NO=np.append(NO,float(arr[1]))
            NO2=np.append(NO2,float(arr[2]))
            CO=np.append(CO,float(arr[3]))
            NOx=np.append(NOx,float(arr[4]))
            caudal=np.append(caudal,float(arr[5]))
            
duracion= float(88.58)  #minutos

puntos=len(NO)



            
#%%
# PLOTEAR NO

duracionNO= float(88.58)  #minutos

puntosNO=len(NO)

tiempoNO=np.linspace(0,duracionNO,puntosNO)
plt.plot(tiempoNO,NO)

plt.xlabel('Tiempo (m)')
plt.ylabel('Concentración de NO (ppm)')
plt.grid(True)


#%%
 #PLOTEAR NO2

duracionNO2= float(88.58)  #minutos

puntosNO2=len(NO2)

tiempoNO2=np.linspace(0,duracionNO2,puntosNO2)
plt.plot(tiempoNO2,NO2)

plt.xlabel('Tiempo (m)')
plt.ylabel('Concentración de NO2 (ppm)')
plt.grid(True)


#%%

#PLOTEAR CO
 
duracionCO= float(88.58)  #minutos

puntosCO=len(CO)

tiempoCO=np.linspace(0,duracionCO,puntosCO)
plt.plot(tiempoCO,CO)

plt.xlabel('Tiempo (m)')
plt.ylabel('Concentración de CO (ppm)')
plt.grid(True)

 
 #%%
 
 #PLOTEAR NOX

duracionNOx= float(88.58)  #minutos

puntosNOx=len(NOx)

tiempoNOx=np.linspace(0,duracionNOx,puntosNOx)
plt.plot(tiempoNOx,NOx)

plt.xlabel('Tiempo (m)')
plt.ylabel('Concentración de NOx (ppm)')
plt.grid(True)


#%%

#------------------- ------CÁLCULO DE EFICIENCIA EXPERIMENTAL-------------------------


pot=60 #ingresar potencia en watts

inicio=67 #poner el minuto en que se encendió la descarga

donde=np.where(tiempoNO>=inicio)[0] # array cuyo primer valor es el índice donde comienza la descarga
inicio=tiempoNO[donde[0]] #tiempo de inicio medido por la máquina

ci= max(NO[donde[0]:(len(NO)-1)]) #concentracion inicial en ppm
cf= min(NO[donde[0]:(len(NO)-1)]) #concentracion final en ppm

efic_porcentual= (ci-cf)/ci *100 #eficiencia porcentual absoluta

caudalprom=np.mean(caudal)

efic = (caudalprom*(ci-cf)*1e-3 * 0.0407)/pot #eficiencia relativa a la potencia suministrada en mol/(kW H)









            
        





























