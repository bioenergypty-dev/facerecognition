from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, flash
from functools import wraps
from werkzeug.middleware.proxy_fix import ProxyFix

import os, cv2, csv, base64, re
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
    if not os.path.exists(CSV_RRHH):
        return [], []

    with open(CSV_RRHH, 'r', encoding='utf-8', newline='') as f:
        lector = csv.DictReader(f)
        if not lector.fieldnames:
            return [], []

        cabeceras = [normalizar_cabecera(h) for h in lector.fieldnames]
        lector.fieldnames = cabeceras

        filas = []
        for row in lector:
            fila = {k: (v.strip() if v is not None else '') for k, v in row.items() if k}
            filas.append(normalizar_fila_rrhh(fila))

    return cabeceras, filas


def leer_vig_csv():
    if not os.path.exists(CSV_VIG):
        return [], []

    with open(CSV_VIG, 'r', encoding='utf-8', newline='') as f:
        lector = csv.DictReader(f)
        if not lector.fieldnames:
            return [], []

        cabeceras = [normalizar_cabecera(h) for h in lector.fieldnames]
        lector.fieldnames = cabeceras

        filas = []
        for row in lector:
            filas.append({k: (v.strip() if v is not None else '') for k, v in row.items() if k})

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


def map_rrhh_row(row, index=None):
    numero_id = str(index + 1) if index is not None else row.get("numero_id", "") or ""
    if not numero_id.isnumeric() and index is not None:
        numero_id = str(index + 1)

    fecha_nacimiento = row.get("fecha_nacimiento", "") or ""
    fecha_alta = row.get("fecha_alta", "") or ""

    salida = {
        "Numero_ID": numero_id,
        "Usuario": row.get("usuario", "") or "",
        "Password": row.get("contraseña", row.get("password", "")) or "",
        "Nombre": row.get("nombre", "") or "",
        "Apellido": row.get("apellidos", row.get("apellido", "")) or "",
        "Cargo": row.get("cargo", "") or "",
        "Fecha_Nacimiento": re.sub(r"\D", "", fecha_nacimiento),
        "Fecha_alta": re.sub(r"\D", "", fecha_alta),
        "Hora Captura": row.get("hora", "") or "",
        "Coordenadas": row.get("coordenadas", "") or "",
    }
    return salida


def map_vig_row(row):
    mapping = [
        ("usuario", "Usuario"),
        ("evento", "Evento"),
        ("fecha", "Fecha"),
        ("estado", "Estado"),
    ]
    salida = {}
    for src, dst in mapping:
        salida[dst] = row.get(src, "") or ""
    return salida


@app.route("/admin")
@login_required
def admin():
    rrhh_display_headers = [
        "Numero_ID",
        "Usuario",
        "Password",
        "Nombre",
        "Apellido",
        "Cargo",
        "Fecha_Nacimiento",
        "Fecha_alta",
        "Hora Captura",
        "Coordenadas",
    ]

    vig_headers = [
        "Usuario",
        "Evento",
        "Fecha",
        "Estado",
    ]

    rrhh = [map_rrhh_row(r, idx) for idx, r in enumerate(leer_rrhh_csv()[1])]
    vig = [map_vig_row(v) for v in leer_vig_csv()[1]]

    return render_template(
        "admin.html",
        rrhh=rrhh,
        rrhh_headers=rrhh_display_headers,
        vig=vig,
        vig_headers=vig_headers,
        header_labels=HEADER_LABELS
    )


@app.route("/admin_data")
@login_required
def admin_data():
    rrhh_display_headers = [
        "Numero_ID",
        "Usuario",
        "Password",
        "Nombre",
        "Apellido",
        "Cargo",
        "Fecha_Nacimiento",
        "Fecha_alta",
        "Hora Captura",
        "Coordenadas",
    ]
    vig_headers = [
        "Usuario",
        "Evento",
        "Fecha",
        "Estado",
    ]

    rrhh = [map_rrhh_row(r, idx) for idx, r in enumerate(leer_rrhh_csv()[1])]
    vig = [map_vig_row(v) for v in leer_vig_csv()[1]]

    return jsonify({
        "rrhh_headers": rrhh_display_headers,
        "rrhh": rrhh,
        "vig_headers": vig_headers,
        "vig": vig,
    })


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
                    "fecha",
                    "estado"
                ])

            w.writerow([
                d["usuario"],
                d["evento"],
                datetime.now(),
                estado
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
