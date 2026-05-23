import bcrypt
import os
from functools import wraps
from flask import Flask, request
import jwt
from ai_function import categorize_inventory
from validation import (
    validate_inventory,
    validate_register_admin,
    validate_admin_login
)

from datetime import datetime, timezone, timedelta

from crud import (
    add_inventory,
    get_inventory_by_dateadded,
    get_inventory_by_id,
    delete_inventory,
    update_inventory,
    add_admin,
    get_admin,
    delete_admin,
    update_admin
)


app = Flask(__name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"Error": "Authentication eror",
                    "Message": "Invalid token"
                    }, 401

        try:
            token = token.split(" ")[1]

            data = jwt.decode(
                token,
                app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            current_user = data["user_id"]
        except jwt.ExpiredSignatureError:
            return {"Error": "Authentication eror",
                    "Message": "Session expired"
                    }, 401
        except jwt.InvalidTokenError:
            return {"Error": "Authentication eror",
                    "Message": "Invalid token"
                    }, 401

        return f(current_user, *args, **kwargs)
    return decorated


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
print("SECRET_KEY =", os.getenv("SECRET_KEY"))


@app.route("/inventory", methods=["POST"])
@token_required
def new_inventory(current_user):
    data = request.get_json()

    validated_inventory = validate_inventory(data)
    if isinstance(validated_inventory, tuple):
        return validated_inventory

    name = validated_inventory["name"]
    quantity = validated_inventory["quantity"]
    price = validated_inventory["price"]
    date_added = validated_inventory["date_added"]

    category = categorize_inventory(name)

    add_inventory(name, quantity, price, date_added, category, current_user)

    return {
        "Message": "Inventory successfully created"
    }, 200


@app.route("/inventory/<int:inventory_id>", methods=["GET"])
@token_required
def select_inventory_by_id(current_user, inventory_id):
    result = get_inventory_by_id(current_user, inventory_id)
    return {"inventory": result
            }, 200


@app.route("/inventory", methods=["GET"])
@token_required
def select_inventory_by_date_added(current_user):

    date_added = request.args.get("date_added")
    result = get_inventory_by_dateadded(current_user, date_added)
    return {"inventory": result
            }, 200


@app.route("/inventory/<int:inventory_id>", methods=["DELETE"])
@token_required
def remove_inventory(current_user, inventory_id):
    delete_inventory(current_user, inventory_id)
    return {
        "Message": "Inventory successfully deleted"
    }, 200


@app.route("/inventory/<int:inventory_id>", methods=["PUT"])
@token_required
def renew_inventory(current_user, inventory_id):
    data = request.get_json()

    validated_inventory = validate_inventory(data)
    if isinstance(validated_inventory, tuple):
        return validated_inventory

    name = validated_inventory["name"]
    quantity = validated_inventory["quantity"]
    price = validated_inventory["price"]
    date_added = validated_inventory["date_added"]

    category = categorize_inventory(name)

    update_inventory(name, quantity, price, date_added,
                     category, current_user, inventory_id)

    print("DEBUG DATA:", validated_inventory)
    print("DATE ADDED TYPE:", type(validated_inventory["date_added"]))

    return {
        "Message": "Inventory successfully updated"
    }, 200


@app.route("/register", methods=["POST"])
def new_admin():
    data = request.get_json()

    validated_register = validate_register_admin(data)
    if isinstance(validated_register, tuple):
        return validated_register

    user_name = validated_register["user_name"]
    email = validated_register["email"]
    password = validated_register["password"]

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    add_admin(user_name, email, hashed_password.decode("utf-8"))

    return {
        "Message": "Admin successfully created"
    }, 200


@app.route("/login", methods=["POST"])
def login_admin():
    data = request.get_json()

    validated_login = validate_admin_login(data)
    if isinstance(validated_login, tuple):
        return validated_login

    email = validated_login["email"]
    password = validated_login["password"]

    user = get_admin(email)

    if not user:
        return {"Error": "Validation error",
                "Message": "User not found"
                }, 404

    stored_password = user[3]

    check_password = bcrypt.checkpw(
        password.encode("utf-8"),
        stored_password.encode("utf-8")
    )

    if not check_password:
        return {"Error": "Validation error",
                "Message": "Wrong password"
                }, 400

    token = jwt.encode(
        {
            "user_id": user[0],
            "exp": datetime.now(timezone.utc) + timedelta(days=8)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return {"Message": "Login successful",
            "Token": token
            }, 200


@app.route("/admin/<int:user_id>", methods=["DELETE"])
@token_required
def remove_admin(current_user, user_id):
    delete_admin(user_id)

    return {"Message": "Admin successfully deleted"
            }, 200


@app.route("/admin/<int:user_id>", methods=["PUT"])
@token_required
def renew_admin(current_user, user_id):
    data = request.get_json()

    validated_admin = validate_register_admin(data)
    if isinstance(validated_admin, tuple):
        return validated_admin

    user_name = validated_admin["user_name"]
    email = validated_admin["email"]
    password = validated_admin["password"]

    update_admin(user_name, email, password, user_id)

    return {"Message": "Admin updated successfully"
            }, 200


@app.route("/ai-categorize", methods=["POST"])
@token_required
def ai_categorize(current_user):
    data = request.get_json()

    field = data.get("field")
    if not field:
        return {"Error": "field is required"}, 400

    category = categorize_inventory(field)

    return {"Message": "Category successfully generated",
            "field": field,
            "category": category
            }, 200


if __name__ == "__main__":
    app.run(debug=True)
