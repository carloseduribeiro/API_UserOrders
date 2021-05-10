from json import loads, dumps

from flask import Flask, request

from database import db
from utils import id_exists

app = Flask("__name__")


@app.route("/users", methods=["GET"])
def get_all():
    response_data = db.get_all()

    if response_data:
        return dumps(response_data), 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


@app.route("/users/<int:user_id>", methods=["GET"])
def get_by_id(user_id=None):
    if not user_id:
        response = dict(status=400, error="User id was not provided!", message="Check the user id.")
        return response, 400

    # Checks if the ID exists:
    if not id_exists("users", user_id):
        response = dict(status=400, error="User id not exists!", message="Check the user information.")
        return response, 400

    response_data = db.get_by_id(user_id)

    if response_data:
        return dumps(response_data), 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


@app.route("/users", methods=["POST"])
def save():
    # Gets the body request:
    body_request = loads(request.data.decode('utf-8'))

    # Checks whether the body request is as expected:
    expected = ["name", "cpf", "email", "phone_number"]
    received = list(body_request.keys())
    expected.sort()
    received.sort()
    if expected != received:
        response = dict(status=400, error="Invalid body request!", message="Enter all the user information.")
        return response, 400

    response_data = db.insert(body_request)

    if response_data:
        return dumps(response_data), 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


@app.route("/users", methods=["PUT"])
def update():
    # Gets the body request:
    body_request = loads(request.data.decode('utf-8'))

    # Gets the body request keys:
    received = list(body_request.keys())

    # Ckecks whether user id was provided:
    if 'id' not in received:
        response = dict(status=400, error="User id was not provided!", message="Check the user id.")
        return response, 400

    # Checks if the ID exists:
    if not id_exists("users", body_request["id"]):
        response = dict(status=400, error="User id not exists!", message="Check the user information.")
        return response, 400

    # Checks whether body request is valid:
    expect = ["id", "name", "email", "phone_number"]
    received = list(body_request.keys())
    # Checks if the body request keys is in expected keys:
    if not set(received).issubset(expect):
        result = dict(status=400, message="Check the user information.", error="Invalid body request!")
        return result, 400

    received_data = body_request.copy()
    id_user = received_data["id"]
    received_data.pop("id")

    response_data = db.update(received_data, id_user)

    if response_data:
        return dumps(response_data), 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete(user_id=None):
    if not user_id:
        response = dict(status=400, error="User id was not provided!", message="Check the user id.")
        return response, 400

    # Checks if the ID exists:
    if not id_exists("users", user_id):
        response = dict(status=400, error="User id not exists!", message="Check the user information.")
        return response, 400

    response_data = db.delete(user_id)

    if response_data:
        response = dict(status=200, message="User has been deleted.")
        return response, 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


if __name__ == "__main__":
    app.run(debug=True)
