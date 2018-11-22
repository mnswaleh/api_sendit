"""Tests module"""
import json
import unittest
from app import create_app


class TestDeliveryOrders(unittest.TestCase):
    """Class for testing app endpoints"""

    def setUp(self):
        """Set up test"""
        create_app('app.config.TestingConfig').testing = True
        self.app = create_app('app.config.TestingConfig').test_client()
        self.user_data = {
            "username": "tomtom",
            "first_name": "thomas",
            "second_name": "wakati",
            "email": "mnswaleh@gmail.com",
            "gender": "male",
            "location": "eldoret",
            "type": "user",
            "password": "Ac67789"
        }

        self.admin_data = {
            "username": "tito",
            "first_name": "titaus",
            "second_name": "mzalendo",
            "email": "swaleh2031@gmail.com",
            "gender": "male",
            "location": "narok",
            "type": "admin",
            "password": "Atsf52rty"
        }

        self.order_data = {
            "pick up location": "nanyuki",
            "delivery location": "nairobi",
            "weight": 2,
            "price": 2000
        }

        self.edit_data = {
            "delivery location": "narok",
            "current location": "kikuyu",
            "status": "in transit"
        }

        self.headers = {}

    def test_create_user(self):
        """Test endpoint to create user"""
        response = self.app.post(
            '/api/v2/auth/signup', data=json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data)
        self.assertIn('Signup successul!', str(result))

    def test_create_admin(self):
        """Test endpoint to create user"""
        response = self.app.post(
            '/api/v2/auth/signup', data=json.dumps(self.admin_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data)
        self.assertIn('Signup successul!', str(result))

    def test_signin_user(self):
        """Test endpoint to signin user"""
        response = self.app.post(
            '/api/v2/auth/signup', data=json.dumps(self.user_data), content_type='application/json')
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('access', str(result))

    def test_create_order(self):
        """Test endpoint to create order"""
        self.app.post('/api/v2/auth/signup', data=json.dumps(self.user_data),
                      content_type='application/json')
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')

        result = json.loads(response.data)

        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.post(
            '/api/v2/parcels', data=json.dumps(self.order_data), headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        result = json.loads(response.data)
        self.assertIn('pending', str(result))

        self.app.post('/api/v2/auth/signup', data=json.dumps(self.admin_data),
                      content_type='application/json')

        new_order = self.order_data
        new_order['pick up location'] = ""

        response = self.app.post(
            '/api/v2/parcels', data=json.dumps(new_order), headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        result = json.loads(response.data)
        self.assertIn('Error', str(result))

    def test_get_all_orders(self):
        """Test endpoint to fetch all orders"""
        self.test_create_order()
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.get(
            '/api/v2/parcels', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('order_no', str(result))

    def test_get_specific_order(self):
        """Test endpoint to fetch a specific order"""
        self.test_create_order()
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.get(
            '/api/v2/parcels/1', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('order_no', str(result))

    def test_get_delivery_orders_by_user(self):
        """Test endpoint to fetch delivery orders for a specific user"""
        self.test_create_order()
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.get(
            '/api/v2/users/1/parcels', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('Delivery orders list', str(result))

    def test_cancel_delivery_order(self):
        """Test endpoint to cancel delivery order"""
        self.test_create_order()
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.put(
            '/api/v2/parcels/1/cancel', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('canceled', str(result))

    def test_edit_current_location(self):
        """Test endpoint to change current location"""
        self.test_create_order()
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.put(
            '/api/v2/parcels/1/presentLocation', headers=req_header, data=json.dumps(self.edit_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('kikuyu', str(result))

    def test_edit_status(self):
        """Test endpoint to change status"""
        self.test_create_order()
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.put(
            '/api/v2/parcels/1/status', headers=req_header, data=json.dumps(self.edit_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('in transit', str(result))

    def test_change_delivery_location(self):
        """Test endpoint to change delivery location"""
        self.test_create_order()
        user_login = {
            "username": self.user_data['username'], "password": self.user_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.put(
            '/api/v2/parcels/1/destination', headers=req_header, data=json.dumps(self.edit_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('narok', str(result))

    def test_get_delivered_orders_for_user(self):
        """Test endpoint to get the number of delivered orders for a specific user"""
        response = self.app.post(
            '/api/v2/auth/signup', data=json.dumps(self.admin_data), content_type='application/json')
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.get(
            '/api/v2/users/1/delivered', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('Delivered', str(result))

    def test_get_in_transit_orders_for_user(self):
        """Test endpoint to get the number of orders in transit for a specific user"""
        response = self.app.post(
            '/api/v2/auth/signup', data=json.dumps(self.admin_data), content_type='application/json')
        user_login = {
            "username": self.admin_data['username'], "password": self.admin_data['password']}
        response = self.app.post(
            '/api/v2/auth/login', data=json.dumps(user_login), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        req_header = {'Authorization': 'Bearer {}'.format(result['access'])}
        response = self.app.get(
            '/api/v2/users/1/in-transit', headers=req_header, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.data)
        self.assertIn('in-transit', str(result))


if __name__ == '__main__':
    unittest.main()
