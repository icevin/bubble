from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///test.db'
socketio = SocketIO(app)
db = SQLAlchemy(app)

@app.route( '/' )
def hello():
  return render_template('./index.html')

@socketio.on('message')
def handle_my_custom_event( json ):
  print( 'received message: ' + str( json ) )
  socketio.emit('my response', json)

if __name__ == '__main__':
  socketio.run( app, debug = True )