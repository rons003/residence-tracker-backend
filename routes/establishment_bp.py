from flask import Blueprint
from controllers.establishment_controller import index

establishment_bp = Blueprint('establishment_bp', __name__)
establishment_bp.route('/', methods=['GET'])(index)