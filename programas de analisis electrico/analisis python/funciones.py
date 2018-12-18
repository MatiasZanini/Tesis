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
#devuelve un diccionario con los vectores del archivo csv. El archivo no debe contener mas columnas que las que se desea pasar a array.

def csv2arrays(path, fila_inicio = 0, pycoma = False):
    matriz=[]
    
    if pycoma:
        csv.register_dialect('pycoma', delimiter=';')
        with open(path) as csvfile:
            reader = csv.reader(csvfile,dialect='pycoma', quoting=csv.QUOTE_NONNUMERIC) # cambia todo a float
            for row in reader: # cada fila es una lista
                matriz.append(row)
    else:
        with open(path) as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # cambia todo a float
            for row in reader: # cada fila es una lista
                matriz.append(row)
    
    fila_fin = len(matriz) - 1 
    cant_vectores = len(matriz[fila_inicio])

    vectores = {}
    for x in range(cant_vectores):
        vectores["vector{0}".format(x)]= np.array([])
         
    
    for i in range(fila_inicio, fila_fin):
        for j in range(cant_vectores):
            vectores["vector{0}".format(j)]= np.append(vectores["vector{0}".format(j)], float(matriz[i][j]))
              
    return vectores



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
    plt.plot(tiempo,gas, linewidth = 3)
    plt.tick_params(axis = 'both', which = 'both', width = 2, length = 4, labelsize = 20)
    
    plt.xlabel('Tiempo (min)', fontsize = 20)
    plt.ylabel('Concentración de '+ nombre+ ' (ppm)', fontsize=20)
    plt.grid(axis = 'both', which = 'both', alpha = 0.8, linewidth = 2, linestyle = '--')
    
    
    
    
    
    
    
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
def pico_pico(senal):
    
    maximo = max(senal)
    minimo = min(senal)
    
    vpp = maximo - minimo
    
    return vpp



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
    
def recortar_corriente(t_corr,corr,tper, niter=30, altafrec_rec=True, atenuar_corte=1):
    
    indmax=indice_max(corr)
    cor_rec = np.copy(corr)
    if altafrec_rec:
        
        for k in range(niter):
        
            fiteada = fitear(funcaux, t_corr, cor_rec, ([tper,1,1,1]))   
            cor_rec=np.array([])
            
            datoscorte=np.array([])
           
            for i in range(-15,16):     #setea la tolerancia para diferenciar pico de ruido
                datoscorte=np.append(datoscorte,(corr[indmax+i]-fiteada[indmax+i]))
            corte=np.mean(datoscorte)/atenuar_corte
            
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
        corte=np.mean(datoscorte)/atenuar_corte
        
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

def potencia(t_pot, cor_pot, v_ac_in, cant_periodos, v_dc_in = (-9000), altafrec=True, streamer= True,tolerancia_corte=1):
    
    ind_per, t_per = calculo_per(cant_periodos, t_pot, v_ac_in)
    
    t_streamer = 1.2e-6 #duracion de un streamer en seg
    
    if altafrec:
        cor_pot_fit, cor_pot_rec = recortar_corriente(t_pot, cor_pot, t_per, niter=50, atenuar_corte=tolerancia_corte)
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
        #pot_avg = pot*t_streamer*0.5/t_per             #potencia media en W
        #cor_avg = cor_suma*t_streamer*0.5/t_per     #corriente promedio en A
    else:
        cor_aux = cor_pot - recortar_corriente(t_pot, cor_pot, t_per,niter=50, altafrec_rec=False, atenuar_corte=tolerancia_corte)
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
#        pot_avg = pot/ind_per             #potencia media en W
#        cor_avg = cor_suma/ind_per   #corriente promedio en A
        pot_avg = pot*t_streamer*0.5/t_per             #potencia media en W
        cor_avg = cor_suma*t_streamer*0.5/t_per     #corriente promedio en A
    


    return pot_avg, cor_avg, cor_aux

#%%
    
def eficiencia( duracion_med, concent_gas, caudal_gas, pot_total, inicio_desc, fin_desc,):

    t_efic = np.linspace(0,duracion_med,len(concent_gas))

    cuandoini=np.where(t_efic>=inicio_desc)[0][0] # índice donde comienza la descarga
        
    cuandofin=np.where(t_efic>=fin_desc)[0][0]#índice donde comienza la descarga
     
    ci= max(concent_gas[cuandoini:cuandofin]) #concentracion inicial en ppm
    cf= min(concent_gas[cuandoini:cuandofin]) #concentracion final en ppm
    
    efic_porcentual= (ci-cf)/ci *100 #eficiencia porcentual absoluta
    
    caudalprom=np.mean(caudal_gas[cuandoini:cuandofin])
    
    efic_energetica = (caudalprom*(ci-cf)*1e-3 * 0.0407)/pot_total #eficiencia relativa a la potencia

    return efic_porcentual, efic_energetica


#%%
    
