# coding: utf8
import csv 
import sys, getopt, os.path
import requests
import urllib.request, urllib.parse, urllib.error
import getpass
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

headers = {
		'Content-Type': 'application/json',
		'Nemopay-Version': '2017-12-15',
}

def readCsv(inputfile,action,sessionid,fundation):
	with open(inputfile, 'rt') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		if action=="addWalletToGroup":
			lastparam=getWalletGroups(sessionid)
			callable=addWalletToGroup
		elif action=="addUserToGroup":
			lastparam=getUserGroups(sessionid)
			callable=addUserToGroup
		elif action=="addWalletRight":
			lastparam=fundation
			callable=addRightToWallet
		elif action=="addUserRight":
			lastparam=fundation
			callable=addRightToUser
		elif action=="addGratuitees":
			lastparam=fundation
			callable=addGratuitees
		for row in spamreader:
			if(row[0]+row[1]+row[2]!=''):
				callable(getWallet(row[0]+' '+row[1]+' '+row[2],sessionid),row[3],sessionid,lastparam)
				
def getWalletGroups(sessionid):
	print(bcolors.HEADER + 'Getting wallet groups' + bcolors.ENDC)
	params = (
		('event', '1'),
		('ordering', 'id'),
		('system_id', 'payutc'),
		('active', True),
		('sessionid', sessionid),
	)
	response = requests.get('https://api.nemopay.net/resources/walletgroups', headers=headers, params=params)
	if response.status_code==200:
		ret = {}
		for group in response.json():
			ret[group['id']]=group['name']
		return ret
	else:
		print(bcolors.FAIL + "FAIL (unhandled error)" + bcolors.ENDC)
		print(response.json())
		sys.exit(9)
		
def addGratuitees(wallet,qte,sessionid,currency):

	params = (
		('system_id', 'payutc'),
		('sessionid', sessionid),
		('id__in',str(wallet['id']))
	)

	print(bcolors.OKBLUE + 'Adding '+ str(int(qte)*100) + ' of currency ' + str(currency) + ' to ' + str(wallet['id']) + bcolors.ENDC)

	data = '{"action_set":[{"currency":' + str(currency) + ',"quantity":' + str(int(qte)*100) + ',"kind":"add","refill_kind":"Gratuités"}]}'
	response = requests.post('https://api.nemopay.net/resources/wallets/batch_refill', headers=headers, params=params, data=data)

	if response.status_code == 201:
		print(bcolors.OKGREEN + "OK" + bcolors.ENDC)
	else:
		print(bcolors.FAIL + "FAIL (cannot add Gratuites)" + bcolors.ENDC)
		print(response.text)

def getUserGroups(sessionid):
	print(bcolors.HEADER + 'Getting user groups' + bcolors.ENDC)

	params = (
		('system_id', 'payutc'),
		('app_key', '0a93e8e18e6ed78fa50c4d74e949801b'),
		('sessionid', sessionid),
	)

	data = '{"fun_id":null}'

	response = requests.post('https://api.nemopay.net/services/GESGROUPS/getGroups', headers=headers, params=params, data=data)
	if response.status_code==200:
		ret = {}
		for group in response.json():
			ret[group['id']]=group['name']
		return ret
	else:
		print(bcolors.FAIL + "FAIL (unhandled error)" + bcolors.ENDC)
		print(response.json())
		sys.exit(9)

def tranfert(walletsrc,walletdst,amount,message,sessionid):
	print(bcolors.HEADER + 'Transferring '+ str(amount/100.0) + ' from wallet ' + walletsrc + ' to wallet ' + walletdst + ' (' + message + ')' + bcolors.ENDC)
	params = (
		('system_id', 'payutc'),
		('sessionid', sessionid),
	)
	data = '{"wallet_src":'+walletsrc+',"wallet_dst":'+walletdst+',"amount":'+amount+',"message":"'+message+'"}'
	response = requests.post('https://api.nemopay.net/services/GESUSERS/transfer', headers=headers, params=params, data=data)
	if response.status_code==200:
		ret = {}
		for group in response.json():
			ret[group['id']]=group['name'].encode('utf8')
		return ret
	else:
		print(bcolors.FAIL + "FAIL (unhandled error)" + bcolors.ENDC)
		print(response.json())
		sys.exit(9)

