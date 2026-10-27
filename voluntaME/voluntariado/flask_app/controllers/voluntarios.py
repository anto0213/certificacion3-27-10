from flask import redirect, url_for, session, flash
from .. import app, mysql
from datetime import datetime

@app.route("/inscribir/<int:mision_id>")
def inscribir(mision_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT fecha, voluntarios_necesarios FROM misiones WHERE id = %s", (mision_id,))
    mision = cur.fetchone()
    if not mision:
        return redirect(url_for("misiones.dashboard"))

    hoy = datetime.now().date()
    if mision["fecha"] < hoy:
        flash("La misión ya pasó", "error")
        return redirect(url_for("misiones.ver_mision", mision_id=mision_id))

    cur.execute("SELECT * FROM voluntarios_en_mision WHERE mision_id = %s AND usuario_id = %s",
                (mision_id, session["usuario_id"]))
    if cur.fetchone():
        cur.close()
        return redirect(url_for("misiones.ver_mision", mision_id=mision_id))

    cur.execute("SELECT COUNT(*) AS total FROM voluntarios_en_mision WHERE mision_id = %s", (mision_id,))
    actual = cur.fetchone()["total"]
    if actual >= mision["voluntarios_necesarios"]:
        flash("La misión ya está completa", "error")
        cur.close()
        return redirect(url_for("misiones.ver_mision", mision_id=mision_id))

    cur.execute("INSERT INTO voluntarios_en_mision (mision_id, usuario_id) VALUES (%s, %s)",
                (mision_id, session["usuario_id"]))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("misiones.ver_mision", mision_id=mision_id))

@app.route("/desinscribir/<int:mision_id>")
def desinscribir(mision_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT fecha FROM misiones WHERE id = %s", (mision_id,))
    mision = cur.fetchone()
    if mision and mision["fecha"] >= datetime.now().date():
        cur.execute("DELETE FROM voluntarios_en_mision WHERE mision_id = %s AND usuario_id = %s",
                    (mision_id, session["usuario_id"]))
        mysql.connection.commit()
    cur.close()
    return redirect(url_for("misiones.ver_mision", mision_id=mision_id))