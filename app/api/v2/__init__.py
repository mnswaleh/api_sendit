"""Initialize version 2"""

from flask_restful import Api, Resource
from flask import Blueprint
from app.api.v2.views.orders_view import (DeliveryOrders, DeliveryOrder, DeliveryOrderUpdate,
                                          DeliveryOrderDeliveryUpdate, DeliveryOrderStatus, DeliveryOrderLocation)
from app.api.v2.views.users_view import (
    UserOrders, UserDeliveredOrders, UserOrdersInTransit, Users, UserSignin, UserLogout, UserProfile)

VERSION2 = Blueprint('sendit2', __name__, url_prefix="/api/v2")

API = Api(VERSION2)

"""Add resources"""

API.add_resource(DeliveryOrders, '/parcels', strict_slashes=False)
API.add_resource(DeliveryOrder, '/parcels/<parcelId>', strict_slashes=False)
API.add_resource(DeliveryOrderUpdate,
                 '/parcels/<int:parcelId>/cancel', strict_slashes=False)
API.add_resource(DeliveryOrderDeliveryUpdate,
                 '/parcels/<int:parcelId>/destination', strict_slashes=False)
API.add_resource(DeliveryOrderLocation,
                 '/parcels/<int:parcelId>/presentLocation', strict_slashes=False)
API.add_resource(DeliveryOrderStatus,
                 '/parcels/<int:parcelId>/status', strict_slashes=False)
API.add_resource(UserOrders, '/users/<int:userId>/parcels',
                 strict_slashes=False)
API.add_resource(UserDeliveredOrders,
                 '/users/<int:userId>/delivered', strict_slashes=False)
API.add_resource(UserOrdersInTransit,
                 '/users/<int:userId>/in-transit', strict_slashes=False)
API.add_resource(UserProfile, '/user/<int:userId>', strict_slashes=False)
API.add_resource(Users, '/auth/signup', strict_slashes=False)
API.add_resource(UserSignin, '/auth/login', strict_slashes=False)
API.add_resource(UserLogout, '/auth/logout', strict_slashes=False)
