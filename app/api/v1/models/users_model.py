"""Users Module"""
from app.db_config import init_db

class UsersModel():
    """Create Users Model"""

    def __init__(self):
        self.user_db = init_db()

    def create_user(self, data):
        """Create user and append to users db"""
        user = {
            "username": data['username'],
            "first_name": data['first_name'],
            "second_name": data['second_name'],
            "email": data['email'],
            "gender": data['gender'],
            "location": data['location'],
            "password": data['password'],
            "type": data['type']
        }
        query = """INSERT INTO users(
                                     username, firstname, secondname, email, gender, location, type, password
                                     ) 
                                VALUES(
                                        %(username)s, %(first_name)s, %(second_name)s, %(email)s, %(gender)s, %(location)s, %(type)s, %(password)s
                                        )"""

        curr = self.user_db.cursor()
        curr.execute(query, user)

        self.user_db.commit()

        return user

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

    def user_login(self, username, password):
        """User login method"""
        result = {}
        query = "SELECT * FROM users WHERE username='{}' and password='{}'".format(username, password)

        curr = self.user_db.cursor()
        curr.execute(query)

        data = curr.fetchone()

        if not data:
            result = {"ERROR": "invalid user name or password"}
        else:
            for i, key in enumerate(curr.description):
                result[key[0]] = data[i]

        return result
