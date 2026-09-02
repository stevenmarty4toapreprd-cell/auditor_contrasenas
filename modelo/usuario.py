"""Clase Usuario: representa a un miembro del directorio auditado."""

from datetime import date, datetime
import hashlib


class Usuario:
    """
    Representa un usuario del directorio organizacional.

    Encapsulación: los atributos internos (_id_usuario, _nombre, __contrasena_hash,
    _fecha_ultimo_cambio, _historial_contrasenas) son privados/protegidos y solo se
    exponen mediante @property, evitando que el resto del sistema modifique el estado
    interno sin pasar por las validaciones de la clase.
    """

    def __init__(self, id_usuario: int, nombre: str, contrasena: str,
                 fecha_ultimo_cambio: date = None):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de usuario no puede estar vacío.")
        self._id_usuario = id_usuario
        self._nombre = nombre.strip()
        self.__contrasena_hash = self._hashear(contrasena)
        self._contrasena_actual_plana = contrasena  # solo para fines didácticos de evaluación
        self._fecha_ultimo_cambio = fecha_ultimo_cambio or date.today()
        self._historial_contrasenas = [self.__contrasena_hash]

    # ---------- Propiedades (encapsulación) ----------
    @property
    def id_usuario(self) -> int:
        return self._id_usuario

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def fecha_ultimo_cambio(self) -> date:
        return self._fecha_ultimo_cambio

    @property
    def contrasena_actual(self) -> str:
        """Expone la contraseña en texto plano SOLO para que los evaluadores de requisitos
        puedan analizarla (longitud, complejidad). En un sistema real esto no existiría:
        se evaluaría en el momento de la captura y solo se guardaría el hash."""
        return self._contrasena_actual_plana

    @property
    def historial_contrasenas(self) -> list:
        """Devuelve una copia para que nadie modifique el historial desde afuera."""
        return list(self._historial_contrasenas)

    # ---------- Métodos de negocio ----------
    def actualizar_contrasena(self, nueva_contrasena: str) -> None:
        """Actualiza la contraseña, valida que no esté vacía y registra el cambio en el
        historial (necesario para el requisito de 'no reúso')."""
        if not nueva_contrasena:
            raise ValueError("La nueva contraseña no puede estar vacía.")
        nuevo_hash = self._hashear(nueva_contrasena)
        self._contrasena_actual_plana = nueva_contrasena
        self.__contrasena_hash = nuevo_hash
        self._historial_contrasenas.append(nuevo_hash)
        self._fecha_ultimo_cambio = date.today()

    def dias_desde_ultimo_cambio(self) -> int:
        return (date.today() - self._fecha_ultimo_cambio).days

    @staticmethod
    def _hashear(texto: str) -> str:
        return hashlib.sha256(texto.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict:
        """Serializa el usuario para persistencia en JSON."""
        return {
            "id_usuario": self._id_usuario,
            "nombre": self._nombre,
            "contrasena_actual": self._contrasena_actual_plana,
            "fecha_ultimo_cambio": self._fecha_ultimo_cambio.isoformat(),
            "historial_contrasenas": self._historial_contrasenas,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Usuario":
        """Reconstruye un Usuario a partir de un diccionario (lectura desde JSON)."""
        fecha = datetime.strptime(data["fecha_ultimo_cambio"], "%Y-%m-%d").date()
        usuario = cls(data["id_usuario"], data["nombre"], data["contrasena_actual"], fecha)
        usuario._historial_contrasenas = list(data.get("historial_contrasenas", []))
        return usuario

    def __repr__(self) -> str:
        return f"Usuario(id={self._id_usuario}, nombre='{self._nombre}')"
