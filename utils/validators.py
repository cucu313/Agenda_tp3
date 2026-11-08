"""Validación de datos de contacto (misma lógica que el TP1 en terminal)."""

import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
TELEFONO_RE = re.compile(r"^\+?[0-9\s\-()]{6,}$")

EXTENSIONES_IMAGEN_PERMITIDAS = {"png", "jpg", "jpeg", "gif", "webp"}


class ValidationError(ValueError):
    pass


def email_valido(email: str) -> bool:
    return bool(EMAIL_RE.match((email or "").strip()))


def telefono_valido(telefono: str) -> bool:
    telefono = (telefono or "").strip()
    if not TELEFONO_RE.match(telefono):
        return False
    return sum(c.isdigit() for c in telefono) >= 6


def extension_imagen_valida(nombre_archivo: str) -> bool:
    if "." not in nombre_archivo:
        return False
    extension = nombre_archivo.rsplit(".", 1)[1].lower()
    return extension in EXTENSIONES_IMAGEN_PERMITIDAS


def validar_datos(datos: dict) -> list[str]:
    errores: list[str] = []

    if not (datos.get("nombre") or "").strip():
        errores.append("el nombre es obligatorio")

    telefono = (datos.get("telefono") or "").strip()
    if not telefono:
        errores.append("el teléfono es obligatorio")
    elif not telefono_valido(telefono):
        errores.append(f"teléfono inválido: '{telefono}'")

    email = (datos.get("email") or "").strip()
    if not email:
        errores.append("el email es obligatorio")
    elif not email_valido(email):
        errores.append(f"email inválido: '{email}'")

    return errores
