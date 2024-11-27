from app.repositories import InventarioRepository
from app.models import Stock
from threading import Lock

locker = Lock() # Para controlar concurrencia entre hilos

class InventarioService:

    def __init__(self):
        self.inventario_respository = InventarioRepository()

    def ingresar_producto(self, stock: Stock):
        """ Registra stock de entrada """
        stock.entrada_salida = 1
        return self.inventario_respository.add(stock)

    def egresar_producto(self, stock: Stock):
        """ Registra stock de salida """
        locker.acquire() # pedimos el token
        # Verificamos stock
        result = None
        if self.obtener_stock(stock.producto_id) >= stock.cantidad:
            stock.entrada_salida = -1
            result = self.inventario_respository.add(stock)
        locker.release() # liberamos token
        return result
    
    def get_by_product_id(self, producto_id: int):
        """ Devuelve lista de registros de inventario de un producto en base a su id. """
        return self.inventario_respository.get_by_product_id(producto_id)
    
    def obtener_stock(self, producto_id: int):
        """ Devuelve la cantidad de stock actual de un producto por su id. 
            Se calcula en base a todos los registros del stock
        """
        return self.inventario_respository.get_product_stock(producto_id)