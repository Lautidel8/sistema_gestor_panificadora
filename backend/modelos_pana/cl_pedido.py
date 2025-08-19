
class Pedido:
    def __init__(self,pedido_id,nombre_pedido,fecha_pedido,cliente,cantidad):
        self.pedido_id = pedido_id
        self.nombre_pedido = nombre_pedido
        self.fecha_pedido = fecha_pedido
        self.cliente = cliente
        self.cantidad = cantidad
        
class FuncionesPedido:
    def __init__(self,pedido:Pedido):
        self.pedido = pedido
        
    def mostrar_pedido(self):
        pass
    
    def generar_reporte(self):
        pass