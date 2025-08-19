from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from src.models.user import db, User
from src.models.curso import Curso
from src.models.topico import Topico
from src.schemas import TopicoCreateSchema, TopicoUpdateSchema

topicos_bp = Blueprint('topicos', __name__)

@topicos_bp.route('/topicos', methods=['GET'])
def listar_topicos():
    """Lista todos os tópicos"""
    topicos = Topico.query.order_by(Topico.created_at.desc()).all()
    return jsonify([topico.to_dict() for topico in topicos]), 200

@topicos_bp.route('/topicos/<int:topico_id>', methods=['GET'])
def obter_topico(topico_id):
    """Obtém um tópico específico por ID"""
    topico = Topico.query.get(topico_id)
    
    if not topico:
        return jsonify({'error': 'Tópico não encontrado'}), 404
    
    return jsonify(topico.to_dict()), 200

@topicos_bp.route('/topicos', methods=['POST'])
@jwt_required()
def criar_topico():
    """Cria um novo tópico"""
    schema = TopicoCreateSchema()
    
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    # Busca ou cria o curso
    curso = Curso.query.filter_by(nome=data['curso_nome']).first()
    if not curso:
        curso = Curso(nome=data['curso_nome'])
        db.session.add(curso)
        db.session.flush()  # Para obter o ID do curso
    
    # Cria o tópico
    topico = Topico(
        titulo=data['titulo'],
        mensagem=data['mensagem'],
        autor_id=user.id,
        curso_id=curso.id
    )
    
    db.session.add(topico)
    db.session.commit()
    
    return jsonify({
        'message': 'Tópico criado com sucesso',
        'topico': topico.to_dict()
    }), 201

@topicos_bp.route('/topicos/<int:topico_id>', methods=['PUT'])
@jwt_required()
def atualizar_topico(topico_id):
    """Atualiza um tópico existente"""
    schema = TopicoUpdateSchema()
    
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    current_user_id = get_jwt_identity()
    topico = Topico.query.get(topico_id)
    
    if not topico:
        return jsonify({'error': 'Tópico não encontrado'}), 404
    
    # Verifica se o usuário é o autor do tópico
    if topico.autor_id != current_user_id:
        return jsonify({'error': 'Você não tem permissão para editar este tópico'}), 403
    
    # Atualiza os campos fornecidos
    if 'titulo' in data:
        topico.titulo = data['titulo']
    
    if 'mensagem' in data:
        topico.mensagem = data['mensagem']
    
    if 'curso_nome' in data:
        # Busca ou cria o curso
        curso = Curso.query.filter_by(nome=data['curso_nome']).first()
        if not curso:
            curso = Curso(nome=data['curso_nome'])
            db.session.add(curso)
            db.session.flush()
        topico.curso_id = curso.id
    
    db.session.commit()
    
    return jsonify({
        'message': 'Tópico atualizado com sucesso',
        'topico': topico.to_dict()
    }), 200

@topicos_bp.route('/topicos/<int:topico_id>', methods=['DELETE'])
@jwt_required()
def deletar_topico(topico_id):
    """Deleta um tópico"""
    current_user_id = get_jwt_identity()
    topico = Topico.query.get(topico_id)
    
    if not topico:
        return jsonify({'error': 'Tópico não encontrado'}), 404
    
    # Verifica se o usuário é o autor do tópico
    if topico.autor_id != current_user_id:
        return jsonify({'error': 'Você não tem permissão para deletar este tópico'}), 403
    
    db.session.delete(topico)
    db.session.commit()
    
    return jsonify({'message': 'Tópico deletado com sucesso'}), 200

