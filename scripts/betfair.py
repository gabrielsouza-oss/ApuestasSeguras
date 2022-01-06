import requests 
from bs4 import BeautifulSoup
from fractions import Fraction

from .data_classes import Dato, Jugador, Equipo, CasaDeApuestas

class Betfair(CasaDeApuestas):
	def __init__(self):
		self.s=requests.Session()
		self.nombre='betfair'
		self.DATA=[]
	
	def buscar_partidos(self):
		self.respuesta=self.s.get("https://www.betfair.es/sport/tennis")
		# https://www.betstars.es/?no_redirect=1#/tennis/daily
		# https://sports.m.bwin.es/es/sports/tenis-5
		#print(respuesta.text)

		self.soup=BeautifulSoup(self.respuesta.text,'html.parser')
		#partidos=soup.find_all('a',{'class':'ui-nav event-team-container ui-top event-link ui-gtm-click'})
		#partidos[0]['data-galabel']

		self.partidos=self.soup.find_all('li',{'class':'com-coupon-line-new-layout betbutton-layout avb-row avb-table market-avb set-template market-1-columns'})
		#print("hay ",len(self.partidos)," partidos")
		for partido in self.partidos:
			# Esta web dara problemas porque muchas veces solo pone los apellidos
			# Los partidos pueden ser variaciones de las dos siguientes formas:
			#J Delaney / E Vanshelboim v K Onishi / S Sekiguchi
			#Goffin - Albot
			#Pervolarakis v F Auger-Aliassime
			#Soeda - M Cuevas
			#Nishioka - P Cuevas
			try:
				nombre1,nombre2=partido.find_all('span',{'class':'team-name'})
				nombre1=nombre1['title']
				nombre2=nombre2['title']
				p1=Fraction(partido.find('li',{'class':'selection sel-0'}).find('span').text.replace('\n',''))
				p2=Fraction(partido.find('li',{'class':'selection sel-1'}).find('span').text.replace('\n',''))

				dobles=True if '/' in nombre1 else False
				# print("\tnombre1",nombre1,"nombre2:",nombre2,"dobles:",dobles)
				if dobles:
					e1j1,e1j2=nombre1.split('/')
					if ' ' in e1j1:
						n1,a1=e1j1.split(' ')
						if len(n1)==1:
							e1j1=Jugador(inicial_nombre=n1,apellido=a1)
						else:
							e1j1=Jugador(nombre=n1,apellido=a1)
					else:
						e1j1=Jugador(apellido=e1j1)
					if ' ' in e1j2:
						n1,a1=e1j2.split(' ')
						if len(n1)==1:
							e1j2=Jugador(inicial_nombre=n1,apellido=a1)
						else:
							e1j2=Jugador(nombre=n1,apellido=a1)
					else:
						e1j2=Jugador(apellido=e1j2)
					e2j1,e2j2=nombre2.split('/')
					if ' ' in e2j1:
						n1,a1=e2j1.split(' ')
						if len(n1)==1:
							e2j1=Jugador(inicial_nombre=n1,apellido=a1)
						else:
							e2j1=Jugador(nombre=n1,apellido=a1)
					else:
						e2j1=Jugador(apellido=e2j1)
					if ' ' in e2j2:
						n1,a1=e2j2.split(' ')
						if len(n1)==1:
							e2j2=Jugador(inicial_nombre=n1,apellido=a1)
						else:
							e2j2=Jugador(nombre=n1,apellido=a1)
					else:
						e2j2=Jugador(apellido=e2j2)
					self.DATA.append(Dato(Equipo(e1j1,e1j2),Equipo(e2j1,e2j2),p1,p2,dobles=dobles))

				else:
					if ' ' in nombre1:
						n1,a1=nombre1.split(' ')
						if len(n1)==1:
							j1=Jugador(inicial_nombre=n1,apellido=a1)
						else:
							j1=Jugador(nombre=n1,apellido=a1)
					else:
						j1=Jugador(apellido=nombre1)
					if ' ' in nombre2:
						n2,a2=nombre2.split(' ')
						if len(n2)==1:
							j2=Jugador(inicial_nombre=n1,apellido=a2)
						else:
							j2=Jugador(nombre=n2,apellido=a2)
					else:
						j2=Jugador(apellido=nombre2)
					self.DATA.append(Dato(Equipo(j1),Equipo(j2),p1,p2,dobles=dobles))
				
			except Exception as e:
				print("\tERROR: un partido no se ha podido parsear bien:",e)

if __name__=='__main__':
	b=Betfair()
	b.cargar_data_de_json()
	# b.buscar_partidos()
	# b.guardar_html()
	# b.guardar_data_en_json()
	b.print()