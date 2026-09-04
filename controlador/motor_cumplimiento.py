"""
MotorCumplimiento: orquesta la auditoría.

*** POLIMORFISMO ***
El método auditar_usuario() recorre self._politica.listar_requisitos(), una lista que
puede contener objetos RequisitoLongitud, RequisitoComplejidad, RequisitoCaducidad o
RequisitoReuso simultáneamente. En la línea marcada abajo se llama a
`requisito.evaluar(usuario)` UNA sola vez, de forma uniforme, sin preguntar de qué
subclase es cada objeto (nada de "if isinstance(...)"). Python decide en tiempo de
ejecución qué versión de evaluar() ejecutar según el tipo real del objeto.
"""

from modelo.politica import Politica
from modelo.usuario import Usuario
from modelo.incumplimiento import Incumplimiento
from modelo.reporte_auditoria import ReporteAuditoria
from modelo.excepciones import PoliticaSinRequisitosError


class MotorCumplimiento:
    def __init__(self, politica: Politica):
        self._politica = politica
        self._contador_incumplimientos = 0

    def auditar_usuario(self, usuario: Usuario) -> list:
        """Evalúa un usuario contra todos los requisitos de la política activa.
        Devuelve la lista de Incumplimiento detectados para ese usuario."""
        requisitos = self._politica.listar_requisitos()
        if not requisitos:
            raise PoliticaSinRequisitosError(self._politica.nombre)

        incumplimientos_usuario = []
        for requisito in requisitos:
            cumple = requisito.evaluar(usuario)  # <-- LÍNEA CLAVE DE POLIMORFISMO
            if not cumple:
                self._contador_incumplimientos += 1
                incumplimientos_usuario.append(
                    Incumplimiento(
                        id_incumplimiento=self._contador_incumplimientos,
                        id_usuario=usuario.id_usuario,
                        nombre_usuario=usuario.nombre,
                        nombre_requisito=requisito.nombre,
                        detalle=requisito.obtener_detalle(usuario),
                    )
                )
        return incumplimientos_usuario

    def auditar_todos(self, usuarios: list) -> ReporteAuditoria:
        """Audita una lista completa de usuarios y arma el ReporteAuditoria final."""
        todos_los_incumplimientos = []
        total_evaluaciones = 0
        num_requisitos = len(self._politica.listar_requisitos())

        for usuario in usuarios:
            todos_los_incumplimientos.extend(self.auditar_usuario(usuario))
            total_evaluaciones += num_requisitos

        return ReporteAuditoria(
            total_usuarios_evaluados=len(usuarios),
            total_evaluaciones=total_evaluaciones,
            incumplimientos=todos_los_incumplimientos,
        )
