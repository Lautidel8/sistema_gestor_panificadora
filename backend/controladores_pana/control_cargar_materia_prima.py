
from backend.conexion_a_BD.conexion_db import conectar

class CargarMateriaPrima:
    
    def __init__(self):
        self.conexion = conectar()
        self.cursor = self.conexion.cursor()
        
        
    def cargar_materia_prima(self, nombre, distribuidor):
        try:
            self.cursor.execute(
                "INSERT INTO MateriaPrima (nombre_materia_prima, distribuidor) VALUES (%s, %s)",
                (nombre, distribuidor)
            )
            self.conexion.commit()
            return True
        
        except Exception as e:
            print("Error al cargar materia prima:", e)
            self.conexion.rollback()
            return False
    
    
    # Funcion que cierra el cursor y la conexión a la base de datos para ahorro de recursos.    
    def cerrar_conexion(self):
        
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
            self.cursor = None
        
        if hasattr(self, 'conexion') and self.conexion:
            self.conexion.close()
            self.conexion = None