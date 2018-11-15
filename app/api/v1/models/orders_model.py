"""Orders Models"""
from datetime import date
from .users_model import UsersModel
from app.db_config import init_db


class OrdersModel():
    """Create Orders Model"""

    def __init__(self):
        self.order_db = init_db()

    def create_order(self, data):
        """Create order and append it to orders"""
        today = date.today()

        created = today.strftime("%d/%m/%Y")

        order = {
            "date_created": created,
            "pick_up_location": data['pick up location'],
            "delivery_location": data['delivery location'],
            "current_location": data['pick up location'],
            "weight": data['weight'],
            "price": data['price'],
            "status": "pending",
            "sender": data['sender']
        }

        query = """INSERT INTO orders(
                                     pickup, destination, current_location, weight, price, sender, status, created
                                     ) 
                                VALUES(
                                        %(pick_up_location)s, %(delivery_location)s, %(current_location)s, %(weight)s, %(price)s, %(sender)s, %(status)s, %(date_created)s
                                        )"""

        curr = self.order_db.cursor()
        curr.execute(query, order)

        self.order_db.commit()

        return order

    def get_orders(self):
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

    def cancel_order(self, order_id):
        """Cancel delivery order"""
        result = {}
        if_exist = self.get_order(order_id)
    
        if "message" in if_exist:
            result = {"message": "order unknown"}
        else:
            query = "UPDATE orders SET status='canceled' WHERE order_no={}".format(order_id)
            curr = self.order_db.cursor()
            curr.execute(query)

            result = self.get_order(order_id)

        return result

    def change_delivery(self, order_id, delivery_location):
        """change delivery location"""
        result = {"message": "order unknown"}

        for order in self.order_db:
            if order['order no'] == order_id:
                order['delivery location'] = delivery_location
                result = {"message": "order " + order_id +
                                     " Delivery location changed!", "Order " + order_id: order}
                break

        return result

    def change_location(self, order_id, current_location):
        """change current location"""
        result = {"message": "order unknown"}

        for order in self.order_db:
            if order['order no'] == order_id:
                order['current location'] = current_location
                result = {"message": "order " + order_id +
                                     " Current location changed!", "Order " + order_id: order}
                break

        return result

    def change_status(self, order_id, status):
        """change delivery order status"""
        result = {"message": "order unknown"}

        for order in self.order_db:
            if order['order no'] == order_id:
                order['status'] = status
                result = {"message": "order " + order_id +
                                     " Status changed!", "Order " + order_id: order}
                break

        return result

    # def get_user_orders(self, user_id):
    #     """Get orders created by specific order"""
    #     users = self.users_db.get_users()

    #     user_orders = []
    #     for order in self.order_db:
    #         if order['sender'] == user_id:
    #             for user in users:
    #                 if user['user id'] == order['sender']:
    #                     order['sender'] = user['username']
    #                     break
    #             user_orders.append(order)

    #     return user_orders

    def get_delivered_orders(self, user_id):
        """Get delivered orders for a specific user"""
        user_orders = [order for order in self.order_db if (
            order['sender'] == user_id and order['status'] == 'delivered')]

        return len(user_orders)

    def get_orders_in_transit(self, user_id):
        """Get orders in transit by a specific user"""
        user_orders = [order for order in self.order_db if (
            order['sender'] == user_id and order['status'] == 'in transit')]
        return len(user_orders)


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
