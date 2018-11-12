# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 12:38:02 2018

@author: Matías
"""

import csv
#import sys
import matplotlib.pyplot as plt
import numpy as np
import funciones as func
from importlib import reload

#%%  ---------------------Recargar el modulo con las funciones----------

reload(func)

#%%

#------------------------------ CONCENTRACION DE GASES-------------------------


csv.register_dialect('pycoma', delimiter=';')

#datos = open(r'C:\Users\Matías\Documents\GitHub\Tesis\20180928\Concentracion NO.csv', 'rt')

matriz=[]
NO=np.array([]) #en PPM
NO2=np.array([]) #en PPM
CO=np.array([]) #en PPM
NOx=np.array([]) #en PPM
caudal=np.array([]) #en l/h
#arrcomp=[]

with open(r"C:\Users\Matías\Documents\GitHub\Tesis\Mediciones\20181109\Concentracion NO.csv") as csvfile:
    reader = csv.reader(csvfile,dialect='pycoma', quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    for row in reader: # cada fila es una lista
        matriz.append(row)
     
    
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
            

ti=matriz[2][0].split(' ')[1]                #encuentra el tiempo inicial en formato stirng
tf=matriz[len(matriz)-1][0].split(' ')[1]    #encuentra el tiempo final en formato string

duracion=func.lapso(ti,tf)


print('duración de la medición total:',duracion,'minutos')


            
#%%
#--------------------------------------------PLOTEAR CONCENTRACION------------------------------------

#la funcion pide el array con la medicion, la duracion total y 
#el nombre que se quiera en el label 

func.ploteo_concentracion(NO,duracion,'NO')

#%%----------------CARGA LOS DATOS DE POTENCIA MEDIDOS Y LOS GRAFICA------------------------------------------------------


# Ploteo de las mediciones crudas y carga de datos
path=r"C:\Users\Matías\Documents\GitHub\Tesis\Mediciones\20181109\Trafo gas 1.csv"  #ingresar el path de la medicion electrica

t_volt, volt, t_idbd, idbd, t_istr, istr = func.acondic(path)

plt.subplot(3,1,1)
plt.plot(t_volt*1000,volt)
plt.xlabel('tiempo (ms)')
plt.ylabel('Voltaje entrada (V)')
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(t_idbd*1000,idbd*1000,'.-')
plt.xlabel('tiempo (ms)')
plt.ylabel('Corriente de DBD (mA)')
plt.grid(True)

plt.subplot(3,1,3)
plt.plot(t_istr*1000,istr*1000, '.-')
plt.xlabel('tiempo (ms)')
plt.ylabel('Corriente de streamers (mA)')
plt.grid(True)


#%% ------------------------------PREVISUALIZACION DE LAS POTENCIAS-------------------------
cant_periodos=6

tolerancia_picos= 1 # si es >1 aumentara la cantidad de picos reconocidos como streamers, si es <1 los mas chicos se eliminaran.

fuente_continua= -9.02 #en kV

alta_frecuencia=False #si es una medicion de alta frecuencia poner True, o False de lo contrario.

iper, tper = func.calculo_per(cant_periodos, t_volt, volt) #calcula la cantidad de elementos en un periodo y su duracion

potencia_istr, cor_media_istr, istr_aux = func.potencia(t_istr, istr, volt, cant_periodos, altafrec=alta_frecuencia,  v_dc_in=fuente_continua*1000 , tolerancia_corte=tolerancia_picos)

print('Potencia media de streamers en W:', potencia_istr)
print('Corriente media de streamers en mA:', cor_media_istr*1000)

plt.plot(t_istr[:iper]*1000,istr_aux[:iper]*1000)
plt.xlabel('tiempo (ms)')
plt.ylabel('Corriente de streamers (mA)')
plt.grid()


#%%
iper, tper = func.calculo_per(cant_periodos, t_volt, volt) #calcula la cantidad de elementos en un periodo y su duracion

tolerancia_picos= 1  # si es >1 aumentara la cantidad de picos reconocidos como streamers, si es <1 los mas chicos se eliminaran.

potencia_idbd, cor_media_idbd, idbd_aux = func.potencia(t_idbd, idbd,volt,cant_periodos, v_dc_in=fuente_continua*1000, altafrec=alta_frecuencia, streamer=False , tolerancia_corte=tolerancia_picos)

print('Potencia media de DBD en W:', potencia_idbd)
print('Corriente media de DBD en mA:', cor_media_idbd*1000)

plt.plot(t_istr[:iper]*1000,idbd_aux[:iper]*1000)
plt.xlabel('tiempo (ms)')
plt.ylabel('Corriente de DBD (mA)')
plt.grid()











#%%---------------------------POTENCIA PROMEDIADA ENTRE VARIAS MEDICIONES-----------------

cant_per_iter=6 #cantidad de periodos que hay en la medicion "a ojo"

voltaje_continua = -9.02 #indicar voltaje de la fuente externa en kilovolts

alta_frec = False  # indicar si se trata de una medicion de alta frecuencia (True) o baja (False).

tolerancia_corte_str= 1  # si es >1 aumentara la cantidad de picos reconocidos como streamers, si es <1 los mas chicos se eliminaran.

tolerancia_corte_dbd= 1

path = r"C:\Users\Matías\Documents\GitHub\Tesis\Mediciones\20181109"

subpath= 'Trafo gas '  #indicar nombre generico de las mediciones

inicio_med = 1 # indicar primer numero de la tira de mediciones

fin_med = 6 # indicar ultimo numero de la tira de mediciones

    
potencia_istr, potencia_idbd, cor_media_istr, cor_media_idbd = func.potencia_prom(cant_per_iter, voltaje_continua, alta_frec, tolerancia_corte_str, tolerancia_corte_dbd, path, subpath, inicio_med, fin_med)

print('Potencia media de streamers en W:', potencia_istr)
print('Corriente media de streamers en mA:', cor_media_istr*1000)

print('Potencia media de DBD en W:', potencia_idbd)
print('Corriente media de DBD en mA:', cor_media_idbd*1000)






#%%

#------------------- ------CÁLCULO DE EFICIENCIA EXPERIMENTAL-------------------------

#dado que este mismo analisis se hace para cualquier gas, hay que meter todo esto
#en una funcion que pida: gas, potencia, duracion, tiempo de inicio y fin.


potencia_final= potencia_idbd + potencia_istr #en watts

inicio=9 #poner el minuto en que se encendió la descarga

fin=19  #poner el minuto en que finalizó la descarga

efic_porcentual, efic_ener = func.eficiencia(duracion, NO, caudal, potencia_final, inicio, fin)

print('eficiencia porcentual:', efic_porcentual, '%')
print('eficiencia por potencia:',efic_ener,'mol/(kW H)')







            
        



#%%

#LEER UN ARCHIVO CSV
csv.register_dialect('pycoma', delimiter=';')

f = open(r'C:\Users\Matías\Documents\GitHub\Tesis\20181016(Jorge)\reactor jorge.csv', 'rt')
try:
    #reader = csv.reader(f,dialect='pycoma') #si no se pone el dialect es ',' por defecto
    reader = csv.reader(f)
    for row in reader:
        print(row)
finally:
    f.close()

#%%
    
#medicion de Jorge
matriz=[]
with open(r'C:\Users\Matías\Documents\GitHub\Tesis\20181016(Jorge)\reactor jorge.csv') as csvfile:
        reader = csv.reader(csvfile) # change contents to floats
        for row in reader: # cada fila es una lista
            matriz.append(row)
            
            
volt=np.array([]) #en volts
t_volt=np.array([]) #en segundos
istr=np.array([]) #en amper
t_istr=np.array([]) #en segundos
idbd=np.array([]) #en amper
t_idbd=np.array([]) #en segundos

for i in range(len(matriz)):
        arr=np.asarray(matriz[i])
        t_volt= np.append(t_volt, float(arr[0]))
        volt = np.append(volt, float(arr[2]))
        t_idbd= np.append(t_volt, float(arr[0]))
        idbd = np.append(idbd, float(arr[3]))
        t_istr= np.append(t_volt, float(arr[0]))
        istr = np.append(istr, float(arr[1]))
        
idbd=np.append(idbd,0)
istr=np.append(istr,0)
volt=np.append(volt,0)
t_volt=np.append(t_volt,0)

#%%

#Probar la funcion recortar

fit, rec =func.recortar_corriente(t_istr,istr,tper,niter=100) #guarda la funcion recortada y su fiteo

plt.subplot(1,2,1)
plt.plot(t_istr,istr*1000)
plt.plot(t_istr,fit*1000)
plt.xlabel('tiempo (s)')
plt.ylabel('corriente (mA)')

plt.subplot(1,2,2)
plt.plot(t_istr,(istr-fit)*1000)

plt.xlabel('tiempo (s)')
plt.ylabel('corriente (mA)')























