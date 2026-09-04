"""Clase Politica: agrupa (composición) los requisitos que se auditarán."""

from datetime import date, datetime
from modelo.requisito_base import RequisitoBase


class Politica:
    """
    Encapsulación: la lista interna de requisitos (_requisitos) no se expone
    directamente; solo se puede modificar mediante agregar_requisito(), lo que
    garantiza que solo se agreguen objetos que respeten el contrato RequisitoBase.
    """

    def __init__(self, id_politica: int, nombre: str, fecha_creacion: date = None):
        self._id_politica = id_politica
        self._nombre = nombre
        self._fecha_creacion = fecha_creacion or date.today()
        self._requisitos: list[RequisitoBase] = []

    @property
    def id_politica(self) -> int:
        return self._id_politica

    @property
    def nombre(self) -> str:
        return self._nombre

    def agregar_requisito(self, requisito: RequisitoBase) -> None:
        if not isinstance(requisito, RequisitoBase):
            raise TypeError("Solo se pueden agregar objetos que hereden de RequisitoBase.")
        self._requisitos.append(requisito)

    def listar_requisitos(self) -> list:
        return list(self._requisitos)

    def __repr__(self) -> str:
        return f"Politica(id={self._id_politica}, nombre='{self._nombre}', requisitos={len(self._requisitos)})"
