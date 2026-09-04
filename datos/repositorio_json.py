"""
RepositorioJSON: encapsula la lectura/escritura del archivo de persistencia temporal.

Esta es la capa /datos del patrón MVC: ni el modelo ni el controlador saben cómo se
guarda la información en disco; solo llaman a cargar()/guardar().
"""

import json
import os
from modelo.excepciones import PersistenciaError


class RepositorioJSON:
    def __init__(self, ruta_archivo: str):
        self._ruta_archivo = ruta_archivo
        directorio = os.path.dirname(self._ruta_archivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

    def cargar(self) -> dict:
        if not os.path.exists(self._ruta_archivo):
            return {}
        try:
            with open(self._ruta_archivo, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return {}
                return json.loads(contenido)
        except (json.JSONDecodeError, OSError) as error:
            raise PersistenciaError(f"no se pudo leer '{self._ruta_archivo}': {error}")

    def guardar(self, data: dict) -> None:
        try:
            with open(self._ruta_archivo, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except OSError as error:
            raise PersistenciaError(f"no se pudo escribir '{self._ruta_archivo}': {error}")
