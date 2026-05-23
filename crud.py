from conn import get_connection


def add_inventory(name, quantity, price, date_added, category, current_user):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO inventory (name,quantity,price,date_added,category,user_id) VALUES(%s,%s,%s,%s,%s,%s)",
                   (name, quantity, price, date_added, category, current_user)
                   )
    connection.commit()
    connection.close()


def get_inventory_by_id(current_user, inventory_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM inventory WHERE user_id = %s AND inventory_id = %s",
                   (current_user, inventory_id)
                   )
    row = cursor.fetchone()
    connection.close()
    return row


def get_inventory_by_dateadded(current_user, date_added):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM inventory WHERE user_id =%s AND date_added = %s",
                   (current_user, date_added)
                   )
    rows = cursor.fetchall()
    connection.close()
    return rows


def delete_inventory(current_user, inventory_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM inventory WHERE user_id = %s AND inventory_id = %s",
                   (current_user, inventory_id)
                   )
    connection.commit()
    connection.close()


def update_inventory(name, quantity, price, date_added, category, current_user, inventory_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE inventory SET name = %s, quantity = %s, price = %s, "
        "date_added = %s, category = %s WHERE user_id = %s AND inventory_id = %s",
        (name, quantity, price, date_added, category, current_user, inventory_id)
    )
    if cursor.rowcount == 0:
        connection.close()
        return {"Message": "Inventory not found"}
    connection.commit()
    connection.close()


def add_admin(user_name, email, password):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO admin (user_name, email, password) VALUES(%s,%s,%s)",
                   (user_name, email, password)
                   )
    connection.commit()
    connection.close()


def get_admin(email):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM admin WHERE email = %s",
                   (email,)
                   )
    row = cursor.fetchone()
    connection.close()
    return row


def delete_admin(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM admin WHERE user_id = %s",
                   (user_id,)
                   )
    connection.commit()
    connection.close()


def update_admin(user_name, email, password, current_user):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE admin SET user_name = %s, email = %s, password = %s WHERE user_id = %s",
                   (user_name, email, password, current_user)
                   )
    if cursor.rowcount == 0:
        connection.close()
        return {"Message": "admin not found"}
    connection.commit()
    connection.close()
    return {"Message": "admin updated"}
