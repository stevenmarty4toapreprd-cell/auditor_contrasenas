"""Subclase RequisitoReuso."""

from modelo.requisito_base import RequisitoBase
from modelo.usuario import Usuario
from modelo.excepciones import RequisitoInvalidoError


class RequisitoReuso(RequisitoBase):
    def __init__(self, historial_maximo: int):
        if historial_maximo <= 0:
            raise RequisitoInvalidoError("el historial máximo debe ser mayor que 0.")
        super().__init__(
            nombre="No reúso",
            descripcion=f"No se pueden repetir las últimas {historial_maximo} contraseñas."
        )
        self._historial_maximo = historial_maximo

    def evaluar(self, usuario: Usuario) -> bool:
        historial = usuario.historial_contrasenas
        # El último elemento es la contraseña actual; el resto es lo "anterior".
        anteriores = historial[:-1][-self._historial_maximo:]
        return historial[-1] not in anteriores if historial else True

    def obtener_detalle(self, usuario: Usuario) -> str:
        return (f"Contraseñas guardadas en historial: {len(usuario.historial_contrasenas)} "
                f"(se revisan las últimas {self._historial_maximo})")
