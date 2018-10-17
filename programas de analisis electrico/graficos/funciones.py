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
    volt_func=np.array([]) #en volts
    t_volt_func=np.array([]) #en segundos
    istr_func=np.array([]) #en amper
    t_istr_func=np.array([]) #en segundos
    idbd_func=np.array([]) #en amper
    t_idbd_func=np.array([]) #en segundos
    
    
    with open(path) as csvfile:
        reader = csv.reader(csvfile) # change contents to floats
        for row in reader: # cada fila es una lista
            matriz.append(row)
    for i in range(len(matriz)):
        arr=np.asarray(matriz[i])
        t_volt_func=np.append(t_volt_func,float(arr[3]))
        volt_func=np.append(volt_func,float(arr[4]))
        t_idbd_func=np.append(t_idbd_func,float(arr[9]))
        idbd_func=np.append(idbd_func,fdbd*float(arr[10]))
        t_istr_func=np.append(t_istr_func,float(arr[15]))
        istr_func=np.append(istr_func,fstr*float(arr[16]))
        
    return t_volt_func, volt_func, t_idbd_func, idbd_func, t_istr_func, istr_func
    

#%%
    
def funcaux(t,tper,b,c,d):
    return b*np.cos(2*np.pi/tper*t + c) + d
    
    
#%%
    
def recortar_corriente(t_corr,corr,tper):
    
        
    fiteada_param, fiteada_covar=fit(funcaux, t_corr,corr ,p0=([tper,1,1,1]))
    
    fiteada=funcaux(t_corr, fiteada_param[0], fiteada_param[1], fiteada_param[2], fiteada_param[3])
    
    indmax=int(np.mean(np.where(corr==max(corr))[0]))
    
    
    cor_rec=np.copy(corr)
    
    
    datoscorte=np.array([])
    for i in range(-15,16):
        datoscorte=np.append(datoscorte,(corr[indmax+i]-fiteada[indmax+i]))
    corte=np.mean(datoscorte)/3
    
    for j in range(len(corr)):
        
        if abs(corr[j]-fiteada[j])>corte:
            cor_rec[j]=fiteada[j]
            
    fiteada2_param, fiteada2_covar=fit(funcaux,t_corr,cor_rec,p0=([tper,1,1,1]))
    fiteada2=funcaux(t_corr, fiteada2_param[0], fiteada2_param[1], fiteada2_param[2], fiteada2_param[3])
    
    return fiteada2
    
#def potencia

#en el programa de analisis, no hace falta llamar a recortar. Que potencia ya llame a recortar y listo.    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
