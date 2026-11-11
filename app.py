"""
NoDesperdicio
-------------
Aplicación web para llevar el control de los alimentos que tienes en casa
y saber cuáles vencen pronto, para no botar comida.

Hecha con Python, Flask, SQLite, HTML y CSS.
"""

import os
import sqlite3
from datetime import date, datetime

from flask import Flask, flash, g, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "despensa.db")

# Días que faltan para considerar que un alimento "vence pronto"
DIAS_ALERTA = 3


# ---------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------
def get_db():
    """Abre la conexión a la base de datos (una por petición)."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def cerrar_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Crea la tabla si todavía no existe."""
    db = sqlite3.connect(DATABASE)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS alimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 1,
            categoria TEXT NOT NULL,
            vencimiento TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'activo'
        )
        """
    )
    db.commit()
    db.close()


# ---------------------------------------------------------------
# Funciones de ayuda
# ---------------------------------------------------------------
def calcular_estado(fecha_texto):
    """Devuelve los días restantes y la clase de color según la fecha."""
    fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
    dias = (fecha - date.today()).days

    if dias < 0:
        return dias, "vencido", "Vencido"
    if dias <= DIAS_ALERTA:
        return dias, "pronto", "Vence pronto"
    return dias, "bien", "En buen estado"


def texto_dias(dias):
    if dias < -1:
        return f"Venció hace {-dias} días"
    if dias == -1:
        return "Venció ayer"
    if dias == 0:
        return "Vence hoy"
    if dias == 1:
        return "Vence mañana"
    return f"Vence en {dias} días"


# ---------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------
@app.route("/")
def inicio():
    db = get_db()
    filas = db.execute(
        "SELECT * FROM alimentos WHERE estado = 'activo' ORDER BY vencimiento ASC"
    ).fetchall()

    alimentos = []
    vencidos = 0
    por_vencer = 0

    for fila in filas:
        dias, clase, etiqueta = calcular_estado(fila["vencimiento"])
        if clase == "vencido":
            vencidos += 1
        elif clase == "pronto":
            por_vencer += 1

        alimentos.append(
            {
                "id": fila["id"],
                "nombre": fila["nombre"],
                "cantidad": fila["cantidad"],
                "categoria": fila["categoria"],
                "vencimiento": fila["vencimiento"],
                "clase": clase,
                "etiqueta": etiqueta,
                "texto": texto_dias(dias),
            }
        )

    aprovechados = db.execute(
        "SELECT COUNT(*) FROM alimentos WHERE estado = 'consumido'"
    ).fetchone()[0]

    resumen = {
        "total": len(alimentos),
        "vencidos": vencidos,
        "por_vencer": por_vencer,
        "aprovechados": aprovechados,
    }

    return render_template(
        "index.html",
        alimentos=alimentos,
        resumen=resumen,
        hoy=date.today().isoformat(),
    )


@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form.get("nombre", "").strip()
    categoria = request.form.get("categoria", "Otros")
    vencimiento = request.form.get("vencimiento", "")
    cantidad_texto = request.form.get("cantidad", "1")

    # Validaciones sencillas
    if not nombre:
        flash("Escribe el nombre del alimento.", "error")
        return redirect(url_for("inicio"))

    try:
        cantidad = int(cantidad_texto)
        if cantidad < 1:
            raise ValueError
    except ValueError:
        flash("La cantidad debe ser un número mayor a 0.", "error")
        return redirect(url_for("inicio"))

    try:
        datetime.strptime(vencimiento, "%Y-%m-%d")
    except ValueError:
        flash("Elige una fecha de vencimiento válida.", "error")
        return redirect(url_for("inicio"))

    db = get_db()
    db.execute(
        "INSERT INTO alimentos (nombre, cantidad, categoria, vencimiento) VALUES (?, ?, ?, ?)",
        (nombre, cantidad, categoria, vencimiento),
    )
    db.commit()

    flash(f"«{nombre}» se agregó a tu despensa.", "ok")
    return redirect(url_for("inicio"))


@app.route("/consumido/<int:id>", methods=["POST"])
def consumido(id):
    db = get_db()
    db.execute("UPDATE alimentos SET estado = 'consumido' WHERE id = ?", (id,))
    db.commit()
    flash("¡Muy bien! Aprovechaste ese alimento.", "ok")
    return redirect(url_for("inicio"))


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    db = get_db()
    db.execute("DELETE FROM alimentos WHERE id = ?", (id,))
    db.commit()
    flash("Alimento eliminado de la lista.", "ok")
    return redirect(url_for("inicio"))


@app.route("/consejos")
def consejos():
    return render_template("consejos.html")


# ---------------------------------------------------------------
# Ejecución
# ---------------------------------------------------------------
init_db()

if __name__ == "__main__":
    app.run(debug=True)
