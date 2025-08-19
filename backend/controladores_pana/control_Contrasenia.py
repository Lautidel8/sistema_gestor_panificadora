
from backend.conexion_a_BD.conexion_db import conectar
import bcrypt

class Valida_contrasenia:

    def verficar_contra(contrasenia_ingresada):
        conexion = conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT contrasenia FROM Gerente")
        resultado = cursor.fetchone()
        
        
        if resultado:
            hash_guardado = resultado[0].encode('utf-8')
            if bcrypt.checkpw(contrasenia_ingresada.encode('utf-8'), hash_guardado):
                return True
            else:
                return False
        else:
            return False

        cursor.close()
        conexion.close()

