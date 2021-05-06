from datetime import datetime

import MySQLdb

from database.db import cursor


# Converts a list keys in a string to use in SQL commands:
def keys_to_str_sql_format(data: list, separator=", "):
    sql_format = [f"{key} = %s" for key in data]
    string_values = f"{separator}".join(sql_format)
    return string_values


# Executes the SQL command and returns json with result:
def exectute_sql_command(sql: str, values=None, success_msg="Done!", error_msg="") -> tuple:
    default_message = "Internal error! Please contact the suport."

    status = 500
    message = default_message if len(error_msg) == 0 else error_msg
    error_message = ""
    sql_result = []

    # Ensure that values are an iterable object:
    if values:
        if not isinstance(values, tuple) and not isinstance(values, list):
            values = [values]

    try:
        # Exectutes the sql command:
        result = cursor.execute(sql, values)

        if result > 0:
            status = 200
            message = success_msg

            # Checks whether cursor contains data:
            data = cursor.fetchall()
            if len(data) > 0:
                # Gets result of the SQL command:
                columns = [i[0] for i in cursor.description]
                for entity in data:
                    entty = {}
                    for key, value in zip(columns, entity):
                        entty[key] = value if not type(value) == datetime else value.isoformat(sep=' ')
                    sql_result.append(entty)
        else:
            status = 400
            error_message = "Unknow Error."

    except MySQLdb.OperationalError as error:
        error_message = error.args[1]
    except MySQLdb.ProgrammingError as error:
        error_message = error.args[1]
    except MySQLdb.DataError as error:
        error_message = error.args[1]

    results = dict(status=status, message=message)
    if len(error_message) > 0:
        results['error'] = error_message
    if len(sql_result) > 0:
        results["result"] = sql_result

    return results, status
