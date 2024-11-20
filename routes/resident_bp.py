from flask import Blueprint
from controllers.resident_controller import index, show, create, update

resident_bp = Blueprint('resident_bp', __name__)
resident_bp.route('/', methods=['GET'])(index)
resident_bp.route('/<int:id>', methods=['GET'])(show)
resident_bp.route('/create', methods=['POST'])(create)
resident_bp.route('/update/<int:id>', methods=['PUT'])(update)
