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

os.makedirs(DATA, exist_ok=True)
os.makedirs(os.path.join(CAP, "rrhh"), exist_ok=True)
os.makedirs(os.path.join(CAP, "vigilancia"), exist_ok=True)

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
                    and row.get('contraseña') == password
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

    rrhh = []

    if os.path.exists(CSV_RRHH):

        with open(CSV_RRHH, "r", encoding="utf-8") as f:
            rrhh = list(csv.DictReader(f))

    vig = []

    if os.path.exists(CSV_VIG):

        with open(CSV_VIG, "r", encoding="utf-8") as f:
            vig = list(csv.DictReader(f))

    return render_template(
        "admin.html",
        rrhh=rrhh,
        vig=vig
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