def addRightToUser(user,right,sessionid,fundation):
	print(bcolors.HEADER + 'Adding '+ right + ' permission to user ' + user['name'].encode('utf8') + bcolors.ENDC)
	params = (
		('system_id', 'payutc'),
		('sessionid', sessionid),
	)
	data = '{"fun_id":'+fundation+',"service":"'+right+'","usr_id":'+str(user['user_id'])+'}'
	response = requests.post('https://api.nemopay.net/services/USERRIGHT/setUserRight', headers=headers, params=params, data=data)
	if response.status_code==200:
		print(bcolors.OKGREEN + "OK" + bcolors.ENDC)
	else:
		print(bcolors.FAIL + "FAIL (unhandled error)" + bcolors.ENDC)
		print(response.json())
		sys.exit(9)
		
def getWallet(user,sessionid):

	print(bcolors.OKBLUE + 'Getting ' + user + ' wallet infos' + bcolors.ENDC)
	params = (
		('system_id', 'payutc'),
		('sessionid', sessionid),
	)
	data = '{"queryString":"'+str(user)+'","wallet_config":1}'

	response = requests.post('https://api.nemopay.net/services/GESUSERS/walletAutocomplete', headers=headers, params=params, data=data)
	if response.status_code == 403:
		print(bcolors.FAIL + "FAIL (Forbidden, maybe a bad session id is used)" + bcolors.ENDC)
		print(bcolors.FAIL + "Exiting" + bcolors.ENDC)
		sys.exit(6)
	elif response.json() == []:
		print(bcolors.FAIL + "FAIL (account not found)" + bcolors.ENDC)
		print(bcolors.FAIL + "Exiting" + bcolors.ENDC)
		sys.exit(7)
	elif response.status_code==200:
		return response.json()[0]
	else:
		print(bcolors.FAIL + "FAIL (unhandled error)" + bcolors.ENDC)
		print(response.json())
		sys.exit(8)
			
def addWalletToGroup(wallet,walletGroup,sessionid,walletgroups):

	params = (
		("system_id", 'payutc'),
		("sessionid", sessionid),
	)

	print(bcolors.OKBLUE + 'Adding wallet ' + str(wallet['id']) + ' to group ' + walletgroups[int(walletGroup)].encode('utf8') + bcolors.ENDC)

	data = '{"wallet_id":'+str(wallet['id'])+'}'

	response = requests.post('https://api.nemopay.net/resources/walletgroups/'+walletGroup+'/members', headers=headers, params=params, data=data)

	if response.status_code == 204:
		print(bcolors.OKGREEN + "OK" + bcolors.ENDC)
	else:
		print(bcolors.FAIL + "FAIL (cannot add to group)" + bcolors.ENDC)

def addUserToGroup(user,userGroup,sessionid,usergroups):

	params = (
		("system_id", 'payutc'),
		("sessionid", sessionid),
	)

	print(bcolors.OKBLUE + 'Adding user ' + user['name'].encode('utf8') + ' to group ' + usergroups[int(userGroup)].encode('utf8') + bcolors.ENDC)

	data = '{"usr_id":'+str(user['user_id'])+',"grp_id":'+str(userGroup)+'}'

	response = requests.post('https://api.nemopay.net/services/GESGROUPS/addUserToGroup', headers=headers, params=params, data=data)

	if response.status_code == 200:
		print(bcolors.OKGREEN + "OK" + bcolors.ENDC)
	else:
		print(bcolors.FAIL + "FAIL (cannot add to group)" + bcolors.ENDC)
		
def addRightToWallet(wallet,permission,sessionid,fundation):

	params = (
		("system_id", 'payutc'),
		("sessionid", sessionid),
	)

	print(bcolors.OKBLUE + 'Adding permission ' + str(permission) + ' to wallet ' + str(wallet['id']) + ' on fundation ' + str(fundation) + bcolors.ENDC)

	data = '{"obj":'+str(wallet['id'])+',"fundation":'+str(fundation)+',"location":null,"event":1,"name":"'+permission+'"}'

	response = requests.post('https://api.nemopay.net/resources/walletrights', headers=headers, params=params, data=data)

	if response.status_code == 201:
		print(bcolors.OKGREEN + "OK" + bcolors.ENDC)
	else:
		print(bcolors.FAIL + "FAIL (cannot add permission)" + bcolors.ENDC)
		
