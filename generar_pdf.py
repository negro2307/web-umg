# generar_pdf.py
import pyodbc
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from io import BytesIO
import qrcode  # Asumiendo que instalaste la librería oficial 'qrcode'
from database import conectar_db  # Importamos la función de conexión

# Registrar las fuentes Poppins
pdfmetrics.registerFont(TTFont("Poppins-Bold", "Poppins-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Poppins-Regular", "Poppins-Regular.ttf"))

def obtener_ultimo_usuario():
    """
    Obtiene el id, nickname, correo electrónico y contraseña
    del último usuario registrado en la base de datos.
    """
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        # Consulta para obtener el último usuario registrado
        # Asegúrate de que 'contrasenia' sea el nombre de la columna de la contraseña
        cursor.execute(
            """
            SELECT TOP 1
                id,
                nickname,
                correo_electronico,
                contrasenia
            FROM usuarios
            ORDER BY id DESC
            """
        )
        ultimo_usuario = cursor.fetchone()
        conexion.close()

        if ultimo_usuario:
            # Retorna (id, nickname, correo_electronico, contrasenia)
            return ultimo_usuario
        else:
            raise Exception("No hay usuarios registrados en la base de datos.")

    except Exception as e:
        print(f"Error al obtener el último usuario: {str(e)}")
        return None

def generar_qr_contrasena(contrasenia: str):
    """
    Genera un código QR en memoria basado en la contraseña del usuario.
    """
    try:
        # Crear el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        # Agregamos la contraseña como contenido del QR
        qr.add_data(contrasenia)
        qr.make(fit=True)

        # Crear una imagen del código QR en memoria
        img = qr.make_image(fill_color="#000000", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        return buffer

    except Exception as e:
        print(f"Error al generar el código QR: {str(e)}")
        return None

def crear_pdf(nickname: str, correo: str, contrasenia: str, output_pdf: str, fondo_path: str):
    """
    Crea un PDF con:
      - Imagen de fondo (credencia2.jpg o la que uses).
      - Nickname y correo electrónico.
      - Un código QR que contiene la contraseña.
    """
    try:
        # Crear un PDF
        c = canvas.Canvas(output_pdf, pagesize=A4)

        # Agregar la imagen de fondo (cubre todo A4: 595x842 aprox)
        fondo = ImageReader(fondo_path)
        c.drawImage(fondo, 0, 0, width=A4[0], height=A4[1])

        # Configurar color y fuentes
        color_texto = HexColor("#000000")  # Negro (cámbialo si quieres otro)
        c.setFillColor(color_texto)

        # Título o Nickname
        c.setFont("Poppins-Bold", 20)
        # Ajusta las coordenadas para que coincidan con tu diseño
        # Por ejemplo, (x=300, y=480)
        c.drawString(300, 480, f"{nickname}")

        # Correo
        c.setFont("Poppins-Regular", 16)
        c.drawString(300, 450, f"{correo}")

        # Generar el código QR con la contraseña
        qr_buffer = generar_qr_contrasena(contrasenia)
        if qr_buffer:
            qr_image = ImageReader(qr_buffer)
            # Ajusta las coordenadas (x, y) y tamaño para que el QR
            # aparezca donde está la "caja" en tu diseño
            c.drawImage(qr_image, 60, 360, width=120, height=120)

        # (Opcional) Mostrar la contraseña en texto (si lo deseas)
        # c.setFont("Poppins-Regular", 12)
        # c.drawString(300, 420, f"Contraseña: {contrasenia}")

        # Guardar el PDF
        c.save()
        print(f"PDF generado y guardado en: {output_pdf}")

    except Exception as e:
        print(f"Error al generar el PDF: {str(e)}")

if __name__ == "__main__":
    # Obtener el último usuario registrado
    usuario = obtener_ultimo_usuario()

    if usuario:
        # Ahora la consulta retorna (id, nickname, correo, contrasenia)
        id_usuario, nickname, correo, contrasenia = usuario

        # Ruta de la imagen de fondo
        # Ajusta esto si tu imagen se llama credencia2.jpg, etc.
        fondo_path = "credencia2.jpg"

        # Generar el PDF
        output_pdf = f"tarjeta_{nickname}.pdf"
        crear_pdf(nickname, correo, contrasenia, output_pdf, fondo_path)
    else:
        print("No se pudo obtener la información del último usuario.")

