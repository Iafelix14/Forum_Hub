from src.models.user import db
from datetime import datetime

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com tópicos
    topicos = db.relationship('Topico', backref='curso', lazy=True)

    def __repr__(self):
        return f'<Curso {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

