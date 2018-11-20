# apisendIT
[![Maintainability](https://api.codeclimate.com/v1/badges/ef93ec6eaef2a2345a71/maintainability)](https://codeclimate.com/github/mnswaleh/api_sendit/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/mnswaleh/api_sendit/badge.svg?branch=develop)](https://coveralls.io/github/mnswaleh/api_sendit?branch=develop)
[![Build Status](https://travis-ci.org/mnswaleh/api_sendit.svg?branch=develop)](https://travis-ci.org/mnswaleh/api_sendit)
# FEATURES
API has the following features:
1. GET /parcels
2. GET /parcels/<parcelId>
3. PUT /parcels/<parcelId>/status
4. PUT /parcels/<parcelId>/cancel
5. PUT /parcels/<parcelId>/destination
6. PUT /parcels/<parcelId>/presentLocation
7. GET /users/<userId>/in-transit
8. GET /users/<userId>/delivered
9. GET /users/<userId>/parcels
10. POST /parcels
11. POST /auth/signup
12. POST /auth/login

# INSTALLATION
pip install virtualenv

###### Clone the github repo:
1. Open new folder
2. Open Terminal on this folder
3. Type
    ```
     git clone https://github.com/mnswaleh/api_sendit.git .
    ```

###### create virtual evironment:
```
virtualenv venv
source venv/bin/activate
```

```
pip install -r requirements.txt
```

###### create Database:
on postreSQL database create
1. apisendit database
2. apitest database

# TEST
install postman

## on pytets
1. on terminal type
    ```
    pytest
    ```
2. all the tests should pass

on terminal: type 
    ```
    export FLASK_APP=run.py
    flask run
    ```

## On postman:
###### CREATE USER
1. Enter URL http://127.0.0.1:5000/api/v1/auth/signup
2. send post request with user details eg,
```
{
    "username": "tom",
    "first_name": "thomas",
    "second_name": "Kalume",
    "email": "tom@gmail.com",
    "gender": "male",
    "location": "kakamega",
    "password": "243677"
}
```
3. should receive response with code 201 and user details access tokeneg,
```
{
    "access:": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDI2NTIzNDgsIm5iZiI6MTU0MjY1MjM0OCwianRpIjoiYmQ0YTc1MWEtMmNhMy00YzhlLTkyYTgtNGEwZjIyMmNlOTJiIiwiZXhwIjoxNTQyNjUzMjQ4LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.lhTNtrG58sk7muegEBtiymc2NGphTOae8dQgZAH7kyQ",
    "user:": {
        "email": "tom@gmail.com",
        "firstname": "thomas",
        "gender": "male",
        "location": "kakamega",
        "password": "$2b$12$ropcC2L5z0xeqrjwmcF10eAC8SizfmezkhFkQwaxAQ9v8vIwb0mxm",
        "secondname": "Kalume",
        "type": "user",
        "user_id": 1,
        "username": "tom"
    }
}
```

###### SIGNIN USER
1. Enter URL http://127.0.0.1:5000/api/v1/auth/login
2. send post request with username and password eg,
```
{
    "username": "tom",
    "password": "243677"
}
```
3. should receive response with code 201, user details and access tokeneg,
```
{
    "access:": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NDI2NTIzNDgsIm5iZiI6MTU0MjY1MjM0OCwianRpIjoiYmQ0YTc1MWEtMmNhMy00YzhlLTkyYTgtNGEwZjIyMmNlOTJiIiwiZXhwIjoxNTQyNjUzMjQ4LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.lhTNtrG58sk7muegEBtiymc2NGphTOae8dQgZAH7kyQ",
    "user:": {
        "email": "tom@gmail.com",
        "firstname": "thomas",
        "gender": "male",
        "location": "kakamega",
        "password": "$2b$12$ropcC2L5z0xeqrjwmcF10eAC8SizfmezkhFkQwaxAQ9v8vIwb0mxm",
        "secondname": "Kalume",
        "type": "user",
        "user_id": 1,
        "username": "tom"
    }
}
```

###### CREATE ORDER
1. Login as user
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/parcels
4. send post request with delivery order eg,
```
{
	"pick up location": "nyahururu",
	"delivery location": "kitale",
	"weight": 2,
	"price": 200,
	"sender": 1
}
```
5. should receive response with code 201 and order details eg,
```
{
    "current_location": "nyahururu",
    "delivery_location": "kitale",
    "pick_up_location": "nyahururu",
    "price": 200,
    "sender": 1,
    "status": "pending",
    "weight": 2
}
```

###### FETCH ALL ORDERS
1. Login as admin
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/parcels
4. send get request 
5. should receive response with code 200 and all delivery orders created eg,
```
{
    "Delivery orders list": [
        {
            "created": "Mon, 19 Nov 2018 00:00:00 GMT",
            "current_location": "nyahururu",
            "destination": "kitale",
            "order_no": 1,
            "pickup": "nyahururu",
            "price": 200,
            "sender": 1,
            "status": "pending",
            "weight": 2
        }
    ],
    "Title": "Delivery orders"
}
```

###### FETCH ORDERS OF A PARTICULAR USER
1. Login as admin or user
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/users/1/parcels
4. send get request 
5. should receive response with code 200 and all delivery orders created by user with user id 1 ie,
```
{
    "Delivery orders list": [
        {
            "created": "Mon, 19 Nov 2018 00:00:00 GMT",
            "current_location": "nyahururu",
            "destination": "kitale",
            "order_no": 1,
            "pickup": "nyahururu",
            "price": 200,
            "sender": 1,
            "status": "pending",
            "weight": 2
        }
    ],
    "Title": "Delivery orders by user 1"
}
```

###### FETCH PARTICULAR ORDER
1. Login as admin or user
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/parcels/1
4. send get request 
5. should receive response with code 200 and details of order 367857 ie,
```
{
    "created": "Mon, 19 Nov 2018 00:00:00 GMT",
    "current_location": "nyahururu",
    "destination": "kitale",
    "order_no": 1,
    "pickup": "nyahururu",
    "price": 200,
    "sender": 1,
    "status": "pending",
    "weight": 2
}
```

###### CANCEL PARCEL DELIVERY ORDER
1. Login as user
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/parcels/1/cancel
4. send put request 
5. should receive response with code 200 and details of order 1 with status as canceled ie,
```
{
    "created": "Mon, 19 Nov 2018 00:00:00 GMT",
    "current_location": "nyahururu",
    "destination": "kitale",
    "order_no": 1,
    "pickup": "nyahururu",
    "price": 200,
    "sender": 1,
    "status": "canceled",
    "weight": 2
}
```

###### CHANGE DELIVERY LOCATION
1. Login as user
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/parcels/1/destination
4. send put request with desired delivery location eg,
```
{
	"delivery location": "kisumu"
}
```
4. should receive response with code 200 and details of order 1 with new delivery location eg,
```
{
    "created": "Mon, 19 Nov 2018 00:00:00 GMT",
    "current_location": "nyahururu",
    "destination": "kisumu",
    "order_no": 1,
    "pickup": "nyahururu",
    "price": 200,
    "sender": 1,
    "status": "canceled",
    "weight": 2
}
```

###### CHANGE ORDER CURRENT LOCATION
1. Login as admin
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/parcels/1/presentLocation
4. send put request with current location eg,
```
{
	"current location": "naivasha"
}
```
5. should receive response with code 200 and details of order 1 with new current location eg,
```
{
    "created": "Mon, 19 Nov 2018 00:00:00 GMT",
    "current_location": "naivasha",
    "destination": "kisumu",
    "order_no": 1,
    "pickup": "nyahururu",
    "price": 200,
    "sender": 1,
    "status": "canceled",
    "weight": 2
}
```

###### CHANGE ORDER STATUS
1. Login as admin
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/parcels/1/status
4. send put request with status eg,
```
{
	"status": "in transit"
}
```
5. should receive response with code 200 and details of order 1 with new status eg,
```
{
    "created": "Mon, 19 Nov 2018 00:00:00 GMT",
    "current_location": "naivasha",
    "destination": "kisumu",
    "order_no": 1,
    "pickup": "nyahururu",
    "price": 200,
    "sender": 1,
    "status": "in transit",
    "weight": 2
}
```

###### GET ORDERS OF A PARTICULAR USER THAT ARE DELIVERED
1. Login as admin or user
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/users/1/delivered
4. send get request 
5. should receive response with code 200 and the number of orders of user 1 that are delivered ie,
```
{
    "Delivered orders for user 1": 0
}
```

###### GET ORDERS OF A PARTICULAR USER THAT ARE IN TRANSIT
1. Login as admin or user
2. Copy the access token and paste it as Bearer Token on headers
3. Enter URL http://127.0.0.1:5000/api/v1/users/1/in-transit
4. send get request 
5. should receive response with code 200 and the number of orders of user 1 that are in transit ie,
```
{
    "Orders in-transit for user 1": 0
}
```

## on heroku
reapet the postman tests above replacing server url http://127.0.0.1:5000 with https://apisendit.herokuapp.com/
