from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Todo(db.Model):
    __tablename__ = 'work'
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(32))
    deadline = db.Column(db.DateTime)     #d와 t가 대문자
    
    def __init__(self, todo, deadline):
        self.todo = todo
        self.deadline = deadline