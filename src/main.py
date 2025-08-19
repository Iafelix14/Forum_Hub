import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

# Importar modelos
from src.models.user import db, User
from src.models.curso import Curso
from src.models.topico import Topico

# Importar rotas
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.topicos import topicos_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(topicos_bp, url_prefix='/api')

# Criar tabelas
with app.app_context():
    db.create_all()
    
    # Criar alguns cursos padrão se não existirem
    if not Curso.query.first():
        cursos_padrao = [
            Curso(nome='Java', descricao='Curso de programação Java'),
            Curso(nome='Python', descricao='Curso de programação Python'),
            Curso(nome='JavaScript', descricao='Curso de programação JavaScript'),
            Curso(nome='Spring Boot', descricao='Curso de Spring Boot'),
            Curso(nome='React', descricao='Curso de React')
        ]
        for curso in cursos_padrao:
            db.session.add(curso)
        db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Handler para tokens expirados
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token expirado'}), 401

# Handler para tokens inválidos
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Token inválido'}), 401

# Handler para tokens ausentes
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Token de autorização necessário'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
