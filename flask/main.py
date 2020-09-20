from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import json
import time

app = Flask(__name__)

app.config['SECRET_KEY'] = 'lol'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)


class Bubble(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    upvotes = db.Column(db.Integer)
    time_created = db.Column(db.Float)
    name = db.Column(db.String(200), nullable=False)

@app.route('/')
def hello():
    return render_template('login.html')

@app.route('/lecture')
def attendee():
    return render_template('index.html')

@app.route('/host')
def host():
    return render_template('host.html')


@socketio.on('pop')
def pop(json_msg):
    bubble_to_pop = Bubble.query.fitler(Bubble.message == json_msg['message'])
    try:
        db.session.delete(bubble_to_pop)
        db.session.commit()
    except:
        return 'There was a problem popping that bubble'
    db_bubbles = Bubble.query.all()
    bubble_list = [{"id": bubble.id, "upvotes": bubble.upvotes, "message": bubble.message,
                    "time_created": bubble.time_created} for bubble in db_bubbles]
    jsonn = json.dumps(bubble_list)
    socketio.emit('my response', jsonn)


@socketio.on('add_bubble')
def handle_my_custom_event(msg):
    new_bubble = Bubble(message=msg['message'], upvotes=0,
                        time_created=time.time(), name=msg['user_name'])
    db.session.add(new_bubble)
    db.session.commit()
    print('received message: ' + str(msg))
    db_bubbles = Bubble.query.all()
    bubble_list = [{"id": bubble.id, "upvotes": bubble.upvotes, "message": bubble.message,
                    "time_created": bubble.time_created, "name": bubble.name} for bubble in db_bubbles]
    jsonn = json.dumps(bubble_list)
    print(jsonn)
    socketio.emit('list_update', jsonn)


@socketio.on('message')
def connect(msg):
    print('received message: ' + str(msg))
    db_bubbles = Bubble.query.all()
    bubble_list = [{"id": bubble.id, "upvotes": bubble.upvotes, "message": bubble.message,
                    "time_created": bubble.time_created, "name": bubble.name} for bubble in db_bubbles]
    jsonn = json.dumps(bubble_list)
    print(jsonn)
    socketio.emit('list_update', jsonn)


if __name__ == '__main__':
    socketio.run(app, debug=True)

# from main import db
# from main import Bubble
# db.session.query(Bubble).delete()
# db.session.commit()
