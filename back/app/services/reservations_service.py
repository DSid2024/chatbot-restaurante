# Recebe dados já validados pelo modelo Pydantic.
# Para este exemplo, retornamos a mesma reserva com uma mensagem de confirmação.

def create_reservation(reservation_data: dict):
    # Aqui podemos adicionar lógica extra, por ex. checar disponibilidade.
    # Por enquanto, apenas retornamos uma mensagem de confirmação e os dados da reserva.
    return {
        "message": "Reserva confirmada!",
        "reserva": reservation_data
    }