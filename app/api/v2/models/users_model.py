"""Users Module"""
from flask_jwt_extended import create_access_token
import flask_bcrypt
from app.db_config import init_db


class UsersModel():
    """Create Users Model"""

    def __init__(self):
        self.user_db = init_db()

    def create_user(self, data):
        """Create user and append to users db"""
        user_pass = flask_bcrypt.generate_password_hash(
            data['password']).decode('utf-8')
        user = {
            "username": data['username'].lower(),
            "first_name": data['first_name'].lower(),
            "second_name": data['second_name'].lower(),
            "email": data['email'],
            "gender": data['gender'],
            "location": data['location'].lower(),
            "password": user_pass,
            "type": data['type']
        }
        query = """INSERT INTO users(username, firstname, secondname, email, gender, location, type, password) VALUES(%(username)s, %(first_name)s, %(second_name)s, %(email)s, %(gender)s, %(location)s, %(type)s, %(password)s)"""

        curr = self.user_db.cursor()
        curr.execute(query, user)
        self.user_db.commit()
        result = self.get_username(data['username'])
        if result == "ok":
            return {"message": "Signup Failed!"}

        del result["password"]
        return {"message": "Signup successul!", "user": result}

    def get_user(self, user_id, user_auth=[]):
        """Get a specific user from the database"""
        result = {}
        query = "SELECT * FROM users WHERE user_id={}".format(user_id)

        curr = self.user_db.cursor()
        curr.execute(query)

        data = curr.fetchone()

        if not data:
            result = {"message": "user unknown"}
        elif user_auth and (user_id != user_auth[0] and user_auth[1] != "admin"):
            result = {
                "ERROR": "Forbidden access!! You do not have permission to view this  user details"}
        else:
            for i, key in enumerate(curr.description):
                result[key[0]] = data[i]
            del result["password"]

        return result

    def get_username(self, user_name):
        """Get a specific user from the database"""
        result = {}
        query = "SELECT * FROM users WHERE username='{}'".format(user_name)

        curr = self.user_db.cursor()
        curr.execute(query)

        data = curr.fetchone()

        if data:
            for i, key in enumerate(curr.description):
                result[key[0]] = data[i]
        else:
            result = "ok"

        return result

    def get_email(self, user_email):
        """Get a specific user from the database using email"""
        query = "SELECT * FROM users WHERE email='{}'".format(user_email)

        curr = self.user_db.cursor()
        curr.execute(query)

        data = curr.fetchone()

        if data:
            return "data"

        return "ok"

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
                    identity=[result['user_id'], result['type']])
                result = {"Message": "Login Successful!",
                          "user": str(result['user_id']) + ',' + result['type'],
                          "access": access_token}

        return result
