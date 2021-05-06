from datetime import datetime

import MySQLdb

from database.db import cursor


# Converts a list keys in a string to use in SQL commands:
def keys_to_str_sql_format(data: list, separator=", "):
    sql_format = [f"{key} = %s" for key in data]
    string_values = f"{separator}".join(sql_format)
    return string_values


# Executes the SQL command and returns json with result:
def exectute_sql_command(sql: str, values=None, success_msg="", error_msg="") -> tuple:
    default_message = "Internal error! Please contact the suport."

    status = 500
    error_message = ""
    message = success_msg
    result_data = []

    # Ensure that values are an iterable object:
    if values:
        if not isinstance(values, tuple) and not isinstance(values, list):
            values = [values]

    try:
        # Exectutes the sql command:
        result = cursor.execute(sql, values)

        if result > 0:
            status = 200

            # Checks whether cursor contains data:
            data = cursor.fetchall()
            if len(data) > 0:
                # Gets result of the SQL command:
                columns = [i[0] for i in cursor.description]
                for entity in data:
                    entty = {}
                    for key, value in zip(columns, entity):
                        entty[key] = value if not type(value) == datetime else value.isoformat(sep=' ')
                    result_data.append(entty)
        else:
            status = 400
            message = error_msg

    except MySQLdb.OperationalError as error:
        error_message = error.args[1]
        message = default_message if len(error_msg) == 0 else error_msg
    except MySQLdb.ProgrammingError as error:
        error_message = error.args[1]
        message = default_message if len(error_msg) == 0 else error_msg
    except MySQLdb.DataError as error:
        error_message = error.args[1]
        message = default_message if len(error_msg) == 0 else error_msg

    json_result = dict(status=status)
    if len(message) > 0:
        json_result['message'] = message
    if len(error_message) > 0:
        json_result['error'] = error_message
    if len(result_data) > 0:
        json_result['result'] = result_data

    return json_result, status


# Returns true if a id exists
def id_exists(table: str, id_entity: int) -> bool:
    sql = f"SELECT id FROM {table} WHERE id = %s;"
    result = cursor.execute(sql, [id_entity])
    return True if result > 0 else False
