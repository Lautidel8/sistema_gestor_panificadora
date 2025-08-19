import bcrypt
from conexion_a_BD.conexion_db import conectar
from modelos_pana.cl_gerente import Gerente

def insertar_gerente(gerente:Gerente):
    conexion = conectar()
    cursor = conexion.cursor()

    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(gerente.contrasenia.encode('utf-8'), bcrypt.gensalt())

    
    query = """
    insert into Gerente (correo_electronico,nombre_gerente,contrasenia)
    values (%s, %s, %s)
    """
    
    valores = (gerente.correo, gerente.nombre_gerente, hashed_password)
    
    cursor.execute(query, valores)
    conexion.commit()
    cursor.close()
    conexion.close()
    
    print("okkk")