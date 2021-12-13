import datetime
from xmlrpc.client import Boolean

from flask import Flask, request
from flask import jsonify
from peewee import Model, AutoField, CharField, BooleanField, SqliteDatabase

db = SqliteDatabase('taxi.db')

app = Flask(__name__)


class Drivers(Model):
    id = AutoField(primary_key=True)
    name = CharField(null=False)
    car = CharField(null=False)

    class Meta:
        database = db


def create_table():
    with db:
        db.create_tables([Drivers])


create_table()


class Clients(Model):
    id = AutoField(primary_key=True)
    name = CharField(null=False)
    is_vip = BooleanField(Boolean)

    class Meta:
        database = db


def create_table():
    with db:
        db.create_tables([Clients])


create_table()


class Reservations(Model):
    client_id = AutoField(primary_key=True)
    driver_id = AutoField(primary_key=True)
    address_from = CharField(null=False)
    address_to = CharField(null=False)
    date_created = CharField(null=False)
    status = CharField(null=False)

    class Meta:
        database = db


def create_table():
    with db:
        db.create_tables([Reservations])


create_table()

class Orders(Model):
    client_id = AutoField(primary_key=True)
    driver_id = AutoField(primary_key=True)
    address_from = CharField(null=False)
    address_to = CharField(null=False)
    date_created = CharField(null=False)
    status = CharField(null=False)

    class Meta:
        database = db

def create_table():
    with db:
        db.create_tables([Orders])



@app.route('/drivers/<int:id>', methods=['GET'])
def get_driver_by_id(id):
    driver = Drivers.get_by_id(id)
    data = {"id": driver.id, "name": driver.name, "car": driver.car}
    return jsonify(data), 200


@app.route('/drivers', methods=['POST'])
def create_driver():
    json = request.get_json()
    driver = Drivers.create(name=json.get('name'), car=json.get('car'))
    return f"Водитель добавлен с даннымиЖ id: {driver.id}", 201


@app.route('/drivers/<int:id>', methods=['DELETE'])
def delete_driver(id):
    delete_driver = Drivers.delete_by_id(id)
    return f"Удален  водитель с id : {id}", 204


@app.route('/clients/<int:id>', methods=['GET'])
def get_client_by_id(id):
    client = Clients.get_by_id(id)
    data = {"id": client.id, "name": client.name, "is_vip": client.is_vip, "order": client.order}
    return jsonify(data), 200


@app.route('/clients/<int:id>', methods=['DELETE'])
def delete_client(id):
    delete_client = Clients.delete_by_id(id)
    return f"Удален клинт с id : {id}", 204


@app.route('/clients', methods=['POST'])
def create_client():
    json = request.get_json()
    client = Clients.create(name=json.get('name'), is_vip=json.get('is_vip'))
    return f"Клиент добавлен с данными id: {client.id}", 201


@app.route('/reservations/<int: id>', methods=['GET'])
def get_reservation_by_id(id):
    reservation = Reservations.get_by_id(id)
    data = {"id": reservation.id,
            "client_id": reservation.client_id,
            "driver_id": reservation.driver_id,
            "date_created": reservation.date_created,
            "status": reservation.status,
            "address_from": reservation.address_from,
            "address_to": reservation.address_to}
    return jsonify(data), 200


@app.route('/reservations', methods=['POST'])
def create_reservation():
    json = request.get_json()
    client_id = json.get('client_id')
    driver_id = json.get('driver_id')
    client = Clients.get_by_id(client_id)
    driver = Drivers.get_by_id(driver_id)
    if client is not None and driver is not None:
        reservation = Reservations(address_from=json.get('address_from'),
                                   address_to=json.get('address_to'),
                                   client_id=json.get('client_id'),
                                   driver_id=json.get('driver_id'),
                                   date_created=datetime.datetime.now(),
                                   status='not_accepted')
        return f"Заказ добавлен с данными id: {reservation.id}", 201
    else:
        return "Клиент / водитель не найден", 404


@app.route('/orders/<id>', methods=['PUT'])
def update_order(id):
    json = request.get_json()
    order = Orders.put_by_id(id)
    if order.status == 'not_accepted':
        order.address_from = json.get('address_from')
        order.address_to = json.get('address_to')
        order.client_id = json.get('client_id')
        order.driver_id = json.get('driver_id')
        order.date_created = datetime.datetime.now()
        return f"Заказ c id : {order.id} отредактирован", 200

    else:
        return "Заказ не может быть изменен", 400


@app.route('/orders/<id>/change-status', methods=['PUT'])
def change_order_status(id):
    json = request.get_json()
    new_status = json.get('status')
    order = Orders.put_by_id(id)
    if order.status == 'not_accepted':
        if new_status in ('not_accepted', 'in_progress', 'cancelled'):
            order.status = new_status
            return f"Статус заказа с id: {order.id} успешно изменен на {new_status}", 200
        elif new_status == 'done':
            return f"Статус заказа с id: {order.id} не может быть изменен на {new_status}", 400
        else:
            return "Неверный статус заказа", 400

    elif order.status == 'in_progress':
        if new_status in ('in_progress', 'cancelled', 'done'):
            order.status = new_status
            return f"Статус заказа с id: {order.id} успешно изменен на {new_status}", 200
        elif new_status == 'not_accepted':
            return f"Статус заказа с id: {order.id} НЕ может быть изменен на {new_status}", 400
        else:
            return "Неверный статус заказа", 400

    elif order.status in ('done', 'cancelled'):
        if new_status in ('in_progress', 'cancelled', 'done', 'not_accepted'):
            return f"Статус заказа с id: {order.id} НЕ может быть изменен на {new_status}", 400
        else:
            return "Неверный статус заказа", 400


@app.route('/orders/<int:id>', methods=['GET'])
def get_order_by_id(id):
    order = Orders.get_by_id(id)
    data = {"id": order.id,
            "client_id": order.client_id,
            "driver_id": order.driver_id,
            "date_created": order.date_created,
            "status": order.status,
            "address_from": order.address_from,
            "address_to": order.address_to}
    return data, 200