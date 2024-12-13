# Blueprint para lidar com rotas de reservas. Faz o parsing do JSON da requisição,
# valida usando o Pydantic, chama o service e retorna resposta.

from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from ..services.reservations_service import create_reservation
from ..models.reservation_model import ReservationModel

reservations_bp = Blueprint('reservations', __name__)

@reservations_bp.route('', methods=['POST'])
def new_reservation():
    # Pega o JSON do corpo da requisição
    json_data = request.get_json()
    if not json_data:
        # Se não há dados, retorna erro
        return {"error": "No input data provided"}, 400

    try:
        # Cria instância do modelo Pydantic a partir dos dados recebidos.
        # Se dados forem inválidos, ocorre ValidationError.
        reservation = ReservationModel(**json_data)
    except ValidationError as err:
        # err.errors() retorna detalhes dos erros de validação,
        # incluindo quais campos falharam e por quê.
        return jsonify({"errors": err.errors()}), 400

    # Se chegamos aqui, a validação foi bem sucedida.
    # Chamamos o service para criar a reserva.
    result = create_reservation(reservation.model_dump())
    # Retornamos a resposta JSON com status 201 (criado)
    return jsonify(result), 201