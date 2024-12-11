import pytest
from app import create_app

@pytest.fixture
def client():
    # Cria a aplicação Flask para teste usando a factory function.
    # Configura o app em modo de teste.
    app = create_app()
    app.testing = True
    # Cria um client de testes.
    return app.test_client()

def test_get_menu(client):
    # Faz requisição GET na rota /menu para obter o cardápio.
    response = client.get('/menu')
    assert response.status_code == 200
    data = response.get_json()
    # Verifica se data é uma lista (cardápio), 
    # com pelo menos um item.
    assert isinstance(data, list)
    assert len(data) > 0