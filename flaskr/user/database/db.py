import MySQLdb

from flaskr.auth import DB_NAME, DB_PASSWD, DB_PORT, DB_USER, DB_HOST

try:
    conn = MySQLdb.connect(db=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWD)
    conn.autocommit(True)
    cursor = conn.cursor()
except MySQLdb.OperationalError as error:
    print("Error: " + error.args[1])
