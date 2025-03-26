import reflex as rx
import re
from .database import conectar_db  # Importamos la función de conexión

class FormularioRegistroState(rx.State):
    correo: str = ""
    contrasena: str = ""
    confirmar_contrasena: str = ""
    telefono: str = ""
    nickname: str = ""
    avatar: str = ""
    codigo_verificacion: str = ""
    correo_valido: bool = True
    codigo_valido: bool = True

    def validar_correo(self):
        # Expresión regular para validar el correo electrónico
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        self.correo_valido = re.match(regex, self.correo) is not None

    def validar_codigo(self):
        # Validar que el código tenga exactamente 6 dígitos
        self.codigo_valido = len(self.codigo_verificacion) == 6 and self.codigo_verificacion.isdigit()

    def insertar_usuario(self):
        try:
            # Validar el correo y el código antes de insertar
            self.validar_correo()
            self.validar_codigo()

            if not self.correo_valido:
                return rx.window_alert("Por favor, introduce un correo electrónico válido.")
            if self.contrasena != self.confirmar_contrasena:
                return rx.window_alert("Las contraseñas no coinciden.")
            if not self.codigo_valido:
                return rx.window_alert("El código de verificación debe tener exactamente 6 dígitos.")

            # Conectar a la base de datos
            conexion = conectar_db()
            cursor = conexion.cursor()

            # Insertar el usuario en la base de datos
            cursor.execute(
                """
                INSERT INTO usuarios (correo_electronico, numero_telefono, nickname, contrasenia)
                VALUES (?, ?, ?, ?)
                """,
                (self.correo, self.telefono, self.nickname, self.contrasena),
            )

            # Confirmar la transacción
            conexion.commit()
            conexion.close()

            # Mostrar mensaje de éxito
            return rx.window_alert("Usuario registrado con éxito.")

        except pyodbc.IntegrityError:
            # Manejar errores de duplicados (correo electrónico ya existe)
            return rx.window_alert("El correo electrónico ya está registrado.")
        except Exception as e:
            # Manejar otros errores
            return rx.window_alert(f"Error al registrar el usuario: {str(e)}")
        
@rx.page(route="/sign-up", title="Registro")
def signup() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Registro", size="4", class_name="titulo"),
            rx.box(
                rx.vstack(
                    rx.input(
                        placeholder="Correo Electrónico",
                        on_change=FormularioRegistroState.set_correo,
                        class_name="input-correo",
                    ),
                    rx.cond(
                        ~FormularioRegistroState.correo_valido,
                        rx.text("Correo electrónico no válido", color="red", class_name="mensaje-error"),
                    ),
                    rx.input(
                        type="password",
                        placeholder="Contraseña",
                        on_change=FormularioRegistroState.set_contrasena,
                        class_name="input-contrasena",
                    ),
                    rx.input(
                        type="password",
                        placeholder="Confirmar Contraseña",
                        on_change=FormularioRegistroState.set_confirmar_contrasena,
                        class_name="input-confirmar-contrasena",
                    ),
                    rx.input(
                        placeholder="Número de Teléfono",
                        on_change=FormularioRegistroState.set_telefono,
                        class_name="input-telefono",
                    ),
                    rx.input(
                        placeholder="Nickname",
                        on_change=FormularioRegistroState.set_nickname,
                        class_name="input-nickname",
                    ),
                    rx.input(
                        type="file",
                        accept="image/*",
                        on_change=FormularioRegistroState.set_avatar,
                        class_name="input-avatar",
                    ),
                    rx.input(
                        placeholder="Código de Verificación (6 dígitos)",
                        on_change=FormularioRegistroState.set_codigo_verificacion,
                        class_name="input-codigo-verificacion",
                    ),
                    rx.cond(
                        ~FormularioRegistroState.codigo_valido,
                        rx.text("El código debe tener exactamente 6 dígitos", color="red", class_name="mensaje-error"),
                    ),
                    rx.button("Registrarse", on_click=FormularioRegistroState.insertar_usuario, class_name="boton-registrarse"),
                    spacing="3",
                ),
                class_name="contenedor-formulario",
            ),
            rx.text("¿Ya tienes una cuenta? Inicia sesión aquí.", class_name="texto-inicio-sesion"),
            spacing="6",
            align="center",
        ),
        class_name="contenedor-principal",
    )

# Estilos CSS (puedes agregar más estilos según necesites)
estilos = {
    ".contenedor-principal": {
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh",
        "background-color": "#f0f2f5",
    },
    ".titulo": {
        "font-size": "1.5rem",
        "font-weight": "bold",
        "color": "#333",
        "margin-bottom": "1rem",
    },
    ".contenedor-formulario": {
        "background-color": "white",
        "padding": "2rem",
        "border-radius": "0.5rem",
        "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
        "width": "100%",
        "max-width": "400px",
    },
    ".input-correo, .input-contrasena, .input-confirmar-contrasena, .input-telefono, .input-nickname, .input-avatar, .input-codigo-verificacion": {
        "padding": "0.75rem",
        "border-radius": "0.5rem",
        "border": "1px solid #ccc",
        "width": "100%",
        "margin-bottom": "1rem",
    },
    ".mensaje-error": {
        "color": "red",
        "font-size": "0.8rem",
        "margin-bottom": "1rem",
    },
    ".boton-registrarse": {
        "background-color": "#007bff",
        "color": "white",
        "padding": "0.75rem",
        "border-radius": "0.5rem",
        "border": "none",
        "cursor": "pointer",
        "width": "100%",
    },
    ".texto-inicio-sesion": {
        "color": "#007bff",
        "cursor": "pointer",
        "text-align": "center",
    },
}

# Crear la aplicación
app = rx.App(style=estilos)