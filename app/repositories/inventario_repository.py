from app import db
from app.models import Stock
from sqlalchemy import func


class InventarioRepository:
    
    def add(self, stock: Stock):
        db.session.add(stock)
        db.session.commit()
        return stock
    
    def get_by_product_id(self, producto_id: int):
        return db.session.query(Stock).filter(Stock.producto_id == producto_id).all()
    
    def get_product_stock(self, producto_id: int):
        return db.session.query(
            func.sum(Stock.cantidad * Stock.entrada_salida)) \
            .filter(Stock.producto_id == producto_id).scalar()