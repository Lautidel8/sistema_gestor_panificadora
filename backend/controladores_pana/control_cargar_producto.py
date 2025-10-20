
from backend.conexion_a_BD.conexion_db import conectar

class control_cargar_producto:
    
    def __init__(self):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()
    
    def cargar_producto(self, nombre_producto, precio_unitario):
        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM Producto WHERE LOWER(nombre_producto) = LOWER(%s)",
                (nombre_producto,)
            )
            resultado = self.cursor.fetchone()
            
            if resultado[0] > 0:
                return False

            id_producto = self.obtener_ultimo_id_producto()

            # Usar explícitamente el ID calculado
            self.cursor.execute(
                "INSERT INTO Producto (id_producto, nombre_producto, precio_unitario) VALUES (%s, %s, %s)",
                (id_producto, nombre_producto, precio_unitario)
            )
            
            self.conexion.commit()
            return id_producto
            
        except Exception as e:
            print("Error al cargar producto:", e)
            self.conexion.rollback()
            return False
        
    def eliminar_producto(self, nombre_producto):
        try:
            # Primero obtener el ID del producto
            self.cursor.execute(
                "SELECT id_producto FROM Producto WHERE nombre_producto = %s",
                (nombre_producto,)
            )
            resultado = self.cursor.fetchone()
            
            if not resultado:
                print(f"No se encontró el producto '{nombre_producto}'")
                return False
                
            id_producto = resultado[0]
            
            # Primero eliminar las relaciones en MateriaPrima_Producto
            self.cursor.execute(
                "DELETE FROM MateriaPrima_Producto WHERE id_producto = %s",
                (id_producto,)
            )
            
            # Luego eliminar el producto
            self.cursor.execute(
                "DELETE FROM Producto WHERE id_producto = %s",
                (id_producto,)
            )
            
            self.conexion.commit()
            return True
            
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            self.conexion.rollback()
            return False   
        
    def listar_productos(self):
        try:
            self.cursor.execute("SELECT id_producto, nombre_producto FROM Producto")
            return self.cursor.fetchall()
        except Exception as e:
            print("Error al obtener productos:", e)
            return []
    
    def agregar_materia_prima_a_producto(self, id_producto, id_materia_prima, cantidad):

        try:
            self.cursor.execute(
                "INSERT INTO MateriaPrima_Producto (id_materia_prima, id_producto, cantidad) VALUES (%s, %s, %s)",
                (id_materia_prima, id_producto, cantidad)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error al agregar materia prima al producto:", e)
            self.conexion.rollback()
            return False
            
    def obtener_ultimo_id_producto(self):

        try:
            self.cursor.execute("SELECT MAX(id_producto) FROM Producto")
            resultado = self.cursor.fetchone()
            if resultado[0] is None:
                return 1
            return resultado[0] + 1
        
        except Exception as e:
            print("Error al obtener último ID:", e)
            return 1
        
    def obtener_producto_por_id(self, id_producto: int):
        try:
            self.cursor.execute(
                "SELECT id_producto, nombre_producto, precio_unitario FROM Producto WHERE id_producto = %s",
                (id_producto,)
            )
            return self.cursor.fetchone()
        except Exception as e:
            print("Error al obtener producto:", e)
            return None

    def actualizar_producto(self, id_producto: int, nuevo_nombre: str, nuevo_precio: float):
        try:
            # Evitar duplicados por nombre (excluyendo el mismo producto)
            self.cursor.execute(
                "SELECT COUNT(*) FROM Producto WHERE LOWER(nombre_producto) = LOWER(%s) AND id_producto <> %s",
                (nuevo_nombre, id_producto)
            )
            existe = self.cursor.fetchone()[0]
            if existe > 0:
                return "duplicado"

            self.cursor.execute(
                "UPDATE Producto SET nombre_producto = %s, precio_unitario = %s WHERE id_producto = %s",
                (nuevo_nombre, nuevo_precio, id_producto)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error al actualizar producto:", e)
            self.conexion.rollback()
            return False

    def cerrar_conexion(self):

        if self.conexion:
            self.cursor.close()
            self.conexion.close()