from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, flash
from functools import wraps
from werkzeug.middleware.proxy_fix import ProxyFix

import os, cv2, csv, base64
import numpy as np
from datetime import datetime
import sys

# Descargar modelo si no existe
try:
    from descargar_modelos import descargar_modelo
    descargar_modelo()
except Exception as e:
    print(f"⚠️ Advertencia al descargar modelos: {e}")

from faceid_engine import procesar

app = Flask(__name__)

# ---------------- CONFIG RENDER ----------------

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.secret_key = os.environ.get(
    'SECRET_KEY',
    'c0mfL1ctR3nd3r2026'
)

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['PREFERRED_URL_SCHEME'] = 'https'

# ---------------- CREDENCIALES ----------------

USERNAME = "admin"
PASSWORD = "123456"

SESION_RRHH = {}  # Estado RRHH

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
CAP = os.path.join(BASE, "capturas")

CSV_RRHH = os.path.join(DATA, "empleados.csv")
CSV_VIG = os.path.join(DATA, "registros_vigilancia.csv")

HEADER_LABELS = {
    "usuario": "Usuario",
    "contraseña": "Contraseña",
    "password": "Contraseña",
    "nombre": "Nombre",
    "apellidos": "Apellidos",
    "apellido": "Apellidos",
    "numero_id": "Número ID",
    "cargo": "Cargo",
    "fecha_nacimiento": "Fecha Nac.",
    "fecha_alta": "Fecha Alta",
    "hora": "Hora Captura",
    "coordenadas": "Coordenadas",
    "evento": "Evento",
    "fecha": "Fecha"
}

os.makedirs(DATA, exist_ok=True)
os.makedirs(os.path.join(CAP, "rrhh"), exist_ok=True)
os.makedirs(os.path.join(CAP, "vigilancia"), exist_ok=True)

def normalizar_cabecera(nombre):
    nombre = nombre.strip().lstrip("\ufeff").lower()
    equivalencias = {
        "password": "contraseña",
        "contraseña": "contraseña",
        "apellido": "apellidos",
        "apellidos": "apellidos",
        "fecha nacimiento": "fecha_nacimiento",
        "fecha nac": "fecha_nacimiento",
        "fecha_nacimiento": "fecha_nacimiento",
        "fecha alta": "fecha_alta",
        "fecha_alta": "fecha_alta",
        "numero id": "numero_id",
        "numero_id": "numero_id",
        "numero de id": "numero_id",
        "cargo": "cargo",
        "nombre": "nombre",
        "usuario": "usuario",
        "hora": "hora",
        "coordenadas": "coordenadas"
    }
    return equivalencias.get(nombre, nombre.replace(" ", "_").replace("-", "_").lower())


def normalizar_fila_rrhh(row):
    if "password" in row and "contraseña" not in row:
        row["contraseña"] = row.get("password", "")
    if "apellido" in row and "apellidos" not in row:
        row["apellidos"] = row.get("apellido", "")

    row["usuario"] = row.get("usuario", "")
    row["contraseña"] = row.get("contraseña", row.get("password", ""))
    row["nombre"] = row.get("nombre", "")
    row["apellidos"] = row.get("apellidos", row.get("apellido", ""))
    row["numero_id"] = row.get("numero_id", row.get("numero id", ""))
    row["cargo"] = row.get("cargo", "")
    row["fecha_nacimiento"] = row.get("fecha_nacimiento", "")
    row["fecha_alta"] = row.get("fecha_alta", "")
    row["hora"] = row.get("hora", "")
    row["coordenadas"] = row.get("coordenadas", "")
    return row


def leer_csv(path, extra_headers=None):
    if not os.path.exists(path):
        return [], []

    with open(path, "r", encoding="utf-8") as f:
        lector = csv.reader(f)
        try:
            cabeceras_raw = [h.strip().lstrip("\ufeff") for h in next(lector)]
        except StopIteration:
            return [], []

        cabeceras = [normalizar_cabecera(h) for h in cabeceras_raw]
        cabeceras_normalizadas = []
        for cab in cabeceras:
            if cab not in cabeceras_normalizadas:
                cabeceras_normalizadas.append(cab)

        for clave in extra_headers or []:
            if clave not in cabeceras_normalizadas:
                cabeceras_normalizadas.append(clave)

        filas = []
        for fila in lector:
            if len(fila) < len(cabeceras):
                fila += [""] * (len(cabeceras) - len(fila))
            elif len(fila) > len(cabeceras):
                fila = fila[: len(cabeceras) - 1] + [",".join(fila[len(cabeceras) - 1 :])]

            datos = dict(zip(cabeceras, fila))
            filas.append(datos)

        return cabeceras_normalizadas, filas


