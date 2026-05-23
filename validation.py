def validate_inventory(data):

    name = data.get("name")
    quantity = data.get("quantity")
    price = data.get("price")
    date_added = data.get("date_added")

    if name is None or name == "":
        return {"Error": "Validation error",
                "Message": "Name cant be empty"
                }, 400

    if quantity is None or quantity == "":
        return {"Error": "Validation error",
                "Message": "quantity cant be empty"
                }, 400

    if price is None or price == "":
        return {"Error": "Validation error",
                "Message": "Price cant be empty"
                }, 400

    if date_added is None or date_added == "":
        return {"Error": "Validation error",
                "Message": "date_added cant be empty"
                }, 400

    if not isinstance(name, str):
        return {"Error": "Validation error",
                "Message": "Name must be text"
                }, 400

    if not isinstance(date_added, int):
        return {"Error": "Validation error",
                "Message": "date_added must be numbers"
                }, 400

    try:
        quantity = int(quantity)
    except ValueError:
        return {"Error": "Validation error",
                "Message": "quantity must be numbers"
                }, 400

    try:
        price = float(price)
    except ValueError:
        return {"Error": "Validation error",
                "Message": "price must be numbers"
                }, 400

    if price <= 0:
        return {"Error": "Validation error",
                "Message": "price must be positive"
                }, 400

    if quantity <= 0:
        return {"Error": "Validation error",
                "Message": "quantity must be positive"
                }, 400

    return {"name": name,
            "quantity": quantity,
            "price": price,
            "date_added": date_added
            }


def validate_register_admin(data):
    user_name = data.get("user_name")
    email = data.get("email")
    password = data.get("password")

    if user_name is None or user_name == "":
        return {"Error": "Validation error",
                "Message": "user_name cant be empty"
                }, 400

    if email is None or email == "":
        return {"Error": "Validation error",
                "Message": "email cant be empty"
                }, 400

    if password is None or password == "":
        return {"Error": "Validation error",
                "Message": "password cant be empty"
                }, 400

    if not isinstance(user_name, str):
        return {"Error": "Validation error",
                "Message": "user_name must be text"
                }, 400

    if not isinstance(email, str):
        return {"Error": "Validation error",
                "Message": "email must be text"
                }, 400

    if not isinstance(password, str):
        return {"Error": "Validation error",
                "Message": "password must be text"
                }, 400

    return {"user_name": user_name,
            "email": email,
            "password": password
            }


def validate_admin_login(data):
    email = data.get("email")
    password = data.get("password")

    if email is None or email == "":
        return {"Error": "Validation error",
                "Message": "email cant be empty"
                }, 400

    if password is None or password == "":
        return {"Error": "Validation error",
                "Message": "password cant be empty"
                }, 400

    if not isinstance(email, str):
        return {"Error": "Validation error",
                "Message": "email must be text"
                }, 400

    if not isinstance(password, str):
        return {"Error": "Validation error",
                "Message": "password must be text"
                }, 400

    return {
        "email": email,
        "password": password
    }
