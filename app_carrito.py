import reflex as rx

# Componente para el formulario de inicio de sesión
def login_default_icons() -> rx.Component:
    return rx.card(
        rx.vstack(
            # Logo y título
            rx.center(
                rx.image(
                    src="/logo.png",
                    class_name="logo",  # Clase CSS para el logo
                ),
                rx.heading(
                    "Ingresar a tu cuenta",
                    class_name="heading",  # Clase CSS para el título
                ),
                class_name="logo-container",  # Clase CSS para el contenedor del logo y título
            ),
            # Campo de entrada para el correo electrónico
            rx.vstack(
                rx.text(
                    "Correo Electrónico",
                    class_name="input-label",  # Clase CSS para la etiqueta del input
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="user@umg.ejemplo",
                    type="email",
                    class_name="input-field",  # Clase CSS para el campo de entrada
                ),
                class_name="input-container",  # Clase CSS para el contenedor del input
            ),
            # Campo de entrada para la contraseña
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Contraseña",
                        class_name="input-label",  # Clase CSS para la etiqueta del input
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.input(
                    rx.input.slot(rx.icon("lock")),
                    placeholder="Ingrese su contraseña",
                    type="password",
                    class_name="input-field",  # Clase CSS para el campo de entrada
                ),
                class_name="input-container",  # Clase CSS para el contenedor del input
            ),
            # Botón de inicio de sesión
            rx.button(
                "Ingresar",
                class_name="login-button",  # Clase CSS para el botón de inicio de sesión
            ),
            # Enlace para registrarse
            rx.center(
                rx.text("Aún no tienes cuenta?", class_name="text"),  # Clase CSS para el texto
                rx.link("Registrarse", href="#", class_name="signup-link"),  # Clase CSS para el enlace
                class_name="signup-container",  # Clase CSS para el contenedor del enlace
            ),
            
            class_name="login-form",  # Clase CSS para el formulario de inicio de sesión
        ),
        class_name="login-card",  # Clase CSS para el card de inicio de sesión
    )

# Nuevo contenedor rosa que envuelve al login-card
def container_login() -> rx.Component:
    return rx.flex(
        login_default_icons(),
        class_name="container-login",  # Clase CSS para el nuevo contenedor rosa
    )


# Página de inicio de sesión
@rx.page(route="/", title="Login")
def login():
    return rx.flex(
        rx.image(  # Imagen SVG al lado del login
            src="/lateral-login.svg",
            class_name="lateral-image",
        ),
        container_login(),  # Contenedor del login
        class_name="page-container",  # Clase CSS para el contenedor de la página
    )

# Inicialización de la aplicación
app = rx.App(stylesheets=["/style_login.css"])