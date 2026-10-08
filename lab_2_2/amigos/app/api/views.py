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