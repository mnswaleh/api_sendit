"""Orders View Module"""

from flask import make_response, jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v1.models.orders_model import OrdersModel, ValidateInputs


class DeliveryOrders(Resource):
    """Create Delivery Orders Object to create delivery order and fetch all orders"""

    def __init__(self):
        self.orders_db = OrdersModel()
        self.result = reqparse.RequestParser()

    @jwt_required
    def get(self):
        """Fetch all orders"""
        user_auth = get_jwt_identity()
        result = self.orders_db.get_orders(user_auth)
        response = {}
        if result and "ERROR" in result[0]:
            response = make_response(jsonify(result[0]), 403)
        else:
            response = make_response(
                jsonify({"Title": "Delivery orders", "Delivery orders list": result}))

        return response

    @jwt_required
    def post(self):
        """Create delivery order"""
        user_auth = get_jwt_identity()
        
        data = self.pars_data()
        data = request.get_json(force=True)
        inputs_validate = ValidateInputs(data, 'create_order')
        data_validation = inputs_validate.confirm_input()

        response = {}
        if data_validation != "ok":
            response = make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = self.orders_db.create_order(data, user_auth)
            if "ERROR" in result:
                response = make_response(jsonify(result), 403)
            else:
                response = make_response(jsonify(result), 201)

        return response

    def pars_data(self):
        self.result.add_argument('pick up location', type=str,
                            help="pick up location' is required to be a string", required=True)
        self.result.add_argument('delivery location', type=str,
                            help="delivery location' is required to be a string", required=True)
        self.result.add_argument(
            'weight', type=int, help="weight is required to be an integer", required=True)
        self.result.add_argument(
            'price', type=int, help="price is required to be an integer", required=True)

        return self.result.parse_args()


class DeliveryOrder(Resource):
    """Create Delivery Order Object to fetch a specific delivery order or update current location"""

    @jwt_required
    def get(self, parcelId):
        """Fetch a specific delivery order"""
        orders_db = OrdersModel()
        response = {}
        user_auth = get_jwt_identity()
        result = orders_db.get_order(parcelId, user_auth)

        if "message" in result:
            response = make_response(jsonify(result), 404)
        elif "ERROR" in result:
            response = make_response(jsonify(result), 403)
        else:
            response = make_response(jsonify(result))

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
        result = self.orders_db.update_order(parcelId, 'cancel', 'canceled', user_auth)

        if "ERROR" in result:
            response = make_response(jsonify(result), 403)
        elif "message" in result:
            response = make_response(jsonify(result), 404)
        else:
            response = make_response(jsonify(result))

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
        result.add_argument('delivery location', type=str,
                            help="delivery location is required", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'change_delivery')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            response = make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = orders_db.update_order(
                parcelId, 'delivery', data['delivery location'], user_auth)
            if "ERROR" in result:
                response = make_response(jsonify(result), 403)
            elif "message" in result:
                response = make_response(jsonify(result), 404)
            else:
                response = make_response(jsonify(result))

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
        result.add_argument('current location', type=str,
                            help="current location is required", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'change_location')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            response = make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = orders_db.update_order(
                parcelId, 'location', data['current location'], user_auth)
            if "ERROR" in result:
                response = make_response(jsonify(result), 403)
            elif "message" in result:
                response = make_response(jsonify(result), 404)
            else:
                response = make_response(jsonify(result))
        
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
            'status', type=str, help="status' is required to be a string", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'update_status')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            response = make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = orders_db.update_order(
                parcelId, 'status', data['status'], user_auth)
            if "ERROR" in result:
                response = make_response(jsonify(result), 403)
            elif "message" in result:
                response = make_response(jsonify(result), 404)
            else:
                response = make_response(jsonify(result))

        return response
