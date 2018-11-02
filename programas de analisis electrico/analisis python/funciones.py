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


#%%
def calculo_per(cant_per, t_volt, voltaje_per):    
    volt_rec = voltaje_per[0:(int((len(voltaje_per)/cant_per)+1))]
    indmax = indice_max(volt_rec)
    indmin = indice_min(volt_rec)
    
    iper = 2*abs(indmax-indmin)                       #cantidad de elementos en un periodo
    tper = 2*abs(t_volt[indmax]-t_volt[indmin])       #periodo en segundos
    
    return iper, tper


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
    
def recortar_corriente(t_corr,corr,tper, niter=30, altafrec_rec=True):
    
    indmax=indice_max(corr)
    cor_rec = np.copy(corr)
    if altafrec_rec:
        
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
    
    else:
        cor_rec=np.array([])
        datoscorte=np.array([])
           
        for i in range(-15,16):     #setea la tolerancia para diferenciar pico de ruido
            datoscorte = np.append(datoscorte,corr[indmax+i])
        corte=np.mean(datoscorte)
        
        for j in range(len(corr)):
            
            if abs(corr[j])>corte:
                cor_rec=np.append(cor_rec,0.0)
            else:
                cor_rec=np.append(cor_rec,corr[j])
            
    
        return cor_rec
    
    # Tener en cuenta que es  posible que haya que dividir el corte por 2 o 3 dependiendo
    #de la señal. Habría que ver una forma de relativizar el corte a partir de la amplitud
    #de la señal.

#%% ----------------------------------CALCULO DE LA POTENCIA--------------------------

def potencia(t_pot, cor_pot, v_ac_in, cant_periodos, v_dc_in = (-9000), altafrec=True, streamer= True):
    
    ind_per, t_per = calculo_per(cant_periodos, t_pot, v_ac_in)
    
    if altafrec:
        cor_pot_fit, cor_pot_rec = recortar_corriente(t_pot, cor_pot, t_per, niter=50)
        cor_aux = np.copy(cor_pot) - np.copy(cor_pot_rec)
        vmax = max(v_ac_in)
        vmin = min(v_ac_in)
            
        v_ac_med = (vmax+vmin)/2
        
        v_dc = v_ac_med-v_dc_in
        
        pot=0.0
        cor_suma=0.0
        if streamer:        
            for ind_pot in range(ind_per):
            
                pot += cor_aux[ind_pot]*(v_ac_in[ind_pot] - v_ac_med + v_dc)*0.5*(1+np.sign(cor_aux[ind_pot]))
                cor_suma += cor_pot[ind_pot]*0.5*(1+np.sign(cor_aux[ind_pot]))
        else:
            for ind_pot in range(ind_per):
                pot += cor_aux[ind_pot]*(v_ac_in[ind_pot] - v_ac_med + v_dc)
                cor_suma += cor_pot[ind_pot]
            
        pot_avg = pot/ind_per             #potencia media en W
        cor_avg = cor_suma/ind_per   #corriente promedio en A
    else:
        cor_aux = cor_pot - recortar_corriente(t_pot, cor_pot, t_per,niter=50, altafrec_rec=False)
        vmax = max(v_ac_in)
        vmin = min(v_ac_in)
            
        v_ac_med = (vmax+vmin)/2
        
        v_dc = v_ac_med-v_dc_in
        
        pot=0.0
        cor_suma=0.0
                
        if streamer:
            for ind_pot in range(ind_per):
                pot += cor_aux[ind_pot]*(v_ac_in[ind_pot] - v_ac_med + v_dc)*0.5*(1+np.sign(cor_aux[ind_pot]))
                cor_suma += cor_pot[ind_pot]*0.5*(1+np.sign(cor_aux[ind_pot]))
        else:
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
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
