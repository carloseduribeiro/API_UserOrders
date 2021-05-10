from datetime import datetime
from decimal import Decimal

import MySQLdb

from flaskr.auth import DB_NAME, DB_PASSWD, DB_PORT, DB_USER, DB_HOST

try:
    conn = MySQLdb.connect(db=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWD)
    conn.autocommit(True)
    cursor = conn.cursor()
except MySQLdb.OperationalError as error:
    print("Error: " + error.args[1])


# Returns a dict with user information or None whether operation not performed:
def insert(data: dict) -> dict:
    columns = [col for col in data.keys()]
    columns.append("created_at")
    values = [val for val in data.values()]
    created_at = datetime.now().isoformat(sep=' ', timespec='seconds')
    values.append(created_at)

    sql = f"INSERT INTO users (id, {', '.join(columns)}) VALUES (default{', %s' * len(columns)});"

    result_data = None

    try:
        cursor.execute(sql, values)

        # Mount a dict to return:
        if cursor.rowcount == 1:
            result_data = {}
            result_data = dict(id=cursor.lastrowid)
            result_data.update(data)
            result_data['created_at'] = created_at
    except MySQLdb.OperationalError as e:
        print(e.args[1])
    except MySQLdb.ProgrammingError as e:
        print(e.args[1])
    except MySQLdb.DataError as e:
        print(e.args[1])

    return result_data


# Returns a dict with user information or None whether operation not performed:
def update(data: dict, id_user: int) -> dict:
    columns = [f"{col} = %s" for col in data.keys()]
    columns.append("updated_at = %s")
    values = [val for val in data.values()]
    updated_at = datetime.now().isoformat(sep=' ', timespec='seconds')
    values.append(updated_at)
    values.append(id_user)

    sql = f"UPDATE users SET {', '.join(columns)} WHERE id = %s;"

    result_data = None

    try:
        cursor.execute(sql, values)

        # Mount a dict to return:
        if cursor.rowcount == 1:
            result_data = get_by_id(id_user)
    except MySQLdb.OperationalError as e:
        print(e.args[1])
    except MySQLdb.ProgrammingError as e:
        print(e.args[1])
    except MySQLdb.DataError as e:
        print(e.args[1])

    return result_data


# Returns False whether operation not performed:
def delete(id_user: int) -> bool:
    sql = "DELETE FROM users WHERE id = %s;"

    try:
        cursor.execute(sql, [id_user])
    except MySQLdb.OperationalError as e:
        print(e.args[1])
    except MySQLdb.ProgrammingError as e:
        print(e.args[1])
    except MySQLdb.DataError as e:
        print(e.args[1])

    if cursor.rowcount > 0:
        return True

    return False


# Returns a dict with user information or None whether operation not performed:
def get_by_id(id_user: int) -> dict:
    sql = "SELECT * FROM users WHERE id = %s"
    result_data = None

    try:
        cursor.execute(sql, [id_user])

        # Checks whether cursor contains data:
        received_data = cursor.fetchall()

        if cursor.rowcount > 0:
            # Gets result of the SQL command:
            columns = [i[0] for i in cursor.description]
            result_data = {}
            for key, value in zip(columns, received_data[0]):
                if type(value) == datetime:
                    val = value.isoformat(sep=' ')
                elif type(value) == Decimal:
                    val = float(value)
                else:
                    val = value
                result_data[key] = val
    except MySQLdb.OperationalError as e:
        print(e.args[1])
    except MySQLdb.ProgrammingError as e:
        print(e.args[1])
    except MySQLdb.DataError as e:
        print(e.args[1])

    return result_data


# Returns a list with all users or None whether operation not performed:
def get_all() -> list:
    sql = "SELECT * FROM users;"

    result_data = None

    try:
        cursor.execute(sql)

        if cursor.rowcount > 0:
            # Gets result of the SQL command:
            columns = [i[0] for i in cursor.description]
            result_data = []
            for entity in cursor.fetchall():
                entty = {}
                for key, value in zip(columns, entity):
                    if type(value) == datetime:
                        val = value.isoformat(sep=' ')
                    elif type(value) == Decimal:
                        val = float(value)
                    else:
                        val = value
                    entty[key] = val
                result_data.append(entty)
    except MySQLdb.OperationalError as e:
        print(e.args[1])
    except MySQLdb.ProgrammingError as e:
        print(e.args[1])
    except MySQLdb.DataError as e:
        print(e.args[1])

    return result_data
