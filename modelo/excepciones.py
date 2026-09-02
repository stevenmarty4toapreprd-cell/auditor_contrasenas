"""
Excepciones personalizadas del dominio 'Auditor de Políticas de Contraseñas'.

Definir excepciones propias (en lugar de usar solo Exception genérica) permite que el
controlador y la vista distingan errores de negocio (datos inválidos, usuario no
encontrado, política vacía) de errores de programación inesperados.
"""


class AuditorError(Exception):
    """Excepción base de la aplicación. Todas las excepciones propias heredan de esta."""
    pass


class RequisitoInvalidoError(AuditorError):
    """Se lanza cuando un requisito de política recibe un parámetro fuera de rango."""
    def __init__(self, mensaje: str):
        super().__init__(f"Requisito inválido: {mensaje}")


class UsuarioNoEncontradoError(AuditorError):
    """Se lanza cuando se busca un usuario que no existe en el repositorio."""
    def __init__(self, id_usuario):
        super().__init__(f"No se encontró un usuario con id '{id_usuario}'.")


class PoliticaSinRequisitosError(AuditorError):
    """Se lanza al intentar auditar con una política que no tiene requisitos configurados."""
    def __init__(self, nombre_politica: str):
        super().__init__(
            f"La política '{nombre_politica}' no tiene requisitos configurados; "
            "no se puede ejecutar la auditoría."
        )


class PersistenciaError(AuditorError):
    """Se lanza cuando falla la lectura o escritura del archivo de almacenamiento (JSON)."""
    def __init__(self, detalle: str):
        super().__init__(f"Error de persistencia: {detalle}")
