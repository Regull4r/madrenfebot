import time
import re
import requests
from bs4 import BeautifulSoup

import paradas

def peticion(origen,destino):
    org = paradas.paradas[origen]
    dest = paradas.paradas[destino]
    
    payload = {
        'nucleo' : '10',
        'i' : 's',
        'cp' : 'NO',
        'o' : "19002",
        'd' : "35600",
        'df' : time.strftime("%Y%m%d"),
        'ho' : time.strftime("%H"),
        'hd' : '26', #Todas
        'TXTInfo': ''
    }

    URL = 'http://horarios.renfe.com/cer/hjcer310.jsp'
    r = requests.post(URL, data=payload) #petiticion http POST

    soup = BeautifulSoup(r.text, "lxml")
    textpar = str(soup.find_all("tr", class_="par")) #separar las filas
    textimpar = str(soup.find_all("tr", class_="impar"))

    horaspar = re.findall('[0-9]+\.[0-9][0-9]',textpar)#sacr las horas y los tiempos de trayecto
    horasimpar = re.findall('[0-9]+\.[0-9][0-9]',textimpar)

    respar = []
    fila = []


    for x in horaspar:#agrupar por opcion
        fila.append(x)
        if len(x)==4:
            respar.append(fila)
            fila = []

    resimpar = []        
    fila = []

    for x in horasimpar:
        fila.append(x)
        if len(x)==4:
            resimpar.append(fila)
            fila = []


    cont = 0

    for x in respar:#descartar trenes que ya han pasado
        if  x[0]>=time.strftime("%H.%M"):
            break#oh no un break dentro de un bucle      
        cont = cont + 1

    pares = respar[cont:]#eliminar trenes que ya han pasado de la lista
    impares = resimpar[cont:]

    resultado = [None]*(len(pares)+len(impares))#stackoverflow copypaste 
    resultado[::2] = pares#empezando en 0 meter elemento cada dos
    resultado[1::2] = impares#empezando en 1 meter elemento cada dos

    print(*resultado[:6], sep ="\n")#imprimir 6 primeros trenes


#list(map(lambda x: x.strip(), re.findall('[A-Z][a-zA-Z0-9-. ]*',texto)))

peticion("ValdelasFuentes", "Aluche")
