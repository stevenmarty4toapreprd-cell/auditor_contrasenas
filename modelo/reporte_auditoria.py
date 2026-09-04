"""Clase ReporteAuditoria: agrega (agregación) los incumplimientos de una corrida de auditoría."""

from datetime import date
from modelo.incumplimiento import Incumplimiento


class ReporteAuditoria:
    def __init__(self, total_usuarios_evaluados: int, total_evaluaciones: int,
                 incumplimientos: list, fecha_generacion: date = None):
        self._fecha_generacion = fecha_generacion or date.today()
        self._total_usuarios_evaluados = total_usuarios_evaluados
        self._total_evaluaciones = total_evaluaciones
        self._incumplimientos: list[Incumplimiento] = incumplimientos

    @property
    def incumplimientos(self) -> list:
        return list(self._incumplimientos)

    def calcular_porcentaje_cumplimiento(self) -> float:
        if self._total_evaluaciones == 0:
            return 0.0
        cumplidas = self._total_evaluaciones - len(self._incumplimientos)
        return round((cumplidas / self._total_evaluaciones) * 100, 1)

    def resumen_por_requisito(self) -> dict:
        """Cuenta cuántos incumplimientos hay por cada tipo de requisito."""
        conteo = {}
        for inc in self._incumplimientos:
            conteo[inc.nombre_requisito] = conteo.get(inc.nombre_requisito, 0) + 1
        return conteo

    def exportar_texto(self) -> str:
        lineas = [
            f"Reporte de auditoría — {self._fecha_generacion}",
            f"Usuarios evaluados: {self._total_usuarios_evaluados}",
            f"Evaluaciones realizadas: {self._total_evaluaciones}",
            f"Cumplimiento general: {self.calcular_porcentaje_cumplimiento()}%",
            f"Incumplimientos detectados: {len(self._incumplimientos)}",
            "-" * 50,
        ]
        for inc in self._incumplimientos:
            lineas.append(inc.generar_resumen())
        return "\n".join(lineas)
