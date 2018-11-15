import os
import psycopg2

url = "host='localhost' dbname='apisendit' port='5432' user='postgres' password='92203243'"

def connection(url):
    con = psycopg2.connect(url)
    return con

def init_db():
    con = connection(url)
    return con

def create_tables():
    tables_q = tables()
    conn = connection(url)
    curl = conn.cursor()

    for table in tables_q:
        curl.execute(table)

    conn.commit()

def destroy_tables():
    orders_tbl = """DROP TABLE IF EXISTS orders CASCADE;"""
    users_tbl = """DROP TABLE IF EXISTS users CASCADE;"""

    query = [orders_tbl, users_tbl]

    conn = connection(url)
    curl = conn.cursor()

    for table in query:
        curl.execute(table)

    conn.commit()

def tables():
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
        password TEXT NOT NULL);"""

    query = [tb_orders, tb_users]
    return query