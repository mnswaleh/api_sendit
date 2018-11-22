"""Orders Models"""
import re
from validate_email import validate_email
from app.db_config import init_db
from app.api.v2.models.users_model import UsersModel


class OrdersModel():
    """Create Orders Model"""

    def __init__(self):
        self.order_db = init_db()
        self.user_db = UsersModel()

    def create_order(self, data, user_auth):
        """Create order and append it to orders"""
        response = {}
        order = {
            "pick_up_location": data['pick up location'].lower(),
            "delivery_location": data['delivery location'].lower(),
            "current_location": data['pick up location'].lower(),
            "weight": float(data['weight']),
            "price": float(data['price']),
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
            response = {
                "ERROR": "Forbidden access!! You do not have permission to create order"}

        return response

    def get_orders(self, user_auth):
        """Get orders in database"""
        response = [
            {"ERROR": "Forbidden access!! You do not have permission to view this orders"}]

        if user_auth == "admin":
            query = "SELECT * FROM orders"
            curr = self.order_db.cursor()
            curr.execute(query)
            data = curr.fetchall()

            response = self.objectify_data(data, curr)

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
                result = {
                    "ERROR": "Forbidden access!! You do not have permission to view this order"}
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
            response = self.objectify_data(data, curr)
        else:
            response = [
                {"ERROR": "Forbidden access!! You do not have permission to view this orders"}]

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
                db_query = "SELECT COUNT(*) FROM orders WHERE status='in transit' and sender={}".format(
                    user_id)

            curr = self.order_db.cursor()
            curr.execute(db_query)
            data = curr.fetchone()

            num = data[0]

            return num
        else:
            return "Forbid"

    def objectify_data(self, data, curr):
        """Create objects out of tuples"""
        response = []
        for row in data:
            item_resp = {}
            for i, key in enumerate(curr.description):
                item_resp[key[0]] = row[i]

            response.append(item_resp)
        return response

    def make_user_response(self, parcel_id, update_type, user_data, user_req):
        response = [
            {"ERROR": "Forbidden access!! You do not have permission to make this change"}, 403]
        result = {}
        if_exist = self.get_order(parcel_id)
        if "message" in if_exist:
            response = [{"message": "This parcel order doesn't exist"}, 404]
        elif if_exist['sender'] == user_req[0]:
            if update_type == "cancel" or update_type == "delivery":
                if if_exist['status'] == "canceled":
                    response = [
                        {"message": "This Order is already canceled"}, 403]
                elif if_exist['status'] == "delivered":
                    response = [
                        {"message": "This Order is already delivered"}, 403]
                else:
                    result = self.update_order(
                        parcel_id, update_type, user_data)
                    response = [result, 200]
        elif user_req[1] == "admin":
            if update_type == "status" or update_type == "location":
                if update_type == "location" and if_exist['destination'] == user_data:
                    response = [
                        {"message": "This Order location is already at " + user_data}, 403]
                if update_type == "status" and if_exist['status'] == user_data:
                    response = [
                        {"message": "This Order already " + user_data}, 403]
                else:
                    result = self.update_order(
                        parcel_id, update_type, user_data)
                    response = [result, 200]

        return response


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
                message = self.validate_name(
                    self.user_input['current location'])
            elif self.data_for == "signin":
                message = self.user_signin_inputs()
            else:
                message = self.validate_name(
                    self.user_input['delivery location'])

        return message

    def create_user_inputs(self):
        """confirm inputs for creating user"""
        if self.validate_username(self.user_input['username']) != "ok":
            message = self.validate_username(self.user_input['username'])
        elif self.validate_name(self.user_input['first_name']) != "ok":
            message = "First name " + \
                self.validate_name(self.user_input['first_name'])
        elif self.validate_name(self.user_input['second_name']) != "ok":
            message = "Second name " + \
                self.validate_name(self.user_input['second_name'])
        elif not validate_email(self.user_input['email']):
            message = "Invalid email"
        elif self.validate_name(self.user_input['location']) != "ok":
            message = "Location " + \
                self.validate_name(self.user_input['location'])
        elif self.user_input['gender'] != "male" and self.user_input['gender'] != "female":
            message = "gender should be 'male' or 'female'"
        elif self.user_input['type'] != "admin" and self.user_input['type'] != "user":
            message = "user type should be 'admin' or 'user'"
        elif not re.match("^[a-zA-Z0-9]{6,20}$", self.user_input['password']):
            message = "password should have capital letter,small letter, number and be between 6-10 alphanumeric characters"
        elif self.user_db.get_username(self.user_input['username']) != "ok":
            message = "username already exists!!"
        elif self.user_db.get_email(self.user_input['email']) != "ok":
            message = "email is already registered!!"
        else:
            message = "ok"

        return message

    def user_signin_inputs(self):
        """confirm inputs for user signin"""
        if not re.match("^[a-zA-Z]{1}[a-zA-Z0-9]{2,10}$", self.user_input['username']):
            message = "Invalid username or password"
        elif not re.match("^[a-zA-Z0-9]{6,20}$", self.user_input['password']):
            message = "Invalid username or password"
        else:
            message = "ok"

        return message

    def create_order_inputs(self):
        """confirm inputs for creating order"""
        if self.validate_name(self.user_input['pick up location']) != "ok":
            message = "Pick up location " + \
                self.validate_name(self.user_input['pick up location'])
        elif self.validate_name(self.user_input['delivery location']) != "ok":
            message = "Delivery location " + \
                self.validate_name(self.user_input['delivery location'])
        elif not self.user_input['weight'].replace('.', '', 1).isdigit():
            message = "Weight should be decimal number"
        elif not self.user_input['weight'].replace('.', '', 1).isdigit():
            message = "price should be decimal number"
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

    def validate_username(self, user_name):
        message = "ok"
        if not user_name.strip():
            message = "username is missing"
        elif " " in user_name:
            message = "should not have spaces"
        elif not user_name[0].isalpha():
            message = "username should start with a letter"
        elif not re.match("[a-zA-Z0-9]", user_name):
            message = "username should be alphanumerical"
        elif len(user_name) < 3 or len(user_name) > 10:
            message = "username should be between 3-10 words"

        return message

    def validate_name(self, data_name):
        message = "ok"
        if not data_name.strip():
            message = "is missing"
        elif " " in data_name:
            message = "should not have spaces"
        elif not data_name.isalpha():
            message = "should be alphabetical letter"
        elif len(data_name) < 3 or len(data_name) > 20:
            message = "should be between 3-20 words"

        return message
