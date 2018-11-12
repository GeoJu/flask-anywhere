from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.sql.expression import func
from datetime import datetime, timedelta
from flask_migrate import Migrate

from models import *
import os

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///works'  # plsql로 생성한 데이터 베이스 이름을 적는 다
# #app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
# app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
# db.init_app(app)
# migrate = Migrate(app,db)


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="GeoJu", # 위 사진의 파란색 영역값
    password="rmdwjdtkfkd1@11", # MySQL 설정 초반의 비밀번호
    hostname="GeoJu.mysql.pythonanywhere-services.com", # 위 사진의 빨간색 영역값
    databasename="GeoJu$default", # 위 사진의 초록색 영역값
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)


@app.route('/')
def index():
    do = Todo.query.all()
    return render_template('index.html', do = do) 

@app.route('/new')
def new():
    return render_template('create.html')
    
@app.route('/create', methods = ['POST'])
def create():
    do = request.form.get('todo')
    line = request.form.get('deadline')
    
    todo = Todo(todo=do, deadline=line)
    
    db.session.add(todo)
    db.session.commit()
    
    
    return redirect('/')
    
    
@app.route('/todos/<int:id>/upgrade', methods=['POST', 'GET'])
def upgrade(id):
    todo = Todo.query.get(id)
    
    if request.method == 'POST':
        
        todo.todo = request.form.get('todo')
        todo.deadline = request.form.get('deadline')
        db.session.commit()
        return redirect('/')
    #수정 할 수 있는 홈을 설정
    return render_template('edit.html', todo = todo)    


@app.route('/todos/<int:id>/delete')
def delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    
    
@app.route('/keyboard')
def keyboard():
    keyboard = {
                    "type": "text"
                     #"buttons": ["긴급", "투두"]
                }
    return jsonify(keyboard)
    
@app.route('/message', methods = ['POST'])
def message():
    
    todo_f = Todo.query.order_by(Todo.deadline.asc()).all()
    
    user_msg = request.json['content']
    
    li = [(i.deadline, i.todo)  for i in todo_f if i.deadline > datetime.now()]
    #할일추가 결혼 10일뒤
    user_msg = user_msg.split(' ')
    msg = '일만 추가 했어'
    if user_msg[0] =='긴급':
        print(todo_f)
        msg = li[0][1] + "/" + str(li[0][0]) 
    elif user_msg[0] == '투두':
        msg = 'http://flask-geo-jugeo.c9users.io:8080/'
        
    elif user_msg[0] =='할일추가':
        day = datetime.now()  
        day = day + timedelta(days=int(user_msg[2]))
        todo = Todo(todo = user_msg[1], deadline = day)
        db.session.add(todo)
        db.session.commit()
        
    return_dict = {
            'message' : {
                     'text' : msg,
                     
                    #  'photo' : {'url': url,
                    #             'width': 720,
                    #             'height': 630 },
                     "message_button": {
                             "label": "투두",
                             "url": msg
                     }
                    },                
                    
        'keyboard': {
                    # 'type' : 'text'
                      "type": "text"
                     # "buttons": ["긴급", "투두"]
                    }
                         
        }

        
    return jsonify(return_dict)
    