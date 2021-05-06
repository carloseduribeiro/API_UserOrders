from flask import Flask

app = Flask("__main__")


# @app.route("/orders", methods=["GET"])
def get_all():
    pass


# @app.route("/orders/user/<int:user_id>", methods=["GET"])
def get_by_user_id(user_id=None):
    pass


# @app.route("/order/<int:order_id>", methods=["GET"])
def get_by_id(order_id):
    pass


# @app.route("/order", methods=["POST"])
def save():
    pass


# @app.route("/order", methods=["PUT"])
def update():
    pass


# @app.route("/order", methods=["DELETE"])
def delete():
    pass


if app.name == "__main__":
    app.run(debug=True)
