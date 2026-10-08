from flask import render_template, redirect, url_for
from . import html
from ..models import Amigo
from .. import db

@html.route("/amigos")
def tabla_amigos():
    """
    Obtiene la lista de amigos de la base de datos y la
    devuelve en una tabla HTML.
    """
    amigos = Amigo.query.all()
    return render_template("tabla_amigos.html", amigos=amigos)

@html.route("/delete_amigo/<int:id>")
def delete_amigo(id):
    """
    Borra un amigo de la base de datos
    """
    # El método get_or_404 proporcionado por SQLAlchemy
    # se ocupa de generar un error 404 si el id no está en
    # la base de datos
    amigo = Amigo.query.get_or_404(id)
    
    # Una vez obtenido, lo borramos
    db.session.delete(amigo)
    db.session.commit()
    
    # Y redireccionamos a la vista /amigos
    return redirect(url_for('html.tabla_amigos'))