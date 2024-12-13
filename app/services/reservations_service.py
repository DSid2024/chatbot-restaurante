# Recebe dados já validados pelo modelo Pydantic.
# Para este exemplo, retornamos a mesma reserva com uma mensagem de confirmação.

def create_reservation(reservation_data: dict):
    # Aqui podemos adicionar lógica extra, por ex. checar disponibilidade.
    # Por enquanto, apenas retornamos uma mensagem de confirmação e os dados da reserva.
    return {
        "message": "Pedido de reserva recebido! Aguarda confirmação pelo operador humano",
        "reserva": reservation_data
    }