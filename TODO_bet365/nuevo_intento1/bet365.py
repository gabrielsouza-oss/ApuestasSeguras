import requests
import json
import re

def guardar_json(d):
    f=open("cookies.json","w")
    json.dump(d,f)
    f.close()

def leer_json():
    f=open("cookies.json","r")
    d=json.load(f)
    f.close()
    return d

# cookies de las 21h del 30-01-22
cookies = {
    'pstk': '2669CE9B907264859AA3D6C68684346B000003', # expires in 1 week
    'rmbs': '3', # expires in 6 months
    'aps03': 'cf=N&cg=4&cst=0&ct=171&hd=N&lng=3&oty=2&tzi=4', # expires in 10 years
    '__cf_bm': 'dHu4rUmjxVzmf9ytfEMVA0Fpx7v1xrOieWERk_FUqvY-1643586632-0-ASJ3JPBbI6nqdD+ds364EotFuw100o+02ouoo+CYqKwJ6yV7NlgRJzACsbee95dhk9iYzu6lAJ6FLq7EK9m0eBH+5hPRdNFcthu5jw60kFSj5J2uG7lCw14C9YLdyNdgELae0jhx0Wg+Uon1hIgxHs3q/1XJ7CLhrxMJM8ZzadWM', #expires in 1 day
}

cookies={
    'pstk': '2669CE9B907264859AA3D6C68684346B000003',
    'rmbs': '3',
    'aps03': 'cf=N&cg=4&cst=0&ct=171&hd=N&lng=3&oty=2&tzi=4',
    '__cf_bm': '30.cXVqL3y8wiq0SGa8FqIp6f2xp3ZAvi8EPNPl0KIc-1643590041-0-AXQoa35pkM+jyb0d5EFU6rLWJAUgHfHbCdyAVFwP54ZX21NlWsxjJMjmGFcnYiCsB+fgpax+9Qjty7sH51RMgaI='
}


headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'X-Net-Sync-Term': 'QnL4YQ==.iTu0w96J594DCMCnlRZkZDa24evFcv1aXqfOHbT4Gbo=', # este es el unico que cambia pero da igual, lo importante son las cookies
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.bet365.es/',
    'Accept-Language': 'es-ES,es;q=0.9',
}

# los params son siempre iguales
params = (
    ('lid', '3'),
    ('zid', '0'),
    ('pd', '#AS#B13#'),
    ('cid', '171'),
    ('cgid', '4'),
    ('ctid', '171'),
)

s=requests.Session()

# https://stackoverflow.com/questions/17224054/how-to-add-a-cookie-to-the-cookiejar-in-python-requests-library
requests.utils.add_dict_to_cookiejar(s.cookies, cookies)
s.headers=headers

response = s.get('https://www.bet365.es/SportsBook.API/web', params=params)

assert response.status_code==200

if not s.cookies.get_dict()==leer_json():
    guardar_json(s.cookies.get_dict())
    print("ACTUALIZO COOKIES")

# Los nombres de los partidos son de la forma:
# EX=Dougaz/Mansouri v Hemery/Meraut;
# Hay que buscar desde "EX=" hasta ";"

# Tambien pueden ser de la forma
# EX=WTA Limoges - Camila Giorgi v Liudmila Samsonova;
# Por lo que hay que quitarles el nombre del evento

# EX=WTA Limoges - Dobles Femeninos - Garcia-Perez/Sorribes Tormo v Pigossi/Zidansek;
# por lo que hay que cortar hasta el ultimo '-'
# Para buscar el ultimo caracter en una cadena se usa rfind()

texto=response.text
n=len(re.findall("EX=",texto))
partidos=[]
for k in range(n):
    comienzo=texto.find("EX=")
    final=texto.find(";",comienzo)
    nombre=texto[comienzo+3:final]
    if '-' in nombre:
        nombre=nombre[nombre.rfind('-')+2:]
    nombre=nombre.replace(' v ','  -  ')
    partidos.append(nombre)
    texto=texto[final:]
    #print(partidos[k])

# Ahora hay que buscar los ODDs de las apuestas.
# Son de la forma: OD=1/2; 
# Primero se encuentran los ODDs de la pimera columa
# y luego los de la segunda
ODDs=[]
for k in range(2*n):
    comienzo=self.texto.find("OD=")
    final=self.texto.find(";",comienzo)
    string=self.texto[comienzo+3:final]
    # string es de la forma "11/7" hay que pasarlo a float
    '''numerador=string[:string.find('/')]
    denominador=string[string.find('/')+1:]
    ODDs.append(round(1+float(int(numerador)/int(denominador)),2))'''
    ODDs.append(Fraction(string))
    self.texto=self.texto[final:]
    #print(ODDs[k])