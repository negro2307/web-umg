# generar_qr.py
import pyodbc
import qrcode
from database import conectar_db  # Importamos la función de conexión

def obtener_ultimo_usuario():
    """
    Obtiene el ID del último usuario registrado en la base de datos.
    """
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        # Consulta para obtener el último usuario registrado
        cursor.execute(
            "SELECT TOP 1 id FROM usuarios ORDER BY id DESC"
        )
        ultimo_usuario = cursor.fetchone()

        conexion.close()

        if ultimo_usuario:
            return ultimo_usuario[0]  # Retorna el ID del último usuario
        else:
            raise Exception("No hay usuarios registrados en la base de datos.")

    except Exception as e:
        print(f"Error al obtener el último usuario: {str(e)}")
        return None

def generar_qr(id_usuario: str):
    """
    Genera un código QR basado en el ID del usuario.
    """
    try:
        # Crear el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(id_usuario)
        qr.make(fit=True)

        # Guardar el código QR como una imagen
        img = qr.make_image(fill_color="#DFA02B", back_color="white")
        qr_path = f"qr_{id_usuario}.png"
        img.save(qr_path)

        print(f"Código QR generado y guardado en: {qr_path}")
        return qr_path

    except Exception as e:
        print(f"Error al generar el código QR: {str(e)}")
        return None

if __name__ == "__main__":
    # Obtener el ID del último usuario registrado
    id_usuario = obtener_ultimo_usuario()

    if id_usuario:
        # Generar el código QR
        qr_path = generar_qr(id_usuario)
        if qr_path:
            print(f"Código QR generado exitosamente para el usuario con ID: {id_usuario}")
        else:
            print("No se pudo generar el código QR.")
    else:
        print("No se pudo obtener el ID del último usuario.")