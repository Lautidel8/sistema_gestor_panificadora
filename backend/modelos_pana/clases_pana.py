


    
class Producto:
    def __init__(self,producto_id,nombre_producto,cantidad):
        self.producto_id = producto_id
        self.nombre_producto = nombre_producto
        self.cantidad = cantidad

class Materia_prima:
    def __init__(self,materia_pr_id,nombre_materia_pr,cantidad_actual,distribuidor):
        self.mater_pr_id = materia_pr_id
        self.nombre_mat_pr = nombre_materia_pr
        self.cantidad_actual = cantidad_actual
        self.distribuidor = distribuidor
        
class DetallePedido:
    def __init__(self, detalle_id, cantidad, pedido_id, producto_id):
        self.detalle_id = detalle_id
        self.cantidad = cantidad
        self.pedido_id = pedido_id
        self.producto_id = producto_id


# Esta tabla representa una relación muchos a muchos entre Producto y MateriaPrima
# incluyendo la cantidad y unidad necesaria de materia prima para cada producto:

class MateriaPrimaProducto:
    def __init__(self, producto_id, materia_prima_id, cantidad, unidad):
        self.producto_id = producto_id
        self.materia_prima_id = materia_prima_id
        self.cantidad = cantidad
        self.unidad = unidad

#  Esta clase es útil para calcular automáticamente el consumo de materias primas por producto,
#  y para manejar el stock en producción.
