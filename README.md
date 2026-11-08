# Agenda de Contactos — Trabajo Práctico N°3 (Tailwind CSS)

Agenda de contactos del TP1 y TP2 (Flask + CSV + fotos por contacto), ahora
con los estilos reescritos usando el framework **Tailwind CSS**.

## Qué cambió respecto al TP2

- Se **eliminó** `static/css/style.css`: ya no hay hoja de estilos propia.
- Todas las plantillas (`templates/`) usan **clases utilitarias de Tailwind**
  directamente en el HTML (`flex`, `gap-4`, `px-6`, `hover:bg-tinta`, etc.).
- Tailwind se carga con el script de desarrollo indicado en la consigna,
  en `templates/base.html`:

  ```html
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  ```

- La paleta y las tipografías del diseño se registran como **tema propio**
  dentro de un bloque `<style type="text/tailwindcss">` con `@theme`, lo que
  genera clases como `bg-papel`, `text-tinta`, `border-linea` o `font-titulo`.
- El backend (rutas, validaciones, CSV, subida de imágenes) **no cambió**.

> **Nota:** el script por CDN es sólo para desarrollo. Para producción, Tailwind
> se instala con npm y se compila a un CSS final.

## Instalación y ejecución

```bash
pip install -r requirements.txt
python app.py
```

Abrir **http://127.0.0.1:5000** en el navegador. Hace falta conexión a
internet, porque Tailwind y las fuentes se descargan desde un CDN.

## Estructura

```
app.py                  # Rutas Flask (presentación web)
models/contacto.py      # Entidad Contacto
services/               # Lógica de negocio y persistencia en CSV
utils/validators.py     # Validación de email, teléfono e imagen
templates/              # HTML con clases de Tailwind
  ├── base.html         # Script de Tailwind, tema propio, header y avisos
  ├── index.html        # Listado de contactos
  └── form.html         # Alta y edición
static/uploads/         # Fotos de los contactos
data/agenda.csv         # Base de datos (se crea al primer uso)
```

## Funcionalidad

Listar, crear, editar y eliminar contactos, con foto opcional por contacto
(PNG, JPG, GIF o WEBP, hasta 5 MB). Los datos se guardan en `data/agenda.csv`
y las imágenes en `static/uploads/`.
