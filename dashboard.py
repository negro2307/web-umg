# dashboard.py
import reflex as rx

# Página del Dashboard
@rx.page(route="/dashboard", title="Dashboard")
def dashboard() -> rx.Component:
    return rx.text("Bienvenido al Dashboard")
    
app = rx.App()