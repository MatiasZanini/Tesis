# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 15:33:17 2018

@author: Matías
"""

from datetime import datetime as dt



def lapso(inicio,fin):    #devuelve la resta de tiempos en minutos. pide string del tipo hh:mm:ss
   
    format='%H:%M:%S'
    duracion= str(dt.strptime(fin,format)-dt.strptime(inicio,format))
    tiempos=duracion.split(':')
    
    hora=int(tiempos[0])*60
    minutos=int(tiempos[1])
    segundos=int(tiempos[2])/60
    
    mins=hora+minutos+segundos
    return(mins)
    
    
    