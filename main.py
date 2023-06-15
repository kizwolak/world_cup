import matplotlib.pyplot as plt
import csv
import numpy as np


def extractor_de_goles(string):
    '''
    Esta función toma un resultado de partido en el formato "(penal) gol - gol (penal)" o "gol - gol".
    Comprueba el formato y devuelve sólo los goles marcados por los equipos en el partido.

    Entrada:
        cadena: cadena que contiene el resultado del partido
    Salida: 
        un diccionario con 2 o 4 enteros que señalan los goles marcados por cada equipo, 
        incluyendo los goles de penalti si están presentes en la cadena
    '''
    if string[0] == '(':
        home_penal = string[1]
        home_goles = string[4]
        away_goles = string[6]
        away_penal = string[9]
        return {'home_penal': int(home_penal), 'home_goles': int(home_goles),
                'away_goles': int(away_goles), 'away_penal': int(away_penal)}
    else:
        home_goles = string[0]
        away_goles = string[2]
        return {'home_goles': int(home_goles), 'away_goles': int((away_goles))}


def agregar_grupo(archivo, países_procesados, nombre_país):
    '''
    Esta función recibe un archivo que contiene información sobre los grupos, 
    un diccionario que contiene los países procesados por la función padre y un nombre de país 
    que se utiliza para buscar en el diccionario de países.

    Entrada:
        archivo: un archivo que contiene información sobre qué país pertenecía a qué grupo
        países_procesados: diccionario que contiene los países procesados por la función padre
            e información sobre ellos.
        nombre_país: el nombre del país a cuya clave añadiremos la información del grupo

    Salida:
        países_procesados: países_procesados modificado que contiene datos sobre el grupo del país especificado en nombre_país.    
    '''
    with open(archivo, 'r', encoding='utf-8') as data:
        lineas = data.readlines()
        nombres_columnas = lineas[0].strip().split(',')
        group_index = nombres_columnas.index('grupo')
        for linea in lineas:
            nuevos_valores_fila = linea.strip().split(',')
            if nombre_país in linea:
                países_procesados[nombre_país]['grupo'] = nuevos_valores_fila[group_index]


