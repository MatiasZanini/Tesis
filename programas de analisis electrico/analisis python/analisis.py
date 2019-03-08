# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 12:38:02 2018

@author: Mati
"""

import csv
#import sys
import matplotlib.pyplot as plt
import numpy as np
import funciones as func
from importlib import reload
from scipy.signal import savgol_filter as smooth
import scipy.misc as misc

#%%  ---------------------Recargar el modulo con las funciones----------

reload(func)

#%%

#------------------------------ CONCENTRACION DE GASES-------------------------


csv.register_dialect('pycoma', delimiter=';')

#datos = open(r'C:\Users\Mati\Documents\GitHub\Tesis\20180928\Concentracion NO.csv', 'rt')

matriz=[]
NO=np.array([]) #en PPM
NO2=np.array([]) #en PPM
CO=np.array([]) #en PPM
NOx=np.array([]) #en PPM
caudal=np.array([]) #en l/h
#arrcomp=[]

with open(r"C:\Users\Mati\Documents\GitHub\Tesis\Mediciones\20181120\Concentracion NO.csv") as csvfile:
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

#NO=NO-40

plt.figure()

func.ploteo_concentracion(NO,duracion,'NO')


#%%----------------CARGA LOS DATOS DE POTENCIA MEDIDOS Y LOS GRAFICA------------------------------------------------------


# Ploteo de las mediciones crudas y carga de datos
path=r"C:\Users\Mati\Documents\GitHub\Tesis\Mediciones\20181120\Trafo gas ventana 2.csv"  #ingresar el path de la medicion electrica

t_volt, volt, t_idbd, idbd, t_istr, istr = func.acondic(path)

#istr = istr/10 # esto se descomenta en la medicion del  22/10 que tenia el error de la punta x10
#plt.figure()

plt.subplots(3,1, sharex=True)

g1 = plt.subplot(3,1,1)
plt.plot(t_volt*1000,volt/1000)
#plt.xlabel('tiempo (ms)', fontsize=20)
plt.ylabel('V$_{12}$ (kV)', fontsize=18)
plt.grid(True)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)

plt.subplot(3,1,2, sharex=g1)
plt.plot(t_idbd*1000,idbd*1000)
#plt.xlabel('tiempo (ms)', fontsize=20)
plt.ylabel(r'I$_{dbd} $ (mA)', fontsize=18)
plt.grid(True)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)

plt.subplot(3,1,3, sharex=g1)
plt.plot(t_istr*1000,istr*1000)
plt.xlabel('tiempo (ms)', fontsize=20)
plt.ylabel('I$_{str}$ (mA)', fontsize=18)
plt.grid(True)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)


#%% ------------------------------PREVISUALIZACION DE LAS POTENCIAS-------------------------
cant_periodos=6

tolerancia_picos= 1 # si es >1 aumentara la cantidad de picos reconocidos como streamers, si es <1 los mas chicos se eliminaran.

fuente_continua= -9.02 #en kV

alta_frecuencia=True #si es una medicion de alta frecuencia poner True, o False de lo contrario.

iper, tper = func.calculo_per(cant_periodos, t_volt, volt) #calcula la cantidad de elementos en un periodo y su duracion

potencia_istr, cor_media_istr, istr_aux = func.potencia(t_istr, istr, volt, cant_periodos, altafrec=alta_frecuencia,  v_dc_in=fuente_continua*1000 , tolerancia_corte=tolerancia_picos)

print('Potencia media de streamers en W:', potencia_istr)
print('Corriente media de streamers en mA:', cor_media_istr*1000)
print('voltaje pico a pico en kV:', func.pico_pico(volt)/1000)

plt.figure()
plt.plot(t_istr[:iper]*1000,istr_aux[:iper]*1000)
plt.xlabel('tiempo (ms)', fontsize=20)
plt.ylabel('Corriente de streamers (mA)', fontsize=20)
plt.grid()
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)

#%%
iper, tper = func.calculo_per(cant_periodos, t_volt, volt) #calcula la cantidad de elementos en un periodo y su duracion

tolerancia_picos= 1  # si es >1 aumentara la cantidad de picos reconocidos como streamers, si es <1 los mas chicos se eliminaran.

potencia_idbd, cor_media_idbd, idbd_aux = func.potencia(t_idbd, idbd,volt,cant_periodos, v_dc_in=fuente_continua*1000, altafrec=alta_frecuencia, streamer=False , tolerancia_corte=tolerancia_picos)

print('Potencia media de DBD en W:', potencia_idbd)
print('Corriente media de DBD en mA:', cor_media_idbd*1000)

plt.figure()
plt.plot(t_istr[2*iper:3*iper]*1000,idbd_aux[2*iper:3*iper]*1000)
plt.xlabel('tiempo (ms)', fontsize=20)
plt.ylabel('Corriente de DBD (mA)', fontsize=20)
plt.grid()
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)


#%%  ------------------------------potencia con ventana-----------------------------

path_comp = r'C:\Users\Mati\Documents\GitHub\Tesis\Mediciones\20181120\Trafo gas.csv'

path = r'C:\Users\Mati\Documents\GitHub\Tesis\Mediciones\20181120\Trafo gas ventana 1.csv'

fuente_continua= -9.02 #en kV

tolerancia_picos = 1

cant_periodos = 5

t_comp, volt_comp = func.acondic(path_comp)[0:2]

iper, tper = func.calculo_per(cant_periodos, t_comp, volt_comp)

t_volt, volt, t_idbd, idbd, t_istr, istr = func.acondic(path)

alta_frecuencia = False

potencia_istr, cor_media_istr, istr_aux = func.potencia_ventana(t_comp, volt_comp, t_istr, istr, volt, cant_periodos, v_dc_in=fuente_continua*1000, altafrec=alta_frecuencia,  tolerancia_corte=tolerancia_picos)


print('Potencia media de streamers en W:', potencia_istr)
print('Corriente media de streamers en mA:', cor_media_istr*1000)
print('voltaje pico a pico en kV:', func.pico_pico(volt_comp)/1000)
plt.figure()
plt.plot(t_istr*1000,istr_aux*1000)
plt.xlabel('tiempo (ms)')
plt.ylabel('Corriente (mA)')
plt.grid(True)
#plt.plot(t_istr,fiteada)


#%%


tolerancia_picos = 1

potencia_idbd, cor_media_idbd, idbd_aux = func.potencia_ventana(t_comp, volt_comp, t_idbd, idbd, volt, cant_periodos, v_dc_in=fuente_continua*1000 , altafrec=alta_frecuencia, streamer=False,  tolerancia_corte=tolerancia_picos)


print('Potencia media de dbd en W:', potencia_idbd)
print('Corriente media de dbd en mA:', cor_media_idbd*1000)

plt.figure()
plt.plot(t_idbd*1000,idbd_aux*1000)
plt.xlabel('tiempo (ms)')
plt.ylabel('Corriente (mA)')
plt.grid(True)


#iper, tper = func.calculo_per(cant_periodos, t_comp, volt_comp)
#
#potencia_istr_sum = 0
#
#cor_media_istr_sum = 0
#
#vmax = max(volt_comp)
#vmin = min(volt_comp)
#
#
#v_ac_med = (vmax+vmin)/2
#        
#v_dc = v_ac_med-fuente_continua*1000
#
#
#
#for i in range(len(volt)-1):
#    potencia_istr_sum += istr[i]*(volt[i])*0.5*(1+np.sign(istr[i]))
#    cor_media_istr_sum += istr[i]*0.5*(1+np.sign(istr[i]))
#    
#potencia_istr = potencia_istr_sum/len(volt)*(t_volt[len(t_volt)-1]-t_volt[0])/tper             #potencia media en W
#cor_media_istr = cor_media_istr_sum /len(volt)*(t_volt[len(t_volt)-1]-t_volt[0])/tper    #corriente promedio en A
#
#
#


#
#print('Potencia media de streamers en W:', potencia_istr)
#print('Corriente media de streamers en mA:', cor_media_istr*1000)
#
#plt.plot(t_istr[:iper]*1000,istr_aux[:iper]*1000)
#plt.xlabel('tiempo (ms)')
#plt.ylabel('Corriente de streamers (mA)')
#plt.grid()





#%%---------------------------POTENCIA PROMEDIADA ENTRE VARIAS MEDICIONES-----------------

cant_per_iter=6 #cantidad de periodos que hay en la medicion "a ojo"

voltaje_continua = -9.02 #indicar voltaje de la fuente externa en kilovolts

alta_frec = True  # indicar si se trata de una medicion de alta frecuencia (True) o baja (False).

tolerancia_corte_str= 2  # si es >1 aumentara la cantidad de picos reconocidos como streamers, si es <1 los mas chicos se eliminaran.

tolerancia_corte_dbd= 1

path = r"C:\Users\Mati\Documents\GitHub\Tesis\Mediciones\20181210"

subpath= 'Bobina gas '  #indicar nombre generico de las mediciones

inicio_med = 1 # indicar primer numero de la tira de mediciones

fin_med = 3 # indicar ultimo numero de la tira de mediciones

    
potencia_istr, potencia_idbd, cor_media_istr, cor_media_idbd = func.potencia_prom(cant_per_iter, voltaje_continua, alta_frec, tolerancia_corte_str, tolerancia_corte_dbd, path, subpath, inicio_med, fin_med)

#potencia_istr = potencia_istr/10   #solo para la medicion del 22/10 que tuvo los problemas de punta x10
#
#cor_media_istr = cor_media_istr/10 # idem

print('Potencia media de streamers en W:', potencia_istr)               #valor + desviacion estandar
print('Corriente media de streamers en mA:', cor_media_istr*1000)       #valor + desviacion estandar

print('Potencia media de DBD en W:', potencia_idbd)                     #valor + desviacion estandar
print('Corriente media de DBD en mA:', cor_media_idbd*1000)             #valor + desviacion estandar






#%%

#------------------- ------CÁLCULO DE EFICIENCIA EXPERIMENTAL-------------------------

#dado que este mismo analisis se hace para cualquier gas, hay que meter todo esto
#en una funcion que pida: gas, potencia, duracion, tiempo de inicio y fin.


potencia_final= potencia_idbd + potencia_istr #en watts

inicio= 6 #poner el minuto en que se encendió la descarga

fin= 17  #poner el minuto en que finalizó la descarga

efic_porcentual, efic_ener = func.eficiencia(duracion, CO, caudal, potencia_final, inicio, fin)

print('Potencia total en W:', potencia_final)
print('eficiencia porcentual:', efic_porcentual, '%')
print('rendimiento energético:',efic_ener,'mol/(kW H)')



#NOTA EFICIENCIA JORGE REAL: 0.54*1.04/1.33
#SALE DEL PRIMER RENGLON DE LA TABLA DE SU PAPER


#%% -----------------------------------Analisis de un pico---------------------------
path= r"C:\Users\Mati\Documents\GitHub\Tesis\Mediciones\20181211\Pico bobina 1.csv"

t_volt, volt, t_idbd, idbd, t_istr, istr = func.acondic(path)

'''              
estimacion de la duracion del pico a partir de un analisis del ruido de los primeros 100
puntos, y considerando que cuando decae como 1/e ya se termino. 

'''
pico_auxiliar = istr/(max(istr))

#pico_central = np.where(t_istr >= -0.0000005)[0][0]                       #si hay mas de un pico

pico_auxiliar = pico_auxiliar #[pico_central:]                              #si hay mas de un pico. borrar [pico_central:] sino.

t_istr_aux = t_istr #[pico_central:]

#pico_auxiliar = smooth(pico_auxiliar, 51, 3)                              # eliminando ruido

ruido = np.std(pico_auxiliar[:100])                                        #dejando el ruido

inicio_pico = np.where(pico_auxiliar >= ruido*30)[0][0]                     #dejando el ruido (cambiar el factor que multiplica al ruido, acorde a la medicion)

#inicio_pico = np.where(pico_auxiliar>= 0.05)[0][0]                        # eliminando ruido

#fin_pico = np.where(pico_auxiliar[inicio_pico:]< 1/np.e)[0][35]+inicio_pico


fin_pico_aux = np.where(pico_auxiliar[inicio_pico:]< 1/np.e)[0]

for i in range(len(fin_pico_aux)-1):
    if fin_pico_aux[i+1]-fin_pico_aux[i]>5:
        ind_fin_pico = i+1

fin_pico = fin_pico_aux[ind_fin_pico] + inicio_pico



duracion_pico = t_istr[fin_pico]-t_istr[inicio_pico]

print('Duracion del pico en microsegundos:' , duracion_pico *1e6)

plt.plot((t_istr_aux-t_istr_aux[0])*1e6, pico_auxiliar*max(istr)*1e3, label = 'Streamer de 1.65 $\mu$s de duración')
#plt.plot(t_istr_aux[inicio_pico:fin_pico]*1e6, pico_auxiliar[inicio_pico:fin_pico]*max(istr)*1e3, '.-')
plt.xlabel('tiempo ($\mu$s)', fontsize = 20)
plt.ylabel('I$_{str}$ (mA)', fontsize = 20)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)
plt.legend(fontsize = 20)
plt.grid(True) 
   


#%%

#LEER UN ARCHIVO CSV
csv.register_dialect('pycoma', delimiter=';')

f = open(r'C:\Users\Mati\Documents\GitHub\Tesis\20181016(Jorge)\reactor jorge.csv', 'rt')
try:
    #reader = csv.reader(f,dialect='pycoma') #si no se pone el dialect es ',' por defecto
    reader = csv.reader(f)
    for row in reader:
        print(row)
finally:
    f.close()

#%%
    
#-----------------------------------------------------medicion de Jorge------------------------------------------------
matriz=[]
with open(r'C:\Users\Mati\Documents\GitHub\Tesis\20181016(Jorge)\reactor jorge.csv') as csvfile:
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

#---------------------------------------------------PRUEBA DE LA FUNCION RECORTAR----------------------------------------------------

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

#%%

fit0, rec0 = func.recortar_corriente(t_istr, istr, tper, niter=0)

fit1, rec1 = func.recortar_corriente(t_istr, istr, tper, niter=1)

fit2, rec2 = func.recortar_corriente(t_istr, istr, tper, niter=2)

fit100, rec100 = func.recortar_corriente(t_istr, istr, tper, niter=100)

#plt.figure()
#plt.plot(t_istr[iper:3*iper], istr[iper:3*iper])
#plt.plot(t_istr[iper:3*iper], fit100[iper:3*iper])

#COMPARAR UNA FUNCION FITEADA Y SU RECORTADA, CON LAS DEMAS

plt.subplots(1,3, sharey=True)

g1 = plt.subplot(1,3,1)
plt.plot(t_istr[iper:3*iper]*1e3, istr[iper:3*iper]*1e3)
plt.plot(t_istr[iper:3*iper]*1e3, fit0[iper:3*iper]*1e3, label = 'Ajuste sinusoidal sin iterar')
plt.axhline(0.004640026728609554*1e3,linewidth = 1.5, color = 'r', linestyle = '--', label= 'Valor máximo del ajuste sin iterar')
plt.xlabel('tiempo (ms)', fontsize=20)
plt.ylabel('I$_{str}$ (ms)', fontsize=18)
plt.legend(fontsize = 12)
plt.grid(False)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)

plt.subplot(1,3,2, sharex=g1)
plt.plot(t_istr[iper:3*iper]*1e3, istr[iper:3*iper]*1e3)
plt.plot(t_istr[iper:3*iper]*1e3, fit1[iper:3*iper]*1e3, label = '1 iteración')
plt.axhline(0.004640026728609554*1e3,linewidth = 1.5, color = 'r', linestyle = '--')
plt.xlabel('tiempo (ms)', fontsize=20)
#plt.ylabel(r'I$_{dbd} $ (mA)', fontsize=18)
plt.grid(False)
plt.legend(fontsize = 12)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)

plt.subplot(1,3,3, sharex=g1)
plt.plot(t_istr[iper:3*iper]*1e3, istr[iper:3*iper]*1e3)
plt.plot(t_istr[iper:3*iper]*1e3, fit100[iper:3*iper]*1e3)
plt.axhline(0.004640026728609554*1e3,linewidth = 1.5, color = 'r', linestyle = '--', label = '100 iteraciones')
plt.xlabel('tiempo (ms)', fontsize=20)
#plt.ylabel('I$_{str}$ (mA)', fontsize=18)
plt.grid(False)
plt.legend(fontsize = 12)
plt.tick_params(axis = 'both', which = 'both', length = 4, width = 2, labelsize = 15)




#%%

#------------------------------------Calculo de capacidades experimentales------------------------------

periodo = func.calculo_per(5, t_volt, volt)[1]

v = func.fitear(func.funcaux, t_volt, volt, params_opt=([periodo,max(volt),1,1]))

v_deriv = func.derivada_num(t_volt, v) 

plt.plot(t_volt, volt)

plt.plot(t_volt, v)

largo_deriv = len(v_deriv)

idbd_rec = idbd[:(largo_deriv)]

istr_rec = istr[:(largo_deriv)]

c12_exp = -(np.dot(idbd_rec, v_deriv) / sum(v_deriv**2))

c13_exp = -(np.dot(istr_rec, v_deriv) / sum(v_deriv**2))

print('C12, C13 experimentales, en pF:', c12_exp*1e12, c13_exp*1e12)


#%%



















