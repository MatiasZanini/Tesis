# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 15:33:17 2018

@author: Matías
"""

from datetime import datetime as dt
from scipy.optimize import curve_fit as fit
import numpy as np
import matplotlib.pyplot as plt
import csv

#%%

def lapso(inicio,fin):    #devuelve la resta de tiempos en minutos. pide string del tipo hh:mm:ss
   
    format='%H:%M:%S'
    duracion= str(dt.strptime(fin,format)-dt.strptime(inicio,format))
    tiempos=duracion.split(':')
    
    hora=int(tiempos[0])*60
    minutos=int(tiempos[1])
    segundos=int(tiempos[2])/60
    
    mins=hora+minutos+segundos
    return(mins)
    
    
#%%------------------------------Ploteo---------------------------------------------
def ploteo(gas,duracion,nombre):  
    
    
    puntos=len(gas)
    
    tiempo=np.linspace(0,duracion,puntos)
    plt.plot(tiempo,gas)
    
    plt.xlabel('Tiempo (m)')
    plt.ylabel('Concentración de '+ nombre+ ' (ppm)')
    plt.grid(True)
    
    
    
    
    
    
    
#%%
#---------------------------------------Acondicionamiento de la medicion---------------------------------------------

def acondic(path,fdbd=1/50,fstr=1/50):
    matriz=[]
    volt=np.array([]) #en volts
    t_volt=np.array([]) #en segundos
    istr=np.array([]) #en amper
    t_istr=np.array([]) #en segundos
    idbd=np.array([]) #en amper
    t_idbd=np.array([]) #en segundos
    
    
    with open(path) as csvfile:
        reader = csv.reader(csvfile) # change contents to floats
        for row in reader: # cada fila es una lista
            matriz.append(row)
    for i in range(len(matriz)):
        arr=np.asarray(matriz[i])
        t_volt=np.append(t_volt,float(arr[3]))
        volt=np.append(volt,float(arr[4]))
        t_idbd=np.append(t_idbd,float(arr[9]))
        idbd=np.append(idbd,float(arr[10]))
        t_istr=np.append(t_istr,float(arr[15]))
        istr=np.append(istr,float(arr[16]))
        
    return t_volt, volt, t_idbd, idbd, t_istr, istr
    


    
    
#%%
    
#def recortar_corriente(corr,volt,niter=30):
    
    
#def potencia

#en el programa de analisis, no hace falta llamar a recortar. Que potencia ya llame a recortar y listo.    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
