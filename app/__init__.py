from flask import Flask
from flask_babel import Babel
from .blueprints.menu import menu_bp
from .blueprints.reservations import reservations_bp
from .blueprints.orders import orders_bp

def create_app():
    app = Flask(__name__)
    app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'app/i18n'

    babel = Babel(app)

    # Registro de blueprints
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(reservations_bp, url_prefix='/reservas')
    app.register_blueprint(orders_bp, url_prefix='/pedido')

    # Rotas simples, se necessário
    @app.route('/idioma', methods=['POST'])
    def idioma():
        # Aqui entrar lógica para mudar idioma, atualizando algo no app context, session, etc.
        # Exemplo simples:
        # data = request.json
        # lang = data.get('idioma', 'pt')
        # Aqui poderia guardar a escolha em session ou algo similar
        return {"message": "Idioma alterado"}, 200

    return app