def calcular_rangos(lineas, países_procesados):
    '''
    Esta función toma en lineas de un archivo que contiene información del partido, 
    así como un diccionario de países procesados que contendrá información de rangos.
    Recorre las líneas, busca coincidencias y ve qué países estaban entre los 4 primeros y en qué orden.
    entre los 4 primeros y en qué orden.

    Entrada:
        lineas: lineas de un archivo que contienen información sobre los partidos jugados
        países_procesados: el diccionario que contiene la información de los países
    Salida:
        un diccionario modificado con información sobre las clasificaciones de los países
    '''
    equipas_por_tercer = []
    equipas_por_final = []
    for linea in lineas[0:2]:
        if len(equipas_por_tercer) == 2 and len(equipas_por_final) == 2:
            break
        nuevos_valores_fila = linea.strip().split(',')
        first_nombre_país = nuevos_valores_fila[3]
        second_nombre_país = nuevos_valores_fila[4]
        goles = extractor_de_goles(nuevos_valores_fila[7])
        if nuevos_valores_fila[3] == first_nombre_país:
            if goles['home_goles'] > goles['away_goles']:
                equipas_por_final.append(first_nombre_país)
                equipas_por_tercer.append(second_nombre_país)
            elif goles['away_goles'] > goles['home_goles']:
                equipas_por_final.append(second_nombre_país)
                equipas_por_tercer.append(first_nombre_país)
            else:
                if goles['home_penal'] > goles['away_penal']:
                    equipas_por_final.append(first_nombre_país)
                    equipas_por_tercer.append(second_nombre_país)
                else:
                    equipas_por_final.append(second_nombre_país)
                    equipas_por_tercer.append(first_nombre_país)
        if nuevos_valores_fila[4] == first_nombre_país:
            if goles['away_goles'] > goles['home_goles']:
                equipas_por_final.append(first_nombre_país)
                equipas_por_tercer.append(second_nombre_país)
            elif goles['home_goles'] > goles['away_goles']:
                equipas_por_final.append(second_nombre_país)
                equipas_por_tercer.append(first_nombre_país)
            else:
                if goles['away_penal'] > goles['home_penal']:
                    equipas_por_final.append(first_nombre_país)
                    equipas_por_tercer.append(second_nombre_país)
                else:
                    equipas_por_final.append(second_nombre_país)
                    equipas_por_tercer.append(first_nombre_país)

    for linea in lineas:
        if equipas_por_tercer[0] in linea and equipas_por_tercer[1] in linea:
            nuevos_valores_fila = linea.strip().split(',')
            goles = extractor_de_goles(nuevos_valores_fila[7])
            if equipas_por_tercer[0] == nuevos_valores_fila[3]:
                if goles['home_goles'] > goles['away_goles']:
                    países_procesados[equipas_por_tercer[0]]['rango'] = 3
                    países_procesados[equipas_por_tercer[1]]['rango'] = 4
                elif goles['away_goles'] > goles['home_goles']:
                    países_procesados[equipas_por_tercer[0]]['rango'] = 4
                    países_procesados[equipas_por_tercer[1]]['rango'] = 3
                else:
                    if home_penal > away_penal:
                        países_procesados[equipas_por_tercer[0]
                                          ]['rango'] = 3
                        países_procesados[equipas_por_tercer[1]
                                          ]['rango'] = 4
                    else:
                        países_procesados[equipas_por_tercer[0]
                                          ]['rango'] = 4
                        países_procesados[equipas_por_tercer[1]
                                          ]['rango'] = 3
            if equipas_por_tercer[0] == nuevos_valores_fila[4]:
                if goles['away_goles'] > goles['home_goles']:
                    países_procesados[equipas_por_tercer[0]]['rango'] = 3
                    países_procesados[equipas_por_tercer[1]]['rango'] = 4
                elif goles['home_goles'] > goles['away_goles']:
                    países_procesados[equipas_por_tercer[0]]['rango'] = 4
                    países_procesados[equipas_por_tercer[1]]['rango'] = 3
                else:
                    if goles['away_penal'] > goles['home_penal']:
                        países_procesados[equipas_por_tercer[0]
                                          ]['rango'] = 3
                        países_procesados[equipas_por_tercer[1]
                                          ]['rango'] = 4
                    else:
                        países_procesados[equipas_por_tercer[0]
                                          ]['rango'] = 4
                        países_procesados[equipas_por_tercer[1]
                                          ]['rango'] = 3

    for linea in lineas:
        if equipas_por_final[0] in line and equipas_por_final[1] in line:
            nuevos_valores_fila = line.strip().split(',')
            goles = extractor_de_goles(nuevos_valores_fila[7])
            if equipas_por_final[0] == nuevos_valores_fila[3]:
                if goles['home_goles'] > goles['away_goles']:
                    países_procesados[equipas_por_final[0]]['rango'] = 1
                    países_procesados[equipas_por_final[1]]['rango'] = 2
                elif goles['away_goles'] > goles['home_goles']:
                    países_procesados[equipas_por_final[0]]['rango'] = 2
                    países_procesados[equipas_por_final[1]]['rango'] = 1
                else:
                    if goles['home_penal'] > goles['away_penal']:
                        países_procesados[equipas_por_final[0]
                                          ]['rango'] = 1
                        países_procesados[equipas_por_final[1]
                                          ]['rango'] = 2
                    else:
                        países_procesados[equipas_por_final[0]
                                          ]['rango'] = 2
                        países_procesados[equipas_por_final[1]
                                          ]['rango'] = 1
            if equipas_por_final[0] == nuevos_valores_fila[4]:
                if goles['away_goles'] > goles['home_goles']:
                    países_procesados[equipas_por_final[0]]['rango'] = 1
                    países_procesados[equipas_por_final[1]]['rango'] = 2
                elif goles['home_goles'] > goles['away_goles']:
                    países_procesados[equipas_por_final[0]]['rango'] = 2
                    países_procesados[equipas_por_final[1]]['rango'] = 1
                else:
                    if away_penal > home_penal:
                        países_procesados[equipas_por_final[0]
                                          ]['rango'] = 1
                        países_procesados[equipas_por_final[1]
                                          ]['rango'] = 2
                    else:
                        países_procesados[equipas_por_final[0]
                                          ]['rango'] = 2
                        países_procesados[equipas_por_final[1]
                                          ]['rango'] = 1


