import json
import datetime

from models import *

db = SQLAlchemy()


def load_data(file_name):
    """
    Загружает данные json из папки data
    """
    with open(file_name, "r", encoding='utf-8') as file:
        content = json.load(file)
    return content


def create_table_users(file_name):
    """
    Создаем таблицу users в БД
    """
    data = load_data(file_name)
    for user in data:
        db.session.add(User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']))

        db.session.commit()


def create_table_orders(file_name):
    """
    Создаем таблицу orders в БД
    """
    data = load_data(file_name)
    for order in data:
        month_start, day_start, year_start = order['start_date'].split("/")
        month_end, day_end, year_end = order['end_date'].split("/")
        db.session.add(Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
            end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        ))

        db.session.commit()


def create_table_offers(file_name):
    """
    Создаем таблицу offers в БД
    """
    data = load_data(file_name)
    for offer in data:
        db.session.add(Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        ))

        db.session.commit()
