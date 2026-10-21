from flask import render_template, redirect, url_for, request, abort
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

@html.route("/edit_amigo/<int:id>")
def edit_amigo(id):
    """
    Presenta un formulario para obtener datos a modificar de un amigo
    """
    amigo = Amigo.query.get_or_404(id)
    return render_template("edit_amigo.html", amigo=amigo)

@html.route("/new_amigo")
@html.route("/new_amigo/")
def new_amigo():
    """
    Presenta un formulario para obtener datos para crear nuevo amigo
    """
    return render_template("edit_amigo.html", amigo=None)

@html.route("/save_amigo", methods=["POST"])
def save_amigo():
    id = request.form.get("id")
    device = request.form.get("device", "")
    if id is None or id == "":
        # Creación de un nuevo amigo
        name = request.form.get("name")
        if not name:
            abort(422)  # HTTP 422 Unprocessable Entity
        lati = request.form.get("lati") or "0"
        longi = request.form.get("longi") or "0"

        amigo = Amigo(name=name, lati=lati, longi=longi, device=device)
        db.session.add(amigo)
        db.session.commit()
    else:
        # Edicion de un amigo existente
        amigo = Amigo.query.get_or_404(int(id))
        name = request.form.get("name")
        if name:
            amigo.name = name
        lati = request.form.get("lati")
        if lati:
            amigo.lati = lati
        longi = request.form.get("longi")
        if longi:
            amigo.longi = longi

        amigo.device = device

        db.session.commit()

    return redirect(url_for("html.tabla_amigos"))