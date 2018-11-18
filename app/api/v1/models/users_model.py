"""Users Module"""
from flask_jwt_extended import create_access_token
from app.db_config import init_db
import flask_bcrypt


class UsersModel():
    """Create Users Model"""
    def __init__(self):
        self.user_db = init_db()

    def create_user(self, data):
        """Create user and append to users db"""
        user_pass = flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = {
            "username": data['username'],
            "first_name": data['first_name'],
            "second_name": data['second_name'],
            "email": data['email'],
            "gender": data['gender'],
            "location": data['location'],
            "password": user_pass,
            "type": data['type']
        }
        query = """INSERT INTO users(username, firstname, secondname, email, gender, location, type, password) VALUES(%(username)s, %(first_name)s, %(second_name)s, %(email)s, %(gender)s, %(location)s, %(type)s, %(password)s)"""

        curr = self.user_db.cursor()
        curr.execute(query, user)

        self.user_db.commit()

        result = self.user_login(data['username'], data['password'])

        return result

    def get_user(self, user_id):
        """Get a specific user from the database"""
        result = {}
        query = "SELECT * FROM users WHERE user_id={}".format(user_id)

        curr = self.user_db.cursor()
        curr.execute(query)

        data = curr.fetchone()

        if not data:
            result = {"message": "user unknown"}
        else:
            for i, key in enumerate(curr.description):
                result[key[0]] = data[i]

        return result

    def get_username(self, user_name):
        """Get a specific user from the database"""
        result = {}
        query = "SELECT * FROM users WHERE username='{}'".format(user_name)

        curr = self.user_db.cursor()
        curr.execute(query)

        data = curr.fetchone()

        if data:
            result = "username already exists"
        else:
            result = "ok"

        return result

    def user_login(self, username, password):
        """User login method"""
        user_data = {}
        result = {"ERROR": "invalid user name or password"}
        access_token = "Access Denied!"
        
        query = "SELECT * FROM users WHERE username='{}'".format(
            username)

        curr = self.user_db.cursor()
        curr.execute(query)

        data = curr.fetchone()

        if data:
            for i, key in enumerate(curr.description):
                user_data[key[0]] = data[i]

            if flask_bcrypt.check_password_hash(user_data['password'], password):
                result = user_data
                access_token = create_access_token(
                identity=result['user_id'])

        return {"access:": access_token, "user:": result}

class Authenticate_user():
    """Class for user authentication"""
    def __init__(self):
        self.user_db = UsersModel()

    def auth_change(self, user_id, update_type, sender_id):
        """authentivatcate updating order"""
        if update_type == "status" or update_type == "location":
            return self.auth_admin(user_id)
        else:
            return self.auth_user(user_id, sender_id)

    def auth_user(self, user_id, sender_id):
        """Authenticate user updating order"""
        if user_id == sender_id:
            return True

    def auth_admin(self, user_id):
        """Authenticate admin updating order"""
        user_details = self.user_db.get_user(user_id)

        if user_details['type'] == "admin":
            return True
