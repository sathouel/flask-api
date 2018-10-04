from flask import Blueprint

bp = Blueprint('chat', __name__)

from api.chat import routes