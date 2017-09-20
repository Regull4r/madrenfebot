import time
import re
import requests
from bs4 import BeautifulSoup

    
payload = {
    'nucleo' : '10',
    'i' : 's',
    'cp' : 'NO',
    'o' : '19002',
    'd' : '35600',
    'df' : time.strftime("%Y%m%d"),
    'ho' : time.strftime("%H"),
    'hd' : '26', #Todas
    'TXTInfo': ''
}
URL = 'http://horarios.renfe.com/cer/hjcer310.jsp'
r = requests.post(URL, data=payload)

soup = BeautifulSoup(r.text, "lxml")
textpar = str(soup.find_all("tr", class_="par")) #separ las filas
textimpar = str(soup.find_all("tr", class_="impar"))

horaspar = re.findall('[0-9]+.[0-9][0-9]',textpar)
horasimpar = re.findall('[0-9]+.[0-9][0-9]',textimpar)

respar = []
fila = []


for x in horaspar:#agrupar columnas
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

for x in respar:
    if  x[0]>=time.strftime("%H.%M"):
        break#oh no un break dentro de un bucle
        
    cont = cont + 1

pares = respar[cont:]
impares = resimpar[cont:]

resultado = [None]*(len(pares)+len(impares))#stackoverflow copypaste
resultado[::2] = pares
resultado[1::2] = impares

print(resultado[:6])