def potencia_prom(cant_per_iter, voltaje_continua, alta_frec, tolerancia_corte_str, tolerancia_corte_dbd, path, subpath, inicio_med, fin_med):
    
    pot_istr_tot = np.array([])

    coravg_istr_tot = np.array([])
    
    pot_idbd_tot = np.array([])
    
    coravg_idbd_tot = np.array([])
    
    
    for i in range(inicio_med,fin_med+1):
        
        path_iter = path+'\{}{}.csv'.format(subpath, i)
        
        señales = acondic(path_iter) #Indices de señales: tvolt,volt,tidbd,idbd,tistr,istr
        
        pot_istr_i, coravg_istr_i = potencia(señales[4], señales[5],señales[1], cant_per_iter, v_dc_in = voltaje_continua*1000,altafrec=alta_frec, streamer= True, tolerancia_corte=tolerancia_corte_str)[:2]
        
        pot_istr_tot = np.append(pot_istr_tot, pot_istr_i)
        
        coravg_istr_tot = np.append(coravg_istr_tot, coravg_istr_i)
        
        pot_idbd_i, coravg_idbd_i = potencia(señales[2], señales[3],señales[1],cant_per_iter, v_dc_in = voltaje_continua*1000, altafrec=alta_frec, streamer= False, tolerancia_corte=tolerancia_corte_dbd)[:2]
        
        pot_idbd_tot = np.append(pot_idbd_tot, pot_idbd_i)
        
        coravg_idbd_tot = np.append(coravg_idbd_tot, coravg_idbd_i)
        
    potencia_istr = np.mean(pot_istr_tot)
    
    potencia_idbd = np.mean(pot_idbd_tot)
    
    cor_media_istr = np.mean(coravg_istr_tot)
    
    cor_media_idbd = np.mean(coravg_idbd_tot)
    
    return potencia_istr, potencia_idbd, cor_media_istr, cor_media_idbd




#%% ----------------calcula la potencia de mediciones con zoom en la zona de picos---------
    
def potencia_ventana(t_completo, v_completo, t_pot, cor_pot, v_ac_in, cant_periodos, v_dc_in = (-9000), altafrec=True, streamer= True,tolerancia_corte=1):

    ind_per, t_per = calculo_per(cant_periodos, t_completo, v_completo)

    if altafrec:
        cor_pot_fit, cor_pot_rec = recortar_corriente(t_pot, cor_pot, t_per, niter=80, atenuar_corte=tolerancia_corte)
        cor_aux = np.copy(cor_pot) - np.copy(cor_pot_fit)
        
        vmax = max(v_completo)
        vmin = min(v_completo)
            
        v_ac_med = 0 #(vmax+vmin)/2
        
        v_dc = v_ac_med-v_dc_in
        
        pot=0.0
        cor_suma=0.0
        
        ind_per = len(t_pot)-1
        
        if streamer:        
            for ind_pot in range(ind_per):

                pot += cor_aux[ind_pot]*(v_ac_in[ind_pot] - v_ac_med + v_dc)*0.5*(1+np.sign(cor_aux[ind_pot]))
                cor_suma += cor_pot[ind_pot]*0.5*(1+np.sign(cor_aux[ind_pot]))
        else:
            for ind_pot in range(ind_per):
                pot += cor_aux[ind_pot]*(v_ac_in[ind_pot] - v_ac_med + v_dc)
                cor_suma += cor_pot[ind_pot]
        pot_avg = pot/ind_per * (t_pot[len(t_pot)-1]-t_pot[0])/t_per            #potencia media en W
        cor_avg = cor_suma/ind_per* (t_pot[len(t_pot)-1]-t_pot[0])/t_per   #corriente promedio en A    
        
        
    else:
        cor_aux = cor_pot - recortar_corriente(t_pot, cor_pot, t_per,niter=50, altafrec_rec=False, atenuar_corte=tolerancia_corte)
        vmax = max(v_completo)
        vmin = min(v_completo)
            
        v_ac_med = (vmax+vmin)/2
        
        v_dc = v_ac_med-v_dc_in
        
        ind_per = len(t_pot)-1
        
        
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


        pot_avg = pot/ind_per * (t_pot[len(t_pot)-1]-t_pot[0])/t_per            #potencia media en W
        cor_avg = cor_suma/ind_per* (t_pot[len(t_pot)-1]-t_pot[0])/t_per   #corriente promedio en A
    


    return pot_avg, cor_avg, cor_aux



#%%

def derivada_num(x,y):
    
    largo_x = len(x)
    
    largo_y = len(y)
    
    if largo_x != largo_y:
        
        raise ValueError('Los vectores deben ser del mismo tamaño.')
    
    
    derivada = np.array([])
    
    
    for i in range(largo_x-2):
                   
        dx = x[i+1]-x[i]
        
        dy = y[i+1]-y[i]
        
        derivada = np.append(derivada, dy/dx)
            
    return derivada
                






    






#%%
    
#comentarios:

#cor_rec=np.copy(corr)   el comando np.copy copia la variable en el espacio de memoria, con lo cual no sobreescribe la original



#en el programa de analisis, no hace falta llamar a recortar. Que potencia ya llame a recortar y listo.    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
