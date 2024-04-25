"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import csv
import tracemalloc
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    record = model.newRecord()
    return record

# Funciones para la carga de datos

def loadData(record, filesize, memflag=False):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    
    fileLoad = cf.data_dir + f'earthquakes/temblores-utf8-{filesize}.csv'
    input_file = csv.DictReader(open(fileLoad, encoding="utf-8"),
                                delimiter=",")
    for event in input_file:
        model.add_event(record, event)
        model.addMagnitud(record, event)
        model.add_dates_simple(record, event)
        model.add_sig_map(record, event)
        model.addYearLatLong(record, event)
        model.add_prop_map(record, event)
        model.add_mag_simple(record, event)
        model.add_dph(record, event)
    
    total = lt.size(record['sis_events'])
        
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return (delta_time, delta_memory), total

    else:
        return delta_time, total


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog, fecha_i, fecha_f, memflag=False):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    lista_r, totales = model.req_1(catalog, fecha_i, fecha_f)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return (delta_time, delta_memory), lista_r, totales

    else:
        return delta_time, lista_r, totales

def req_2(catalog, min, max, memflag= False):
    """
    Retorna el resultado del requerimiento 2
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    lista = model.req_2(catalog, min, max)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return (delta_time, delta_memory), lista 

    else:
        return delta_time, lista


def req_3(catalog, mag_min, max_prof, memflag=False):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    lista, total = model.req_3(catalog, mag_min, max_prof)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return (delta_time, delta_memory), lista, total

    else:
        return delta_time, lista, total


def req_4(catalog, min_sig, max_gap, memflag=False):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    lista, total = model.req_4(catalog, min_sig, max_gap)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return (delta_time, delta_memory), lista, total

    else:
        return delta_time, lista, total

def req_5(catalog, depths, estaciones, memflag= False):
    """
    Retorna el resultado del requerimiento 5
    """

    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    lista = model.req_5(catalog, depths, estaciones)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return (delta_time, delta_memory), lista 

    else:
        return delta_time, lista

def req_6(catalog, year, lat, long, radius, n, memflag=False):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    sign, total, listBA = model.req_6(catalog, year, lat, long, radius, n)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return (delta_time, delta_memory), sign, total, listBA 

    else:
        return delta_time, sign, total, listBA 


def req_7(catalog, year, title, prop, bins, memflag=False):
    """
    Retorna el resultado del requerimiento 7
    """
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = getTime()

    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
        
    range_bins, totales = model.req_7(catalog, year, title, prop, bins)

    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return (delta_time, delta_memory), range_bins, totales 

    else:
        return delta_time, range_bins, totales


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para medir la memoria utilizada


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory