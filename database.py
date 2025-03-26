# database.py
import pyodbc

# Configuración de la conexión a SQL Server

def conectar_db():

    conexion = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"  # Driver de SQL Server
        "SERVER=LUNI\\SQLEXPRESS;"                 # Nombre del servidor (usa \\ para escapar la barra invertida)
        "DATABASE=umg_robot;"                      # Nombre de la base de datos
        "UID=sa;"                                  # Nombre de usuario
        "PWD=1234;"                                # Contraseña
    )
    return conexion

# Función para validar las credenciales del usuario
def validar_credenciales(correo_electronico: str, contrasenia: str) -> bool:
    conexion = conectar_db()
    cursor = conexion.cursor()

    # Buscar el usuario en la base de datos
    cursor.execute(
        "SELECT correo_electronico,nickname,id FROM usuarios WHERE correo_electronico = ? AND contrasenia = ?",
        (correo_electronico, contrasenia),
    )
    usuario = cursor.fetchone()

    conexion.close()

    # Si se encuentra un usuario, las credenciales son válidas
    return usuario is not None