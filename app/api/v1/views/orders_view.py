"""Orders View Module"""

from flask import make_response, jsonify, request
from flask_restful import Resource, reqparse
from app.api.v1.models.orders_model import OrdersModel, ValidateInputs


class DeliveryOrders(Resource):
    """Create Delivery Orders Object to create delivery order and fetch all orders"""

    def __init__(self):
        self.orders_db = OrdersModel()

    def get(self):
        """Fetch all orders"""
        result = self.orders_db.get_orders()

        return make_response(jsonify({"Title": "Delivery orders", "Delivery orders list": result}))

    def post(self):
        """Create delivery order"""
        result = reqparse.RequestParser()
        result.add_argument('pick up location', type=str,
                            help="pick up location' is required to be a string", required=True)
        result.add_argument('delivery location', type=str,
                            help="delivery location' is required to be a string", required=True)
        result.add_argument(
            'weight', type=int, help="weight is required to be an integer", required=True)
        result.add_argument(
            'price', type=int, help="price is required to be an integer", required=True)
        result.add_argument(
            'sender', type=int, help="sender is required to be an integer", required=True)
        data = result.parse_args()
        data = request.get_json(force=True)
        inputs_validate = ValidateInputs(data, 'create_order')
        data_validation = inputs_validate.confirm_input()

        response = {}
        if data_validation != "ok":
            response = make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = self.orders_db.create_order(data)
            response = make_response(jsonify(result), 201)

        return response


class DeliveryOrder(Resource):
    """Create Delivery Order Object to fetch a specific delivery order or update current location"""

    def get(self, parcelId):
        """Fetch a specific delivery order"""
        orders_db = OrdersModel()
        result = orders_db.get_order(parcelId)

        return make_response(jsonify(result))


class DeliveryOrderUpdate(Resource):
    """Create Delivery Orders Object to cancel delivery order"""

    def __init__(self):
        self.orders_db = OrdersModel()

    def put(self, parcelId):
        """Cancel a delivery order"""
        result = self.orders_db.cancel_order(parcelId)

        return make_response(jsonify(result))


class DeliveryOrderDeliveryUpdate(Resource):
    """Create Delivery Orders Object to update delivery order details"""
    def put(self, parcelId):
        """Change delivery location"""
        orders_db = OrdersModel()
        result = reqparse.RequestParser()
        result.add_argument('delivery location', type=str,
                            help="delivery location is required", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'change_delivery')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            return make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = orders_db.change_delivery(
                parcelId, data['delivery location'])

            return make_response(jsonify(result))

class DeliveryOrderLocation(Resource):
    """Create Delivery Orders Object to update delivery order current location"""
    def put(self, parcelId):
        """Change current location"""
        orders_db = OrdersModel()
        result = reqparse.RequestParser()
        result.add_argument('current location', type=str,
                            help="current location is required", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'change_location')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            return make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = orders_db.change_location(
                parcelId, data['current location'])

            return make_response(jsonify(result))

class DeliveryOrderStatus(Resource):
    """Create Delivery Orders Object to update delivery order status"""
    def put(self, parcelId):
        """Change order status"""
        orders_db = OrdersModel()
        result = reqparse.RequestParser()
        result.add_argument(
            'status', type=str, help="status' is required to be a string", required=True)
        data = result.parse_args()
        inputs_validate = ValidateInputs(data, 'update_status')
        data_validation = inputs_validate.confirm_input()
        if data_validation != "ok":
            return make_response(jsonify({"Error": data_validation}), 400)
        else:
            result = orders_db.change_status(
                parcelId, data['status'])

            return make_response(jsonify(result))
