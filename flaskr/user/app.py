from flask import Flask

app = Flask("__name__")


# @app.route("/users", methods=["GET"])
def get_all():
    pass


# @app.route("/user/<int:user_id>", methods=["GET"])
def get(user_id: int):
    pass


# @app.route("/user", methods=["POST"])
def save():
    pass


# @app.route("/user", methods=["PUT"])
def update():
    pass


# @app.route("/user", methods=["DELETE"])
def delete():
    pass


if __name__ == "__main__":
    app.run(debug=True)
