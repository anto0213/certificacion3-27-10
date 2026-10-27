from flask import render_template, request, redirect, url_for, session, flash
from .. import app, mysql
from datetime import datetime


@app.route("/dashboard")
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.*, u.nombre as lider_nombre, u.apellido as lider_apellido,
               (SELECT COUNT(*) FROM voluntarios_en_mision WHERE mision_id = m.id) AS inscritos
        FROM misiones m
        JOIN usuarios u ON m.lider_id = u.id
        ORDER BY m.fecha ASC
    """)
    misiones = cur.fetchall()
    cur.close()

    hoy = datetime.now().date()
    misiones_activas = [m for m in misiones if m["fecha"] >= hoy]
    misiones_pasadas = [m for m in misiones if m["fecha"] < hoy]

    return render_template("dashboard.html", misiones=misiones_activas, pasadas=misiones_pasadas)

@app.route("/nueva", methods=["GET", "POST"])
def nueva_mision():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        fecha_str = request.form.get("fecha", "")
        voluntarios_necesarios = request.form.get("voluntarios_necesarios", "")
        descripcion = request.form.get("descripcion", "").strip()

        errores = []
        if not descripcion:
            errores.append("Descripción no puede estar vacía")
        if not nombre:
            errores.append("Nombre es requerido")
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            if fecha < datetime.now().date():
                errores.append("No se puede ingresar una fecha pasada")
        except:
            errores.append("Fecha inválida")
        try:
            vn = int(voluntarios_necesarios)
            if vn < 2 or vn > 20:
                errores.append("Voluntarios Necesarios debe ser entre 2 y 20")
        except:
            errores.append("Voluntarios Necesarios debe ser un número")

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("nueva_mision.html", nombre=nombre, fecha=fecha_str,
                                   voluntarios_necesarios=voluntarios_necesarios, descripcion=descripcion)

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO misiones (nombre, fecha, voluntarios_necesarios, descripcion, lider_id) VALUES (%s, %s, %s, %s, %s)",
            (nombre, fecha, voluntarios_necesarios, descripcion, session["usuario_id"])
        )
        mysql.connection.commit()
        cur.close()
        flash("Misión creada exitosamente", "success")
        return redirect(url_for("dashboard"))
    return render_template("nueva_mision.html")

@app.route("/editar/<int:mision_id>", methods=["GET", "POST"])
def editar_mision(mision_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM misiones WHERE id = %s", (mision_id,))
    mision = cur.fetchone()
    cur.close()

    if not mision:
        flash("Misión no encontrada", "error")
        return redirect(url_for("dashboard"))
    if mision["lider_id"] != session["usuario_id"]:
        flash("Solo el creador puede editar esta misión", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        fecha_str = request.form.get("fecha", "")
        voluntarios_necesarios = request.form.get("voluntarios_necesarios", "")
        descripcion = request.form.get("descripcion", "").strip()

        errores = []
        if not descripcion:
            errores.append("Descripción no puede estar vacía")
        if not nombre:
            errores.append("Nombre es requerido")
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            if fecha < datetime.now().date():
                errores.append("No se puede ingresar una fecha pasada")
        except:
            errores.append("Fecha inválida")
        try:
            vn = int(voluntarios_necesarios)
            if vn < 2 or vn > 20:
                errores.append("Voluntarios Necesarios debe ser entre 2 y 20")
        except:
            errores.append("Voluntarios Necesarios debe ser un número")

        if errores:
            for e in errores:
                flash(e, "error")
            return render_template("editar_mision.html", mision=mision)

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE misiones SET nombre=%s, fecha=%s, voluntarios_necesarios=%s, descripcion=%s
            WHERE id=%s
        """, (nombre, fecha, voluntarios_necesarios, descripcion, mision_id))
        mysql.connection.commit()
        cur.close()
        flash("Misión actualizada", "success")
        return redirect(url_for("ver_mision", mision_id=mision_id))
    return render_template("editar_mision.html", mision=mision)

@app.route("/eliminar/<int:mision_id>")
def eliminar_mision(mision_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT lider_id FROM misiones WHERE id = %s", (mision_id,))
    mision = cur.fetchone()
    if mision and mision["lider_id"] == session["usuario_id"]:
        cur.execute("DELETE FROM voluntarios_en_mision WHERE mision_id = %s", (mision_id,))
        cur.execute("DELETE FROM misiones WHERE id = %s", (mision_id,))
        mysql.connection.commit()
        flash("Misión eliminada", "success")
    else:
        flash("No tienes permiso para eliminar esta misión", "error")
    cur.close()
    return redirect(url_for("dashboard"))

@app.route("/ver/<int:mision_id>")
def ver_mision(mision_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT m.*, u.nombre as lider_nombre, u.apellido as lider_apellido
        FROM misiones m
        JOIN usuarios u ON m.lider_id = u.id
        WHERE m.id = %s
    """, (mision_id,))
    mision = cur.fetchone()

    if not mision:
        flash("Misión no encontrada", "error")
        return redirect(url_for("dashboard"))

    cur.execute("""
        SELECT u.id, u.nombre, u.apellido
        FROM voluntarios_en_mision vm
        JOIN usuarios u ON vm.usuario_id = u.id
        WHERE vm.mision_id = %s
    """, (mision_id,))
    voluntarios = cur.fetchall()
    cur.close()

    inscrito = any(v["id"] == session["usuario_id"] for v in voluntarios)
    hoy = datetime.now().date()
    pasada = mision["fecha"] < hoy

    return render_template("ver_mision.html", mision=mision, voluntarios=voluntarios,
                           inscrito=inscrito, pasada=pasada)