def ordenar_elementos(elemento):
    '''
Se utiliza en la siguiente función. Devuelve el elemento con el que debe compararse un valor procesado por .sort en un momento dado.

    Entrada::
        elemento: el elemento actualmente procesado por la función .sort.
    Salida::
        elemento[1]: el ítem que servirá de comparación para el ítem original.
    '''
    return elemento[1]


def crear_ranking_goles(diccionario):
    '''
    Esta función toma un diccionario y crea dos matrices - 
    una con los nombres de los países, y otra con sus goles marcados.
    Luego la función crea una lista comprimida usando lista_de_paises y lista_de_goles,
    y luego ordena la lista por los goles marcados por cada país.

    Entrada:
        diccionario: el diccionario que contiene la información sobre los países.
    Salida:
        lista_combinada: una lista que contiene los países ordenados por goles marcados.
    '''
    lista_paises = []
    lista_goles = []
    for key in diccionario:
        lista_paises.append(key)
        lista_goles.append(diccionario[key]['goles'])
    lista_combinada = sorted(zip(lista_paises, lista_goles))
    lista_combinada.sort(key=ordernar_elementos, reverse=True)
    return lista_combinada


def crear_ranking_grupos(diccionario, fase):
    '''
    Esta función clasifica a los países por la cantidad de puntos que tenían en una determinada
    fase de grupos. Si no se especifica ninguna fase de grupos, se utiliza la última fase. Los puntos se añaden
    simplemente accediendo al elemento derecho de la matriz 'puntos' que cada tecla del diccionario
    tiene.

    Entrada:
        diccionario: un diccionario que contiene información sobre países
        fase: la fase de grupos que debe tenerse en cuenta (por ejemplo, si la fase es la 2a,
        sólo se tendrán en cuenta los puntos alcanzados tras la 2ª jornada).
    Salida:
        lista_combinada: una lista de países ordenados por la cantidad de puntos que tenían
        tras una determinada ronda de partidos.
    '''
    if fase == None:
        fase: 3
    lista_paises = []
    lista_puntos = []
    for key in diccionario:
        lista_paises.append(key)
        lista_puntos.append(diccionario[key]['puntos'][fase])
    lista_combinada = sorted(zip(lista_paises, lista_puntos))
    lista_combinada.sort(key=sort_item, reverse=True)
    return lista_combinada


