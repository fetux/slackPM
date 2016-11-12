import os
import slackpm
from slackpm.settings import *
import unittest
from flask_sqlalchemy import SQLAlchemy

class SlackPMTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd = os.open('slackpm/testing.slackpm.db', os.O_CREAT)
        slackpm.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testing.slackpm.db'
        slackpm.app.config['TESTING'] = True
        def init_db():
            db = SQLAlchemy(slackpm.app)
            class User(db.Model):
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
            db.create_all()
        slackpm.init_db = init_db
        self.app = slackpm.app.test_client()
        with slackpm.app.app_context():
            slackpm.init_db()
        self.post_data = dict(
            token = 'gIkuvaNzQIHg97ATvDxqgjtO',
            team_id = 'T0001',
            team_domain = 'example',
            channel_id = 'C2147483705',
            channel_name = 'test',
            user_id = 'U214748',
            user_name = 'Steve',
            response_url = 'https://hooks.slack.com/commands/1234/5678'
        )

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink('slackpm/testing.slackpm.db')


    def test_jira_help(self):
        self.post_data.update(command = '/jira', text = 'help')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_help(self):
        self.post_data.update(command = '/redmine', text = 'help')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data

    def jira_connect(self):
        self.post_data.update(command = '/jira', text = TESTING_JIRA_CONN)
        return self.app.post('/', data=self.post_data, follow_redirects=True)

    def redmine_connect(self):
        self.post_data.update(command = '/redmine', text = TESTING_REDMINE_CONN)
        return self.app.post('/', data=self.post_data, follow_redirects=True)


    def test_jira_connect(self):
        rv = self.jira_connect()
        assert b'"text":' in rv.data


    def test_redmine_connect(self):
        rv = self.redmine_connect()
        assert b'"text":' in rv.data


    def test_jira_issue_show(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_issue(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 265_\\n<http://redmine.avalith.net/issues/265|' in rv.data

    def test_redmine_issue_not_found(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 12345')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "Ups! Issue not found dude :/"' in rv.data

    def test_jira_issue_status(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11 status')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_issue_status(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265 status')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 265 status_"' in rv.data


    def test_jira_issue_set_status(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11 status done')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_issue_set_status(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265 status resolved')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 265 status resolved_"' in rv.data

    def test_redmine_issue_set_status_invalid(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265 status paused')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "paused is not a valid Redmine Isssue Status"' in rv.data

    def test_jira_issue_priority(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11 priority')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/jira issue FET-11 priority_"' in rv.data


    def test_redmine_issue_priority(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265 priority')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 265 priority_"' in rv.data


    def test_jira_issue_assignee(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11 assignee')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_issue_assignee(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265 assignee')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 265 assignee_"' in rv.data


    def test_jira_issue_subtasks(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-10 subtasks')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_issue_subtasks(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265 subtasks')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 265 subtasks_\\n<http://redmine.avalith.net/issues/265|' in rv.data

    def test_redmine_issue_subtasks_none(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 266 subtasks')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 266 subtasks_\\n<http://redmine.avalith.net/issues/266|' in rv.data
        assert b'Subtasks: None' in rv.data

    def test_jira_issue_related(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11 related')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": ' in rv.data

    def test_redmine_issue_related(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 266 related')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 266 related_\\n<http://redmine.avalith.net/issues/266|' in rv.data

    def test_redmine_issue_related_none(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265 related')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 265 related_\\n<http://redmine.avalith.net/issues/265|' in rv.data
        assert b'Related Issues: None' in rv.data

    def test_jira_issue_comments(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11 comments')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_issue_comments(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 266 comments')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 266 comments_\\n<http://redmine.avalith.net/issues/266|' in rv.data
        assert b'Comments:' in rv.data

    def test_redmine_issue_comments_none(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 267 comments')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 267 comments_\\n<http://redmine.avalith.net/issues/267|' in rv.data
        assert b'No comments.' in rv.data

    def test_jira_issue_comments_last(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11 comments last')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_issue_comments_last(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 266 comments last')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 266 comments last_\\n<http://redmine.avalith.net/issues/266|' in rv.data
        assert b'Last comment:' in rv.data

    def test_redmine_issue_comments_last_none(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 267 comments last')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text": "_/redmine issue 267 comments last_\\n<http://redmine.avalith.net/issues/267|' in rv.data
        assert b'No Comments.' in rv.data

    def test_jira_issue_time_entries(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11 time')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_issue_time_entries(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265 time')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_jira_issue_add_time_entry(self):
        self.jira_connect()
        self.post_data.update(command = '/jira', text = 'issue FET-11 time add 5 this is a comment')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data


    def test_redmine_issue_add_time_entry(self):
        self.redmine_connect()
        self.post_data.update(command = '/redmine', text = 'issue 265 time add 5 this is a comment')
        rv = self.app.post('/', data=self.post_data, follow_redirects=True)
        assert b'"text":' in rv.data

if __name__ == '__main__':
    unittest.main()

# from slackpm import *
# from slackpm import SlackProjectManagerFactory
# from sqlalchemy import and_
# from sqlalchemy.orm import sessionmaker
#
# if __name__ == '__main__':
#
#     slack_post = {
#         'sui': 'U23423',
#         'sci': 'C234242',
#         'name': 'redmine'
#     }
#     engine = create_engine('sqlite:///slackpm.db')
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     user = session.query(User).filter(and_(User.sui == slack_post['sui'], User.sci == slack_post['sci'], User.provider_name == slack_post['name'])).one_or_none()
#     print(user)
#
#     # pms = [
#     #     {
#     #         'sui': 'U23423',
#     #         'sci': 'C234242',
#     #         'name': 'Redmine',
#     #         'url': 'http://redmine.avalith.net',
#     #         'key': '11a4ecdc2cbd816e66d342cd86ba79bce2fd5860',
#     #         'project': 'sml',
#     #         'issue_id': 5
#     #     },
#     #     {
#     #         'sui': 'U23423',
#     #         'sci': 'C234242',
#     #         'name': 'jira',
#     #         'url': 'https://fetuxx.atlassian.net',
#     #         'user': 'fetuavalith.net',
#     #         'password': 'fetux477',
#     #         'project': 'FET',
#     #         'issue_id': 'FET-11'
#     #     }
#     # ]
#     # for pm in pms:
#     #     # Create account object
#     #     manager = SlackProjectManagerFactory.create(pm)
#     #     try:
#     #         # print(manager.todo('sml'))
#     #         print(manager.issue(pm['issue_id']).show())
#     #         print(manager.issue(pm['issue_id']).status)
#     #         print(manager.issue(pm['issue_id']).set_status('done'))
#     #         print(manager.issue(pm['issue_id']).status)
#     #         print(manager.issue(pm['issue_id']).priority)
#     #         print(manager.issue(pm['issue_id']).assignee)
#     #         # print(manager.issue(pm['issue_id']).target)
#     #         print(manager.issue(pm['issue_id']).subtasks)
#     #         print(manager.issue(pm['issue_id']).related)
#     #         print(manager.issue(pm['issue_id']).comments)
#     #         print(manager.issue(pm['issue_id']).last_comment())
#     #         print(manager.issue(pm['issue_id']).time_entries)
#     #         print(manager.issue(pm['issue_id']).add_time_entry(5, "Logged in hours for testing"))
#     #     except (SlackPMProjectNotFoundError,SlackPMIssueNotFoundError) as e:
#     #         print(e)
#     #