def loginCas2(username,password):
	params = (
		('system_id', 'payutc'),
		('app_key', '0a93e8e18e6ed78fa50c4d74e949801b'),
	)

	print(bcolors.OKBLUE + 'Loggin CAS ' + username + bcolors.ENDC)

	service = 'http://localhost/nemopay-mini-cli/login'
	casurl = requests.post('https://api.nemopay.net/services/ROSETTINGS/getCasUrl', headers=headers, params=params).json()
	headerscas = {
		'Content-type': 'application/x-www-form-urlencoded',
		'Accept': 'text/plain',
		'User-Agent':'python'
	}
	paramscas = urllib.parse.urlencode({
		'service': service,
		'username': username,
		'password': password
	})
	
	response = requests.post(casurl+'/v1/tickets/', headers=headerscas, params=paramscas)
	location = response.headers['location']
	tgt = location[location.rfind('/') + 1:]
	
	response = requests.post(casurl+'/v1/tickets/'+tgt, headers=headerscas, params=paramscas)
	st = response.text
	
	params = (
		("system_id", 'payutc'),
		("app_key","0a93e8e18e6ed78fa50c4d74e949801b"),
	)
	
	data = '{"ticket":"'+st+'","service":"'+service+'"}'
	
	response = requests.post('https://api.nemopay.net/services/MYACCOUNT/loginCas2', headers=headers, params=params, data=data)
	if response.status_code == 200:
		print(bcolors.OKGREEN + "Logged in via CAS as " + response.json()['username'] + bcolors.ENDC)
	
	return response.json()

def win_getpass(prompt='Password: ', stream=None):
	"""Prompt for password with echo off, using Windows getch()."""
	import msvcrt
	for c in prompt:
		msvcrt.putch(c.encode()[:1])
	pw = ""
	while 1:
		c = msvcrt.getch()
		if c == '\r' or c == '\n':
			break
		if c == '\003':
			raise KeyboardInterrupt
		if c == '\b':
			pw = pw[:-1]
			msvcrt.putch('\b')
		else:
			pw = pw + c
			msvcrt.putch('*')
	msvcrt.putch('\r')
	msvcrt.putch('\n')
	return pw

def main(argv):
	action = ''
	sessionid = ''
	inputfile = ''
	username = ''
	password = ''
	fundation = 'null'
	helper = sys.argv[0] + ' -i <inputfile> -a <addWalletToGroup|addUserToGroup|addWalletRight|addUserRight|addGratuitees> -u <casUsername> -p <casPassword> [-f <fundationid>]'
	try:
		opts, args = getopt.getopt(argv,"hp:u:f:i:a:",["help","password","ifile=","action=","username=","fundation="])
	except getopt.GetoptError as msg:
		print(msg)
		print(helper)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(helper)
			sys.exit()
		elif opt in ("-i", "--inputfile"):
			if os.path.isfile(os.path.abspath(arg)):
				inputfile = arg			
			else:
				print(bcolors.FAIL + "FAIL ( file " + arg + " does not exist )" + bcolors.ENDC)
				sys.exit(3)
		elif opt in ("-a", "--action"):
			if arg in ("addWalletToGroup","addUserToGroup","addWalletRight","addUserRight","addGratuitees"):
				action = arg
			else:
				print(bcolors.FAIL + "FAIL ( " + arg + " is not a valid action )" + bcolors.ENDC)
				sys.exit(4)
		elif opt in ("-u", "--username"):
			username = arg
		elif opt in ("-p", "--password"):
			password = arg
		elif opt in ("-f", "--fundation"):
			fundation = str(arg)
	if password == '':
		print("Type CAS password")
		password = win_getpass()
	if action == '' or inputfile == '' or fundation == '' or username == '' or password == '':
		print("One or more required parameter is missing")
		print(helper)
		sys.exit(5)
	print(username)
	print(password)
	sessionid=loginCas2(username,password)['sessionid']
	readCsv(inputfile,action,sessionid,fundation)
	
			
if __name__ == "__main__":
	main(sys.argv[1:])
