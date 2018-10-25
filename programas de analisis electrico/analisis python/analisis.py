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

#------------------------OBTENER CONCENTRACION DE GASES-------------------------


csv.register_dialect('pycoma', delimiter=';')

#datos = open(r'C:\Users\Matías\Documents\GitHub\Tesis\20180928\Concentracion NO.csv', 'rt')

matriz=[]
NO=np.array([]) #en PPM
NO2=np.array([]) #en PPM
CO=np.array([]) #en PPM
NOx=np.array([]) #en PPM
caudal=np.array([]) #en l/h
#arrcomp=[]

with open(r"C:\Users\Matías\Documents\GitHub\Tesis\20181022\Concentracion NO.csv") as csvfile:
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
            
#%%
ti=matriz[2][0].split(' ')[1]                #encuentra el tiempo inicial en formato stirng
tf=matriz[len(matriz)-1][0].split(' ')[1]    #encuentra el tiempo final en formato string

duracion=func.lapso(ti,tf)


print('duración de la medición total:',duracion,'minutos')


            
#%%
#--------------------------------------------PLOTEAR CONCENTRACION------------------------------------

#la funcion pide el array con la medicion, la duracion total y 
#el nombre que se quiera en el label 

func.ploteo_concentracion(NO,duracion,'NO')

#%%--------------------------------------------------POTENCIA------------------------------------------------------

path=r"C:\Users\Matías\Documents\GitHub\Tesis\20181005\Bobina gas 1.csv"  #ingresar el path de la medicion electrica

t_volt, volt, t_idbd, idbd, t_istr, istr = func.acondic(path)

plt.subplot(3,1,1)
plt.plot(t_volt,volt)
plt.xlabel('tiempo (s)')
plt.ylabel('Voltaje entrada (V)')
plt.grid(True)

plt.subplot(3,1,2)
plt.plot(t_idbd,idbd*1000)
plt.xlabel('tiempo (s)')
plt.ylabel('Corriente de DBD (mA)')
plt.grid(True)

plt.subplot(3,1,3)
plt.plot(t_istr,istr*1000)
plt.xlabel('tiempo (s)')
plt.ylabel('Corriente de streamers (mA)')
plt.grid(True)

#%%

cant_per=3 #cantidad de periodos que hay en la medicion "a ojo"



volt_rec=volt[0:(int((len(volt)/cant_per)+1))]
indmax=int(np.mean(np.where(volt_rec==max(volt_rec))[0]))
indmin=int(np.mean(np.where(volt_rec==min(volt_rec))[0]))

iper=2*abs(indmax-indmin)                       #cantidad de elementos en un periodo
tper=2*abs(t_volt[indmax]-t_volt[indmin])       #periodo en segundos


#%%

potencia_istr, cor_media_istr, istr_aux = func.potencia(t_istr, istr,volt,iper,tper)

print('Potencia media en W:', potencia_istr)
print('Corriente media en mA:', cor_media_istr*1000)

plt.plot(t_istr[:iper],istr_aux[:iper]*1000)
plt.xlabel('tiempo (s)')
plt.ylabel('Corriente de streamers (mA)')




#%%





#%%

#prueba de recorte

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


#la corriente esta dando bien, pero la potencia da bajisima comparado a lo que da en el mathematica






#%%

#------------------- ------CÁLCULO DE EFICIENCIA EXPERIMENTAL-------------------------

#dado que este mismo analisis se hace para cualquier gas, hay que meter todo esto
#en una funcion que pida: gas, potencia, duracion, tiempo de inicio y fin.


tiempo=np.linspace(0,duracion,len(NO))

pot=60 #ingresar potencia en watts

inicio=22 #poner el minuto en que se encendió la descarga

fin=30  #poner el minuto en que finalizó la descarga

tiempo= np.linspace(0,duracion,len(NO))

dondeini=np.where(tiempo>=inicio)[0][0] # índice donde comienza la descarga
inicio=tiempo[dondeini] #tiempo de inicio medido por la máquina

dondefin=np.where(tiempo>=fin)[0][0]#índice donde comienza la descarga




ci= max(NO[dondeini:dondefin]) #concentracion inicial en ppm
cf= min(NO[dondeini:dondefin]) #concentracion final en ppm

efic_porcentual= (ci-cf)/ci *100 #eficiencia porcentual absoluta

caudalprom=np.mean(caudal)

efic = (caudalprom*(ci-cf)*1e-3 * 0.0407)/pot #eficiencia relativa a la potencia suministrada en mol/(kW H)

print('eficiencia porcentual:', efic_porcentual, '%')
print('eficiencia por potencia:',efic,'mol/(kW H)')







            
        



#%%

#LEER UN ARCHIVO CSV

f = open(r'C:\Users\Matías\Documents\GitHub\Tesis\20181005\Concentracion NO.csv', 'rt')
try:
    reader = csv.reader(f,dialect='pycoma') #si no se pone el dialect es ',' por defecto
    for row in reader:
        print(row)
finally:
    f.close()

























