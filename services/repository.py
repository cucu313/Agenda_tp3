"""Motor de persistencia: lee y escribe la agenda en un archivo CSV.

Única capa que toca el disco para la base de datos. La capa web
(app.py) nunca abre el CSV directamente.
"""

import csv
from pathlib import Path

from models.contacto import Contacto, FIELDNAMES

DB_FILE = Path(__file__).resolve().parent.parent / "data" / "agenda.csv"


class CSVRepository:
    def __init__(self, ruta: Path = DB_FILE) -> None:
        self.ruta = Path(ruta)

    def cargar(self) -> list[Contacto]:
        if not self.ruta.exists():
            return []
        with self.ruta.open("r", encoding="utf-8", newline="") as f:
            filas = list(csv.DictReader(f))
        contactos: list[Contacto] = []
        for fila in filas:
            try:
                contactos.append(Contacto.from_dict(fila))
            except (TypeError, ValueError):
                continue
        return contactos

    def guardar(self, contactos: list[Contacto]) -> None:
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        with self.ruta.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for c in contactos:
                writer.writerow(c.to_dict())
