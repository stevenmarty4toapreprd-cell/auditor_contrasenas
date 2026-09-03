"""Subclase RequisitoCaducidad."""

from modelo.requisito_base import RequisitoBase
from modelo.usuario import Usuario
from modelo.excepciones import RequisitoInvalidoError


class RequisitoCaducidad(RequisitoBase):
    def __init__(self, dias_vigencia: int):
        if dias_vigencia <= 0:
            raise RequisitoInvalidoError("los días de vigencia deben ser mayores que 0.")
        super().__init__(
            nombre="Caducidad",
            descripcion=f"La contraseña no debe superar {dias_vigencia} días sin cambiarse."
        )
        self._dias_vigencia = dias_vigencia

    def evaluar(self, usuario: Usuario) -> bool:
        return usuario.dias_desde_ultimo_cambio() <= self._dias_vigencia

    def obtener_detalle(self, usuario: Usuario) -> str:
        dias = usuario.dias_desde_ultimo_cambio()
        return f"Días transcurridos: {dias} / vigencia máxima: {self._dias_vigencia}"
