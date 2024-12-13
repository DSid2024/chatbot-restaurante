from flask import Flask
from flask_babel import Babel
from .blueprints.menu import menu_bp
from .blueprints.reservations import reservations_bp
from .blueprints.orders import orders_bp


def create_app():
    """
    Factory para criar e configurar a aplicação Flask.
    Isso permite maior flexibilidade para testes e diferentes ambientes (desenvolvimento, produção).
    """
    app = Flask(__name__)

    # Configurações básicas (adicione mais conforme necessário)
    app.config['BABEL_DEFAULT_LOCALE'] = 'pt'  # Idioma padrão
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'app/i18n'  # Caminho das traduções

    # Inicializa extensões
    babel = Babel(app)

    # Registra blueprints
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(reservations_bp, url_prefix='/reservas')
    app.register_blueprint(orders_bp, url_prefix='/pedido')

    # Rota simples de teste
    @app.route('/')
    def index():
        return {"message": "Bem-vindo ao Chatbot Restaurante API! Condições especiais para casamentos e/ou eventos"}, 200

    return app


# Cria a aplicação
app = create_app()


# Configuração para serverless
def handler(request, context):
    """
    Adapta a aplicação Flask para plataformas serverless como Vercel, AWS Lambda, etc.

    No Vercel, por exemplo, a API será acessada pelo vercel.json, que invocará essa função automaticamente.

    request representa a requisição HTTP recebida no ambiente serverless. É um objeto fornecido pela plataforma (como AWS ou Vercel).

    context contém informações adicionais sobre a execução da função serverless (por exemplo, na AWS Lambda, inclui o tempo limite, identificadores, etc.).

    """
    return app(request.environ, context)


if __name__ == '__main__':
    # Roda localmente no modo debug (não usado em produção serverless)
    app.run(debug=True)
