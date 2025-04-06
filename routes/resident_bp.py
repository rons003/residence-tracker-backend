from flask import Blueprint
from controllers.resident_controller import index, show, create, update, birth_date_alert

resident_bp = Blueprint('resident_bp', __name__)
resident_bp.route('/', methods=['GET'])(index)
resident_bp.route('/<int:id>', methods=['GET'])(show)
resident_bp.route('/create', methods=['POST'])(create)
resident_bp.route('/update/<int:id>', methods=['PUT'])(update)
resident_bp.route('/birth-date-alert', methods=['GET'])(birth_date_alert)
