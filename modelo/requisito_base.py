"""
Clase abstracta RequisitoBase.

Define el contrato que toda regla de política de contraseñas debe cumplir. No puede
instanciarse directamente (ABC + @abstractmethod). El método evaluar() es el punto de
polimorfismo: el controlador (MotorCumplimiento) lo invoca de forma uniforme sobre
una lista de objetos de distintas subclases, sin necesidad de preguntar "qué tipo de
requisito es" con condicionales.
"""

from abc import ABC, abstractmethod
from modelo.usuario import Usuario


class RequisitoBase(ABC):
    def __init__(self, nombre: str, descripcion: str = ""):
        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @abstractmethod
    def evaluar(self, usuario: Usuario) -> bool:
        """Debe devolver True si el usuario CUMPLE con este requisito."""
        raise NotImplementedError

    @abstractmethod
    def obtener_detalle(self, usuario: Usuario) -> str:
        """Debe devolver una explicación legible del resultado de la evaluación."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self._nombre}')"
