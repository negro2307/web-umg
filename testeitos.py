import reflex as rx
from .database import validar_credenciales  # Importar la función de validación
from .dashboard import dashboard  # Importar la página del dashboard
from .signup import signup
from .email_validator import validar_correo

# Estado para manejar el formulario de inicio de sesión
class LoginState(rx.State):
    correo_electronico: str = ""
    contrasenia: str = ""
    mensaje_error: str = ""
    
    def validar_login(self, form_data: dict):
        # 1) Capturar valores
        self.correo_electronico = form_data.get("correo_electronico", "")
        self.contrasenia = form_data.get("contrasenia", "")

        # 2) Verificar si el correo es válido
        if not validar_correo(self.correo_electronico):
            self.mensaje_error = "Correo inválido"
            print("Correo inválido")  # Depuración
            return

        # 3) Si el correo es válido, entonces revisar credenciales
        if validar_credenciales(self.correo_electronico, self.contrasenia):
            self.mensaje_error = ""
            return rx.redirect("/dashboard")
        else:
            self.mensaje_error = "Correo electrónico o contraseña incorrectos."
            print("Credenciales incorrectas")  # Depuración

# Componente para el formulario de inicio de sesión
@rx.page(route="/", title="Login")
def login() -> rx.Component:
    return rx.box(
        rx.box(
            rx.text("UMG", class_name="leyenda"),
            rx.card(
                rx.vstack(
                    rx.center(
                        rx.image(
                            src="/logo.png",
                            width="4em",
                            height="auto",
                            border_radius="25%",
                            class_name="card__logo"
                        ),
                        rx.heading(
                            "Ingresa a tu cuenta",
                            as_="h2",
                            text_align="center",
                            class_name="card__heading"
                        ),
                        direction="column",
                        spacing="5",
                        width="100%",
                    ),
                    rx.form(
                        rx.vstack(
                            rx.text(
                                "Correo Electrónico",
                                size="3",
                                weight="medium",
                                text_align="left",
                                width="100%",
                                class_name="card__label"
                            ),
                            rx.input(
                                rx.input.slot(rx.icon("user")),
                                placeholder="usuario@ejmplo.umg",
                                type="email",
                                size="3",
                                width="100%",
                                name="correo_electronico",  # Nombre del campo
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text(
                                "Contraseña",
                                size="3",
                                weight="medium",
                                class_name="card__label"
                            ),
                            rx.input(
                                rx.input.slot(rx.icon("lock")),
                                placeholder="Ingrese su contraseña",
                                type="password",
                                size="3",
                                width="100%",
                                name="contrasenia",  # Nombre del campo
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        rx.button(
                            "Ingresar",
                            type="submit",  # Tipo de botón para enviar el formulario
                            size="3",
                            width="100%",
                            class_name="card__button",
                        ),
                        rx.cond(  # Mostrar mensaje de error si las credenciales son inválidas
                            LoginState.mensaje_error != "",
                            rx.text(
                                LoginState.mensaje_error,
                                color="red",
                                text_align="center",
                            ),
                        ),
                        rx.center(
                            rx.text("No tienes cuenta?", size="3"),
                            rx.link("Registrarse", href="/sign-up", size="3", class_name="card__registro"),
                            opacity="0.8",
                            spacing="2",
                            direction="row",
                            width="100%",
                        ),
                        spacing="6",
                        width="100%",
                        on_submit=LoginState.validar_login,  # Capturar los datos al enviar el formulario
                    ),
                ),
                class_name="card__login",
            ),
            class_name="contenedor-login"
        ),
        class_name="contenedor-padre",
        style={
            "background": "url('/wallpaper.jpg')",
            "background-size": "cover",
        }
    )

# Inicialización de la aplicación
app = rx.App(stylesheets=["/style_login.css"])

