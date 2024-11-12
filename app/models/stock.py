from app import db
from datetime import datetime

class Stock(db.Model):
    
    __tablename__ = 'inventario'

    id: int = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    producto_id: int = db.Column('producto_id', db.Integer, nullable=False)
    fecha_transaccion: datetime = db.Column('fecha_transaccion', db.DateTime, nullable=False, default=datetime.today())
    cantidad: int = db.Column('cantidad', db.Integer, nullable=False)
    entrada_salida: int = db.Column('entrada_salida', db.Integer, nullable=False) # 1: entrada -1: salida

    # Restricción adicional para el campo entrada_salida
    __table_args__ = (
        db.CheckConstraint('entrada_salida = 1 OR entrada_saida = -1'),
    )