from app.repositories import InventarioRepository
from app.models import Stock
from functools import reduce

class InventarioService:

    def __init__(self):
        self.inventario_respository = InventarioRepository()

    def ingresar_producto(self, stock: Stock):
        """ Registra stock de entrada """
        stock.entrada_salida = 1
        return self.inventario_respository.add(stock)

    def egresar_producto(self, stock: Stock):
        """ Registra stock de salida """
        stock.entrada_salida = 2
        return self.inventario_respository.add(stock)
    
    def get_by_product_id(self, producto_id: int):
        """ Devuelve lista de registros de inventario de un producto en base a su id. """
        return self.inventario_respository.get_by_product_id(producto_id)
    
    def calcular_stock(self, producto_id: int):
        """ Devuelve la cantidad de stock actual de un producto por su id. 
            Se calcula en base a todos los registros del stock
        """
        registros_inventario = self.get_by_product_id(producto_id)

        # Filtramos para separar entre registros de entrada (1) y de salida (2) - Complejidad Big(O): O(2*n)
        registros_entrada = list(filter(lambda stock: stock.entrada_salida == 1, registros_inventario))
        registros_salida = list(filter(lambda stock: stock.entrada_salida == 2, registros_inventario))

        # Contamos las cantidades de entrada y salida
        # cantidad_entrada = reduce(lambda stock1, stock2: stock1.cantidad + stock2.cantidad, registros_entrada)
        # cantidad_salida = reduce(lambda stock1, stock2: stock1.cantidad + stock2.cantidad, registros_salida, 0)

        # Nota: al poner un valor inicial 0, asume que todos los elementos de la lista deben ser del tipo int
        # y no puede usarse

        cantidad_entrada = 0
        cantidad_salida = 0
        for stock in registros_entrada:
            cantidad_entrada += stock.cantidad
        for stock in registros_salida:
            cantidad_salida += stock.cantidad

        # Finalmente calculamos el stock del producto
        stock = cantidad_entrada - cantidad_salida

        return stock