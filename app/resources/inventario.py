from flask import Blueprint, jsonify, request
from app.services import InventarioService
from app.models import Stock
from app.mapping import StockSchema
import logging

inventario = Blueprint('inventario', __name__)
inventario_service = InventarioService()
stock_schema = StockSchema()

@inventario.route('/calcular_stock/<int:producto_id>', methods=['GET'])
def calcular_stock(producto_id):
    logging.info(f'Se ha consultado stock del producto id={producto_id}')
    try:
        stock = inventario_service.obtener_stock(producto_id)
        resp = jsonify({
            'stock': stock
        })
        return resp, 200
    except BaseException as e:
        logging.error(e)
        return jsonify({'msg': 'Error'}), 500

@inventario.route('/ingresar_producto', methods=['POST'])
def ingresar_producto():
    stock_data = request.get_json()

    try:
        stock = inventario_service.ingresar_producto(stock_schema.load(stock_data))
        logging.info(f'Stock ingresado del producto id={stock.producto_id} - Cantidad: {stock.cantidad}')
        return stock_schema.dump(stock), 200
    except BaseException as e:
        logging.error(e)
        return jsonify({'msg': 'Error'}), 500


@inventario.route('/egresar_producto', methods=['POST'])
def egresar_producto():
    stock_data = request.get_json()

    try:
        stock = inventario_service.egresar_producto(stock_schema.load(stock_data))
        if stock:
            logging.info(f'Stock retirado del producto id={stock.producto_id} - Cantidad: {stock.cantidad}')
            logging.info(f'Fecha transaccion: {stock.fecha_transaccion}')
            resp = stock_schema.dump(stock)
        else:
            logging.warning(f"Retiro stock de producto id={stock_data['producto_id']} rechazado: Insuficiente stock.")
            resp = jsonify({
                'status': 'Not stock',
                'msg': f"Retiro stock de producto id={stock_data['producto_id']} rechazado: Insuficiente stock."})
        return resp, 200
    except BaseException as e:
        logging.error(e)
        return jsonify({'msg': 'Error'}), 500