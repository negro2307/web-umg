"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config  # Importa la configuración de Reflex
#@rx.page(route="/",title="Login")
def index() -> rx.Component:
    return rx.box(
        rx.box(rx.text("¡Hola! Esta es la página principal."),
        rx.link("Ir a otra página", href="/otra_pag"),class_name="contenedor contenedor-background"),
        rx.box(rx.text("a"),class_name="contenedor contenedor-login"),class_name="contenedorsote"
        
        
    )
def box()-> rx.Component:
    return rx.text("solooo")
#@rx.page(route="/otra_pag",title="otra")
def otra_pag() -> rx.Component:
    return rx.box(
        rx.text("Esta es otra página."),
        rx.link("Regresar a la página principal", href="/")
    )

# Configuración de la aplicación
app = rx.App(stylesheets=["login.css"])
app.add_page(index, route="/")
app.add_page(otra_pag, route="/otra_pag")

