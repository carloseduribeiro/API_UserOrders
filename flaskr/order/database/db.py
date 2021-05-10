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


# Returns a dict with order information or None whether operation not performed:
def order_insert(data: dict) -> dict:
    columns = [col for col in data.keys()]
    columns.append("created_at")
    columns.append("total_price")
    values = [val for val in data.values()]
    created_at = datetime.now().isoformat(sep=' ', timespec='seconds')
    values.append(created_at)
    total_price = data["item_price"] * data["item_quantity"]
    values.append(total_price)

    sql = f"INSERT INTO orders (id, {', '.join(columns)}) VALUES (default{', %s' * len(columns)});"

    result_data = None

    try:
        cursor.execute(sql, values)

        # Mount a dict to return:
        if cursor.rowcount == 1:
            result_data = {}
            result_data = dict(id=cursor.lastrowid)
            result_data.update(data)
            result_data['total_price'] = total_price
            result_data['created_at'] = created_at
    except MySQLdb.OperationalError as e:
        print(e.args[1])
    except MySQLdb.ProgrammingError as e:
        print(e.args[1])
    except MySQLdb.DataError as e:
        print(e.args[1])

    return result_data


# Returns a dict with order information or None whether operation not performed:
def order_update(data: dict, id_order: int) -> dict:
    columns = [f"{col} = %s" for col in data.keys()]
    values = [val for val in data.values()]

    # Calculates a new total_price whether this information are received:
    if "item_price" in data.keys() or "item_quantity" in data.keys():
        columns.append("total_price = %s")

        order_info_db = order_get_by_id(id_order, "item_price", "item_quantity")

        item_price = order_info_db["item_price"]
        item_quantity = order_info_db["item_quantity"]

        # Ckecks if exists a new item price or quantity:
        if "item_price" in data.keys():
            item_price = data["item_price"]
        if "item_quantity" in data.keys():
            item_quantity = data["item_quantity"]

        total_price = round(item_price * item_quantity, 2)
        values.append(total_price)

    columns.append("updated_at = %s")
    updated_at = datetime.now().isoformat(sep=' ', timespec='seconds')
    values.append(updated_at)
    values.append(id_order)

    sql = f"UPDATE orders SET {', '.join(columns)} WHERE id = %s;"

    result_data = None

    try:
        cursor.execute(sql, values)

        # Mount a dict to return:
        if cursor.rowcount == 1:
            result_data = order_get_by_id(id_order)

    except MySQLdb.OperationalError as e:
        print(e.args[1])
    except MySQLdb.ProgrammingError as e:
        print(e.args[1])
    except MySQLdb.DataError as e:
        print(e.args[1])

    return result_data


# Returns False whether operation not performed:
def order_delete(id_order: int) -> bool:
    sql = "DELETE FROM orders WHERE id = %s;"

    try:
        cursor.execute(sql, [id_order])
    except MySQLdb.OperationalError as e:
        print(e.args[1])
    except MySQLdb.ProgrammingError as e:
        print(e.args[1])
    except MySQLdb.DataError as e:
        print(e.args[1])

    if cursor.rowcount > 0:
        return True

    return False


# Returns a dict with order information or None whether operation not performed:
def order_get_by_id(id_order: int, *columns) -> dict:
    result_data = None

    if len(columns) > 0:
        expected_columns = \
            ("id", "id_user", "item_description", "item_quantity", "item_price", "total_price", "created_at",
             "updated_at")
        if not set(columns).intersection(expected_columns):
            return result_data

    sql = f"SELECT {', '.join(columns) if len(columns) > 0 else '*'} FROM orders WHERE id = %s"

    try:
        cursor.execute(sql, [id_order])

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


# Returns a list with orders by a user by id:
def order_get_by_user_id(id_user: int) -> list:
    result_data = None

    sql = f"SELECT orders.* FROM users INNER JOIN orders ON orders.id_user = users.id WHERE orders.id_user = %s;"

    try:
        cursor.execute(sql, [id_user])

        # Checks whether cursor contains data:
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


# Returns a list with all orders or None whether operation not performed:
def order_get_all() -> list:
    sql = "SELECT * FROM orders;"

    result_data = None

    try:
        cursor.execute(sql)

        # Checks whether cursor contains data:
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
