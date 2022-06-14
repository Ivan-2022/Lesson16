from flask import Flask, jsonify, abort, request
from models import db, User, Order, Offer
import utils
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mybase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

app.app_context().push()
with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()
    utils.create_table_users("data/users.json")
    utils.create_table_orders("data/orders.json")
    utils.create_table_offers("data/offers.json")


@app.route("/users")
def get_all_users():
    """
    Получение всех пользователей
    """
    users = db.session.query(User).all()
    result = []
    for user in users:
        result.append(user.serialize())
    return jsonify(result)


@app.route("/users/<int:user_id>")
def get_one_user(user_id):
    """
    Получение одного пользователя по идентификатору
    """
    user = db.session.query(User).filter(User.id == user_id).first()
    if user is None:
        abort(404)
    return jsonify(user.serialize())


@app.route("/orders")
def get_all_orders():
    """
    Получение всех заказов
    """
    orders = db.session.query(Order).all()
    result = []
    for order in orders:
        result.append(order.serialize())
    return jsonify(result)


@app.route("/orders/<int:order_id>")
def get_one_order(order_id):
    """
    Получение одного заказа по идентификатору
    """
    order = db.session.query(Order).filter(Order.id == order_id).first()
    if order is None:
        abort(404)
    return jsonify(order.serialize())


@app.route("/offers")
def get_all_offers():
    """
    Получение всех предложений
    """
    offers = db.session.query(Offer).all()
    result = []
    for offer in offers:
        result.append(offer.serialize())
    return jsonify(result)


@app.route("/offers/<int:offer_id>")
def get_one_offer(offer_id):
    """
    Получение одного предложения по идентификатору
    """
    offer = db.session.query(Offer).filter(Offer.id == offer_id).first()
    if offer is None:
        abort(404)
    return jsonify(offer.serialize())


@app.route("/users", methods=['POST'])
def create_user():
    """
    Создание нового пользователя
    """
    data = request.json
    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        age=data.get('age'),
        email=data.get('email'),
        role=data.get('role'),
        phone=data.get('phone')
        )
    db.session.add(user)
    db.session.commit()
    db.session.close()
    return "Пользователь создан"


@app.route("/users/<int:user_id>", methods=['PUT'])
def update_user(user_id):
    """
    Обновление пользователя
    """
    data = request.json
    user = db.session.query(User).filter(User.id == user_id).first()
    if user is None:
        abort(404)
    db.session.query(User).filter(User.id == user_id).update(data)
    db.session.commit()
    db.session.close()
    return "Данные пользователя обновлены"


@app.route("/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    """
    Удаление пользователя
    """
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    db.session.close()
    return "Пользователь удален"


@app.route("/orders", methods=['POST'])
def create_order():
    """
    Создание нового заказа
    """
    data = request.json

    month_start, day_start, year_start = data['start_date'].split("/")
    month_end, day_end, year_end = data['end_date'].split("/")
    order = Order(
        name=data.get('name'),
        description=data.get('description'),
        start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
        end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
        address=data.get('address'),
        price=data.get('price'),
        customer_id=data.get('customer_id'),
        executor_id=data.get('executor_id')
        )

    db.session.add(order)
    db.session.commit()
    db.session.close()
    return "Новый заказ создан"


@app.route("/orders/<int:order_id>", methods=['PUT'])
def update_order(order_id):
    """
    Обновление заказа
    """
    data = request.json
    order = db.session.query(Order).filter(Order.id == order_id).first()
    if order is None:
        abort(404)
    db.session.query(Order).filter(Order.id == order_id).update(data)
    db.session.commit()
    db.session.close()
    return "Заказ обновлен"


@app.route("/orders/<int:order_id>", methods=['DELETE'])
def delete_order(order_id):
    """
    Удаление заказа
    """
    order = Order.query.get(order_id)
    db.session.delete(order)
    db.session.commit()
    db.session.close()
    return "Заказ удален"


@app.route("/offers", methods=['POST'])
def create_offer():
    """
    Создание нового предложения
    """
    data = request.json
    offer = Offer(
        order_id=data.get('order_id'),
        executor_id=data.get('executor_id')
        )

    db.session.add(offer)
    db.session.commit()
    db.session.close()
    return "Новое предложение создано"


@app.route("/offers/<int:offer_id>", methods=['PUT'])
def update_offer(offer_id):
    """
    Обновление предложения
    """
    data = request.json
    offer = db.session.query(Offer).filter(Offer.id == offer_id).first()
    if offer is None:
        abort(404)
    db.session.query(Offer).filter(Offer.id == offer_id).update(data)
    db.session.commit()
    db.session.close()
    return "Предложение обновлено"


@app.route("/offers/<int:offer_id>", methods=['DELETE'])
def delete_offer(offer_id):
    """
    Удаление предложения
    """
    offer = Offer.query.get(offer_id)
    db.session.delete(offer)
    db.session.commit()
    db.session.close()
    return "Предложение удалено"


if __name__ == '__main__':
    app.run()
