"""Users view Module"""

from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from app.api.v2.models.users_model import UsersModel
from app.api.v2.models.orders_model import OrdersModel, ValidateInputs


class Users(Resource):
    """Create users class to create a user"""

    def __init__(self):
        self.orders_db = UsersModel()
        self.result = reqparse.RequestParser(trim=True)

    def post(self):
        """Create User"""
        result = {}
        data = self.pars_data()
        inputs_validate = ValidateInputs(data, 'create_user')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            result = make_response(jsonify({"ERROR": data_validation}), 400)
        else:
            res = self.orders_db.create_user(data)
            result = make_response(jsonify(res), 201)
        return result

    def pars_data(self):
        """Parse user data"""
        self.result.add_argument(
            'username', type=str, help="username is required", required=True, location='json')
        self.result.add_argument(
            'first_name', type=str, help="first name is required", required=True, location='json')
        self.result.add_argument(
            'second_name', type=str, help="second name is required", required=True, location='json')
        self.result.add_argument(
            'email', type=str, help="email is required", required=True, location='json')
        self.result.add_argument(
            'gender', type=str, help="gender is required", required=True, location='json')
        self.result.add_argument(
            'location', type=str, help="location is required", required=True, location='json')
        self.result.add_argument(
            'type', type=str, help="type is required", required=True, location='json')
        self.result.add_argument(
            'password', type=str, help="password is required", required=True, location='json')

        return self.result.parse_args()


class UserSignin(Resource):
    """Create users class to signin a user"""

    def __init__(self):
        self.users_db = UsersModel()

    def post(self):
        """Create signin user"""
        response = {}
        result = reqparse.RequestParser()

        result.add_argument(
            'username', type=str, help="invalid useraname or password", required=True)
        result.add_argument(
            'password', type=str, help="invalid useraname or password", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'signin')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            response = make_response(jsonify({"ERROR": data_validation}), 400)
        else:
            login_result = self.users_db.user_login(
                data['username'], data['password'])
            if "ERROR" in login_result:
                response = make_response(jsonify(login_result), 400)
            else:
                response = make_response(jsonify(login_result), 200)

        return response


class UserLogout(Resource):
    """Signout a loged user"""
    @jwt_required
    def put(self):
        """Method to signout user"""
        return make_response(jsonify({"message": "successful logout"}), 200)


class UserProfile(Resource):
    """Display user profile"""
    @jwt_required
    def get(self, userId):
        """ Fetch all user details"""
        users_db = UsersModel()
        response = {}
        user_auth = get_jwt_identity()
        result = users_db.get_user(userId, user_auth)

        if "message" in result:
            response = make_response(jsonify(result), 404)
        elif "ERROR" in result:
            response = make_response(jsonify(result), 403)
        else:
            response = make_response(jsonify(result), 200)

        return response


class UserOrders(Resource):
    """Create Users object to fetch all delivery orders"""
    @jwt_required
    def get(self, userId):
        """ Fetch all delivery orders created by a specific user"""
        orders_db = OrdersModel()
        user_auth = get_jwt_identity()
        result = orders_db.get_user_orders(userId, user_auth[0])
        if result and "ERROR" in result[0]:
            response = make_response(jsonify(result[0]), 403)
        else:
            response = make_response(jsonify(
                {"Title": "Delivery orders by user " + str(userId), "orders": result}))

        return response


class UserDeliveredOrders(Resource):
    """Create Users object to fetch specific delivery order"""
    @jwt_required
    def get(self, userId):
        """Fetch delivery orders delivered for a specific user"""
        orders_db = OrdersModel()
        response = {}
        user_auth = get_jwt_identity()
        result = orders_db.get_order_amount(userId, 'delivered', user_auth[0])
        if result == "Forbid":
            response = make_response(
                jsonify({"ERROR": "Forbidden Access!! You do not view this delivery orders"}), 403)
        else:
            response = make_response(
                jsonify({"delivered": result}))

        return response


class UserOrdersInTransit(Resource):
    """User object to fetch orders in transit for a specific user"""

    @jwt_required
    def get(self, userId):
        """Fetch delivery orders in transit for a specific user"""
        orders_db = OrdersModel()
        response = {}
        user_auth = get_jwt_identity()
        result = orders_db.get_order_amount(userId, 'in-transit', user_auth[0])
        if result == "Forbid":
            response = make_response(
                jsonify({"ERROR": "Forbidden Access!! You do not have permission to Update this order"}), 403)
        else:
            response = make_response(
                jsonify({"in_transit": result}))

        return response
