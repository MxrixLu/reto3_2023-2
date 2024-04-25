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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
from datetime import datetime
from haversine import haversine, Unit
import re

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def newRecord():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    record = {'sis_events': None, 
              'dates_simple': None,
              'bigRecord': None, 
              'sig_map': None, 
              'lat_long': None, 
              'prop_map': None, 
              'mag_simple': None, 
              'dephts': None}
    
    record['sis_events'] = lt.newList('ARRAY_LIST', cmp_dates)
    record['dates_simple'] = om.newMap(omaptype='RBT', cmpfunction=cmp_tree)
    record['bigRecord'] = om.newMap(omaptype='RBT', cmpfunction= cmp_tree)
    record['sig_map'] = om.newMap(omaptype='RBT', cmpfunction=cmp_tree)
    record['lat_long'] = mp.newMap(maptype='PROBING')
    record['prop_map'] = mp.newMap(maptype='PROBING')
    record['mag_simple'] = om.newMap(cmpfunction= cmp_tree)
    record['dephts'] = om.newMap (omaptype = 'RBT', cmpfunction= cmp_tree)

    return record

######################################### Funciones para agregar informacion al modelo #########################################

def add_event(record, element):
    """
    Función para agregar nuevos elementos a la lista
    """
    element['time'] = datetime.strptime(element['time'], "%Y-%m-%dT%H:%M:%S.%fZ") 
    element['time'] = datetime(element['time'].year, element['time'].month, element['time'].day, element['time'].hour, element['time'].minute)
    element['updated'] = datetime.strptime(element['updated'], "%Y-%m-%dT%H:%M:%S.%fZ")
    if element['nst'] == '': 
        element['nst'] = 1
    element['nst'] = float(element['nst'])
    if not element['felt'] == '': 
        element['felt'] = round(float(element['felt']), 3)
    else:
        element['felt'] = 'Unknown'
    if not element['cdi'] == '': 
        element['cdi'] = round(float(element['cdi']), 3)   
    else: 
        element['cdi'] = 'Unknown'
    if not element['mmi'] == '': 
        element['mmi'] = round(float(element['mmi']), 3)
    else: 
        element['mmi'] = 'Unknown'
    if element['place'] == '': 
        element['place'] = 'Unknown'
    element['sig'] = round(float(element['sig']), 3)
    element['long'] = round(float(element['long']), 3)
    element['lat'] = round(float(element['lat']), 3)
    element['tsunami'] = castBoolean(element['tsunami'])
    element['depth'] = round(float(element['depth']), 3)
    element['mag'] = round(float(element['mag']), 5)
    if not element['gap'] == '': 
        element['gap'] = round(float(element['gap']), 3)
    else: 
        element['gap'] = 0
    if not element['rms'] == '': 
        element['rms'] = round(float(element['rms']), 3)
    else: 
        element['rms'] = 'Unknown'
    element['long'] = int(element['long'])
    return lt.addLast(record['sis_events'], element)

#-------------------Carga de estructura dates_simple -------------------                         
def add_dates_simple(map, record):
    time = record['time']
    entry = om.get(map['dates_simple'], time)
    if entry is None: 
        time_entry = lt.newList('ARRAY_LIST')
        om.put(map['dates_simple'], time, time_entry)
    else:
        time_entry = me.getValue(entry)
    lt.addLast(time_entry, record)
    return map
def add_mag_simple(map, record):
    mag = record['mag']
    entry = om.get(map['mag_simple'], float(mag))
    if entry == None: 
        mag_entry = lt.newList('ARRAY_LIST', cmp_dates)
        om.put(map['mag_simple'], mag, mag_entry)
    else:
        entry = om.get(map['mag_simple'], float(mag)) 
        mag_entry = me.getValue(entry)
    lt.addLast(mag_entry, record)
    return map
#-------------------Carga de estructura bigRecord ------------------- 
def addMagnitud(map, record):
    mag = int(record['mag'])
    entry = om.get(map['bigRecord'], mag)
    if entry is None: 
        mag_entry = lt.newList('ARRAY_LIST')
        om.put(map['bigRecord'], mag, mag_entry)
    else: 
        mag_entry = me.getValue(entry)
        
    lt.addLast(mag_entry, record)
    return map


#-------------------Carga de estructura sig_map ------------------- 
def add_sig_map(map, record): 
    if int(record['sig']/100) == 0:
        sig = int(record['sig']/10)*10
    else:
        sig = int(record['sig']/100)*100
    
    entry = om.get(map['sig_map'], sig)
    if entry is None: 
        sig_entry = new_sig()
        om.put(map['sig_map'], sig, sig_entry)
    else:
        ent = om.get(map['sig_map'], sig)  
        sig_entry = me.getValue(ent)

    lt.addLast(sig_entry, record)
    return map

