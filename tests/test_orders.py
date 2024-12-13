# Testar pedidos, tanto delivery quanto local.

def test_create_delivery_order_valid(client):
    # Cria um pedido de delivery válido, com itens 1 e 2 e endereço
    payload = {
        "tipo": "delivery",
        "itens": [1, 2],
        "endereco": "Rua Exemplo, 123"
    }
    response = client.post('/pedido', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    # Verifica se voltou pedido, total e endereço
    assert "pedido" in data
    assert "total" in data
    assert "endereco_entrega" in data
    assert data["message"] == "Pedido para delivery confirmado!"

def test_create_local_order_valid(client):
    # Cria um pedido local (retirada), com itens 3 e 4
    payload = {
        "tipo": "local",
        "itens": [3, 4]
    }
    response = client.post('/pedido', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "pedido" in data
    assert "total" in data
    assert data["message"] == "Pedido para consumo local confirmado!"

def test_create_order_missing_items(client):
    # Tenta criar pedido sem itens
    payload = {
        "tipo": "delivery",
        "endereco": "Rua das Flores, 99"
    }
    response = client.post('/pedido', json=payload)
    # Falha na validação Pydantic, itens obrigatórios não fornecidos
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data

def test_create_order_invalid_item(client):
    # Tenta criar pedido com item inexistente, ex: código 999
    payload = {
        "tipo": "local",
        "itens": [999]
    }
    response = client.post('/pedido', json=payload)
    # O service deve retornar erro 404 para item não encontrado
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


# Observações finais:
# - Os testes usam o fixture `client` criado em `test_menu.py`. Pode-se criar um conftest.py para colocar esse fixture global.
# - Cada teste verifica o status_code apropriado e checa se as chaves esperadas estão na resposta.
# - Pode-se expandir os testes para outros casos, validar mensagens de erro, testar lógicas mais complexas.
# - A execução é feita rodando `pytest` na raiz do projeto. Os testes devem rodar e garantir que a lógica do backend esteja funcionando adequadamente.

# Assim, não precisamos deixar os testes em branco. Mesmo um conjunto mínimo de testes já assegura qualidade e robustez ao projeto.