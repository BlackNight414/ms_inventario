from app.repositories import InventarioRepository
from app.models import Stock
from app import cache
from threading import Lock, current_thread
from multiprocessing import Lock as w_lock
import logging
import os
import time
import random

locker = Lock() # Para controlar concurrencia entre hilos
worker_lock = w_lock() # Para controlar concurrencia entre workers

class InventarioService:

    def __init__(self):
        self.inventario_respository = InventarioRepository()

    def ingresar_producto(self, stock: Stock):
        """ Registra stock de entrada """
        stock.entrada_salida = 1
        result = self.inventario_respository.add(stock)

        # Actualizamos el stock en cache en caso de que exista
        stock_cache = cache.get(f'stock_producto_id_{stock.producto_id}')
        if stock_cache is not None:
            cache.set(f'stock_producto_id_{stock.producto_id}', stock_cache+stock.cantidad, timeout=30)

        return result

    def egresar_producto(self, stock: Stock):
        """ Registra stock de salida """
        logging.debug(f'Worker PID: {os.getpid()} - Pidiendo worker-lock')
        worker_lock.acquire() # worker pide token
        logging.debug(f'Thread {current_thread().name} del Worker PID: {os.getpid()} - Pidiendo lock')
        locker.acquire() # thread pide token

        # =====
        
        N_INTENTOS = 10
        for i in range(N_INTENTOS):
            #time.sleep(random.randint(1,5)/100) # tiempo de espera entre intentos 
            #acceso = cache.delete(f'acceso_retiro_producto_id_{stock.producto_id}')
            acceso = cache.delete('acceso_retiro_producto')
            if acceso: # Si se consiguió consumir la llave
                break  

        # =====

        if acceso:
            # Verificamos stock
            logging.debug('Tengo token para acceder al retiro del producto')
            result = 'Insuficiente stock'
            if self.obtener_stock(stock.producto_id) >= stock.cantidad:
                stock.entrada_salida = -1
                result = self.inventario_respository.add(stock)

                # Actualizamos el stock en cache en caso de que exista
                stock_cache = cache.get(f'stock_producto_id_{stock.producto_id}')
                if stock_cache is not None:
                    cache.set(f'stock_producto_id_{stock.producto_id}', stock_cache-stock.cantidad, timeout=30)

            # Liberamos token (volvemos a setear la llave)
            cache.set('acceso_retiro_producto', True, timeout=0)
        else:
            result = 'No se pudo acceder al proceso de retiro'

        logging.debug(f'Thread {current_thread().name} del Worker PID: {os.getpid()} - Liberando lock')
        locker.release() # thread libera token
        logging.debug(f'Worker PID: {os.getpid()} - Liberando worker-lock')
        worker_lock.release() # worker libera token
        return result
    
    def get_by_product_id(self, producto_id: int):
        """ Devuelve lista de registros de inventario de un producto en base a su id. """
        return self.inventario_respository.get_by_product_id(producto_id)
    
    def obtener_stock(self, producto_id: int):
        """ Devuelve la cantidad de stock actual de un producto por su id. 
            Se calcula en base a todos los registros del stock
        """
        stock_producto = cache.get(f'stock_producto_id_{producto_id}') # consultamosa a cache
        if stock_producto is None:
            stock_producto = self.inventario_respository.get_product_stock(producto_id)
            cache.set(f'stock_producto_id_{producto_id}', stock_producto, timeout=30) # seteamos en cache si no está
        return stock_producto