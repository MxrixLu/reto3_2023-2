"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.DataStructures import mapentry as me
from matplotlib.gridspec import GridSpec
import model
import matplotlib.pyplot as plt
assert cf
from tabulate import tabulate
import traceback
from datetime import datetime
import math 

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    return controller.new_controller()


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Conoce los eventos sísmicos entre dos fechas")
    print("3- Conoce los eventos sísmicos entre dos magnitudes")
    print("4- Consulta los 10 eventos más recientes según una magnitud y una profundidad")
    print("5- Consulta los 15 sísmicos más recientes según su significancia y una distancia azimuta")
    print("6- Consulta los 20 eventos más antiguos para una profundidad dada y registrados por un cierto número de estaciones")
    print("7- Reporta el evento más significativo y los N eventos más próximos en el área alrededor de un punto indicado")
    print("8- Grafica un histograma anual de los eventos ocurridos según la región y propiedades de los eventos")
    print("9- Visualizar los eventos sísmicos de cada requerimiento en un mapa interactivo")
    print("0- Salir")

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False
    
def printLoadDataAnswer(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    if isinstance(answer, (list, tuple)) is True:
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "||",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
    else:
        print("Tiempo [ms]: ", f"{answer:.3f}")

def load_data(control, filesize, memflag=False):
    """
    Carga los datos
    """
    return controller.loadData(control, filesize, memflag)



def print_files(records,  sample = 5):
    size = lt.size(records)
    tabla =[]
    if size <= sample*2:
        for earthquake in lt.iterator(records):
            tabla.append([earthquake['code'], earthquake['time'], earthquake['lat'], earthquake['long'],
                          earthquake['mag'], wrap_text(earthquake['title']), earthquake['depth'], earthquake['felt'], 
                          earthquake['cdi'], earthquake['mmi'], earthquake['tsunami']])
    else:
        
        i = 1
        while i <= sample:
            earthquake = lt.getElement(records, i)
            tabla.append([earthquake['code'], earthquake['time'], earthquake['lat'], earthquake['long'],
                          earthquake['mag'], wrap_text(earthquake['title']), earthquake['depth'], earthquake['felt'], 
                          earthquake['cdi'], earthquake['mmi'], earthquake['tsunami']])
            i += 1
        i = size - sample + 1
        while i <= size:
            earthquake = lt.getElement(records, i)
            tabla.append([earthquake['code'], earthquake['time'], earthquake['lat'], earthquake['long'],
                          earthquake['mag'], wrap_text(earthquake['title']), earthquake['depth'], earthquake['felt'], 
                          earthquake['cdi'], earthquake['mmi'], earthquake['tsunami']])
            i += 1
        if tabla:
            headers = ["code", "time", "lat", "long", "mag", "title", "depth", "felt", "cdi","mmi", "tsunami"]
            print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="left"))
def mini_print(earthquake):
    tabla =[[earthquake['time'], earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']),
            earthquake['cdi'],earthquake['mmi'], earthquake['magType'], earthquake['type'], earthquake['code'] ]]
    headers = [ "time", "mag", "lat", "long", "depth", "sig", "gap", "nst", "title", "cdi","mmi", "magType", "type", "code"]
    print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="left"))
    
def print_req_1(lista_r, sample=3):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    size = mp.size(lista_r)
    tabla =[]
    if size <= sample*2:
        for earthquakes in lt.iterator(lista_r):
            inner = []
            if type(earthquakes) == dict:
                earthquake = earthquakes
            else: 
                if earthquake[0]['mag'] > earthquake[1]['mag']: 
                    earthquake = earthquakes[0]['mag']
                    events = 1 
                else: 
                    earthquake = max(earthquakes, key=lambda x: x["mag"])
                    events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append(earthquake['time'], events, inner)
                
    else:
        i = 1
        while i <= sample:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            if type(earthquakes) == dict:
                earthquake = earthquakes
                events = 1
            else: 
                earthquake = max(earthquakes, key=lambda x: x["mag"])
                events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['time'], events, inner])
            i += 1
        i = size - sample + 1
        while i <= size:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            if type(earthquakes) == dict:
                earthquake = earthquakes
                events = 1
            else: 
                earthquake = max(earthquakes, key=lambda x: x["mag"])
                events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['time'], events, inner])
            i += 1
        if tabla:
            tabla.reverse()
            headers = ['time', 'events', 'details']
            print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="left"))


