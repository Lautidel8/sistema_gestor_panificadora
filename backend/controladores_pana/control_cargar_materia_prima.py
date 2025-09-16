
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
        
    def cargar_materia_prima(self, nombre, distribuidor, id_unidad):

        try:
            self.cursor.execute(
                "INSERT INTO MateriaPrima (nombre_materia_prima, distribuidor, id_unidad) VALUES (%s, %s, %s)",
                (nombre, distribuidor, id_unidad)
            )
            self.conexion.commit()
            return True
        except Exception as e:
            print("Error al cargar materia prima:", e)
            self.conexion.rollback()
            return False

    def eliminar_materia_prima(self, nombre):
        try:
            self.cursor.execute(
                "DELETE FROM MateriaPrima WHERE nombre_materia_prima = %s",
                (nombre,)
            )
            self.conexion.commit()
            return True
        
        except Exception as e:
            print("Error al eliminar materia prima:", e)
            self.conexion.rollback()
            return False
    
    def listar_materias_primas(self):
        self.cursor.execute("SELECT nombre_materia_prima FROM MateriaPrima")
        return [row[0] for row in self.cursor.fetchall()]
       
    def cerrar_conexion(self):
        
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
            self.cursor = None
        
        if hasattr(self, 'conexion') and self.conexion:
            self.conexion.close()
            self.conexion = None