#-------------------Carga de estructura lat_long ------------------- 
def addYearLatLong(map, record): 
    year = record['time'].year
    entry = mp.get(map['lat_long'], year)
    if entry is None: 
        yearEntry = new_year()
        mp.put(map['lat_long'], year, yearEntry)
    else: 
        yearEntry = me.getValue(entry)
        
    addLatLong(yearEntry['latLong_records'], record)
    
    return map        

def addLatLong(map, record): 
    latLong= (record['lat'], record['long'])
    entry = mp.get(map, latLong)
    if entry is None:
        latLong_entry = lt.newList('ARRAY_LIST')
        om.put(map, latLong, latLong_entry)
    else: 
        latLong_entry = me.getValue(entry)
    lt.addLast(latLong_entry, record)
    return map
 
#-------------------Carga de estructura prop_map ------------------- 
def add_prop_map(map, record): 
    prop =  record['time'].year
    entry = mp.get(map['prop_map'], prop)
    if entry is None: 
        propMap_entry = new_prop()
        mp.put(map['prop_map'], prop, propMap_entry)
    else: 
        propMap_entry = me.getValue(entry)
    add_title_prop(propMap_entry, record)
    return map 

def add_title_prop(map, record):
    title = find_pais(record['place'])
    entry = mp.get(map['titles'], title)
    if entry is None: 
        title_entry = new_title()
        om.put(map['titles'], title, title_entry)
    else: 
        title_entry = me.getValue(mp.get(map['titles'], title))
    
    om.put(title_entry['records'], [0, record['mag'], record['depth'], record['sig']], record)
    lt.addLast(lt.getElement(title_entry['props'], 1),record['mag'])
    lt.addLast(lt.getElement(title_entry['props'], 2),record['depth'])
    lt.addLast(lt.getElement(title_entry['props'], 3), record['sig'])
    return map
    
def add_dph(map, record):
    
    entry = om.get(map['dephts'], float(record['depth']))
    if entry == None: 
        areaentry = new_dph()
        om.put(map['dephts'], float(record['depth']), areaentry)
    else: 
        ent = om.get(map['dephts'], float(record['depth'])) 
        areaentry = me.getValue(ent)
    
    lt.addLast(areaentry, record)
    return map

######################################### Creacion de estructuras #########################################
 
def new_magnitud(): 
    new_mag = {'profundidades': [],
               'depths': None}
    new_mag['depths'] =om.newMap(omaptype='RBT')
    
    return new_mag

def new_mini_bigTime():
    new_mbt = {'magnitudes': [], 
               'profundidades': [], 
               'mag_records': None}
    new_mbt['mag_records'] = om.newMap(omaptype='RBT')
    return new_mbt

def new_sig(): 
    return lt.newList('ARRAY_LIST', cmpfunction=compare_gap)

def new_year():
    new_year = {'latLong_records': None}
    new_year['latLong_records'] = om.newMap('RBT', cmp_tree)
    return new_year

def new_prop(): 
    new_prop = {'titles': None}
    new_prop['titles'] = mp.newMap(maptype='PROBING', 
                                   loadfactor= 0.5)
    return new_prop

def new_title():
    new_title = {'records': None, 
                 'props' : None }
    
    new_title['records'] = om.newMap(omaptype='RBT', cmpfunction=cmp_tuples3)
    new_title['props'] = lt.newList('ARRAY_LIST')
    mag = lt.newList('ARRAY_LIST')
    depth =lt.newList('ARRAY_LIST')
    sig =lt.newList('ARRAY_LIST')
    lt.addLast(new_title['props'], mag)
    lt.addLast(new_title['props'], depth)
    lt.addLast(new_title['props'], sig)
    return new_title


def new_dph(): 
    return lt.newList('ARRAY_LIST')
    
########################################## Funciones de consulta #########################################

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass

def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass

######################################### Requerimientos #########################################

MAGNITUDES = list(range(3, 10))
YEARS = list(range(1993, 2024))

def req_1(catalog, fecha_i, fecha_f):
    """
    Función que soluciona el requerimiento 1
    """
    by_date = catalog['dates_simple']
    list_val = om.valuesList(by_date, fecha_i, fecha_f )
    total = lt.size(list_val)
    height = om.height(by_date)
    totales = (total, height)
    return list_val, totales


