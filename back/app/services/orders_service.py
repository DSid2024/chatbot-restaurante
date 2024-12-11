# Lógica de negócio para pedidos. Aqui acessamos o MENU_DATA para calcular o total.
# Podemos simular a lógica já existente: procurar itens no MENU e somar preços.
# Se algum item não existir, retornamos erro.

from ..repositories.dummy_data import MENU_DATA

def create_order(order_data: dict):
    # order_data é um dicionário do tipo:
    # {
    #   "tipo": "delivery" ou "local",
    #   "itens": [1, 2, ...],
    #   "endereco": "Rua tal..." (se tipo=delivery)
    # }
    itens = order_data['itens']
    tipo = order_data['tipo']
    endereco = order_data.get('endereco')

    total = 0.0
    pedido_itens = []
    for codigo in itens:
        item = next((i for i in MENU_DATA if i["código"] == codigo), None)
        if not item:
            # Se item não encontrado, pode lançar uma exceção personalizada ou retornar um dict de erro
            # Mas aqui lançaremos uma exceção simples.
            raise ValueError(f"Item com código {codigo} não encontrado.")
        pedido_itens.append(item)
        total += item["preço"]

    # Cria resposta final
    if tipo == 'delivery':
        message = "Pedido para delivery confirmado!"
        response = {
            "message": message,
            "pedido": pedido_itens,
            "total": total,
            "endereco_entrega": endereco
        }
    else:
        message = "Pedido para consumo local confirmado!"
        response = {
            "message": message,
            "pedido": pedido_itens,
            "total": total
        }

    return response