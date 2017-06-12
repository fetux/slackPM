import os
import requests
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


@app.route('/webhook/', methods=['POST'])
def webhook():
    """ Return the Issue action. """
    request_data = json.loads(request.data.decode())
    url = request_data['payload']['url']
    issue = request_data['payload']['issue']
    action = request_data['payload']['action']

    data = {
        "channel" : "#"+issue['project']['name'],
        "text": "_Issue "+action+"_\n"+"<"+url+"/issues/"+str(issue['id'])+"|"+issue['tracker']['name']+"#"+str(issue['id'])+" "+issue['subject']+">",
        "attachments": [
            {
                "title": "Description",
                "pretext": "_created by "+issue['author']['firstname']+" "+issue['author']['lastname']+"_",
                "text": issue['description'],
                "fields":[
                    {
                        "title": "Status",
                        "value": issue['status']['name'],
                        "short": True
                    },
                    {
                        "title": "Priority",
                        "value": issue['priority']['name'],
                        "short": True
                    },
                    {
                        "title": "Assignee",
                        "value": (issue['assignee']['firstname']+" "+issue['assignee']['lastname']) if issue['assignee'] else "-",
                        "short": True
                    },
                    {
                        "title": "Estimated hours",
                        "value": (issue['estimated_hours'] if issue['estimated_hours'] else "-"),
                        "short": True
                    },
                ],
                "mrkdwn_in": ["pretext", "text", "fields"]
            },
        ]
    }

    r = requests.post('https://hooks.slack.com/services/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', data = json.dumps(data))
    print(r)
    return app.response_class(json.dumps({'result': 'success'}), content_type="application/json")


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