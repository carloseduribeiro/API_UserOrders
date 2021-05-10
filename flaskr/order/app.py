from json import dumps
from json import loads

from flask import Flask, request

from database import db
from flaskr.user.utils import id_exists

app = Flask("__name__")


@app.route("/orders", methods=["GET"])
def get_all():
    response_data = db.get_all()

    if response_data:
        return dumps(response_data), 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


@app.route("/orders/user/<int:user_id>", methods=["GET"])
def get_by_user_id(user_id=None):
    if not user_id:
        response = dict(status=400, error="User id was not provided!", message="Check the user id.")
        return response, 400

    # Checks if the ID exists:
    if not id_exists("users", user_id):
        response = dict(status=400, error="User id not exists!", message="Check the user information.")
        return response, 400

    response_data = db.get_by_user_id(user_id)

    if response_data:
        return dumps(response_data), 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_by_id(order_id):
    if not order_id:
        response = dict(status=400, error="Order id was not provided!", message="Check the order id.")
        return response, 400

    # Checks if the ID exists:
    if not id_exists("orders", order_id):
        response = dict(status=400, error="Order id not exists!", message="Check the order information.")
        return response, 400

    response_data = db.get_by_id(order_id)

    if response_data:
        return dumps(response_data), 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


@app.route("/orders", methods=["POST"])
def save():
    body_request = loads(request.data.decode('utf-8'))

    # Checks whether the body request is as expected:
    expected = ["id_user", "item_description", "item_quantity", "item_price"]
    received = list(body_request.keys())
    expected.sort()
    received.sort()
    if expected != received:
        response = dict(status=400, error="Invalid body request!", message="Enter all the order information.")
        return response, 400

    try:
        id_user = int(body_request["id_user"])
        # Checks if the ID exists:
        if not id_exists("users", body_request["id_user"]):
            raise ValueError("User id not exists!")
    except ValueError as error:
        response = dict(status=400, error=error.args[0], message="Check the order information.")
        return response, 400

    try:
        item_quantity = int(body_request["item_quantity"])
    except ValueError:
        response = dict(status=400, error="Invalid body request!", message="The item_quantity is not an integer.")
        return response, 400

    try:
        item_price = float(body_request["item_price"])
    except ValueError:
        response = dict(status=400, error="Invalid body request!",
                        message="The item_price is not an decimal or integer.")
        return response, 400

    item_description = str(body_request["item_description"])

    order_data = dict(
        id_user=id_user,
        item_description=item_description,
        item_quantity=item_quantity,
        item_price=item_price)

    response_data = db.insert(order_data)

    if response_data:
        return dumps(response_data), 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


@app.route("/orders", methods=["PUT"])
def update():
    body_request = loads(request.data.decode('utf-8'))

    # Checks whether the body request is as expected:
    expected = ["id", "item_description", "item_quantity", "item_price"]
    received = list(body_request.keys())
    # Checks if the body request keys is in expected keys:
    if not set(received).issubset(expected):
        result = dict(status=400, error="Invalid body request!", message="Check the order information.")
        return result, 400

    try:
        int(body_request["id"])
        # Checks if the ID exists:
        if not id_exists("orders", body_request["id"]):
            raise ValueError("Order id not exists!")
    except ValueError as error:
        result = dict(status=400, error=error.args[0], message="Check the order information.")
        return result, 400

    if "item_quantity" in received:
        try:
            int(body_request["item_quantity"])
        except ValueError:
            response = dict(status=400, error="Invalid body request!", message="The item_quantity is not an integer.")
            return response, 400

    if "item_price" in received:
        try:
            float(body_request["item_price"])
        except ValueError:
            response = dict(
                status=400,
                error="Invalid body request!",
                message="The item_price is not an decimal or integer.")
            return response, 400

    received_data = body_request.copy()
    id_order = received_data["id"]
    received_data.pop("id")

    response_data = db.update(received_data, id_order)

    if response_data:
        return dumps(response_data), 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


@app.route("/orders/<int:id_order>", methods=["DELETE"])
def delete(id_order: int):
    if not id_order:
        response = dict(status=400, error="Order id was not provided!", message="Check the order id.")
        return response, 400

    # Checks if the ID exists:
    if not id_exists("orders", id_order):
        response = dict(status=400, error="Order id not exists!", message="Check the Order information.")
        return response, 400

    result = db.delete(id_order)

    if result:
        response = dict(status=200, message="User has been deleted.")
        return response, 200
    else:
        response = dict(status=500, error="Internal server error.", message="Please contact the suport.")
        return response, 500


if __name__ == "__main__":
    app.run(debug=True)
