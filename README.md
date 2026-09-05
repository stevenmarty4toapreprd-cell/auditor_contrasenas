# Auditor de Políticas de Contraseñas de un Directorio

**Entregable 2 — Núcleo POO y arquitectura MVC**
Técnico en Ciberseguridad — TECI 26-04
Estudiante: Steven Marty | Profesor: Edgar Hernández

## Descripción
Aplicación de consola que audita si los usuarios de un directorio organizacional
cumplen con una política de contraseñas configurable (longitud, complejidad,
caducidad, no reúso). Los datos se persisten temporalmente en un archivo JSON.

## Cómo ejecutar
Requisitos: Python 3.10 o superior (no requiere librerías externas).

```bash
cd auditor_contrasenas
python3 main.py
```

## Estructura del proyecto (MVC)
```
auditor_contrasenas/
├── modelo/         → Clases del dominio (Usuario, Politica, RequisitoBase y subclases,
│                      Incumplimiento, ReporteAuditoria, excepciones personalizadas)
├── vista/          → Menú por consola (menu_consola.py)
├── controlador/    → ControladorAuditoria y MotorCumplimiento
├── datos/          → RepositorioJSON (persistencia) y carpeta almacenamiento/
└── main.py         → Punto de entrada
```

## Pilares de POO implementados
- **Encapsulación**: `modelo/usuario.py`, `modelo/politica.py` (atributos `_privados`/`__privados` + `@property`).
- **Herencia**: `modelo/requisito_base.py` (padre) → `requisito_longitud.py`, `requisito_complejidad.py`,
  `requisito_caducidad.py`, `requisito_reuso.py` (hijas).
- **Polimorfismo**: `controlador/motor_cumplimiento.py`, línea con `requisito.evaluar(usuario)`.
- **Clase abstracta**: `modelo/requisito_base.py` (`ABC` + `@abstractmethod`).
- **Excepciones personalizadas**: `modelo/excepciones.py`, manejadas en `vista/menu_consola.py`.

## Persistencia
Los datos se guardan en `datos/almacenamiento/datos.json` cada vez que se registra un
usuario, se modifica la política o se cierra el programa.
