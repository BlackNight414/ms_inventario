from app.repositories import InventarioRepository
from app.models import Stock


class InventarioService:

    def __init__(self):
        self.pagos_respository = InventarioRepository()

    def add(self, stock: Stock):
        return self.pagos_respository.add(stock)