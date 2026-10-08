from flask import request, abort, jsonify
from .. import db
from . import api
from ..models import Amigo

@api.route("/amigo/<int:id>")
def get_amigo(id):
    """
    Retorna JSON con información sobre el amigo cuyo id recibe como parámetro
    o un error 404 si no lo encuentra.
    """
    amigo = Amigo.query.get_or_404(id)
    amigodict = {
        'id': amigo.id,
        'name': amigo.name,
        'lati': amigo.lati,
        'longi': amigo.longi
    }
    return jsonify(amigodict)

@api.route("/amigo/byName/<name>")
def get_amigo_by_name(name):
    """
    Busca el amigo por su nombre en la base de datos. Si no lo encuentra
    retorna un error 404. Si lo encuentra retorna el JSON con sus datos
    """
    amigo = Amigo.query.filter_by(name=name).first()
    if not amigo:
        abort(404, "No se encuentra ningún amigo con ese nombre")
    amigodict = {
        'id': amigo.id,
        'name': amigo.name,
        'lati': amigo.lati,
        'longi': amigo.longi
    }
    return jsonify(amigodict)

@api.route("/amigos")
def list_amigos():
    """
    Retorna un JSON con la lista de amigos. Cada amigo es un diccionario
    con los campos 'id', 'name', 'lati' y 'longi'
    """
    amigos = Amigo.query.all()
    lista_amigos = []
    for amigo in amigos:
        amigodict = {
            'id': amigo.id,
            'name': amigo.name,
            'lati': amigo.lati,
            'longi': amigo.longi
        }
        lista_amigos.append(amigodict)
    return jsonify(lista_amigos)

@api.route("/amigo/<int:id>", methods=["PUT"])
def edit_amigo(id):
    """
    Modifica en la base de datos el amigo cuyo id recibe como parámetro.
    Retorna el JSON con el amigo tras la modificación
    """
    # Obtenemos el amigo a partir de su ID
    amigo = Amigo.query.get_or_404(id)

    # Comprobamos que hemos recibido JSON como parte del PUT
    if not request.json:
        abort(422, "No se ha enviado JSON")

    # Intentamos extraer campos del JSON (si no están presentes
    # la extracción retornará None)
    name = request.json.get("name")
    lati = request.json.get("lati")
    longi = request.json.get("longi")

    # Usamos los campos que estén presentes para actualizar el objeto amigo
    if name:
        amigo.name = name
    if lati:
        amigo.lati = lati
    if longi:
        amigo.longi = longi

    # Finalmente, si hemos cambiado algo en el objeto amigo, hacemos
    # el commit a la base de datos para que se guarden las modificaciones
    if name or lati or longi:
        db.session.commit()

    # Y retornamos el JSON con los nuevos datos
    amigodict = {
        "id": amigo.id,
        "name": amigo.name,
        "longi": amigo.longi,
        "lati": amigo.lati
    }
    return jsonify(amigodict)