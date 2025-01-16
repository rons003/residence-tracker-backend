from flask import Blueprint
from controllers.establishment_controller import index, store_coordinates

establishment_bp = Blueprint('establishment_bp', __name__)
establishment_bp.route('/', methods=['GET'])(index)
establishment_bp.route('/coordinates', methods=['POST'])(store_coordinates)