def leer_rrhh_csv():
    cabeceras, filas = leer_csv(CSV_RRHH, extra_headers=["hora", "coordenadas"])
    filas = [normalizar_fila_rrhh(f) for f in filas]
    return cabeceras, filas

# ---------------- AUTENTICACIÓN ----------------

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('usuario'):
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)
    return wrapper


def validar_credenciales(usuario, password):

    admin_user = os.environ.get('ADMIN_USER', USERNAME)
    admin_password = os.environ.get('ADMIN_PASSWORD', PASSWORD)

    # Admin principal
    if usuario == admin_user and password == admin_password:
        return True

    # Usuarios RRHH
    if os.path.exists(CSV_RRHH):
        with open(CSV_RRHH, 'r', encoding='utf-8') as f:

            for row in csv.DictReader(f):
                if (
                    row.get('usuario') == usuario
                    and (row.get('contraseña') or row.get('password')) == password
                ):
                    return True

    return False


@app.route('/login', methods=['GET', 'POST'])
def login():

    if session.get('usuario'):
        return redirect(url_for('index'))

    error = None

    if request.method == 'POST':

        usuario = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if validar_credenciales(usuario, password):

            session['usuario'] = usuario

            flash(
                'Bienvenido, {}.'.format(usuario),
                'success'
            )

            next_page = request.args.get('next')

            if not next_page or next_page == '/login':
                next_page = url_for('index')

            return redirect(next_page)

        error = 'Usuario o contraseña incorrectos.'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():

    session.clear()

    flash(
        'Has cerrado sesión con éxito.',
        'success'
    )

    return redirect(url_for('login'))

# ---------------- RUTAS ----------------

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/rrhh")
@login_required
def rrhh():
    return render_template("rrhh.html")


@app.route("/vigilancia")
@login_required
def vigilancia():
    return render_template("vigilancia.html")


@app.route("/admin")
@login_required
def admin():
    rrhh_headers, rrhh = leer_rrhh_csv()
    vig_headers, vig = leer_csv(CSV_VIG)

    # Expandir columnas RRHH cuando un campo contiene valores separados por comas
    def expandir_por_coma(headers, rows):
        # Determinar cuántas partes máximo por cada header
        max_partes = {}
        for h in headers:
            max_partes[h] = 1
        for row in rows:
            for h in headers:
                val = row.get(h, "") or ""
                partes = [p.strip() for p in str(val).split(",")] if val != "" else [""]
                if len(partes) > max_partes.get(h, 1):
                    max_partes[h] = len(partes)

        # Construir headers expandidos
        headers_expandidos = []
        for h in headers:
            if max_partes.get(h, 1) <= 1:
                headers_expandidos.append(h)
            else:
                for i in range(max_partes[h]):
                    headers_expandidos.append(f"{h}__{i}")

        # Construir filas expandidas
        filas_expandidas = []
        for row in rows:
            nueva = {}
            for h in headers:
                val = row.get(h, "") or ""
                partes = [p.strip() for p in str(val).split(",")] if val != "" else [""]
                if max_partes.get(h, 1) <= 1:
                    nueva[h] = partes[0] if partes else ""
                else:
                    for i in range(max_partes[h]):
                        nueva[f"{h}__{i}"] = partes[i] if i < len(partes) else ""
            filas_expandidas.append(nueva)

        return headers_expandidos, filas_expandidas

    rrhh_display_headers, rrhh_display = expandir_por_coma(rrhh_headers, rrhh)

    return render_template(
        "admin.html",
        rrhh=rrhh_display,
        rrhh_headers=rrhh_display_headers,
        vig=vig,
        vig_headers=vig_headers,
        header_labels=HEADER_LABELS
    )