def creer_diccionario(archivo):
    '''
    Esta función recibe un archivo que contiene información sobre los partidos. Crea un diccionario
    países_procesados que se utilizará en fases posteriores del programa.
    El algoritmo escanea el archivo y busca nuevos nombres de países. Una vez encontrado un nuevo nombre
    se procesa la información sobre el país y se añade al diccionario países_procesados.

    Entrada:
        archivo: un archivo que contiene información sobre todos los partidos jugados
    Salida:
        países_procesados: un diccionario que contiene información crucial sobre los países que
        se utiliza en todo el programa
        ranking_goles: una lista de países ordenados por goles, utilizada posteriormente para generar gráficos.
    '''
    with open(archivo, 'r', encoding='utf-8') as data:
        lineas = data.readlines()
        nombres_columnas = lineas[0].strip().split(',')
        tiempo_indice = nombres_columnas.index('tiempo_del_partido')
        nombre_país_index = nombres_columnas.index('home_team')
        países_procesados = {}

        for linea in lineas[1:]:
            valores_fila = linea.strip().split(',')
            nombre_país = valores_fila[nombre_país_index]
            if nombre_país in países_procesados:
                continue
            tiempo_del_partido = valores_fila[tiempo_indice]
            contador_lineas = 0
            estadisticas_procesadas = {
                'goles': 0, 'puntos': [0, 0, 0, 0], 'rango': 0}

            for linea in lineas[1:]:
                nuevos_valores_fila = line.strip().split(',')
                if nombre_país not in nuevos_valores_fila or contador_lineas == 3:
                    continue
                else:
                    contador_lineas += 1
                    goles = extractor_de_goles(nuevos_valores_fila[7])
                    if nuevos_valores_fila[3] == nombre_país:
                        estadisticas_procesadas['goles'] += goles['home_goles']
                    if nuevos_valores_fila[4] == nombre_país:
                        estadisticas_procesadas['goles'] += goles['away_goles']

                    if int(tiempo_del_partido[6]) == 2:
                        if int(tiempo_del_partido[9]) > 3 or int(tiempo_del_partido[8]) >= 1:
                            continue
                        else:
                            if nuevos_valores_fila[3] == nombre_país:
                                if goles['home_goles'] > goles['away_goles']:
                                    estadisticas_procesadas['puntos'][contador_lineas] += (
                                        estadisticas_procesadas['puntos'][contador_lineas - 1] + 3)
                                if goles['home_goles'] == goles['away_goles']:
                                    estadisticas_procesadas['puntos'][contador_lineas] += (
                                        estadisticas_procesadas['puntos'][contador_lineas - 1] + 1)
                                if goles['home_goles'] < goles['away_goles']:
                                    estadisticas_procesadas['puntos'][contador_lineas] += (
                                        estadisticas_procesadas['puntos'][contador_lineas - 1] + 0)
                            elif nuevos_valores_fila[4] == nombre_país:
                                if goles['away_goles'] > goles['home_goles']:
                                    estadisticas_procesadas['puntos'][contador_lineas] += (
                                        estadisticas_procesadas['puntos'][contador_lineas - 1] + 3)
                                if goles['home_goles'] == goles['away_goles']:
                                    estadisticas_procesadas['puntos'][contador_lineas] += (
                                        estadisticas_procesadas['puntos'][contador_lineas - 1] + 1)
                                if goles['home_goles'] < goles['away_goles']:
                                    estadisticas_procesadas['puntos'][contador_lineas] += (
                                        estadisticas_procesadas['puntos'][contador_lineas - 1] + 0)
                    else:
                        if nuevos_valores_fila[3] == nombre_país:
                            if goles['home_goles'] > goles['away_goles']:
                                estadisticas_procesadas['puntos'][contador_lineas] += (
                                    estadisticas_procesadas['puntos'][contador_lineas - 1] + 3)
                            if goles['home_goles'] == goles['away_goles']:
                                estadisticas_procesadas['puntos'][contador_lineas] += (
                                    estadisticas_procesadas['puntos'][contador_lineas - 1] + 1)
                            if goles['home_goles'] < goles['away_goles']:
                                estadisticas_procesadas['puntos'][contador_lineas] += (
                                    estadisticas_procesadas['puntos'][contador_lineas - 1] + 0)
                        elif nuevos_valores_fila[4] == nombre_país:
                            if goles['away_goles'] > goles['home_goles']:
                                estadisticas_procesadas['puntos'][contador_lineas] += (
                                    estadisticas_procesadas['puntos'][contador_lineas - 1] + 3)
                            if goles['away_goles'] == goles['home_goles']:
                                estadisticas_procesadas['puntos'][contador_lineas] += (
                                    estadisticas_procesadas['puntos'][contador_lineas - 1] + 1)
                            if goles['away_goles'] < goles['home_goles']:
                                estadisticas_procesadas['puntos'][contador_lineas] += (
                                    estadisticas_procesadas['puntos'][contador_lineas - 1] + 0)

            países_procesados[nombre_país] = estadisticas_procesadas
            agregar_grupo('group_stats.csv', países_procesados, nombre_país)
        calcular_rangos(lineas[61:], países_procesados)
        ranking_goles = crear_ranking_goles(países_procesados)
        return [ranking_goles, países_procesados]


def grafico_goles(ranking):
    '''
    Esta función toma una lista de países ordenados por goles 
    y genera un gráfico de barras con el total de goles.
    La función descompone la lista en dos variables
    y genera cada barra empezando por la puntuación más alta.

    Entrada:
        ranking: una lista ordenada de países con su puntuación total de goles
    Salida:
        un gráfico de barras que muestra una lista ordenada de países y goles marcados
    '''
    nombre_país, goles = zip(*ranking)

    fig = plt.figure(figsize=(15, 10))
    plt.bar(nombre_país[::-1], goles[::-1], color='blue', width=0.4)

    plt.xlabel("Países")
    plt.ylabel("goles marcados")
    plt.title(
        "La cantidad de goles marcados por cada participante de la Copa Mundial 2022.")
    plt.xticks(rotation=90)
    plt.show()


