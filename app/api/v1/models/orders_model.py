"""Orders Models"""
from .users_model import UsersModel
from app.db_config import init_db


class OrdersModel():
    """Create Orders Model"""

    def __init__(self):
        self.order_db = init_db()

    def create_order(self, data):
        """Create order and append it to orders"""
        order = {
            "pick_up_location": data['pick up location'],
            "delivery_location": data['delivery location'],
            "current_location": data['pick up location'],
            "weight": data['weight'],
            "price": data['price'],
            "status": "pending",
            "sender": data['sender']
        }

        query = """INSERT INTO orders(
                                     pickup, destination, current_location, weight, price, sender, status
                                     ) 
                                VALUES(
                                        %(pick_up_location)s, %(delivery_location)s, %(current_location)s, %(weight)s, %(price)s, %(sender)s, %(status)s
                                        )"""

        curr = self.order_db.cursor()
        curr.execute(query, order)

        self.order_db.commit()

        return order

    def get_orders(self, user_auth):
        """Get orders in database"""
        query = "SELECT * FROM orders"

        curr = self.order_db.cursor()
        curr.execute(query)

        data = curr.fetchall()

        response = []

        for row in data:
            item_resp = {}
            for i, key in enumerate(curr.description):
                item_resp[key[0]] = row[i]

            response.append(item_resp)

        return response

    def get_order(self, order_id):
        """Get a specific order from database"""
        result = {}
        query = "SELECT * FROM orders WHERE order_no={}".format(order_id)

        curr = self.order_db.cursor()
        curr.execute(query)

        data = curr.fetchone()

        if not data:
            result = {"message": "order unknown"}
        else:
            for i, key in enumerate(curr.description):
                result[key[0]] = data[i]

        return result

    def update_order(self, order_id, update_col, col_val):
        """Cancel delivery order"""
        result = {}
        update_column = ""

        if update_col == 'status':
            update_column = "status='{}'".format(col_val)
        elif update_col == 'location':
            update_column = "current_location='{}'".format(col_val)
        else:
            update_column = "destination='{}'".format(col_val)

        if_exist = self.get_order(order_id)

        if "message" in if_exist:
            result = {"message": "order unknown"}
        else:
            query = "UPDATE orders SET {} WHERE order_no={}".format(
                update_column, order_id)
            curr = self.order_db.cursor()
            curr.execute(query)
            self.order_db.commit()

            result = self.get_order(order_id)

        return result

    def get_user_orders(self, user_id):
        """Get orders created by specific order"""
        query = "SELECT * FROM orders WHERE sender={}".format(user_id)

        curr = self.order_db.cursor()
        curr.execute(query)

        data = curr.fetchall()

        response = []

        for row in data:
            item_resp = {}
            for i, key in enumerate(curr.description):
                item_resp[key[0]] = row[i]

            response.append(item_resp)

        return response

    def get_order_amount(self, user_id, status_type):
        """Get delivered orders for a specific user"""
        num = 0
        db_query = ""
        if status_type == 'delivered':
            db_query = "SELECT COUNT(*) FROM orders WHERE status='delivered' and sender={}".format(
                user_id)
        else:
            db_query = "SELECT COUNT(*) FROM orders WHERE status='in-transit' and sender={}".format(
                user_id)

        curr = self.order_db.cursor()
        curr.execute(db_query)
        data = curr.fetchone()

        num = data[0]

        return num


class ValidateInputs():
    """Class to validate inputs entered by user"""

    def __init__(self, fetch_data, data_for):
        self.user_input = fetch_data
        self.data_for = data_for

    def confirm_input(self):
        """Confirm if there is user input"""
        message = "Bad request, No data entered"
        if self.user_input:
            if self.data_for == "create_user":
                message = self.create_user_inputs()
            elif self.data_for == "create_order":
                message = self.create_order_inputs()
            elif self.data_for == "update_status":
                message = self.update_status_inputs()
            elif self.data_for == "change_location":
                message = self.update_location_inputs()
            elif self.data_for == "signin":
                message = self.user_signin_inputs()
            else:
                message = self.change_delivery_inputs()

        return message

    def create_user_inputs(self):
        """confirm inputs for creating user"""
        if not self.user_input['username']:
            message = "username missing"
        elif not self.user_input['first_name']:
            message = "first name  missing"
        elif not self.user_input['second_name']:
            message = "second name  missing"
        elif not self.user_input['email']:
            message = "email  missing"
        elif not self.user_input['location']:
            message = "location  missing"
        elif not self.user_input['gender']:
            message = "gender missing"
        elif not self.user_input['type']:
            message = "type missing"
        elif not self.user_input['password']:
            message = "password missing"
        else:
            message = "ok"

        return message

    def user_signin_inputs(self):
        """confirm inputs for user signin"""
        if not self.user_input['username']:
            message = "username missing"
        elif not self.user_input['password']:
            message = "password missing"
        else:
            message = "ok"

        return message

    def create_order_inputs(self):
        """confirm inputs for creating order"""
        if not self.user_input['pick up location']:
            message = "pickup location missing"
        elif not self.user_input['delivery location']:
            message = "delivery locationv missing"
        elif not self.user_input['weight']:
            message = "weight missing"
        elif not self.user_input['price']:
            message = "price missing"
        elif not self.user_input['sender']:
            message = "sender missing"
        else:
            message = "ok"

        return message

    def change_delivery_inputs(self):
        """confirm inputs for changing delivery location"""
        if not self.user_input['delivery location']:
            message = "delivery location missing"
        else:
            message = "ok"

        return message

    def update_location_inputs(self):
        """confirm inputs for changing current location"""
        if not self.user_input['current location']:
            message = "current location missing"
        else:
            message = "ok"

        return message

    def update_status_inputs(self):
        """confirm inputs for changing delivery order status"""
        if not self.user_input['status']:
            message = "status missing"
        else:
            message = "ok"

        return message
