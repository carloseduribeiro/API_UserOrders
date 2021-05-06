from datetime import datetime
from json import loads

from flask import Flask, request

from utils import exectute_sql_command, keys_to_str_sql_format

app = Flask("__name__")


@app.route("/users", methods=["GET"])
def get_all():
    sql = "SELECT * FROM user;"
    return exectute_sql_command(sql)


@app.route("/user/<int:user_id>", methods=["GET"])
def get(user_id=None):
    if not user_id:
        result = dict(status=400, message="Check the user id.", error="User id was not provided!")
        return result, 400

    sql = "SELECT * FROM user WHERE id = %s;"

    return exectute_sql_command(sql, user_id, error_msg="User id not found!")


@app.route("/user", methods=["POST"])
def save():
    # Gets the body request:
    body_request = loads(request.data.decode('utf-8'))

    # Checks whether the body request is as expected:
    expected = ["name", "cpf", "email", "phone_number"]
    received = list(body_request.keys())
    expected.sort()
    received.sort()
    if expected != received:
        result = dict(status=400, message="Enter all the user information.", error="Invalid body request!")
        return result, 400

    # Mount the SQL command and values list:
    sql = f"INSERT INTO user ({', '.join(expected)}, created_at) VALUES (%s, %s, %s, %s, %s);"
    values = list(body_request[x] for x in expected)
    values.append(datetime.now().isoformat(sep=' ', timespec='seconds'))

    return exectute_sql_command(sql, error_msg="User not saved!")


@app.route("/user", methods=["PUT"])
def update():
    # Gets the body request:
    body_request = loads(request.data.decode('utf-8'))

    # Gets the body request keys:
    received = list(body_request.keys())

    # Ckecks whether user id was provided:
    if 'id' not in received:
        result = dict(status=400, message="Check the user id.", error="User id was not provided!")
        return result, 400

    # Checks whether body request is valid:
    expect = ["id", "name", "email", "phone_number"]
    received = list(body_request.keys())
    # Checks if the body request keys is in expected keys:
    if not set(received).issubset(expect):
        result = dict(status=400, message="Check the user information.", error="Invalid body request!")
        return result, 400

    # Gets the columns and mount the SQL update command and value list:
    received.pop(received.index('id'))
    values = [body_request[key] for key in received]
    values.append(datetime.now().isoformat(sep=' ', timespec='seconds'))
    values.append(body_request["id"])
    sql = f"UPDATE user SET {keys_to_str_sql_format(received)}, updated_at = %s WHERE id = %s;"

    return exectute_sql_command(sql, values, success_msg="User updated!", error_msg="User not saved!")


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete(user_id=None):
    if not user_id:
        result = dict(status=400, message="Check the user id.", error="User id was not provided!")
        return result, 400

    sql = "DELETE FROM user WHERE id = %s"

    return exectute_sql_command(sql, user_id, success_msg="User deleted!", error_msg="User not deleted!")


if __name__ == "__main__":
    app.run(debug=True)
