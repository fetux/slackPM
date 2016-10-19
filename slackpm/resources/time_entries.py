from . import SlackPMTimeEntry

class RedmineTimeEntry(SlackPMTimeEntry):
    """
    Class RedmineTimeEntry
    """
    # Operations
    def __init__(self, issue, hours, comments, user=None, created_on=None):
        self._issue = issue
        self._created_on = created_on
        self._user = user
        self._hours = hours
        self._comments = comments
        return None

    def save(self):
        new_entry = self._issue._pm._instance.time_entry.create(issue_id=self._issue.id, hours=self._hours, activity_id=9, comments=self._comments)
        self._user = new_entry.user.name
        self._created_on = new_entry.created_on
        return self

    def to_json(self):
        return {
            "pretext": "_"+str(self._created_on)+" "+self._user+" has spent *"+str(self._hours)+" hours:*_",
            "text": self._comments,
            "mrkdwn_in": ["pretext", "text"]
        }


class JiraTimeEntry(SlackPMTimeEntry):
    """
    Class JiraTimeEntry
    """
    # Operations
    def __init__(self, issue, hours, comments, user=None, created_on=None):
        self._issue = issue
        self._created_on = created_on
        self._user = user
        self._hours = hours
        self._comments = comments
        return None

    def save(self):
        new_entry = self._issue._pm._instance.add_worklog(self._issue.key,timeSpent=self._hours,comment=self._comments)
        self._user = new_entry.author.displayName
        self._created_on = new_entry.created
        return self
