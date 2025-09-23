
from backend.conexion_a_BD.conexion_db import conectar

class control_cargar_producto:
    
    def __init__(self):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()
    
    
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
                return 1  # Si no hay productos, empezar con 1
            return resultado[0] + 1
        except Exception as e:
            print("Error al obtener último ID:", e)
            return 1

    def cerrar_conexion(self):

        if self.conexion:
            self.cursor.close()
            self.conexion.close()