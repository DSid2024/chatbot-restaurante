# Testar a rota de reservas, enviando dados válidos e inválidos.

def test_create_reservation_valid(client):
    # Envia uma reserva válida
    payload = {"data": "10/12/2024", "hora": "20:00", "pessoas": 4}
    response = client.post('/reservas', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "reserva" in data
    assert data["reserva"]["data"] == "10/12/2024"
    assert data["reserva"]["hora"] == "20:00"
    assert data["reserva"]["pessoas"] == 4

def test_create_reservation_invalid(client):
    # Sem enviar pessoas, por exemplo
    payload = {"data": "10/12/2024", "hora": "20:00"}
    response = client.post('/reservas', json=payload)
    # Deve falhar, pois não atende ao modelo Pydantic
    assert response.status_code == 400
    data = response.get_json()
    # Verifica se há campo errors
    assert "errors" in data

    