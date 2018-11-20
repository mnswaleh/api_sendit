"""Module for application database"""
from flask import current_app
import psycopg2


def connection(url):
    """open database connection"""
    con = psycopg2.connect(current_app.config['DATABASE_URL'])
    return con


def init_db():
    """Initiate databse connection"""
    con = connection(current_app.config['DATABASE_URL'])
    return con


def create_tables():
    """Create application database tables"""
    tables_q = tables()
    conn = connection(current_app.config['DATABASE_URL'])
    curl = conn.cursor()

    for table in tables_q:
        curl.execute(table)

    conn.commit()


def destroy_tables():
    """destroy application database tables"""
    orders_tbl = """DROP TABLE IF EXISTS orders CASCADE;"""
    users_tbl = """DROP TABLE IF EXISTS users CASCADE;"""

    query = [orders_tbl, users_tbl]

    conn = connection(current_app.config['DATABASE_URL'])
    curl = conn.cursor()

    for table in query:
        curl.execute(table)

    conn.commit()


def tables():
    """Create table queries"""
    tb_orders = """CREATE TABLE IF NOT EXISTS orders(
        order_no SERIAL PRIMARY KEY NOT NULL,
        pickup CHARACTER VARYING(50) NOT NULL,
        destination CHARACTER VARYING(50) NOT NULL,
        weight FLOAT NOT NULL,
        price FLOAT NOT NULL,
        current_location CHARACTER VARYING(50) NOT NULL,
        sender INTEGER NOT NULL,
        status CHARACTER VARYING(10) NOT NULL,
        created DATE NOT NULL DEFAULT CURRENT_DATE);"""

    tb_users = """CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY NOT NULL,
        username CHARACTER VARYING(50) NOT NULL,
        firstname CHARACTER VARYING(50) NOT NULL,
        secondname CHARACTER VARYING(50) NOT NULL,
        gender CHARACTER VARYING(10) NOT NULL,
        email CHARACTER VARYING(50) NOT NULL,
        location CHARACTER VARYING(50) NOT NULL,
        type CHARACTER VARYING(10) NOT NULL,
        password TEXT NOT NULL);"""

    query = [tb_orders, tb_users]

    return query
