"""
Punto de entrada de la aplicación.

Auditor de Políticas de Contraseñas — Entregable 2 (Núcleo POO y arquitectura MVC)
Autor: Steven Marty
"""

from controlador.controlador_auditoria import ControladorAuditoria
from vista.menu_consola import MenuConsola


def main():
    controlador = ControladorAuditoria()
    vista = MenuConsola(controlador)
    vista.iniciar()
    controlador.guardar_estado()  # asegura persistencia al cerrar


if __name__ == "__main__":
    main()
