from .exceptions import *
from .resources.projects import RedmineProject
from .resources.issues import RedmineIssue, JiraIssue
from redminelib import *
from redminelib.exceptions import *
from jira import *
from .wsgi import app, db, User
import json

class SlackProjectManager(object):
    """
    Abstract class SlackProjectManager
    """
    # Operations
    def __init__(self, pm):
        self._sui = pm['sui']
        self._sci = pm['sci']
        self._provider_name = pm['provider_name']

    def connect(self):
        """Abstract connect def."""
        raise NotImplementedError()

    def auth(next):
        """Abstarct auth def."""
        raise NotImplementedError()

    def todo(self, project_name):
        """Abstract todo def."""
        raise NotImplementedError()

    def issue(self, id):
        """Abstract issue def."""
        raise NotImplementedError()

    def help(self):
        """
        Return help information
        """
        return {
            "text": """_/{provider} help_\n*How to use: /{provider} <command> [options]*

            *Lets you interact with your {provider_title} application.*

            Available_commands:

            */{provider} connect <{provider_title}-url> <user-key>*

                This will connect your Slack account with your {provider_title} account.
                <{provider_title}-url> should be the URL of your {provider_title} application.
                <user-key> should be your token that you can find it in 'My Account' at {provider_title}'s

            */{provider} todo*

                This will return what you have to do... According {provider_title} ;)

            */{provider} issue <id>*

                This will return available information of an Issue

            */{provider} issue <id> status [status]*

                This will return or set the status of an Issue.
                e.g: `/{provider} issue 5420 status` will return the status of Issue#5420
                e.g: `/{provider} issue 5420 status resolved` will set the status of Issue#5420 to `Resolved`

            */{provider} issue <id> priority*

                This will return the priority of an Issue.

            */{provider} issue <id> assignee*

                This will return the Assignee of an Issue

            */{provider} issue <id> target*

                This will return the Target of an Issue.

            */{provider} issue <id> subtasks*

                This will return the Subtasks of an Issue.

            */{provider} issue <id> related*

                This will return the Related Issues of an Issue.

            */{provider} issue <id> comments*

                This will return all the Comments of an Issue.

            */{provider} issue <id> comments last*

                This will return the last Comment of an Issue.

            */{provider} issue <id> time*

                This will return the logged hours in an Issue

            */{provider} issue <id> time add <hours> <comment>*

                This will log the hours in the Issue with the comment specified.
            """.format(provider=self._provider_name, provider_title=self._provider_name.title())
        }

class RedmineProjectManager(SlackProjectManager):
    """
    Class RedmineProjectManager
    """
    # Operations
    def __init__(self, pm):
        super(RedmineProjectManager,self).__init__(pm)
        user = User.query.get((self._sui,self._sci,self._provider_name))
        self._provider_url = user.provider_url if user else None
        self._provider_user = user.provider_user if user else None
        self._provider_passwd = user.provider_passwd if user else None
        self._provider_key = user.provider_key if user else None
        return None

    def auth(next):
        def authenticate(self, *args):
            if not self._provider_url: raise SlackPMAuthError
            if self._provider_key:
                self._instance = Redmine(self._provider_url,key=self._provider_key)
            elif self._provider_user and self.provider_passwd:
                self._instance = Redmine(self._provider_url,username=self._provider_user,password=self._provider_passwd)
            if not self._instance: raise SlackPMAuthError
            return next(self, *args)
        return authenticate

    def connect(self, url, key=None, user=None, passwd=None):
        if self._provider_url: return {'text': 'Already connected.'}
        self._provider_url = url.rstrip('/')
        self._provider_user = user
        self._provider_passwd = passwd
        self._provider_key = key
        if not self._provider_url or (not self._provider_key and not self._provider_user and not self._provider_passwd) or (not self._provider_key and not self._provider_passwd) or (not self._provider_key and not self._provider_user):
            return self.help()
        user = User(sui=self._sui, sci=self._sci, provider_name=self._provider_name, provider_url=self._provider_url, provider_key=key, provider_user=user, provider_passwd=passwd)
        db.session.add(user)
        db.session.commit()
        if key:
            self._instance = Redmine(url,key=key).auth()
        elif user and passwd:
            self._instance = Redmine(url,username=user,password=passwd).auth()
        else:
            print('error')
            raise BadAttributesError()
        return {
            "text": "User successfully connected. You are ready to work!"}

    @auth
    def todo(self, project_name):
        try:
            project = RedmineProject(self,project_name)
        except ResourceNotFoundError:
            raise SlackPMProjectNotFoundError from ResourceNotFoundError
        return project.todo()

    @auth
    def issue(self, id):
        try:
            issue = RedmineIssue(self,id)
        except ResourceNotFoundError:
            raise SlackPMIssueNotFoundError from ResourceNotFoundError
        return issue

    def __str__(self):
        if self._provider_url:
            return self._sui+" "+self._sci+" "+self._provider_url
        if self._provider_name:
            return self._sui+" "+self._sci+" "+self._provider_name
        return self._sui+" "+self._sci

    def __repr__(self):
        return self._sui+" "+self._sci


class JiraProjectManager(SlackProjectManager):
    """
    Class JiraProjectManager
    """
    # Operations
    def __init__(self, pm):
        super(JiraProjectManager,self).__init__(pm)
        user = User.query.get((self._sui,self._sci,self._provider_name))
        self._provider_url = user.provider_url if user else None
        self._provider_user = user.provider_user if user else None
        self._provider_passwd = user.provider_passwd if user else None
        self._provider_key = user.provider_key if user else None
        return None

    def auth(next):
        def authenticate(self, *args):
            if not self._provider_url: raise SlackPMAuthError
            if self._provider_user and self._provider_passwd:
                self._instance = JIRA(self._provider_url,basic_auth=(self._provider_user, self._provider_passwd))
            if not self._instance: raise SlackPMAuthError
            return next(self, *args)
        return authenticate

    def connect(self, url, key=None, user=None, passwd=None):
        if self._provider_url: return {"text": "Already connected."}
        self._provider_url = url.rstrip('/')
        self._provider_user = user
        self._provider_passwd = passwd
        self._provider_key = key
        if not self._provider_url or (not self._provider_key and not self._provider_user and not self._provider_passwd) or (not self._provider_key and not self._provider_passwd) or (not self._provider_key and not self._provider_user):
            return self.help()
        self._instance = JIRA(url,basic_auth=(user, passwd))
        if not self._instance:
            return {"text": "Authentication error."}
        user = User(sui=self._sui, sci=self._sci, provider_name=self._provider_name, provider_url=self._provider_url, provider_key=key, provider_user=user, provider_passwd=passwd)
        db.session.add(user)
        db.session.commit()
        return {"text": "User successfully connected. You are ready to work!"}

    @auth
    def todo(self, project_name):
        try:
            project = JiraProject(self,project_name)
        except JIRAError:
            raise SlackPMProjectNotFoundError from JIRAError
        return project.todo()

    @auth
    def issue(self, id):
        try:
            issue = JiraIssue(self,id)
        except JIRAError:
            raise SlackPMIssueNotFoundError from JIRAError
        return issue