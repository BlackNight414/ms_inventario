from flask import Blueprint, jsonify, request
from app.services import InventarioService
from app.models import Stock

inventario = Blueprint('inventario', __name__)
inventario_service = InventarioService()

@inventario.route('/calcular_stock/<int:producto_id>', methods=['GET'])
def calcular_stock(producto_id):
    try:
        stock = inventario_service.calcular_stock(producto_id)
        resp = jsonify({
            'stock': stock
        })
        return resp, 200
    except BaseException as e:
        print(e)
        return jsonify({'msg': 'Error'}), 500

@inventario.route('/ingresar_producto', methods=['POST'])
def ingresar_producto():
    stock_data = request.get_json()

    try:
        stock = inventario_service.ingresar_producto(Stock(**stock_data))
        resp = jsonify({
            'id': stock.id,
            'producto_id': stock.producto_id,
            'fecha_transaccion': stock.fecha_transaccion,
            'cantidad': stock.cantidad,
            'entrada_salida': stock.entrada_salida
        })
        return resp, 200
    except BaseException as e:
        print(e)
        return jsonify({'msg': 'Error'}), 500


@inventario.route('/egresar_producto', methods=['POST'])
def egresar_producto():
    stock_data = request.get_json()

    try:
        stock = inventario_service.egresar_producto(Stock(**stock_data))
        resp = jsonify({
            'id': stock.id,
            'producto_id': stock.producto_id,
            'fecha_transaccion': stock.fecha_transaccion,
            'cantidad': stock.cantidad,
            'entrada_salida': stock.entrada_salida
        })
        return resp, 200
    except BaseException as e:
        return jsonify({'msg': 'Error'}), 500