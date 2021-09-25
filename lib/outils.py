def date2str(dat):
	return dat.strftime("%d/%m/%Y %H:%M:%S")
#findef

def klines_max_prix(lst):
	pos=2
	mx=0
	for i in range(len(lst)):
		if float(lst[i][pos]) > mx: mx=float(lst[i][pos])
	#finpour
	return mx
#findef

def klines_min_prix(lst):
	pos=3
	mn=1000000000000000000 #je sais c'est debile
	for i in range(len(lst)):
		if float(lst[i][pos]) < mn: mn=float(lst[i][pos])
	#finpour
	return mn
#findef

def get_sens(flt):
	#afin de na pas avoir à répéter la règle 
	if flt > 0: return "vente"
	else: return "achat"
	#finSi
#findef

def dev2eth(qte,dev):
#afin de na pas avoir à répéter la règle 
	try:
		func="eth2dev"
		return "{:1.8f}".format(qte/float(api.get_avg_price(symbol=dev+"ETH")['price']))
	except Exception as e:
		#print("erreur dans la fonction "+func+" : ", sys.exc_info()[1])	
		error_std(func,sys.exc_info()[1])
		raise e 
#findef


def devise2stablecoin(api,qte,dev,stc):
#afin de na pas avoir à répéter la règle 
	try:
		func="devise2stablecoin"
		return "{:1.4f}".format(float(api.get_avg_price(symbol=dev+stc)['price'])*qte)
	except Exception as e:
		#print("erreur dans la fonction "+func+" : ", sys.exc_info()[1])	
		error_std(func,sys.exc_info()[1])
		raise e 
#findef

def gaseth2dev(qte,dev,lst):
#afin de na pas avoir à répéter la règle FUNC FAUSSE 
	try:
		func="gaseth2dev"
		if dev+stc in lst: return "{:1.4f}".format(float(api.get_avg_price(symbol=dev+stc)['price'])*qte)

	except Exception as e:
		#print("erreur dans la fonction "+func+" : ", sys.exc_info()[1])	
		error_std(func,sys.exc_info()[1])
		raise e 
#findef

def rechercheeth(lst,dev):
	if dev+"ETH" in lst: return [dev+"ETH",dev,"ETH"]
	elif "ETH"+dev in lst: return ["ETH"+dev,"ETH",dev]
#findef

def binnace_timestamp(millisec):
	#afin de na pas avoir à répéter la règle 
	return datetime.datetime.fromtimestamp(millisec/1000)
#findef


def get_name():
	import socket
	return socket.gethostname()


def get_ip():
	import socket
	hostname = socket.gethostname()
	return socket.gethostbyname(hostname)