@app.route("/download/<tipo>")
@login_required
def download(tipo):

    if tipo == "rrhh" and os.path.exists(CSV_RRHH):
        return send_file(CSV_RRHH, as_attachment=True)

    if tipo == "vig" and os.path.exists(CSV_VIG):
        return send_file(CSV_VIG, as_attachment=True)

    return "Archivo no encontrado"

# ---------------- RRHH ----------------

@app.route("/rrhh_procesar", methods=["POST"])
@login_required
def rrhh_procesar():

    d = request.json
    u = d["usuario"]

    if u not in SESION_RRHH:

        SESION_RRHH[u] = {
            "parp": 0,
            "ojo": "abierto",
            "capturas": 0
        }

    s = SESION_RRHH[u]

    img_bytes = base64.b64decode(
        d["frame"].split(",", 1)[1]
    )

    frame = cv2.imdecode(
        np.frombuffer(img_bytes, np.uint8),
        1
    )

    r = procesar(frame)

    if not r:
        return jsonify({
            "estado": "❌ ROSTRO NO DETECTADO"
        })

    puntos, ear = r

    ojo_actual = (
        "cerrado"
        if ear < 0.23
        else "abierto"
    )

    if ojo_actual == "cerrado" and s["ojo"] == "abierto":
        s["parp"] += 1

    s["ojo"] = ojo_actual

    if s["parp"] < 3:

        return jsonify({
            "estado": f"PARPADEOS {s['parp']}/3",
            "puntos": puntos
        })

    if ojo_actual != "abierto":

        return jsonify({
            "estado": "✔ VIDA CONFIRMADA - ABRA LOS OJOS",
            "puntos": puntos
        })

    if s["capturas"] < 5:

        ahora = datetime.now()

        ruta_usuario = os.path.join(
            CAP,
            "rrhh",
            u
        )

        os.makedirs(ruta_usuario, exist_ok=True)

        nombre_img = (
            f"{ahora.strftime('%Y%m%d_%H%M%S')}_"
            f"{s['capturas']+1}.jpg"
        )

        cv2.imwrite(
            os.path.join(ruta_usuario, nombre_img),
            frame
        )

        s["capturas"] += 1

        existe = os.path.exists(CSV_RRHH)

        with open(
            CSV_RRHH,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            w = csv.writer(f)

            if not existe:

                w.writerow([
                    "usuario",
                    "contraseña",
                    "nombre",
                    "apellidos",
                    "fecha_nacimiento",
                    "fecha_alta",
                    "cargo",
                    "hora",
                    "coordenadas"
                ])

            w.writerow([
                u,
                d["password"],
                d["nombre"],
                d["apellidos"],
                d["nacimiento"],
                ahora.date(),
                d["cargo"],
                ahora.strftime("%H:%M:%S"),
                puntos
            ])

        return jsonify({
            "estado": f"✅ CAPTURA {s['capturas']}/5 REGISTRADA",
            "puntos": puntos
        })

    return jsonify({
        "estado": "✅ REGISTRO COMPLETO",
        "puntos": puntos
    })

# ---------------- VIGILANCIA ----------------

@app.route("/vig_procesar", methods=["POST"])
@login_required
def vig_procesar():

    d = request.json

    img_bytes = base64.b64decode(
        d["frame"].split(",", 1)[1]
    )

    frame = cv2.imdecode(
        np.frombuffer(img_bytes, np.uint8),
        1
    )

    r = procesar(frame)

    pts = None
    estado = "❌ INCORRECTO"

    if r:

        pts, _ = r

        estado = "✅ " + d["evento"] + " CORRECTA"

        ruta_usuario = os.path.join(
            CAP,
            "vigilancia",
            d["usuario"]
        )

        os.makedirs(ruta_usuario, exist_ok=True)

        nombre_img = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        ) + ".jpg"

        cv2.imwrite(
            os.path.join(ruta_usuario, nombre_img),
            frame
        )

        existe = os.path.exists(CSV_VIG)

        with open(
            CSV_VIG,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            w = csv.writer(f)

            if not existe:
                w.writerow([
                    "usuario",
                    "evento",
                    "fecha"
                ])

            w.writerow([
                d["usuario"],
                d["evento"],
                datetime.now()
            ])

    return jsonify({
        "estado": estado,
        "puntos": pts
    })


# ---------------- MAIN ----------------

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
