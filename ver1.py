"""
Program requesting data from zfs-storage

version without pools api and without VAULT new error handling for server not found
"""


import requests
import json
import os
import traceback
from docopt import docopt
requests.packages.urllib3.disable_warnings()



__version__ = '1.0'
__revision__ = '20190626'
__deprecated__ = False

data = {}
def get_headers():
	"""
	Function that contains the user and password authentication

	this returns 'headers' a dictionary that contains the user and password authentication
	"""
	headers = {
		"Content-Type":"application/json",
		"X-Auth-User": 'root',
		"X-Auth-Key": 'password'

	}
	return headers

def get_args():
	"""Function to get command line arguments.

	Defines arguments needed to run this program.

	:return: Dictionary with arguments
	:rtype: dict
	"""
	
	usage = """
	Usage:
		try.py -s <STORAGE> --diag
		try.py --version
		try.py -h | --help

	Options:
		-h --help            Show this message and exit
		-s <STORAGE>         ZFS appliance/storage name

	"""

	args = docopt(usage)
	return args	


def api_list():
	"""Function that contains the RestAPIs

	:return: Array 'url' that contains the API

	"""
	url = [	
			'/hardware/v1/cluster', 
			'/hardware/v1/chassis', 
			'/network/v1/routes', 
			'/storage/v1/pools', 
			'/service/v1/services',
			'/system/v1/updates', 
			'/system/v1/version', 
			'/system/v1/disks', 
			'/system/v1/memory'
			]

	return url


def get_data(storage):
	"""function to retrieve data from the APIs.

	:param storage: contains the ip address of the storage
	:Store all the data from all the called APIs in a Dictionary 'data'
	"""
	header = get_headers()
	base_url = 'https://{}:215'.format(storage)
	# Call the function api_list
	url = api_list()
	# loop on all the api inside the url array
	for i in url:
		ch1_uri = '{}/api'.format(base_url)+i
		
		r = requests.get(ch1_uri, verify=False, headers = header)
		j = r.json()
		# store data into dictionary 'data'
		data.update(j)

	"""
	Creating a json file named 'output.json' that contains all the data 
	 in json format 
	"""

	# with open('output.json', 'w') as outfile:
		# json.dump(data, outfile, indent = 2)


