# Blueprint que define rotas para pedidos.
# Recebe JSON, valida com Pydantic (OrderModel), chama service e retorna resposta.

from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from ..services.orders_service import create_order
from ..models.orders_model import OrderModel

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['POST'])
def new_order():
    json_data = request.get_json()
    if not json_data:
        return {"error": "No input data provided"}, 400

    try:
        order = OrderModel(**json_data)
    except ValidationError as err:
        return jsonify({"errors": err.errors()}), 400

    # Agora validado, chamamos o service
    try:
        result = create_order(order.model_dump())
    except ValueError as e:
        # Se algum item não for encontrado ou outro erro de lógica, retornamos 404 ou 400
        return jsonify({"error": str(e)}), 404

    return jsonify(result), 201