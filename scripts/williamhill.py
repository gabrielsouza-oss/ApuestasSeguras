import requests
from bs4 import BeautifulSoup
from fractions import Fraction
import json


from .data_classes import Dato, Jugador, Equipo, CasaDeApuestas


class Williamhill(CasaDeApuestas):
	def __init__(self):
		self.s=requests.Session()
		self.nombre="williamhill"
		self.DATA=[]	

	def buscar_partidos(self):
		self.respuesta=self.s.get("https://sports.williamhill.es/betting/es-es/tenis/partidos/competici%C3%B3n/hoy")
		if self.respuesta.status_code!=200:
			print("Williamhill: ERROR: Response Code:",self.respuesta.status_code)
			return 0
		self.respuesta_text=self.respuesta.text
	
	def parsear_partidos(self):
		self.soup=BeautifulSoup(self.respuesta_text,'html.parser')
		# eventos es una lista con cadauno de "los partidos"
		self.eventos=self.soup.find_all('div',{'class':'event'})
		for e in self.eventos:
			try:
				# Equipo
				nombres=e.find('a').find_all('span')
				n1=nombres[0].text
				n2=nombres[1].text
				dobles=True if '/' in n1 else False
				# print(n1,n2,dobles)
				if not dobles:
					seleccion=False if ' ' in n1 else True # si es un equipode una seleccion nacional
					if seleccion:
						print("\twilliamhill: buscar_partidos(): se ha omitido un partido de selecciones:",n1)
						continue
					n1,a1=n1.split(' ')
					equipo1=Equipo(Jugador(nombre=n1,apellido=a1))
					n2,a2=n2.split(' ')
					equipo2=Equipo(Jugador(nombre=n2,apellido=a2))
				else:
					e1j1,e1j2=n1.split("/")
					equipo1=Equipo(Jugador(apellido=e1j1),Jugador(apellido=e1j2))
					e2j1,e2j2=n2.split("/")
					equipo2=Equipo(Jugador(apellido=e2j1),Jugador(apellido=e2j2))
				
				# odds
				b=e.find_all('button')
				precio1=Fraction(b[0]['data-odds'])
				precio2=Fraction(b[1]['data-odds'])
				self.DATA.append(Dato(equipo1,equipo2,precio1,precio2,dobles=dobles))
			except Exception as e:
				"""
				Falla cuando el nombre tiene dos palabras (por ejemplo: juan antonio lopez)
				Falla cuando las odds es una string: 'EVS'
				"""
				# print("ERROR: un partido no se ha podido parsear")
				# print(e)
				pass

		
if __name__=='__main__':
	w=Williamhill()
	w.buscar_partidos()
	# w.guardar_html()
	# w.cargar_html()
	w.parsear_partidos()
	w.guardar_data_en_json()
	# w.print()	