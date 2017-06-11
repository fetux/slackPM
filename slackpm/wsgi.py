import os
from flask import Flask
from flask import request, Response
from flask_sqlalchemy import SQLAlchemy
import json
from .exceptions import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///slackpm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
@app.route('/', methods=['POST'])
def dispatcher():
    # TODO: Improve token validation
    # if request.form['token'] != 'wMzTu1U97PHNAqdqOny1gwm3':
    #     return None

    pm = {
        'sui': request.form['user_id'],
        'sci': request.form['channel_id'],
        'provider_name': request.form['command'].strip('/')
    }
    command = request.form['text']
    # Create the SlackProjectManager object
    from . import SlackProjectManagerFactory
    manager = SlackProjectManagerFactory.create(pm)
    # Run command
    from .runners import CommandRunner
    try:
        result = CommandRunner.run(manager, command)
    except SlackPMErrorBase as e:
        result = {"text": "{0}".format(e)}
    return app.response_class(json.dumps(result), content_type="application/json")


class User(db.Model):
    """
    User class
    """
    __tablename__ = 'users'

    sui = db.Column(db.String, primary_key=True)
    sci = db.Column(db.String, primary_key=True)
    provider_name = db.Column(db.String, primary_key=True)
    provider_url = db.Column(db.String)
    provider_key = db.Column(db.String)
    provider_user = db.Column(db.String)
    provider_passwd = db.Column(db.String)

    def __rep__(self):
        return "<User(sui='%s', sci='%s', provider_name='%s')>" % (self.sui, self.sci, self.provider_name)

    def __str__(self):
        return "<User(sui='%s', sci='%s', provider_name='%s')>" % (self.sui, self.sci, self.provider_name)