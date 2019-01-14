"""Orders View Module"""

from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v2.models.orders_model import OrdersModel, ValidateInputs


class DeliveryOrders(Resource):
    """Create Delivery Orders Object to create delivery order and fetch all orders"""

    def __init__(self):
        self.orders_db = OrdersModel()
        self.result = reqparse.RequestParser(trim=True)

    @jwt_required
    def get(self):
        """Fetch all orders"""
        user_auth = get_jwt_identity()
        result = self.orders_db.get_orders(user_auth[1])
        response = {}
        if result and "ERROR" in result[0]:
            response = make_response(jsonify(result[0]), 403)
        else:
            response = make_response(
                jsonify({"Title": "Delivery orders", "orders": result}), 200)

        return response

    @jwt_required
    def post(self):
        """Create delivery order"""
        user_auth = get_jwt_identity()
        data = self.pars_data()
        inputs_validate = ValidateInputs(data, 'create_order')
        data_validation = inputs_validate.confirm_input()

        response = {}
        if data_validation != "ok":
            response = make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = self.orders_db.create_order(data, user_auth[0])
            if "ERROR" in result:
                response = make_response(jsonify(result), 403)
            else:
                response = make_response(jsonify(result), 201)

        return response

    def pars_data(self):
        """Parse user data"""
        self.result.add_argument('pick_up_location', type=str,
                                 help="pick up location is required", required=True)
        self.result.add_argument('delivery_location', type=str,
                                 help="delivery location is required", required=True)
        self.result.add_argument(
            'weight', help="weight is required", required=True)
        self.result.add_argument(
            'price', help="price is required", required=True)

        return self.result.parse_args()


class DeliveryOrder(Resource):
    """Create Delivery Order Object to fetch a specific delivery order or update current location"""

    @jwt_required
    def get(self, parcelId):
        """Fetch a specific delivery order"""
        orders_db = OrdersModel()
        response = {}
        user_auth = get_jwt_identity()
        result = orders_db.get_order(parcelId, user_auth[0])

        if "message" in result:
            response = make_response(jsonify(result), 404)
        elif "ERROR" in result:
            response = make_response(jsonify(result), 403)
        else:
            response = make_response(jsonify(result), 200)

        return response


class DeliveryOrderUpdate(Resource):
    """Create Delivery Orders Object to cancel delivery order"""

    def __init__(self):
        self.orders_db = OrdersModel()

    @jwt_required
    def put(self, parcelId):
        """Cancel a delivery order"""
        user_auth = get_jwt_identity()
        response = {}
        result = self.orders_db.make_user_response(
            parcelId, 'cancel', 'canceled', user_auth)

        response = make_response(jsonify(result[0]), result[1])

        return response


class DeliveryOrderDeliveryUpdate(Resource):
    """Create Delivery Orders Object to change delivery location"""
    @jwt_required
    def put(self, parcelId):
        """Change delivery location"""
        user_auth = get_jwt_identity()
        orders_db = OrdersModel()
        result = reqparse.RequestParser()
        response = {}
        result.add_argument('delivery_location', type=str,
                            help="delivery location is required", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'change_delivery')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            response = make_response(
                jsonify({"Error": "Delivery location" + data_validation}), 400)
        else:
            result = orders_db.make_user_response(
                parcelId, 'delivery', data['delivery_location'], user_auth)
            response = make_response(jsonify(result[0]), result[1])
        return response


class DeliveryOrderLocation(Resource):
    """Create Delivery Orders Object to update delivery order current location"""
    @jwt_required
    def put(self, parcelId):
        """Change current location"""
        user_auth = get_jwt_identity()
        orders_db = OrdersModel()
        result = reqparse.RequestParser()
        response = {}
        result.add_argument('current_location', type=str,
                            help="current location is required", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'change_location')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            response = make_response(
                jsonify({"Error": "Current location" + data_validation}), 400)
        else:
            result = orders_db.make_user_response(
                parcelId, 'location', data['current_location'], user_auth)
            response = make_response(jsonify(result[0]), result[1])
        return response


class DeliveryOrderStatus(Resource):
    """Create Delivery Orders Object to update delivery order status"""
    @jwt_required
    def put(self, parcelId):
        """Change order status"""
        user_auth = get_jwt_identity()
        orders_db = OrdersModel()
        result = reqparse.RequestParser()
        response = {}
        result.add_argument(
            'status', type=str, help="status' is required", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'update_status')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            response = make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = orders_db.make_user_response(
                parcelId, 'status', data['status'], user_auth)
            response = make_response(jsonify(result[0]), result[1])

        return response
