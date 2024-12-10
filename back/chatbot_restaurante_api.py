from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


menu = [
    {"código": 1, "nome": "casquinha", "preço": 4.00, "categoria": "entrada"},
    {"código": 2, "nome": "camarão na moranga", "preço": 7.50, "categoria": "principal"},
    {"código": 3, "nome": "peixe frito", "preço": 6.00, "categoria": "principal"},
    {"código": 4, "nome": "sorvete", "preço": 3.00, "categoria": "sobremesa"},
    {"código": 5, "nome": "Refrigerante", "preço": 3.00, "categoria": "bebida"}
]

reservas = []
horarios = {
    "segunda": "Fechado",
    "terça a sexta": "10:00 às 18:00",
    "sábado e domingo": "10:00 às 18:00"
}

endereco = "Rua Principal, 123, Centro"
advertisement = "Consulte-nos para realizar seu casamento, temos preços especiais para eventos em geral!"
idioma = "pt"  # Padrão: Português

traducoes = {
    "pt": {
        "menu": "Cardápio",
        "schedule": "Horários de Funcionamento",
        "reservations": "Reservas Confirmadas",
        "advertisement": advertisement,
        "exit": "Sair"
    },
    "en": {
        "menu": "Menu",
        "schedule": "Opening Hours",
        "reservations": "Confirmed Reservations",
        "advertisement": "Contact us to host your wedding or event! We offer special prices for general events.",
        "exit": "Exit"
    }
}


def traduzir(mensagem):
    return traducoes[idioma].get(mensagem, mensagem)


@app.route('/idioma', methods=['POST'])
def selecionar_idioma():
    global idioma
    data = request.json
    idioma_escolhido = data.get('idioma', 'pt')
    if idioma_escolhido not in ['pt', 'en']:
        return jsonify({"error": "Idioma inválido. Escolha 'pt' ou 'en'."}), 400
    idioma = idioma_escolhido
    return jsonify({"message": f"Idioma alterado para {'Português' if idioma == 'pt' else 'English'}"})


@app.route('/menu', methods=['GET'])
def mostrar_menu():
    return jsonify(menu)


@app.route('/horarios', methods=['GET'])
def mostrar_horarios():
    return jsonify(horarios)


@app.route('/reservas', methods=['GET', 'POST'])
def gerenciar_reservas():
    if request.method == 'POST':
        data = request.json
        try:
            nova_reserva = {
                "data": data['data'],
                "hora": data['hora'],
                "pessoas": int(data['pessoas'])
            }
            reservas.append(nova_reserva)
            return jsonify({"message": "Reserva confirmada!", "reserva": nova_reserva}), 201
        except (KeyError, ValueError):
            return jsonify({"error": "Dados inválidos. Certifique-se de enviar 'data', 'hora' e 'pessoas'."}), 400
    return jsonify(reservas)


@app.route('/pedido', methods=['POST'])
def fazer_pedido():
    data = request.json
    tipo = data.get('tipo', 'local')
    itens_pedido = data.get('itens', [])
    if not itens_pedido:
        return jsonify({"error": "Nenhum item enviado no pedido."}), 400

    pedido = []
    total = 0
    for codigo in itens_pedido:
        item = next((i for i in menu if i["código"] == codigo), None)
        if item:
            pedido.append(item)
            total += item["preço"]
        else:
            return jsonify({"error": f"Item com código {codigo} não encontrado."}), 404

    response = {"pedido": pedido, "total": total}
    if tipo == "delivery":
        endereco_entrega = data.get("endereco")
        if not endereco_entrega:
            return jsonify({"error": "Endereço para delivery não fornecido."}), 400
        response["endereco_entrega"] = endereco_entrega
        response["message"] = "Pedido para delivery confirmado!"
    else:
        response["message"] = "Pedido para consumo local confirmado!"

    return jsonify(response), 201


@app.route('/advertisement', methods=['GET'])
def mostrar_advertisement():
    return jsonify({"advertisement": traduzir("advertisement")})


@app.route('/endereco', methods=['GET'])
def mostrar_endereco():
    return jsonify({"endereco": endereco})


if __name__ == '__main__':
    app.run(debug=True)
