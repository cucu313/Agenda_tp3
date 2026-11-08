"""Modelo de datos del dominio: Contacto.

Extiende el modelo del TP1 agregando el campo `imagen`, que guarda sólo
el NOMBRE del archivo de foto (no la imagen en sí). El archivo real vive
en static/uploads/ y el CSV sólo referencia su nombre.
"""

from dataclasses import dataclass, asdict, fields
from typing import Any

FIELDNAMES: list[str] = [
    "id",
    "nombre",
    "apellido",
    "telefono",
    "email",
    "categoria",
    "imagen",
]

COLUMNAS_OBLIGATORIAS: set[str] = {"nombre", "telefono", "email"}


@dataclass
class Contacto:
    id: int
    nombre: str
    apellido: str = ""
    telefono: str = ""
    email: str = ""
    categoria: str = "general"
    imagen: str = ""  # nombre de archivo dentro de static/uploads/, o "" si no tiene

    def to_dict(self) -> dict[str, str]:
        return {k: str(v) for k, v in asdict(self).items()}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Contacto":
        validos = {f.name for f in fields(cls)}
        limpio: dict[str, Any] = {
            k: (v or "").strip() if isinstance(v, str) else v
            for k, v in data.items()
            if k in validos
        }
        limpio["id"] = int(limpio.get("id") or 0)
        if not limpio.get("categoria"):
            limpio["categoria"] = "general"
        return cls(**limpio)

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}".strip()

    @property
    def iniciales(self) -> str:
        partes = (self.nombre[:1] + self.apellido[:1]).upper()
        return partes or "?"
