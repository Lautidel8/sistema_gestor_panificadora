
from backend.conexion_a_BD.conexion_db import conectar

class CargarMateriaPrima:
    
    def __init__(self):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()
    
    def listar_unidades(self):
        try:
            self.cursor.execute("SELECT id_unidad, nombre FROM unidad")
            return self.cursor.fetchall()
        except Exception as e:
            print("Error al obtener unidades:", e)
            return []

    def obtener_nombre_unidad(self, id_unidad):
        try:
            self.cursor.execute("SELECT nombre FROM unidad WHERE id_unidad = %s", (id_unidad,))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado[0]
            return None
        except Exception as e:
            print("Error al obtener nombre de unidad:", e)
            return None

    def cargar_materia_prima(self, nombre, distribuidor, id_unidad):
        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM MateriaPrima WHERE LOWER(nombre_materia_prima) = LOWER(%s)",
                (nombre,)
            )
            resultado = self.cursor.fetchone()
            
            if resultado[0] > 0:
                return False
            
            self.cursor.execute(
                "INSERT INTO MateriaPrima (nombre_materia_prima, distribuidor, id_unidad, stock) VALUES (%s, %s, %s, %s)",
                (nombre, distribuidor, id_unidad, 0)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error al cargar materia prima:", e)
            self.conexion.rollback()
            return False

    def eliminar_materia_prima(self, nombre):
        try:
            # Primero verificar si la materia prima está asociada a algún producto
            self.cursor.execute("""
                SELECT COUNT(*) FROM MateriaPrima_Producto mp 
                JOIN MateriaPrima m ON mp.id_materia_prima = m.id_materia_prima
                WHERE m.nombre_materia_prima = %s
            """, (nombre,))
            
            resultado = self.cursor.fetchone()
            
            if resultado and resultado[0] > 0:
                # La materia prima está asociada a productos
                print("No se puede eliminar la materia prima ya que está asignada a un producto")
                return "producto_asociado"  # Retornar un código específico en lugar de False
            
            # Si no está asociada, proceder con la eliminación
            self.cursor.execute(
                "DELETE FROM MateriaPrima WHERE nombre_materia_prima = %s",
                (nombre,)
            )
            self.conexion.commit()
            return True
        
        except Exception as e:
            print("Error al eliminar materia prima:", e)
            self.conexion.rollback()
            
            # Detectar el error específico de clave foránea
            if isinstance(e, Exception) and "foreign key constraint fails" in str(e).lower():
                return "producto_asociado"
            
            return False
    
    def listar_materias_primas(self):
        try:
            self.cursor.execute("""
                SELECT m.id_materia_prima,
                       m.nombre_materia_prima,
                       m.stock,
                       m.id_unidad,
                       u.nombre AS nombre_unidad
                FROM MateriaPrima m
                LEFT JOIN unidad u ON u.id_unidad = m.id_unidad
                ORDER BY m.nombre_materia_prima
            """)
            return self.cursor.fetchall()
        except Exception as e:
            print("Error al listar materias primas:", e)
            return []

    def actualizar_stock_materia_prima(self, id_mp, delta_stock):

        try:
            self.cursor.execute(
                "SELECT stock FROM MateriaPrima WHERE id_materia_prima = %s",
                (id_mp,)
            )
            fila = self.cursor.fetchone()

            if fila is None:
                print(f"No existe materia prima con id {id_mp}")
                return False

            stock_actual = float(fila[0])
            nuevo_stock = stock_actual + delta_stock

            if nuevo_stock < 0:
                print("Stock insuficiente. Operación cancelada.")
                return False

            self.cursor.execute(
                "UPDATE MateriaPrima SET stock = %s WHERE id_materia_prima = %s",
                (nuevo_stock, id_mp)
            )
            self.conexion.commit()
            return True

        except Exception as e:
            print("Error al actualizar stock:", e)
            self.conexion.rollback()
            return False


    def cerrar_conexion(self):
        
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
            self.cursor = None
        
        if hasattr(self, 'conexion') and self.conexion:
            self.conexion.close()
            self.conexion = None
            
