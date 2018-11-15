"""Tests module"""
import json
import unittest
from app import create_app


class TestDeliveryOrders(unittest.TestCase):
    """Class for testing app endpoints"""

    def setUp(self):
        """Set up test"""
        create_app().testing = True
        self.app = create_app().test_client()
        self.user_data = {
            "username": "tom",
            "first_name": "thomas",
            "second_name": "wakati",
            "email": "email@gmail.com",
            "gender": "male",
            "location": "eldoret",
            "password": "123456"
        }

        self.order_data = {
            "order no": "588356",
            "pick up location": "nanyuki",
            "delivery location": "nairobi",
            "weight": 2,
            "price": 2000,
            "sender": 1
        }

        self.edit_data = {
            "delivery location": "narok",
            "current location": "kikuyu",
            "status": "in transit"
        }

    def test_create_user(self):
        """Test endpoint to create user"""
        response = self.app.post(
            '/api/v1/users', data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data)
        self.assertIn('email@gmail.com', str(result))

    def test_signin_user(self):
        """Test endpoint to signin user"""
        user_login = self.user_data
        response = self.app.post(
            '/api/v1/users/signin', data=json.dumps({"username": user_login['username'], "password": user_login['password']}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('tom', str(result))

    def test_create_order(self):
        """Test endpoint to create order"""
        response = self.app.post(
            '/api/v1/parcels', data=json.dumps(self.order_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data)
        self.assertIn('pending', str(result))

        new_order = self.order_data
        new_order['order no'] = ""

        response = self.app.post(
            '/api/v1/parcels', data=json.dumps(new_order), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        result = json.loads(response.data)
        self.assertIn('missing', str(result))

    def test_get_all_orders(self):
        """Test endpoint to fetch all orders"""
        response = self.app.get(
            '/api/v1/parcels', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('588356', str(result))

    def test_get_specific_order(self):
        """Test endpoint to fetch a spoecific order"""
        response = self.app.get(
            '/api/v1/parcels/588356', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('588356', str(result))

    def test_get_delivery_orders_by_user(self):
        """Test endpoint to fetch delivery orders for a specific user"""
        self.test_create_order()
        response = self.app.get(
            '/api/v1/users/1/parcels', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('588356', str(result))

    def test_cancel_delivery_order(self):
        """Test endpoint to cancel delivery order"""
        self.test_create_order()
        response = self.app.put(
            '/api/v1/parcels/588356/cancel', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('canceled', str(result))

    def test_edit_delivery_order(self):
        """Test endpoint to edit delivery order"""
        response = self.app.put(
            '/api/v1/parcels/588356', data=json.dumps(self.edit_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('kikuyu', str(result))

    def test_change_delivery_location(self):
        """Test endpoint to change delivery location"""
        self.test_create_order()

        response = self.app.put(
            '/api/v1/parcels/588356/change-delivery', data=json.dumps(self.edit_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('narok', str(result))

    def test_get_delivered_orders_for_user(self):
        """Test endpoint to get the number of delivered orders for a specific user"""
        response = self.app.get(
            '/api/v1/users/1/delivered', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('Delivered', str(result))

    def test_get_in_transit_orders_for_user(self):
        """Test endpoint to get the number of orders in transit for a specific user"""
        response = self.app.get(
            '/api/v1/users/1/in-transit', content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('in-transit', str(result))


if __name__ == '__main__':
    unittest.main()
