from flask import Blueprint, jsonify
from ..services.menu_service import get_menu_items

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('', methods=['GET'])
def get_menu():
    menu = get_menu_items()
    # Apenas retorna em JSON
    return jsonify(menu), 200
