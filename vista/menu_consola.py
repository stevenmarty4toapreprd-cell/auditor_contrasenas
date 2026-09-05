"""
Vista: MenuConsola.

Solo se encarga de mostrar texto y leer entradas del usuario. Toda la lógica de
negocio se delega al ControladorAuditoria (patrón MVC). Aquí también se capturan
las excepciones de negocio para mostrarle al usuario un mensaje claro en vez de
un traceback (manejo de excepciones en las operaciones de riesgo).
"""

from modelo.excepciones import (
    AuditorError, UsuarioNoEncontradoError, PoliticaSinRequisitosError,
    RequisitoInvalidoError,
)


class MenuConsola:
    def __init__(self, controlador):
        self._controlador = controlador

    def iniciar(self) -> None:
        opciones = {
            "1": self._registrar_usuario,
            "2": self._configurar_politica,
            "3": self._ejecutar_auditoria,
            "4": self._ver_reporte,
            "5": self._listar_usuarios,
        }
        while True:
            self._mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "0":
                print("\nGuardando y saliendo... ¡Hasta luego!")
                break
            accion = opciones.get(opcion)
            if accion is None:
                print("\n⚠ Opción no válida, intente de nuevo.\n")
                continue
            try:
                accion()
            except AuditorError as error:
                # Manejo de excepciones de negocio: mensaje claro, la app no se cae.
                print(f"\n⚠ {error}\n")
            except ValueError as error:
                print(f"\n⚠ Dato inválido: {error}\n")

    def _mostrar_menu(self) -> None:
        print("\n" + "=" * 55)
        print(" AUDITOR DE POLÍTICAS DE CONTRASEÑAS — Menú principal")
        print("=" * 55)
        print(" 1. Registrar usuario")
        print(" 2. Configurar política de contraseñas")
        print(" 3. Ejecutar auditoría de cumplimiento")
        print(" 4. Ver último reporte de auditoría")
        print(" 5. Listar usuarios registrados")
        print(" 0. Salir")

    def _registrar_usuario(self) -> None:
        nombre = input("Nombre del usuario: ").strip()
        contrasena = input("Contraseña a registrar: ").strip()
        usuario = self._controlador.registrar_usuario(nombre, contrasena)
        print(f"\n✔ Usuario registrado con éxito: {usuario}")

    def _configurar_politica(self) -> None:
        print("\n-- Configurar política --")
        print(" a. Agregar requisito de longitud mínima")
        print(" b. Agregar requisito de complejidad")
        print(" c. Agregar requisito de caducidad")
        print(" d. Agregar requisito de no reúso")
        sub = input("Seleccione una sub-opción: ").strip().lower()

        if sub == "a":
            valor = int(input("Longitud mínima (número entero): "))
            self._controlador.agregar_requisito_longitud(valor)
        elif sub == "b":
            self._controlador.agregar_requisito_complejidad()
        elif sub == "c":
            valor = int(input("Días de vigencia (número entero): "))
            self._controlador.agregar_requisito_caducidad(valor)
        elif sub == "d":
            valor = int(input("Cantidad de contraseñas anteriores a comparar: "))
            self._controlador.agregar_requisito_reuso(valor)
        else:
            print("\n⚠ Sub-opción no reconocida.")
            return

        print("\n✔ Requisito agregado. Requisitos actuales de la política:")
        for r in self._controlador.listar_requisitos():
            print(f"   - {r.nombre}: {r.descripcion}")

    def _ejecutar_auditoria(self) -> None:
        reporte = self._controlador.ejecutar_auditoria()
        print(f"\n✔ Auditoría completada. Cumplimiento general: "
              f"{reporte.calcular_porcentaje_cumplimiento()}%")
        print(f"  Incumplimientos detectados: {len(reporte.incumplimientos)}")

    def _ver_reporte(self) -> None:
        reporte = self._controlador.obtener_ultimo_reporte()
        if reporte is None:
            print("\n⚠ Todavía no se ha ejecutado ninguna auditoría (opción 3).")
            return
        print("\n" + reporte.exportar_texto())

    def _listar_usuarios(self) -> None:
        usuarios = self._controlador.listar_usuarios()
        if not usuarios:
            print("\n(No hay usuarios registrados todavía)")
            return
        print("\nUsuarios registrados:")
        for u in usuarios:
            print(f"  [{u.id_usuario}] {u.nombre} — último cambio: {u.fecha_ultimo_cambio} "
                  f"({u.dias_desde_ultimo_cambio()} días atrás)")
