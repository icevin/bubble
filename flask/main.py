from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import json
import time

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'lol'
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)

#from main import db
#db.create_all()
class Bubble(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  message = db.Column(db.String(200), nullable=False)
  upvotes = db.Column(db.Integer)
  time_created = db.Column(db.Float)


@app.route('/')
def index():
    return render_template('./index.html', bubbles=bubble_list)

#try to get this to be called when html emits call
@socketio.on('pop')
def pop(json):
    bubble_to_pop = Bubble.query.fitler(Bubble.message == json['message'])
    try:
        db.session.delete(bubble_to_pop)
        db.session.commit()
    except:
        return 'There was a problem popping that bubble'
    db_bubbles = Bubble.query.all()
    bubble_list = [{"id": bubble.id, "upvotes": bubble.upvotes, "message": bubble.message, "time_created": bubble.time_created} for bubble in db_bubbles]
    jsonn = json.dumps(bubble_list)
    socketio.emit('my response', jsonn)


@socketio.on('message')
def handle_my_custom_event(json):
  new_bubble = Bubble(message=json['message'], upvotes=0, time_created=0.0)
  db.session.add(new_bubble)
  db.session.commit()
  print( 'received message: ' + str(json) )
  db_bubbles = Bubble.query.all()
  bubble_list = [{"id": bubble.id, "upvotes": bubble.upvotes, "message": bubble.message, "time_created": bubble.time_created} for bubble in db_bubbles]
  jsonn = json.dumps(bubble_list)
  socketio.emit('my response', jsonn)

if __name__ == '__main__':
  socketio.run( app, debug = True )