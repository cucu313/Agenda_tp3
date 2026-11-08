"""Lógica de negocio del CRUD de contactos.

La capa web (app.py) sólo le pide cosas a este manager; nunca manipula
la lista de contactos ni el CSV directamente.
"""

from models.contacto import Contacto
from utils.validators import ValidationError, validar_datos
from .repository import CSVRepository


class ContactManager:
    def __init__(self, repositorio: CSVRepository) -> None:
        self.repo = repositorio

    def listar(self) -> list[Contacto]:
        return sorted(self.repo.cargar(), key=lambda c: c.id)

    def obtener(self, contacto_id: int) -> Contacto | None:
        return next((c for c in self.repo.cargar() if c.id == contacto_id), None)

    def _siguiente_id(self, contactos: list[Contacto]) -> int:
        return max((c.id for c in contactos), default=0) + 1

    def crear(self, datos: dict) -> Contacto:
        errores = validar_datos(datos)
        if errores:
            raise ValidationError("; ".join(errores))

        contactos = self.repo.cargar()
        nuevo = Contacto.from_dict({**datos, "id": self._siguiente_id(contactos)})
        contactos.append(nuevo)
        self.repo.guardar(contactos)
        return nuevo

    def actualizar(self, contacto_id: int, datos: dict) -> Contacto:
        contactos = self.repo.cargar()
        objetivo = next((c for c in contactos if c.id == contacto_id), None)
        if objetivo is None:
            raise ValidationError(f"no existe un contacto con ID {contacto_id}")

        # Si no llegó una imagen nueva, conservamos la que ya tenía.
        if not datos.get("imagen"):
            datos["imagen"] = objetivo.imagen

        errores = validar_datos(datos)
        if errores:
            raise ValidationError("; ".join(errores))

        actualizado = Contacto.from_dict({**datos, "id": contacto_id})
        contactos = [actualizado if c.id == contacto_id else c for c in contactos]
        self.repo.guardar(contactos)
        return actualizado

    def eliminar(self, contacto_id: int) -> Contacto:
        contactos = self.repo.cargar()
        objetivo = next((c for c in contactos if c.id == contacto_id), None)
        if objetivo is None:
            raise ValidationError(f"no existe un contacto con ID {contacto_id}")
        self.repo.guardar([c for c in contactos if c.id != contacto_id])
        return objetivo