def req_2(catalog, limi_mag, limf_mag):
    """
    Función que soluciona el requerimiento 2
    """
    mag = catalog['mag_simple']
    rta = om.values(mag, limi_mag, limf_mag)     
    total_sismos = lt.size(rta)
    return rta, total_sismos



def req_3(catalog, mag_min, prof_max):
    """
     Consulta los eventos sísmicos más recientes que superen una magnitud y no superen una profundidad
     dada

    :param catalog: Catálogo de sismos.
    :param mag_min: Magnitud mínima del evento.
    :param prof_Max: Profundidad máxima del evento.
    :return: final = Lista de los 10 eventos más recientes que cumplen con los criterios.
    """
    mag_map = catalog ['mag_simple']
    mag_max = om.maxKey(mag_map)
    lista_mag = om.values(mag_map,mag_min,mag_max)


    final = lt.newList("ARRAY_LIST")

    for lista in lt.iterator(lista_mag):
        for info in lt.iterator(lista):
            if not info ["depth"] == "" or "Unknown":
                if float(info ["depth"]) <= float(prof_max):
                   lt.addLast(final,info)

    merg.sort(final,cmp_req3)
    total = lt.size(final)

    return final, total


def req_4(catalog, min_sig, max_gap):
    """
    Función que soluciona el requerimiento 4
    """
    sig_map = catalog['sig_map']
    limite_sup = om.maxKey(sig_map)
    mapa_new = om.newMap(omaptype= 'RBT', cmpfunction= cmp_tree)
    mapa_new = om.valuesListMap(sig_map, min_sig, limite_sup, mapa_new, 'gap')
    lista = om.valuesBelow(mapa_new, max_gap, cmp_tree)
    lista = lt.mini_sort(lista, 'time')
    event15 = lt.subList(lista, lt.size(lista)-14, 15)
    total = lt.size(lista)
    return event15, total

def req_5(catalog, depth_min, nst_min):
    """
    Consulta los eventos sísmicos más recientes que superen una profundidad mínima y sean identificados
    por un número mínimo de estaciones de monitoreo.

    :param catalog: Catálogo de sismos.
    :param depth_min: Profundidad mínima del evento.
    :param nst_min: Número mínimo de estaciones de monitoreo.
    :return: Lista de los 20 eventos más recientes que cumplen con los criterios.
    """
    mapa = catalog['dephts']
    limite_sup = om.maxKey(mapa)
    mapa_new = om.newMap(omaptype= 'RBT', cmpfunction= cmp_nst)
    mapa_new = om.valuesListMap1(mapa, depth_min, limite_sup, mapa_new)
    lista = om.valuesAbove(mapa_new, nst_min-1, cmp_tree)
    lista = lt.mini_sort1(lista, 'time')
    if lt.size(lista) >= 20:
        lista['elements'] = lista['elements'][:20]
        eventos = lista
    else:
        eventos = lista
    eventos['size'] = len(eventos['elements'])
    total = lt.size(lista)

    return eventos, total
        
def req_6(catalog, year, lat, long, radius, n):
    """
    Función que soluciona el requerimiento 6
    """
    latLongMap = me.getValue(mp.get(catalog['lat_long'], year))['latLong_records']
    hav_entry = (lat, long)
    diferencia = om.valuesBelow(latLongMap, radius, cmp_diferencia_radius, (True, hav_entry ) )
    signList = lt.mini_sort(diferencia, 'sig')
    sign = lt.getElement(signList, lt.size(signList))
    time = lt.mini_sort(diferencia, 'time')
    listBA = binary_storage(time, sign, n)
    total = lt.size(diferencia)
    return sign, total, listBA


def req_7(catalog, year, title, prop, bins):
    """
    Función que soluciona el requerimiento 7
    """
    #prop llega como un entero 1, 2 o 3
    mapa_year = catalog['prop_map']
    mapa_tit = me.getValue(mp.get(mapa_year, year))['titles']
    datos = me.getValue(mp.get(mapa_tit, title))
    propi = lt.getElement(datos['props'], prop)
    records = datos['records']
    range_bins ={}
    low = round(min(propi['elements']), 4)
    high = round(max(propi['elements']), 4)
    totales = (om.size(records) ,low, high)
    dif_prop = (high- low)/bins
    residuo = (high- low)%bins
    high = low + dif_prop
    for i in range(1, bins+1): 
        llave= str(low) + '-' + str(high)
        t_low = [0, 0, 0, 0]
        t_high = [0, 0, 0, 0]
        t_low[prop] = low
        t_high[prop] = high
        valores = om.values(records, t_low, t_high)
        range_bins[llave] = valores
        low = high
        high= round(low + dif_prop, 4)
    return range_bins, totales
        
    