def get_val():

	def get_chassis():

		print('\n')
		print('+'+'-'*30+'+')
		print('  *** CHASSIS INFORMATION ***\n')
		print('* Chassis Name: ',data['chassis'][0]['name'])
		print('* Chassis Manufacturer: ',data['chassis'][0]['manufacturer'])
		print('* Chassis Model: ',data['chassis'][0]['model'])
		print('* Chassis Serial: ',data['chassis'][0]['serial'],"\n")

	def get_services():
		print('\n')
		print('+'+'-'*30+'+')
		print('  *** SERVICES ***\n')
		print('Name'+' '*25+'Status'+' '*7+'Details'+' '*30)
		print('-'*26+'   '+'-'*9+'   '+'-'*37)
		for i in data['services']:
			x = 29 - len(i['name'])
			print(i['name']+' '*x+i['<status>'])

	def get_cluster():
		c = len(data['cluster']['state'])
		print('\n')
		print('+'+'-'*30+'+')
		print('  *** CLUSTER CHACK ***\n')
		print('Name'+' '*25+'Status'+' '*( c - 3)+'Details'+' '*30)	
		print('-'*26+'   '+'-'*c+'   '+'-'*37)
		print('Cluster Enabled '+' '*13+data['cluster']['state']+' '*3+data['cluster']['description'])


	def get_route():

		print('\n')
		print('+'+'-'*30+'+')
		print('  *** Additional Information***\n')
		print('ROUTE'+' '*8+'DESTINATION'+' '*8+'GATEWAY'+' '*10+'INTERFACE'
			+' '*3+'TYPE'+' '*5+'STATUS')
		e = 0
		for i in data['routes']:
			des = len(i['destination'])
			gate = len(i['gateway'])
			face = len(i['interface'])
			types = len(i['type'])
			stat = len(i['status'])
			route = ('route-00'+str(e))
			print(route,' '*2,i['destination'],' '*(17-des),i['gateway'],' '*(15-gate),
				i['interface'],' '*(10-face),i['type'],' '*(7-types),i['status'])
			e+=1

	def get_version():

		print('\n')
		print('+'+'-'*30+'+')
		print('  *** General Information***\n')
		print('* Product Name: ',data['version']['product'])
		print('* Version: ',data['version']['version'])
		print('* Asn: ',data['version']['asn'])
		print('* Csn: ',data['version']['csn'])
		print('* part Name: ',data['version']['part'])
		print('* ak_version: ',data['version']['ak_version'])
		print('* os_version: ',data['version']['os_version'])
		print('* bios_version: ',data['version']['bios_version'])


	def get_updates():

		print('\n')
		print('+'+'-'*30+'+')
		print('  *** UPDATES ***\n')
		# print(data)
		for i in data['updates']:
			print('* Name: ',i['install_date'])
			print('* Version: ',i['version'])
			print('* Status: ',i['status'])
			print("\n")




	def get_disk():

		def con_mb(mb):
			gb = (mb/1024)

			if gb > 100:
				pb = (gb/1.126e+6)

				out = str("{:.2f}".format(pb))+" Pib"
				return out
			else:
				out = str("{:.2f}".format(gb))+" Gib"
				return out

		root = con_mb(data['disks']['root'])
		var = con_mb(data['disks']['var'])
		update = con_mb(data['disks']['update'])
		stash = con_mb(data['disks']['stash'])
		dump = con_mb(data['disks']['dump'])
		cores = con_mb(data['disks']['cores'])
		free = con_mb(data['disks']['free'])


		print('\n')
		print('+'+'-'*30+'+')
		print('  *** DISK DETAILS***\n')
		print('Profile'+' '*(4)+'   '+'Root'+' '*9+'Var'+' '*10+'Update'
			+' '*7+'Stash'+' '*8+'Dump'+' '*9+'Cores'+' '*8+'Free')
		print('-'*11+'   '+'-'*10+'   '+'-'*10+'   '+'-'*10+'   '+'-'*10+'   '+'-'*10+'   '+'-'*10+'   '+'-'*10)
		print(data['disks']['profile']+' '*10+root+' '*(5)+var+' '*5+update+' '*5+stash
			+' '*5+dump+' '*4+cores+' '*5+free)
		print('\n')

	def get_memory():

		def con_mb(mb):
			gb = (mb/1024)

			if gb > 100:
				pb = (gb/1.126e+6)

				out = str("{:.2f}".format(pb))+" Pib"
				return out
			else:
				out = str("{:.2f}".format(gb))+" Gib"
				return out

		cache = con_mb(data['memory']['cache'])
		unused = con_mb(data['memory']['unused'])
		management = con_mb(data['memory']['management'])
		other = con_mb(data['memory']['other'])
		kernel = con_mb(data['memory']['kernel'])


		print('\n')
		print('+'+'-'*30+'+')
		print('  *** MEMORY ***\n')
		print('* Cache: ',cache)
		print('* Unused: ',unused)
		print('* Management: ',management)
		print('* other: ',other)
		print('* kernel: ',kernel)


	get_chassis()
	get_services()
	get_cluster()
	get_route()
	get_version()
	get_updates()
	get_disk()
	get_memory()

def main(args):
	storage = args['<STORAGE>']
	get_data(storage)
	get_val()


if __name__ == '__main__':
	"""Main method will be executed within try:except block so that, when
	ctrl+C is pressed, it will not print any call tracebacks on the console.
	"""
	try:
		ARGS = get_args()

		main(ARGS)
	except KeyboardInterrupt:
		print('\nReceived Ctrl^C. Exiting....')
	except OSError:
		print('\nSERVER is down or not found....')
	except Exception:
		ETRACE = traceback.format_exc()
		print(ETRACE)