def grafico_grupos(diccionario, grupo):
    '''
    Esta función toma un diccionario de países con su respectiva información,
    hace un bucle a través de las claves para encontrar los países en un grupo proporcionado
    y luego procesa cada equipo uno por uno tomando sus puntos y proporcionando una etiqueta.

    ENTRADA:
        diccionario: un diccionario de países con información
        grupo: el grupo que el usuario quiere ver graficado
    SALIDA:
        un gráfico que muestra el progreso en puntos de cada equipo de un grupo
    '''
    partidos = [0, 1, 2, 3]
    equipos_en_grupo = []
    for key in diccionario:
        if diccionario[key]['grupo'] == str(grupo):
            teams_in_group.append([key, [diccionario[key]['puntos']]])
        if len(equipos_en_grupo) == 4:
            break
    for index, team in enumerate(equipos_en_grupo):
        plt.plot(equipos_en_grupo[index][1][0],
                 label=equipos_en_grupo[index][0], marker='o')
    plt.legend()
    plt.xticks(matches)
    plt.title('resultados de grupo por partido')
    plt.xlabel('# del partido')
    plt.ylabel('puntos')
    plt.show()


def creer_archivo(diccionario):
    '''
    Función que crea un nuevo archivo a partir de un diccionario proporcionado.
    Primero genera la fila de información y luego recorre las claves 
    y extrae la información necesaria.

    Entrada:
        diccionario: diccionario que se utilizará para extraer los datos
    Salida:
        un fichero que contiene la información extraída del diccionario
    '''
    with open('processed_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['teams', 'goles', 'grupo', 'score1',
                        'score2', 'score3', 'rango'])
        for key in diccionario:
            writer.writerow([key, diccionario[key]['goles'], diccionario[key]['grupo'], diccionario[key]['puntos']
                            [0], diccionario[key]['puntos'][1], diccionario[key]['puntos'][2], diccionario[key]['rango']])


def grafico_podio(diccionario):
    '''
    Esta función toma un diccionario, busca los 3 primeros países
    y genera una barra gráfica que parece un podio.
    Los tamaños están codificados y se basan en las clasificaciones,
    el ganador obtiene el tamaño más grande.
    El código también incluye algunas comprobaciones para acortar el tiempo de ejecución.

    Entrada:
        diccionario: un diccionario con información sobre los rangos alcanzados por los países
    Salida:
        un gráfico en forma de podio que muestra los 3 primeros países de la Copa del Mundo
    '''
    top3 = {}
    for key in diccionario:
        if diccionario[key]['rango'] != 1 and diccionario[key]['rango'] != 2 and diccionario[key]['rango'] != 3:
            continue
        if diccionario[key]['rango'] == 1:
            top3[key] = 3
        if diccionario[key]['rango'] == 2:
            top3[key] = 2
        if diccionario[key]['rango'] == 3:
            top3[key] = 1
        if len(top3) == 3:
            break
    for pais in top3:
        if top3[pais] == 2:
            barplot = plt.bar(
                pais, top3[pais], width=1.0, color='royalblue')
            plt.bar_label(barplot, labels=[pais])
            top3.pop(pais)
            break
    for pais in top3:
        if top3[pais] == 3:
            barplot = plt.bar(
                pais, top3[pais], width=1.0, color='royalblue')
            plt.bar_label(barplot, labels=[pais])
            top3.pop(pais)
            break
    for pais in top3:
        if top3[pais] == 1:
            barplot = plt.bar(
                pais, top3[pais], width=1.0, color='royalblue')
            plt.bar_label(barplot, labels=[pais])
    plt.axis('off')
    plt.show()


diccionario = creer_diccionario('data.csv')
gráfico_podio(diccionario[1])
# print(create_group_ranking(diccionario[1], 3))
# create_archivo(diccionario[1])
# group_graph(diccionario[1], 2)
# goals_graphic(diccionario[0])
