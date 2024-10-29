from marshmallow import Schema, fields, post_load, validate
from app.models import Stock
from datetime import datetime

class StockSchema(Schema):
    id: int = fields.Integer()
    producto_id: int = fields.Integer(required=True)
    fecha_transaccion: datetime = fields.DateTime(load_default=datetime.today())
    cantidad: float = fields.Float(required=True)
    entrada_salida: int = fields.Integer(dump_only=True, validate=validate.OneOf([1,2]))

    @post_load
    def deserializar_stock(self, data, **kwargs):
        return Stock(**data)