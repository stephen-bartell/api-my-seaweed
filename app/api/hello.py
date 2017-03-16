from flask import Blueprint


blueprint = Blueprint('hello', __name__)


@blueprint.route('/')
def index():
    return 'Hello World!'
