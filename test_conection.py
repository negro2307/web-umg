# test_connection.py
from database import conectar_db

try:
    conexion = conectar_db()
    print("¡Conexión exitosa!")
    conexion.close()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")