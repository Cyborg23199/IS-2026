from flask import Blueprint

html = Blueprint('html', __name__, template_folder='templates')

from . import views