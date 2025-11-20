from django.db import connection
from contextlib import closing


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row)) for row in cursor.fetchall()
    ]


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return  dict(zip(columns, row))


def get_order_by_user(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT fo.id, fc.first_name, 
        fc.last_name, fo.address, fo.payment_type,
        fo.status,  fo.created_at FROM "Food_order" fo 
        INNER JOIN "Food_customer" fc  ON fc.id = fo.customer_id 
        WHERE fo.customer_id = %s
        """, [id])
        order = dict_fetchall(cursor)
        return order


def get_product_by_order(id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""
        SELECT fo.count, fo.price, fo.created_at,
        fp.title FROM "Food_orderproduct" fo  INNER JOIN "Food_product" fp  ON
        fo.product_id = fp.id where order_id = %s
        """, [id])
        order_product = dict_fetchall(cursor)
        return order_product


def get_table():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""
        SELECT fo.product_id, COUNT(fo.product_id), 
        fp.title  
        FROM "Food_orderproduct" fo 
        INNER JOIN "Food_product" fp 
        ON fp.id = fo.product_id
        GROUP BY fo.product_id, fp.title
        ORDER BY count DESC
        LIMIT 10;
        """)
        table = dict_fetchall(cursor)
        return table

