from flask import render_template, request, redirect, url_for, session, flash
from .. import app, mysql
import re
from datetime import datetime

@app.route("/")
def inicio():
    if "usuario_id" in session:
        return redirect(url_for("misiones.dashboard"))
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        contrasena = request.form.get("contrasena", "")

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre, apellido, contrasena FROM usuarios WHERE email = %s", (email,))
        usuario = cur.fetchone()
        cur.close()

        if not usuario:
            flash("El email no está registrado", "error")
        elif usuario["contrasena"] != contrasena:
            flash("La contraseña no corresponde a la registrada", "error")
        else:
            session["usuario_id"] = usuario["id"]
            session["nombre"] = usuario["nombre"]
            return redirect(url_for("misiones.dashboard"))
    return render_template("login.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        email = request.form.get("email", "").strip()
        contrasena = request.form.get("contrasena", "")
        confirmar = request.form.get("confirmar_contrasena", "")

        errores = []
        if len(nombre) < 2 or len(apellido) < 2:
            errores.append("Nombre y apellido deben tener al menos 2 caracteres")
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            errores.append("El email no tiene un formato válido")
        if contrasena != confirmar:
            errores.append("Las contraseñas no coinciden")

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cur.fetchone():
            errores.append("El email ya está registrado")
        cur.close()

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("registro.html", nombre=nombre, apellido=apellido, email=email)

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO usuarios (nombre, apellido, email, contrasena) VALUES (%s, %s, %s, %s)",
            (nombre, apellido, email, contrasena)
        )
        mysql.connection.commit()
        cur.close()
        flash("Registro exitoso. Inicia sesión.", "success")
        return redirect(url_for("login"))
    return render_template("registro.html")

@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect(url_for("inicio"))

@app.before_request
def proteger_rutas():
    rutas_publicas = ["/", "/login", "/registro"]
    if request.path not in rutas_publicas and not request.path.startswith("/static/"):
        if "usuario_id" not in session:
            return redirect(url_for("inicio"))