def print_req_2(lista_r, sample=3):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    size = lt.size(lista_r)
    tabla =[]
    if size <= sample*2:
        for earthquakes in lt.iterator(lista_r):
            inner = []
            events = len(earthquakes)
            contador= 0 
            for earthquake in earthquakes['elements']:
                
                inner.append([earthquake['time'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                          earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']),
                          earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
                contador+=1
                if contador== 6:
                    break
            
            inner.reverse()
            inner = tabulate(inner, headers=['time', 'lat', 'long', 'depth', 'sig', 'gap', 'nst', 'title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append(earthquake['mag'], contador, inner)
                
    else:
        i = 1
        while i <= sample:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            contador = 0
            for earthquake in earthquakes['elements']:
                inner.append([earthquake['time'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                          earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']),
                          earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
                events = len(earthquakes)
                contador+=1
                if contador== 6:
                    break
                
            inner.reverse()
            inner = tabulate(inner, headers=['time', 'lat', 'long', 'depth', 'sig', 'gap', 'nst', 'title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['mag'], contador, inner])
            i += 1
        i = size - sample + 1
        while i <= size:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            
            contador = 0
            for earthquake in earthquakes['elements']:
                inner.append([earthquake['time'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                          earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']),
                          earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
                contador+=1
                
                if contador== 6:
                    break
            
            inner.reverse()
            inner = tabulate(inner, headers=['time', 'lat', 'long', 'depth', 'sig', 'gap', 'nst', 'title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['mag'], contador, inner])
            i += 1
        if tabla:
            tabla.reverse()
            headers = ['mag', 'events', 'details']
            print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="left"))


def print_req_3(lista, sample=3):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    nuevo = {
        
    }
    lista2= []
    final=[]
    for diccionario in lt.iterator(lista):
        nuevo = {
        
    }
        diccionario_final={   
    }
        diccionario_final['mag']=diccionario['mag']
        diccionario_final['lat']=diccionario['lat']
        diccionario_final['long']=diccionario['long']
        diccionario_final['depth']=diccionario['depth']
        diccionario_final['sig']=diccionario['sig']
        diccionario_final['gap']=diccionario['gap']
        diccionario_final['nst']=diccionario['nst']
        diccionario_final['lat']=diccionario['lat']
        diccionario_final['lat']=diccionario['lat']
        diccionario_final['title']=diccionario['title']
        diccionario_final['cdi']=diccionario['cdi']
        diccionario_final['mmi']=diccionario['mmi']
        diccionario_final['magType']=diccionario['magType']
        diccionario_final['type']=diccionario['type']
        diccionario_final['code']=diccionario['code']
        
        nuevo['time'] = diccionario['time']
        if not diccionario ['tsunami'] == 0:
            nuevo['events'] = 2
        else:
            nuevo['events'] = 1
        lista3=[diccionario_final]
        nuevo['details'] = tabulate(lista3, 
                                    headers= "keys", tablefmt="grid")
        lista2.append(nuevo)
    if len(lista2) > 6:
        final.append(lista2[0])
        final.append(lista2[1])
        final.append(lista2[2])
        final.append(lista2[-3])
        final.append(lista2[-2])
        final.append(lista2[-1])
    else:
        final= lista2       
    print(tabulate(final, headers= "keys", tablefmt="grid"))


def print_req_4(lista_r, sample=3):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    size = lt.size(lista_r)
    tabla =[]
    if size <= sample*2:
        for earthquakes in lt.iterator(lista_r):
            inner = []
            if type(earthquakes) == dict:
                earthquake = earthquakes
            else: 
                if earthquake[0]['mag'] > earthquake[1]['mag']: 
                    earthquake = earthquakes[0]['mag']
                    events = 1 
                else: 
                    for earthquake in earthquakes:
                         if max_mag is None or earthquake["mag"] > max_mag:
                             max_mag = earthquake["mag"]
                             max_earthquake = earthquake
                    events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append(earthquake['time'], events, inner)
                
    else:
        i = 1
        while i <= sample:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            if type(earthquakes) == dict:
                earthquake = earthquakes
                events = 1
            else: 
                earthquake = max(earthquakes, key=lambda x: x["mag"])
                events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['time'], events, inner])
            i += 1
        i = size - sample + 1
        while i <= size:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            if type(earthquakes) == dict:
                earthquake = earthquakes
                events = 1
            else: 
                earthquake = max(earthquakes, key=lambda x: x["mag"])
                events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['time'], events, inner])
            i += 1
        if tabla:
            tabla.reverse()
            headers = ['time', 'events', 'details']
            print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="left"))




def print_req_5(lista_r, sample=3):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    
    size = lt.size(lista_r)
    tabla =[]
    if size <= sample*2:
        for earthquakes in lt.iterator(lista_r):
            inner = []
            if type(earthquakes) == dict:
                earthquake = earthquakes
            else: 
                if earthquake[0]['mag'] > earthquake[1]['mag']: 
                    earthquake = earthquakes[0]['mag']
                    events = 1 
                else: 
                    earthquake = max(earthquakes, key=lambda x: x["mag"])
                    events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append(earthquake['time'], events, inner)
                
    else:
        i = 1
        while i <= sample:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            if type(earthquakes) == dict:
                earthquake = earthquakes
                events = 1
            else: 
                earthquake = max(earthquakes, key=lambda x: x["mag"])
                events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['time'], events, inner])
            i += 1
        i = size - sample + 1
        while i <= size:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            if type(earthquakes) == dict:
                earthquake = earthquakes
                events = 1
            else: 
                earthquake = max(earthquakes, key=lambda x: x["mag"])
                events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['time'], events, inner])
            i += 1
        if tabla:
            headers = ['time', 'events', 'details']
            print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="left"))



def print_req_6(listBA, sample =3):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    lista_r = lt.newList('ARRAY_LIST')
    lista_r['elements'] = listBA[0]['elements'] +  listBA[1]['elements'] 
    size = lt.size(lista_r)
    tabla =[]
    if size <= sample*2:
        for earthquakes in lista_r['elements']:
            inner = []
            if type(earthquakes) == dict:
                earthquake = earthquakes
                events = 1
            else: 
                if earthquakes[0]['mag'] > earthquakes[1]['mag']: 
                    earthquake = earthquakes[0]['mag']
                    events = 1 
                else: 
                    earthquake = max(earthquakes, key=lambda x: x["mag"])
                    events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['mmi'],  earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'mmi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['time'], events, inner])
                
    else:
        i = 1
        while i <= sample:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            if type(earthquakes) == dict:
                earthquake = earthquakes
                events = 1
            else: 
                earthquake = max(earthquakes, key=lambda x: x["mag"])
                events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['mmi'],  earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'mmi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['time'], events, inner])
            i += 1
        i = size - sample + 1
        while i <= size:
            inner = []
            earthquakes = lt.getElement(lista_r, i)
            if type(earthquakes) == dict:
                earthquake = earthquakes
                events = 1
            else: 
                earthquake = max(earthquakes, key=lambda x: x["mag"])
                events = len(earthquakes)
            inner.append([earthquake['mag'], earthquake['lat'], earthquake['long'], earthquake['depth'],
                            earthquake['sig'], earthquake['gap'], earthquake['nst'], wrap_text(earthquake['title']), 
                            earthquake['cdi'], earthquake['mmi'],  earthquake['magType'], earthquake['type'], earthquake['code']])
            inner = tabulate(inner, headers=['mag', 'lat', 'long', 'depth', 'sig', 'gap', 'nst','title', 'cdi', 'mmi', 'magType', 'type', 'code'], tablefmt="grid")
            tabla.append([earthquake['time'], events, inner])
            i += 1
    if tabla:
        headers = ['time', 'events', 'details']
        print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="left"))

    
