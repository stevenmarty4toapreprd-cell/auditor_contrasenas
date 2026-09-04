"""Clase Incumplimiento: registra que un usuario no cumplió un requisito específico."""

from datetime import date, datetime


class Incumplimiento:
    def __init__(self, id_incumplimiento: int, id_usuario: int, nombre_usuario: str,
                 nombre_requisito: str, detalle: str, fecha_deteccion: date = None):
        self._id_incumplimiento = id_incumplimiento
        self._id_usuario = id_usuario
        self._nombre_usuario = nombre_usuario
        self._nombre_requisito = nombre_requisito
        self._detalle = detalle
        self._fecha_deteccion = fecha_deteccion or date.today()

    @property
    def nombre_requisito(self) -> str:
        return self._nombre_requisito

    @property
    def nombre_usuario(self) -> str:
        return self._nombre_usuario

    def generar_resumen(self) -> str:
        return (f"[{self._fecha_deteccion}] Usuario '{self._nombre_usuario}' "
                f"incumple '{self._nombre_requisito}': {self._detalle}")

    def to_dict(self) -> dict:
        return {
            "id_incumplimiento": self._id_incumplimiento,
            "id_usuario": self._id_usuario,
            "nombre_usuario": self._nombre_usuario,
            "nombre_requisito": self._nombre_requisito,
            "detalle": self._detalle,
            "fecha_deteccion": self._fecha_deteccion.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Incumplimiento":
        fecha = datetime.strptime(data["fecha_deteccion"], "%Y-%m-%d").date()
        return cls(data["id_incumplimiento"], data["id_usuario"], data["nombre_usuario"],
                   data["nombre_requisito"], data["detalle"], fecha)

    def __repr__(self) -> str:
        return f"Incumplimiento(usuario='{self._nombre_usuario}', requisito='{self._nombre_requisito}')"
