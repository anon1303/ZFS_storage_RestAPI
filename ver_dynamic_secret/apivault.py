import requests
import json

"""
    Version 1 on the program that will request credentials from the vault 
    that will be used to open the MYSQL database
"""
def init_server():

    response = requests.get(
    'http://127.0.0.1:8200/v1/database/creds/my_role',
    params={'q': 'requests+language:python'},
    headers={'X-Vault-Token': 's.AxQp2ia1K46wn0XtIlsiPGPq'},
    )
    json_response = response.json()
    return json_response    