def print_req_7(dict_valores, valores_ad):
    keys = list(dict_valores.keys())
    list_values = list(dict_valores.values())
    values = [] 
    data = lt.newList('ARRAY_LIST')
    for val in list_values: 
        values.append(lt.size(val))
        for dic in val['elements']: 
            lt.addLast(data, dic)
            
    plt.bar(keys, values, width=0.6, align='center', color='#FFB6C1', edgecolor='black')
    plt.xlabel('Rango')
    plt.ylabel('Tamaño')
    plt.title('Histograma de '+ str(valores_ad[1]) + ' en ' + str(valores_ad[0]))
    plt.xticks(range(len(keys)), keys, rotation=45, ha='right')
    for llave, valor in zip(keys, values):
        plt.annotate(str(valor), xy=(llave, valor), ha='center', va='bottom')
    
    lt.mini_sort(data, 'time')
    tabla = []
    i = 0
    if i <= 6:
        i = 1
        while i <= 3:
            earthquake = lt.getElement(data, i)
            tabla.append([earthquake['time'], earthquake['lat'], earthquake['long'], earthquake['title'],
                      earthquake['code'], earthquake['mag']])


            i += 1
        i = lt.size(data) - 3 + 1
        while i <= lt.size(data) :
            earthquake = lt.getElement(data, i)
            tabla.append([earthquake['time'], earthquake['lat'], earthquake['long'], earthquake['title'],
                      earthquake['code'], earthquake['mag']])

            i += 1
    
    if tabla:
        headers = ['time', 'lat', 'long', 'title', 'code', 'mag']
        print(tabulate(tabla, headers=headers, tablefmt="grid", stralign="left"))
    plt.show()