def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

def binary_storage(lst, element, n):
    low = 1
    high = lt.size(lst)
    before = lt.newList('ARRAY_LIST')
    after = lt.newList('ARRAY_LIST')

    while low <= high:
        mid = (low + high) // 2
        tem_elem = lt.getElement(lst, mid)

        if tem_elem == element:
            for i in range(mid, min(mid + n + 1, lt.size(lst) + 1)):
                lt.addLast(after, lt.getElement(lst, i))

            for i in range(max(mid - n, 1), mid):  # Ensure the index is not less than 1
                lt.addLast(before, lt.getElement(lst, i))

            return before, after
        elif tem_elem['time'] > element['time']:
            high = mid - 1
        else:
            low = mid + 1


def binary_search(lst, element, prop): 
    
    low = 1
    high = lt.size(lst)
    while low<= high: 
        mid = (low + high)//2
        tem_elem = lt.getElement(lst, mid)
        if tem_elem[prop] == element : 
            last = mid     
            low = mid+1       
        elif tem_elem[prop] > element: 
            high = mid-1
        else: 
            low = mid+1
    return last
                
def find_pais(cadena): 
    if len(cadena) < 7:
        return cadena  # O devuelve la cadena original, dependiendo de lo que prefieras

    patron = r',\s([^,]+)$|-\s([^,]+)$'
    match = re.search(patron, cadena)

    if match:
        pais_encontrado = match.group(1) or match.group(2)
        return pais_encontrado
    else:
        return 'Unknown'
                
########################################## Funciones utilizadas para comparar elementos dentro de una lista #########################################
def cmp_req3 (dicionario1,dicionario2):
    return dicionario1 ['time'] > dicionario2 ['time']
def cmp_tuples3(tuple1, tuple2): 
    if tuple1[1] == tuple2[1]:
        if tuple1[2] == tuple2[2]:
            if tuple1[3] == tuple2[3]: 
                return 0
            elif tuple1[3] > tuple2[3]: 
                return 1
            else: 
                return -1
        elif tuple1[2] > tuple2[2]: 
            return 1
        else: 
            return -1
    elif tuple1[1]> tuple2[1]: 
        return 1
    else: 
        return -1
def cmp_dates(event1, event2): 
    if event1['time']> event2['time']: 
        return 1
    elif event1['time'] < event2['time']: 
        return -1
    else: 
        return 0
    
def cmp_mag(event1, event2): 
    if event1['mag']> event2['mag']: 
        return 1
    elif event1['mag'] < event2['mag']: 
        return -1
    else: 
        return 0
def cmp_depth(event1, event2): 
    if event1['depth']> event2['depth']: 
        return 1
    elif event1['depth'] < event2['depth']: 
        return -1
    else: 
        return 0
def cmp_sig(event1, event2): 
    if event1['sig']> event2['sig']: 
        return 1
    elif event1['sig'] < event2['sig']: 
        return -1
    else: 
        return 0
    
def cmp_tree(elemet1, element2):
    if (elemet1 == element2):
        return 0
    elif (elemet1 > element2):
        return 1
    else:
        return -1
    

def cmp_miniTree_gap(gap1, gap2):         
    if (gap1 == gap2): 
        return 0
    if gap1 == 'Unknown': 
        return 1
    if gap2 == 'Unknown' : 
        return -1
    if (gap1 > gap2) : 
        return 1 
    else: 
        return -1
    
def compare_gap(record1, record2): 
    if type(record1) == list: 
        record1= record1[0] 
    if type(record2) == list: 
        record2= record2[0] 
    if record1['gap'] == record2['gap']:
        return 0
    elif record1['gap'] > record2['gap']: 
        if record1['time'] == record2['time']: 
            return 0
        elif record1['time'] > record2['time']: 
            return 1
        else:
            return -1
    else: 
        return -1
    
def cmp_diferencia_radius(pair, pair2, radius): 
    hav = haversine(pair, pair2)
    if hav == radius: 
        return 0
    elif hav < radius: 
        return 1
    else:
        return -1
    
def cmp_nst(sig_key, sig2): 
    if float(sig_key) == float(sig2):
        return 0
    elif  float(sig_key) > float(sig2):
        return 1
    else:
        return -1

# ######################################### Funciones de ordenamiento #########################################


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass