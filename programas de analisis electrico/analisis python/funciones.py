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
def ploteo_concentracion(gas,duracion,nombre):  
    
    
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

#%%  ------------Indice del maximo o minimo de un vector--------------
    
def indice_max(vector_max):
    return int(np.mean(np.where(vector_max==max(vector_max))[0]))

def indice_min(vector_min):
    return int(np.mean(np.where(vector_min==min(vector_min))[0]))


#%% -Fitea una funcion a ciertos datos, y devuelve la funcion ajustada, evaluada en esos datos--------------
    

def fitear(funcion_aux, x_data, y_data, params_opt=None):
    
    if params_opt:
        fit_params, fit_covar = fit(funcion_aux, x_data, y_data, p0=params_opt)
    else:
        fit_params, fit_covar = fit(funcion_aux, x_data, y_data)
    
    cant_param = len(fit_params)
    params=np.array([])
    
    for ind_param in range(cant_param):
        params = np.append(params,fit_params[ind_param])
        
        
    return funcion_aux(x_data, *params)

    
    
#%%
    
def recortar_corriente(t_corr,corr,tper, niter=30):
    
    
    indmax=indice_max(corr)
    cor_rec = np.copy(corr)
    for k in range(niter):
    
        fiteada = fitear(funcaux, t_corr, cor_rec, ([tper,1,1,1]))   
        cor_rec=np.array([])
        
        datoscorte=np.array([])
       
        for i in range(-15,16):     #setea la tolerancia para diferenciar pico de ruido
            datoscorte=np.append(datoscorte,(corr[indmax+i]-fiteada[indmax+i]))
        corte=np.mean(datoscorte)/3
        
        for j in range(len(corr)):
            
            if abs(corr[j]-fiteada[j])>corte:
                cor_rec=np.append(cor_rec,fiteada[j])
            else:
                cor_rec=np.append(cor_rec,corr[j])
            
    
    return fitear(funcaux,t_corr,cor_rec,([tper,1,1,1])) , cor_rec
    

#%% ----------------------------------CALCULO DE LA POTENCIA--------------------------

def potencia(t_pot, cor_pot, v_ac_in, ind_per, t_per, v_dc_in = (-9000)):
    
    cor_pot_fit, cor_pot_rec = recortar_corriente(t_pot, cor_pot, t_per,niter=50)
    cor_aux = cor_pot - cor_pot_rec
    vmax = max(v_ac_in)
    vmin = min(v_ac_in)
        
    v_ac_med = (vmax+vmin)/2
    
    v_dc = v_ac_med-v_dc_in
    
    pot=0.0
    cor_suma=0.0
            
    for ind_pot in range(ind_per):
        pot += cor_aux[ind_pot]*(v_ac_in[ind_pot] - v_ac_med + v_dc)
        cor_suma += cor_pot[ind_pot]
    pot_avg = pot/ind_per             #potencia media en W
    cor_avg = cor_suma/ind_per   #corriente promedio en A
    


    return pot_avg, cor_avg, cor_aux


#%%
    
#comentarios:

#cor_rec=np.copy(corr)   el comando np.copy copia la variable en el espacio de memoria, con lo cual no sobreescribe la original



#en el programa de analisis, no hace falta llamar a recortar. Que potencia ya llame a recortar y listo.    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
