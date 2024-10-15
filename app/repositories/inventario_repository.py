from app import db
from app.models import Stock


class InventarioRepository:
    
    def add(self, stock: Stock):
        db.session.add(stock)
        db.session.commit()
        return stock