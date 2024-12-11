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
        return {"message": "Bem-vindo ao Chatbot Restaurante API!"}, 200

    return app


if __name__ == '__main__':
    # Cria a aplicação e roda no modo debug
    app = create_app()
    app.run(debug=True)
