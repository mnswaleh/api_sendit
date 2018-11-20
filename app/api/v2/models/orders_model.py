"""Orders Models"""
import re
from app.db_config import init_db
from app.api.v2.models.users_model import UsersModel
from app.api.v2.models.users_model import AuthenticateUser
from validate_email import validate_email

class OrdersModel():
    """Create Orders Model"""

    def __init__(self):
        self.order_db = init_db()
        self.user_db = UsersModel()
        self.user_auth = AuthenticateUser()

    def create_order(self, data, user_auth):
        """Create order and append it to orders"""
        response = {}
        order = {
            "pick_up_location": data['pick up location'],
            "delivery_location": data['delivery location'],
            "current_location": data['pick up location'],
            "weight": data['weight'],
            "price": data['price'],
            "status": "pending",
            "sender": user_auth
        }
        user_details = self.user_db.get_user(user_auth)
        if user_details['type'] == 'user':
            query = """INSERT INTO orders(pickup, destination, current_location, weight, price, sender, status) VALUES(%(pick_up_location)s, %(delivery_location)s, %(current_location)s, %(weight)s, %(price)s, %(sender)s, %(status)s)"""

            curr = self.order_db.cursor()
            curr.execute(query, order)
            self.order_db.commit()

            response = order
        else:
            response = {"ERROR": "Forbidden access!! You do not have permission to create order"}

        return response

    def get_orders(self, user_auth):
        """Get orders in database"""
        response = []

        if self.user_auth.auth_admin(user_auth):
            query = "SELECT * FROM orders"
            curr = self.order_db.cursor()
            curr.execute(query)
            data = curr.fetchall()

            for row in data:
                item_resp = {}
                for i, key in enumerate(curr.description):
                    item_resp[key[0]] = row[i]

                response.append(item_resp)
        else:
            response = [{"ERROR": "Forbidden access!! You do not have permission to view this orders"}]

        return response

    def get_order(self, order_id, user_auth=0):
        """Get a specific order from database"""
        result = {}
        query = "SELECT * FROM orders WHERE order_no={}".format(order_id)

        curr = self.order_db.cursor()
        curr.execute(query)

        data = curr.fetchone()

        if not data:
            result = {"message": "order unknown"}
        elif user_auth != 0:
            for i, key in enumerate(curr.description):
                result[key[0]] = data[i]
            user_details = self.user_db.get_user(user_auth)
            if result['sender'] == user_auth or user_details['type'] == 'admin':
                pass
            else:
                result = {"ERROR": "Forbidden access!! You do not have permission to view this order"}
        else:
            for i, key in enumerate(curr.description):
                result[key[0]] = data[i]

        return result

    def update_order(self, order_id, update_col, col_val, user_id):
        """Cancel delivery order"""
        result = {}
        update_column = ""
        if_exist = self.get_order(order_id)

        if "message" in if_exist:
            result = {"message": "order unknown"}
        elif self.user_auth.auth_change(user_id, update_col, if_exist['sender']):
            if update_col == 'status':
                update_column = "status='{}'".format(col_val)
            elif update_col == 'cancel':
                update_column = "status='{}'".format(col_val)
            elif update_col == 'location':
                update_column = "current_location='{}'".format(col_val)
            else:
                update_column = "destination='{}'".format(col_val)

            query = "UPDATE orders SET {} WHERE order_no={}".format(
                update_column, order_id)
            curr = self.order_db.cursor()
            curr.execute(query)
            self.order_db.commit()

            result = self.get_order(order_id)
        else:
            result = {"ERROR": "Forbidden access!! You do not have permission to Update this order"}

        return result

    def get_user_orders(self, user_id, auth_user):
        """Get orders created by specific order"""
        response = []
        user_details = self.user_db.get_user(auth_user)
        if user_id == auth_user or user_details['type'] == 'admin':
            query = "SELECT * FROM orders WHERE sender={}".format(user_id)

            curr = self.order_db.cursor()
            curr.execute(query)

            data = curr.fetchall()
            for row in data:
                item_resp = {}
                for i, key in enumerate(curr.description):
                    item_resp[key[0]] = row[i]

                response.append(item_resp)
        else:
            response = [{"ERROR": "Forbidden access!! You do not have permission to view this orders"}]

        return response

    def get_order_amount(self, user_id, status_type, auth_user):
        """Get delivered orders for a specific user"""
        user_details = self.user_db.get_user(auth_user)
        if user_id == auth_user or user_details['type'] == 'admin':
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
        else:
            return "Forbid"


