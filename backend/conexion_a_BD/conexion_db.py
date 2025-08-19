
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="admin",
        database="Panaderia"
    )
