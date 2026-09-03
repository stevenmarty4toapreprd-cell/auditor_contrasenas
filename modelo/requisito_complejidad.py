"""Subclase RequisitoComplejidad."""

import re
from modelo.requisito_base import RequisitoBase
from modelo.usuario import Usuario


class RequisitoComplejidad(RequisitoBase):
    def __init__(self, requiere_mayuscula: bool = True, requiere_simbolo: bool = True):
        super().__init__(
            nombre="Complejidad",
            descripcion="La contraseña debe combinar mayúsculas, minúsculas, números y símbolos."
        )
        self._requiere_mayuscula = requiere_mayuscula
        self._requiere_simbolo = requiere_simbolo

    def evaluar(self, usuario: Usuario) -> bool:
        contrasena = usuario.contrasena_actual
        tiene_minuscula = re.search(r"[a-z]", contrasena) is not None
        tiene_numero = re.search(r"\d", contrasena) is not None
        tiene_mayuscula = (not self._requiere_mayuscula) or re.search(r"[A-Z]", contrasena)
        tiene_simbolo = (not self._requiere_simbolo) or re.search(r"[^a-zA-Z0-9]", contrasena)
        return bool(tiene_minuscula and tiene_numero and tiene_mayuscula and tiene_simbolo)

    def obtener_detalle(self, usuario: Usuario) -> str:
        contrasena = usuario.contrasena_actual
        faltantes = []
        if not re.search(r"[a-z]", contrasena):
            faltantes.append("minúscula")
        if not re.search(r"\d", contrasena):
            faltantes.append("número")
        if self._requiere_mayuscula and not re.search(r"[A-Z]", contrasena):
            faltantes.append("mayúscula")
        if self._requiere_simbolo and not re.search(r"[^a-zA-Z0-9]", contrasena):
            faltantes.append("símbolo")
        if not faltantes:
            return "Cumple con todos los criterios de complejidad."
        return "Falta(n): " + ", ".join(faltantes)
