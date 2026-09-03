"""Subclase RequisitoLongitud: primera implementación concreta de RequisitoBase."""

from modelo.requisito_base import RequisitoBase
from modelo.usuario import Usuario
from modelo.excepciones import RequisitoInvalidoError


class RequisitoLongitud(RequisitoBase):
    def __init__(self, longitud_minima: int):
        if longitud_minima <= 0:
            raise RequisitoInvalidoError("la longitud mínima debe ser mayor que 0.")
        super().__init__(
            nombre="Longitud mínima",
            descripcion=f"La contraseña debe tener al menos {longitud_minima} caracteres."
        )
        self._longitud_minima = longitud_minima

    @property
    def longitud_minima(self) -> int:
        return self._longitud_minima

    def evaluar(self, usuario: Usuario) -> bool:
        return len(usuario.contrasena_actual) >= self._longitud_minima

    def obtener_detalle(self, usuario: Usuario) -> str:
        actual = len(usuario.contrasena_actual)
        return (f"Longitud actual: {actual} / mínima requerida: {self._longitud_minima}")