class ValidateInputs():
    """Class to validate inputs entered by user"""

    def __init__(self, fetch_data, data_for):
        self.user_input = fetch_data
        self.data_for = data_for
        self.user_db = UsersModel()

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
        if not re.match("^[a-zA-Z]{1}[a-zA-Z0-9]{2,7}$", self.user_input['username']):
            message = "username should start with a letter and be between 3-10 alphanumeric characters"
        elif not re.match("^[a-zA-Z]{3,20}$", self.user_input['first_name']):
            message = "First name should be between 3-20 alphabetical characters"
        elif not re.match("^[a-zA-Z]{3,20}$", self.user_input['second_name']):
            message = "Second name should be between 3-20 alphabetic characters"
        elif not validate_email(self.user_input['email'], verify=True):
            message = "Invalid email"
        elif not re.match("^[a-zA-Z]{3,20}$", self.user_input['location']):
            message = "Location should be between 3-20 alphabeticcharacters"
        elif self.user_input['gender'] != "male" and self.user_input['gender'] != "female":
            message = "gender should be 'male' or 'female'"
        elif self.user_input['type'] != "admin" and self.user_input['type'] != "user":
            message = "user type should be 'admin' or 'user'"
        elif not re.match("^[a-zA-Z0-9]{6,20}$", self.user_input['password']):
            message = "password should have capital letter,small letter, number and be between 6-10 alphanumeric characters"
        else:
            message = self.user_db.get_username(self.user_input['username'])

        return message

    def user_signin_inputs(self):
        """confirm inputs for user signin"""
        if not re.match("^[a-zA-Z]{1}[a-zA-Z0-9]{2,7}$", self.user_input['username']):
            message = "username missing"
        elif not re.match("^[a-zA-Z0-9]{6,20}$", self.user_input['password']):
            message = "password missing"
        else:
            message = "ok"

        return message

    def create_order_inputs(self):
        """confirm inputs for creating order"""
        if not re.match("^[a-zA-Z]{3,20}$", self.user_input['pick up location']):
            message = "Pick up location should be between 3-20 alphabetic characters"
        elif not re.match("^[a-zA-Z]{3,20}$", self.user_input['delivery location']):
            message = "Delivery location should be between 3-20 alphabetic characters"
        elif not isinstance(self.user_input['weight'], (int, float)):
            message = "Weight should be decimal number"
        elif not isinstance(self.user_input['weight'], (int, float)):
            message = "price should be decimal number"
        else:
            message = "ok"

        return message

    def change_delivery_inputs(self):
        """confirm inputs for changing delivery location"""
        if not re.match("^[a-zA-Z]{3,20}$", self.user_input['delivery location']):
            message = "Delivery location should be between 3-20 alphabetic characters"
        else:
            message = "ok"

        return message

    def update_location_inputs(self):
        """confirm inputs for changing current location"""
        if not re.match("^[a-zA-Z]{3,20}$", self.user_input['current location']):
            message = "current location should be between 3-20 alphabetic characters"
        else:
            message = "ok"

        return message

    def update_status_inputs(self):
        """confirm inputs for changing delivery order status"""
        message = "ok"
        if self.user_input['status'] != "pending" and self.user_input['status'] != "in transit":
            if self.user_input['status'] != "delivered" and self.user_input['status'] != "canceled":
                message = "status should be 'pending', 'in transit', 'delivered' or canceled"
            

        return message
        
