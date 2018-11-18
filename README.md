# apisendIT
[![Maintainability](https://api.codeclimate.com/v1/badges/ef93ec6eaef2a2345a71/maintainability)](https://codeclimate.com/github/mnswaleh/api_sendit/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/mnswaleh/api_sendit/badge.svg?branch=develop)](https://coveralls.io/github/mnswaleh/api_sendit?branch=develop)
[![Build Status](https://travis-ci.org/mnswaleh/api_sendit.svg?branch=develop)](https://travis-ci.org/mnswaleh/api_sendit)
# FEATURES
API has the following features:
1. GET /parcels
2. GET /parcels/<parcelId>
3. PUT /parcels/<parcelId>
4. PUT /parcels/<parcelId>/cancel
5. PUT /parcels/<parcelId>/change-delivery
6. GET /users/<userId>/in-transit
7. GET /users/<userId>/delivered
8. GET /users/<userId>/parcels
9. POST /parcels

# INSTALLATION
pip install virtualenv

###### Clone the github repo:
1. Open new folder
2. Open Terminal on this folder
3. Type
    ```
     git clone https://github.com/mnswaleh/apisendIT/tree/bg-change-delivery-location-161859761 .
    ```

###### create virtual evironment:
```
virtualenv venv
source venv/bin/activate
```

```
pip install -r requirements.txt
```

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
3. should receive response with code 201 and user details eg,
```
    {
    "email": "tom@gmail.com",
    "first_name": "thomas",
    "gender": "male",
    "location": "kakamega",
    "password": "243677",
    "second_name": "Kalume",
    "type": "user",
    "user id": 1,
    "username": "tom"
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
3. should receive response with code 201 and user details eg,
```
    {
    "email": "tom@gmail.com",
    "first_name": "thomas",
    "gender": "male",
    "location": "kakamega",
    "password": "243677",
    "second_name": "Kalume",
    "type": "user",
    "user id": 1,
    "username": "tom"
}
```

###### CREATE ORDER
1. Enter URL http://127.0.0.1:5000/api/v1/parcels
2. send post request with delivery order eg,
```
    {
	"pick up location": "nyahururu",
	"delivery location": "kitale",
	"weight": 2,
	"price": 200,
	"sender": 1
}
```
3. should receive response with code 201 and order details eg,
```
    {
    "current location": "nyahururu",
    "date created": "12/11/2018",
    "delivery location": "kitale",
    "order id": 1,
    "order no": "367857",
    "pick up location": "nyahururu",
    "price": 200,
    "sender": 1,
    "status": "pending",
    "weight": 2
}
```

###### FETCH ALL ORDERS
1. Enter URL http://127.0.0.1:5000/api/v1/parcels
2. send get request 
3. should receive response with code 200 and all delivery orders created eg,
    {
    "Delivery orders list": [
        {
            "current location": "nyahururu",
            "date created": "12/11/2018",
            "delivery location": "kitale",
            "order id": 1,
            "order no": "367857",
            "pick up location": "nyahururu",
            "price": 200,
            "sender": "tom",
            "status": "pending",
            "weight": 2
        }
    ],
    "Title": "Delivery orders"
}

###### FETCH ORDERS OF A PARTICULAR USER
1. Enter URL http://127.0.0.1:5000/api/v1/users/1/parcels
2. send get request 
3. should receive response with code 200 and all delivery orders created by user with user id 1 ie,
```
    {
    "Delivery orders list": [
        {
            "current location": "nyahururu",
            "date created": "12/11/2018",
            "delivery location": "kitale",
            "order id": 1,
            "order no": "367857",
            "pick up location": "nyahururu",
            "price": 200,
            "sender": "tom",
            "status": "pending",
            "weight": 2
        }
    ],
    "Title": "Delivery orders by tom"
}
```

###### FETCH PARTICULAR ORDER
1. Enter URL http://127.0.0.1:5000/api/v1/parcels/367857
2. send get request 
3. should receive response with code 200 and details of order 367857 ie,
```
    {
    "current location": "nyahururu",
    "date created": "12/11/2018",
    "delivery location": "kitale",
    "order id": 1,
    "order no": "367857",
    "pick up location": "nyahururu",
    "price": 200,
    "sender": "tom",
    "status": "pending",
    "weight": 2
}
```

###### CANCEL PARCEL DELIVERY ORDER
1. Enter URL http://127.0.0.1:5000/api/v1/parcels/367857/cancel
2. send put request 
3. should receive response with code 200 and details of order 367857 with status as canceled ie,
```
    {
    "Order 367857": {
        "current location": "nyahururu",
        "date created": "12/11/2018",
        "delivery location": "kitale",
        "order id": 1,
        "order no": "367857",
        "pick up location": "nyahururu",
        "price": 200,
        "sender": "tom",
        "status": "canceled",
        "weight": 2
    },
    "message": "order 367857 is canceled!"
}
```

###### CHANGE DELIVERY LOCATION
1. Enter URL http://127.0.0.1:5000/api/v1/parcels/367857/destination
2. send put request with desired delivery location eg,
```
    {
	"delivery location": "kisumu"
}
```
3. should receive response with code 200 and details of order 367857 with new delivery location eg,
```
    {
    "Order 367857": {
        "current location": "nyahururu",
        "date created": "12/11/2018",
        "delivery location": "kisumu",
        "order id": 1,
        "order no": "367857",
        "pick up location": "nyahururu",
        "price": 200,
        "sender": "tom",
        "status": "canceled",
        "weight": 2
    },
    "message": "order 367857 Delivery location changed!"
}
```

###### CHANGE ORDER CURRENT LOCATION
1. Enter URL http://127.0.0.1:5000/api/v1/parcels/367857/presentLocation
2. send put request with current location eg,
```
    {
	"current location": "naivasha"
}
```
3. should receive response with code 200 and details of order 367857 with new current location eg,
```
    {
    "current location": "naivasha",
    "date created": "12/11/2018",
    "delivery location": "kisumu",
    "order id": 1,
    "order no": "367857",
    "pick up location": "nyahururu",
    "price": 200,
    "sender": "tom",
    "status": "canceled",
    "weight": 2
}
```

###### CHANGE ORDER STATUS
1. Enter URL http://127.0.0.1:5000/api/v1/parcels/367857/status
2. send put request with status eg,
```
    {
	"status": "in transit"
}
```
3. should receive response with code 200 and details of order 367857 with new status eg,
```
    {
    "current location": "naivasha",
    "date created": "12/11/2018",
    "delivery location": "kisumu",
    "order id": 1,
    "order no": "367857",
    "pick up location": "nyahururu",
    "price": 200,
    "sender": "tom",
    "status": "in transit",
    "weight": 2
}
```

###### GET ORDERS OF A PARTICULAR USER THAT ARE DELIVERED
1. Enter URL http://127.0.0.1:5000/api/v1/users/1/delivered
2. send get request 
3. should receive response with code 200 and the number of orders of user 1 that are delivered ie,
```
    {
    "Delivered orders for tom": 0
}
```

###### GET ORDERS OF A PARTICULAR USER THAT ARE IN TRANSIT
1. Enter URL http://127.0.0.1:5000/api/v1/users/1/in-transit
2. send get request 
3. should receive response with code 200 and the number of orders of user 1 that are in transit ie,
```
    {
    "Orders in-transit for tom": 0
}
```

## on heroku
reapet the postman tests above replacing server url http://127.0.0.1:5000 with https://apisendit.herokuapp.com/
