"""
ControladorAuditoria: capa que conecta la vista (consola) con el modelo y la
persistencia. La vista NUNCA importa clases del modelo directamente; siempre pasa
por aquí, siguiendo el patrón MVC.
"""

from datetime import date

from modelo.usuario import Usuario
from modelo.politica import Politica
from modelo.requisito_longitud import RequisitoLongitud
from modelo.requisito_complejidad import RequisitoComplejidad
from modelo.requisito_caducidad import RequisitoCaducidad
from modelo.requisito_reuso import RequisitoReuso
from modelo.excepciones import (
    UsuarioNoEncontradoError, RequisitoInvalidoError, PoliticaSinRequisitosError,
)
from controlador.motor_cumplimiento import MotorCumplimiento
from datos.repositorio_json import RepositorioJSON


class ControladorAuditoria:
    def __init__(self, ruta_almacenamiento: str = "datos/almacenamiento/datos.json"):
        self._repositorio = RepositorioJSON(ruta_almacenamiento)
        self._usuarios: list[Usuario] = []
        self._politica: Politica = Politica(id_politica=1, nombre="Política General")
        self._ultimo_reporte = None
        self._cargar_estado_inicial()

    # ---------- Persistencia ----------
    def _cargar_estado_inicial(self) -> None:
        datos = self._repositorio.cargar()
        self._usuarios = [Usuario.from_dict(u) for u in datos.get("usuarios", [])]
        politica_data = datos.get("politica")
        if politica_data:
            self._politica = Politica(politica_data["id_politica"], politica_data["nombre"])
            for r in politica_data.get("requisitos", []):
                self._politica.agregar_requisito(self._reconstruir_requisito(r))

    def guardar_estado(self) -> None:
        data = {
            "usuarios": [u.to_dict() for u in self._usuarios],
            "politica": {
                "id_politica": self._politica.id_politica,
                "nombre": self._politica.nombre,
                "requisitos": [self._serializar_requisito(r)
                               for r in self._politica.listar_requisitos()],
            },
        }
        self._repositorio.guardar(data)

    @staticmethod
    def _serializar_requisito(r) -> dict:
        base = {"tipo": r.__class__.__name__}
        if isinstance(r, RequisitoLongitud):
            base["parametro"] = r.longitud_minima
        elif isinstance(r, RequisitoCaducidad):
            base["parametro"] = r._dias_vigencia
        elif isinstance(r, RequisitoReuso):
            base["parametro"] = r._historial_maximo
        elif isinstance(r, RequisitoComplejidad):
            base["parametro"] = None
        return base

    @staticmethod
    def _reconstruir_requisito(data: dict):
        tipo = data["tipo"]
        parametro = data.get("parametro")
        if tipo == "RequisitoLongitud":
            return RequisitoLongitud(parametro)
        if tipo == "RequisitoCaducidad":
            return RequisitoCaducidad(parametro)
        if tipo == "RequisitoReuso":
            return RequisitoReuso(parametro)
        if tipo == "RequisitoComplejidad":
            return RequisitoComplejidad()
        raise RequisitoInvalidoError(f"tipo de requisito desconocido '{tipo}'.")

    # ---------- Operaciones expuestas a la vista (menú) ----------
    def registrar_usuario(self, nombre: str, contrasena: str) -> Usuario:
        nuevo_id = (max((u.id_usuario for u in self._usuarios), default=0)) + 1
        usuario = Usuario(nuevo_id, nombre, contrasena)
        self._usuarios.append(usuario)
        self.guardar_estado()
        return usuario

    def listar_usuarios(self) -> list:
        return list(self._usuarios)

    def buscar_usuario(self, id_usuario: int) -> Usuario:
        for u in self._usuarios:
            if u.id_usuario == id_usuario:
                return u
        raise UsuarioNoEncontradoError(id_usuario)

    def agregar_requisito_longitud(self, longitud_minima: int) -> None:
        self._politica.agregar_requisito(RequisitoLongitud(longitud_minima))
        self.guardar_estado()

    def agregar_requisito_complejidad(self) -> None:
        self._politica.agregar_requisito(RequisitoComplejidad())
        self.guardar_estado()

    def agregar_requisito_caducidad(self, dias_vigencia: int) -> None:
        self._politica.agregar_requisito(RequisitoCaducidad(dias_vigencia))
        self.guardar_estado()

    def agregar_requisito_reuso(self, historial_maximo: int) -> None:
        self._politica.agregar_requisito(RequisitoReuso(historial_maximo))
        self.guardar_estado()

    def listar_requisitos(self) -> list:
        return self._politica.listar_requisitos()

    def ejecutar_auditoria(self):
        """Ejecuta la auditoría completa. Puede lanzar PoliticaSinRequisitosError."""
        motor = MotorCumplimiento(self._politica)
        reporte = motor.auditar_todos(self._usuarios)
        self._ultimo_reporte = reporte
        return reporte

    def obtener_ultimo_reporte(self):
        return self._ultimo_reporte
