import mysql.connector
import apivault

"""
    Version 1 on the program that will GET the credentials from the MYSQL database using
    the dynamic credentials generated from vault 
"""
vault1 = apivault.init_server() 

def doQuery( conn ) :
    cur = conn.cursor()

    cur.execute( "SELECT * FROM secret" )

    data = cur.fetchone()
    return data
       

def vault():
  cnx = mysql.connector.connect(
      host='localhost',
      database='mysql-db',
      user=vault1['data']['username'],
      password=vault1['data']['password'],
      port=3306
  )

  return doQuery( cnx )
  cnx.close()

