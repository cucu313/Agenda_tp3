"""Agenda de contactos con interfaz web (Actividad Práctica 2).

Capas:
  app.py              -> presentación web (rutas Flask), equivalente al
                         cli/ del TP1: traduce pedidos HTTP a llamadas
                         al ContactManager y renderiza HTML.
  services/manager.py -> lógica de negocio (igual rol que en el TP1).
  services/repository -> persistencia en CSV.
  models/contacto.py  -> entidad Contacto.

Las imágenes se guardan como archivos en static/uploads/ y el CSV sólo
referencia el nombre de archivo (columna "imagen"), tal como se haría
con cualquier campo que no es texto plano.
"""

import uuid
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

from services.manager import ContactManager
from services.repository import CSVRepository
from utils.validators import ValidationError, extension_imagen_valida

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.secret_key = "tp3c-agenda-clave-de-desarrollo"  # alcanza para un TP local
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB por imagen

manager = ContactManager(CSVRepository())


def _guardar_imagen(archivo) -> str:
    """Guarda la imagen subida con un nombre único y devuelve su nombre
    de archivo. Si no vino ninguna imagen, devuelve cadena vacía."""
    if not archivo or not archivo.filename:
        return ""
    nombre_original = secure_filename(archivo.filename)
    if not extension_imagen_valida(nombre_original):
        raise ValidationError(
            "formato de imagen no permitido (usar png, jpg, jpeg, gif o webp)"
        )
    nombre_unico = f"{uuid.uuid4().hex}_{nombre_original}"
    archivo.save(UPLOAD_DIR / nombre_unico)
    return nombre_unico


def _datos_del_formulario() -> dict:
    return {
        "nombre": request.form.get("nombre", "").strip(),
        "apellido": request.form.get("apellido", "").strip(),
        "telefono": request.form.get("telefono", "").strip(),
        "email": request.form.get("email", "").strip(),
        "categoria": request.form.get("categoria", "").strip() or "general",
    }


@app.route("/")
def index():
    contactos = manager.listar()
    return render_template("index.html", contactos=contactos)


@app.route("/contactos/nuevo", methods=["GET", "POST"])
def nuevo_contacto():
    if request.method == "GET":
        return render_template("form.html", contacto=None, accion=url_for("nuevo_contacto"))

    datos = _datos_del_formulario()
    try:
        datos["imagen"] = _guardar_imagen(request.files.get("imagen"))
        manager.crear(datos)
    except ValidationError as e:
        flash(str(e), "error")
        return render_template("form.html", contacto=datos, accion=url_for("nuevo_contacto")), 400

    flash(f"Contacto '{datos['nombre']}' registrado correctamente.", "exito")
    return redirect(url_for("index"))


@app.route("/contactos/<int:contacto_id>/editar", methods=["GET", "POST"])
def editar_contacto(contacto_id: int):
    existente = manager.obtener(contacto_id)
    if existente is None:
        flash(f"No existe un contacto con ID {contacto_id}.", "error")
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template(
            "form.html", contacto=existente, accion=url_for("editar_contacto", contacto_id=contacto_id)
        )

    datos = _datos_del_formulario()
    try:
        datos["imagen"] = _guardar_imagen(request.files.get("imagen"))
        manager.actualizar(contacto_id, datos)
    except ValidationError as e:
        flash(str(e), "error")
        return render_template(
            "form.html", contacto=datos, accion=url_for("editar_contacto", contacto_id=contacto_id)
        ), 400

    flash(f"Contacto #{contacto_id} actualizado correctamente.", "exito")
    return redirect(url_for("index"))


@app.route("/contactos/<int:contacto_id>/eliminar", methods=["POST"])
def eliminar_contacto(contacto_id: int):
    try:
        eliminado = manager.eliminar(contacto_id)
    except ValidationError as e:
        flash(str(e), "error")
        return redirect(url_for("index"))

    if eliminado.imagen:
        (UPLOAD_DIR / eliminado.imagen).unlink(missing_ok=True)

    flash(f"Contacto '{eliminado.nombre_completo}' eliminado.", "exito")
    return redirect(url_for("index"))


@app.route("/static/uploads/<path:nombre_archivo>")
def imagen_subida(nombre_archivo: str):
    return send_from_directory(UPLOAD_DIR, nombre_archivo)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