def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

def wrap_text(text, line_length=20):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= line_length:
            if current_line:
                current_line += " "
            current_line += word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')

        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            
            filesize = input('Indica el tamaño de la muestra que deseas analizar (small, ...pct, large): ')
            control = controller.new_controller() 
            
            mem = castBoolean(input('¿Quieres medir la memoria utilizada?: '))
            deltas, total = load_data(control, filesize)
            
            print('\nLoading data... \n')
            print('-'*50)
            print('Tamaño de los eventos temblores: '+ str(total))
            printLoadDataAnswer(deltas)
            print('\n'+'-'*50 ,'\n')
            
            print('='*50)
            print('REPORTES DE REGISTROS DE TEMBLORES'.center(50, '='))
            print('='*50, '\n')
            
            print('\nImprimiendo 5 primeros y 5 últimos...')
            
            print('\n','-'*9, 'Resultados de temblores:', '-'*9)
            print(('Total de temblores: ' + str(total)).center(49, ' '))
            
            print('\nADT tiene más de 10 registros... ' )
            print_files(control['sis_events'])
            
        elif int(inputs) == 2:
            fecha_i = datetime.strptime(input('Inserta fecha incial del intervalo la búsqueda de temblores: '), "%Y-%m-%dT%H:%M")
            fecha_f = datetime.strptime(input('Inserta fecha final del intervalo la búsqueda de temblores: '), "%Y-%m-%dT%H:%M")
            
            deltas, lista_r, totales= controller.req_1(control, fecha_i, fecha_f)
            
            print("\n"+ "Inputs".center(26, '='))
            print("Fecha inicial: " + str(fecha_i) )
            print("Fecha final: " + str(fecha_f) )
            print("\n"+ "Resultados".center(30, '='))
            print("Total de elementos entre las fechas: "+str(totales[0]))
            print("Total de nodos entre las fechas: "+str(totales[0]))
            print("Altura total de árbol de fechas: " + str(totales[1]))
            
            printLoadDataAnswer(deltas)
            print_req_1(lista_r)

        elif int(inputs) == 3:
            min = float(input('Inserta el mínimo: '))
            max = float(input('Inserta el máximo: '))
            delta, lista= controller.req_2(control, min, max)
            print("\n"+ "Inputs".center(26, '='))
            print("Magnitud mínima: " + str(min) )
            print(" Magnitud Máxima: " + str(max) )
            print("\n"+ "Resultados".center(30, '='))
            print("Total de diferentes magnitudes: "+ "0")
            print("Total de eventos: "+str(lista[1]))
            printLoadDataAnswer(delta)
            print_req_2(lista[0])

        elif int(inputs) == 4:
            min_mag =round(float(input('Inserta la magnitud mínima de la búsqueda: ')),3 )
            profmax=round(float(input('Inserta la profundidad maxima de la búsqueda: ')),3 )
            deltas, lista, total= controller.req_3(control, min_mag, profmax)
            print("\n"+ "Inputs".center(26, '='))
            print("Magnitud Minima " + str(min_mag) )
            print("Profundidad Máxima: " + str(profmax) )
            print("\n"+ "Resultados".center(30, '='))
            print("Total fechas diferentes: "+str(total))
            print("Total de eventos en el rango: "+str(total))
            
            printLoadDataAnswer(deltas)
            print_req_3(lista)

        elif int(inputs) == 5:
            min_sig =round(float(input('Inserta la significancia mínima de la búsqueda: ')),3 )
            max_gap = round(float(input('Inserta distancia azimutal máxima de la búsqueda: ')), 3)
            
            deltas, lista_r, total= controller.req_4(control, min_sig, max_gap)
            
            print("\n"+ "Inputs".center(26, '='))
            print("Signifcancia mín: " + str(min_sig) )
            print("Distancia Azimutal máx: " + str(max_gap) )
            print("\n"+ "Resultados".center(30, '='))
            print("Total fechas diferentes: "+str(total))
            print("Total de eventos en el rango: "+str(total))
            
            printLoadDataAnswer(deltas)
            print_req_4(lista_r)

        elif int(inputs) == 6:
            depths = float(input('Inserta la profundidad mínima del evento: '))
            estaciones = float(input('Inserta el número mínimo de estaciones del evento: '))
            
            
            deltas, lista = controller.req_5(control, depths, estaciones)
            
            print("\n"+ "Inputs".center(26, '='))
            print("Profundidad mínima: " + str(depths) )
            print("Estaciones: " + str(estaciones) )
            
    
            print("\n"+ "Resultados".center(30, '='))
            print("\nTotal de sismos: " + str(lista[1]))
        
            
            printLoadDataAnswer(deltas)

            print("\n" + "-"*4 + "Los eventos más cronologicamente cercanos" + "-"*4)
            print_req_5(lista[0]) 

        elif int(inputs) == 7:
            year = int(input('Inserta el año que te gustaria tomar de referencia: '))
            lat = float(input('Inserta la latitud de referencia para el área de eventos: '))
            long = float(input('Inserta la longitud de referencia para el área de eventos: '))
            radius = float(input('Inserta el radio del área circundante : '))
            n = int(input('Inserta el número de los n eventos de magnitud más cercana: '))
            
            deltas, sign, total, listBA = controller.req_6(control, year, lat, long, radius, n)
            
            print("\n"+ "Inputs".center(26, '='))
            print("Año: " + str(year) )
            print("Lat buscada: " + str(lat) )
            print("Long buscada: " + str(long) )
            print("Radio a buscar: " + str(radius) )
            print("Número de eventos antes y despues: " + str(n) )
    
            print("\n"+ "Resultados".center(30, '='))
            print("\nCódigo del sismo más significativo en condiciones: " + str(sign['code']))
            print("Eventos en el sismo: "+str(total))
            print("-"*7 , "Evento más significativo", "-"*7)
            mini_print(sign)
            
            printLoadDataAnswer(deltas)

            print("\n" + "-"*4 + "Los eventos más cronologicamente cercanos" + "-"*4)
            print_req_6(listBA)

        elif int(inputs) == 8:
            year = int(input('Inserta el año que te gustaria tomar de referencia: '))
            title = input('Inserta el título de la región de la que quiere investigar: ')
            prop = (input('Indica la propiedad que quieres escoger (mag, depth o sig): '))
            if prop == 'mag': 
                prop_1 = 1
            elif prop_1 == 'depth':
                prop_1 = 2
            else: 
                prop = 3
            bins = int(input('Inserta el número de segmentos que quieres para el histograma : '))
            
            deltas, range_bins, totales = controller.req_7(control, year, title, prop_1, bins)
            
            print("\n"+ "Inputs".center(26, '='))
            print("Año: " + str(year) )
            print("Área de interés : " + str(title) )
            print("Propiedad de interés: " + str(prop) )
            print("Número de bins: " + str(bins) )
    
            valores_ad = (year, title, prop)
            
            print("\n"+ "Resultados".center(30, '='))
            print("\nEl número de eventos sísmicos usados en el histogramas: " + str(totales[0]))
            print("Valor mínimo de la propiedad: "+str(totales[1]))
            print("Valor máximo de la propiedad: "+str(totales[2]))
            
            printLoadDataAnswer(deltas)

            print("\n" + "-"*4 + "El histograma y la tabla" + "-"*4)
            print_req_7(range_bins, valores_ad)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
#
    sys.exit(0)