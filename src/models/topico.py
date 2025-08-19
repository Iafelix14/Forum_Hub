from src.models.user import db
from datetime import datetime

class Topico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Chaves estrangeiras
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)

    def __repr__(self):
        return f'<Topico {self.titulo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'mensagem': self.mensagem,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'autor': {
                'id': self.autor.id,
                'username': self.autor.username
            } if self.autor else None,
            'curso': {
                'id': self.curso.id,
                'nome': self.curso.nome
            } if self.curso else None
        }

