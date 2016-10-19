import pprint
from . import SlackPMIssue
from .projects import RedmineProject, JiraProject
from .comments import RedmineComment, JiraComment
from .time_entries import RedmineTimeEntry,JiraTimeEntry

class RedmineIssue(SlackPMIssue):
    """
    Class RedmineIssue
    """
    # Operations
    def __init__(self, pm, id):
        self._pm = pm
        self._instance = self._pm._instance.issue.get(id)
        self.id = self._instance.id
        self._author = self._instance.author.name
        self._tracker = self._instance.tracker.name
        self._project = None
        self._subject = self._instance.subject
        self._description = self._instance.description
        self._assignee = (self._instance.assigned_to.name if "assigned_to" in dir(self._instance) else "Unassigned")
        self._priority = self._instance.priority.name
        self._status = self._instance.status.name
        self._target = (self._instance.fixed_version.name if "fixed_version" in dir(self._instance) else "Not targeted")
        self._estimated_hours = (self._instance.estimated_hours if "estimated_hours" in dir(self._instance) else "-")
        self._comments = []
        self._time_entries = []
        self._subtasks = []
        self._related = []
        return None

    def show(self):
        """ Return the Issue Detail information. """
        return {
            "text": "_/redmine issue "+str(self.id)+"_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">",
            "attachments": [
                {
                    "title": "Description",
                    "pretext": "_created by "+self._author+"_",
                    "text": self._description,
                    "fields":[
                        {
                            "title": "Status",
                            "value": self._status,
                            "short": True
                        },
                        {
                            "title": "Priority",
                            "value": self._priority,
                            "short": True
                        },
                        {
                            "title": "Assignee",
                            "value": self._assignee,
                            "short": True
                        },
                        {
                            "title": "Estimated hours",
                            "value": self._estimated_hours,
                            "short": True
                        },
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                },
            ]
        }

    @property
    def status(self):
        """ Return the Issue Status. """
        return {
            "text": "_/redmine issue "+str(self.id)+" status_",
            "attachments":[
                {
                    "text": "<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">",
                    "fields": [
                        {
                            "title": "Status",
                            "value": self._status,
                            "short": True
                        },
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                }
            ]
        }

    def set_status(self, value):
        """ Set the Issue Status. """
        statuses = self._pm._instance.issue_status.all()
        for s in statuses:
            if value.title() == s.name:
                return {
                    "text": "_/redmine issue "+str(self.id)+" status "+value+"_",
                    "attachments":[
                        {
                            "text": "<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">",
                            "pretext": "_Status successfully changed_" if self._pm._instance.issue.update(self.id,status_id=s.id) else "_Status wasn't changed. Couldn't update Issue. Please try again.",
                            "fields": [
                                {
                                    "title": "Status",
                                    "value": value.title(),
                                    "short": True
                                },
                            ],
                            "mrkdwn_in": ["pretext", "text", "fields"]
                        }
                    ]
                }
        return {
            "text": value+" is not a valid Redmine Isssue Status",
            "attachments": [
                {
                    "title": "Available Redmine Issue Statuses",
                    "text": ", ".join([s.name for s in statuses])
                }
            ]
        }

    @property
    def priority(self):
        """ Return the Issue Priority. """
        return {
            "text": "_/redmine issue "+str(self.id)+" priority_",
            "attachments":[
                {
                    "text": "<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">",
                    "fields": [
                        {
                            "title": "Priority",
                            "value": self._priority,
                            "short": True
                        },
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                }
            ]
        }

    @property
    def assignee(self):
        """ Return the Issue Assignee.  """
        return {
            "text": "_/redmine issue "+str(self.id)+" assignee_",
            "attachments":[
                {
                    "text": "<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">",
                    "fields": [
                        {
                            "title": "Assignee",
                            "value": self._assignee,
                            "short": True
                        },
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                }
            ]
        }

    @property
    def target(self):
        """ Return the Issue Target. """
        return {
            "text": "_/redmine issue "+str(self.id)+" tracker_",
            "attachments":[
                {
                    "text": "<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">",
                    "fields": [
                        {
                            "title": "Target",
                            "value": self._target,
                            "short": True
                        },
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                }
            ]
        }

    @property
    def subtasks(self):
        """ Return the Issue subtasks. """
        self._subtasks = self._pm._instance.issue.get(self.id,include='children').children
        if not self._subtasks:
            return {
                "text": "_/redmine issue "+str(self.id)+" subtasks_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nSubtasks: None"
            }
        subtasks = []
        for task in self._subtasks:
            subtasks.append({
                "title": "<"+self._pm._provider_url+"/issues/"+str(task.id)+"|"+task.tracker.name+"#"+str(task.id)+" "+task.subject+">"
            })
        return {
            "text": "_/redmine issue "+str(self.id)+" subtasks_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nSubtasks:",
            "attachments": subtasks
        }

    @property
    def related(self):
        """ Return the Issue related. """
        self._related = self._pm._instance.issue.get(self.id,include='relations').relations
        if not self._related:
            return {
                "text": "_/redmine issue "+str(self.id)+" related_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nRelated Issues: None",
            }
        related = []
        for relation in self._related:
            rel = self._pm._instance.issue.get(relation.issue_to_id) if (relation.issue_to_id != self.id) else self._pm._instance.issue.get(relation.issue_id)
            related.append({
                "title": "<"+self._pm._provider_url+"/issues/"+str(rel.id)+"|"+rel.tracker.name+"#"+str(rel.id)+" "+rel.subject+">"
            })
        return {
            "text": "_/redmine issue "+str(self.id)+" related_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nRelated Issues:",
            "attachments": related
        }

    @property
    def comments(self):
        """ Return the Issue Comments """
        self.__get_comments()
        if not self._comments:
            return {
                "text": "_/redmine issue "+str(self.id)+" comments_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nNo comments."
            }
        return {
            "text": "_/redmine issue "+str(self.id)+" comments_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nComments:",
            "attachments": self._comments
        }

    def last_comment(self):
        """ Return the last Issue Comment. """
        self.__get_comments(last=True)
        if not self._comments:
            return {
                "text": "_/redmine issue "+str(self.id)+" comments last_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nNo Comments."
            }
        return {
            "text": "_/redmine issue "+str(self.id)+" comments last_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nLast comment:",
            "attachments": self._comments
        }

    def __get_comments(self, **kwargs):
        """ Get Issue Comments from Provider. """
        journals = self._pm._instance.issue.get(self.id,include='journals').journals
        for journal in journals:
            if "notes" in dir(journal) and journal.notes != "":
                self._comments.append({
                    "pretext": "_"+str(journal.created_on)+" "+journal.user.name+" wrote:_",
                    "text": journal.notes,
                    "mrkdwn_in": ["pretext", "text"]
                })
        if (kwargs.get('last', False) and self._comments):
            self._comments = [self._comments[-1]]

    @property
    def time_entries(self):
        """ Return the Issue Time Entries. """
        self.__get_time_entries()
        if not self._time_entries:
            return {
                "text": "_/redmine issue "+str(self.id)+" time_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nTime entries: None"
            }
        entries = []
        for entry in self._time_entries:
            entries.append(entry.to_json())
        return {
            "text": "_/redmine issue "+str(self.id)+" time_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\nTime entries:",
            "attachments": entries
        }


    def __get_time_entries(self):
        """ Get Issue Time Entries from Provider. """
        entries = self._pm._instance.time_entry.filter(issue_id=self.id)
        for entry in entries:
            self._time_entries.append(RedmineTimeEntry(self, entry.hours,entry.comments,entry.user.name,entry.created_on))


    def add_time_entry(self, hours, comments):
        """ Add a new Issue Time Entry.  """
        time_entry = RedmineTimeEntry(self,hours,comments).save()
        if not time_entry:
            return {
                "text": "_/redmine issue "+str(self.id)+" time add "+hours+" "+comments+"_\n"+"<"+self._pm._provider_url+"/issues/"+str(issue.id)+"|"+issue._tracker+"#"+str(issue.id)+" "+issue._subject+">\nCouldn't add entry",
            }
        return {
            "text": "_/redmine issue "+str(self.id)+" time add "+str(hours)+" "+comments+"_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.id)+"|"+self._tracker+"#"+str(self.id)+" "+self._subject+">\n_New Entry Time added:_",
            "attachments": [
                {
                    "pretext": "_"+str(time_entry._created_on)+" "+time_entry._user+" has spent *"+str(time_entry._hours)+" hours*:_",
                    "text": time_entry._comments,
                    "mrkdwn_in": ["pretext", "text"]
                }
            ]
        }

class JiraIssue(SlackPMIssue):
    """
    Class JiraIssue
    """
    # Operations
    def __init__(self, pm, key):
        self._pm = pm
        self._instance = self._pm._instance.issue(key)
        self.key = self._instance.key
        self._creator = self._instance.fields.creator.displayName
        self._issuetype = self._instance.fields.issuetype.name
        self._project = self._instance.fields.project
        self._summary = self._instance.fields.summary
        self._description = self._instance.fields.description
        self._assignee = (self._instance.fields.assignee.displayName if self._instance.fields.assignee else "Unassigned")
        self._priority = self._instance.fields.priority.name
        self._status = self._instance.fields.status.name
        self._target = None #(self._instance.fixed_version.name if "fixed_version" in dir(self._instance) else "Not targeted")
        self._estimated_hours = (self._instance.estimated_hours if "estimated_hours" in dir(self._instance) else "-")
        self._comments = []
        self._time_entries = []
        self._subtasks = []
        self._related = []
        return None

    def show(self):
        """ Return the Issue Detail information. """
        return {
            "text": "_/jira issue "+self.key+"_\n"+"<"+self._pm._provider_url+"/browse/"+self.key+"|"+self._issuetype+" "+self.key+" "+self._summary+">",
            "attachments": [
                {
                    "title": "Description",
                    "pretext": "_created by "+self._creator+"_",
                    "text": self._description,
                    "fields":[
                        {
                            "title": "Status",
                            "value": self._status,
                            "short": True
                        },
                        {
                            "title": "Priority",
                            "value": self._priority,
                            "short": True
                        },
                        {
                            "title": "Assignee",
                            "value": self._assignee,
                            "short": True
                        },
                        # {
                        #     "title": "Story Points",
                        #     "value": (issue.fields.customfield_10024 if issue.fields.customfield_10024 else "-"),
                        #     "short": True
                        # },
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                },
            ]
        }

    @property
    def status(self):
        """ Return the Issue Status. """
        return {
            "text": "_/redmine issue "+str(self.key)+" status_",
            "attachments":[
                {
                    "text": "<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">",
                    "fields": [
                        {
                            "title": "Status",
                            "value": self._status,
                            "short": True
                        },
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                }
            ]
        }

    def set_status(self,value):
        """ Set the Issue Status. """
        statuses = self._pm._instance.statuses()
        for s in statuses:
            if value.title() == s.name:
                self._pm._instance.transition_issue(self.key,s.name)
                return {
                    "text": "_/ issue "+str(self.key)+" status "+value+"_",
                    "attachments":[
                        {
                            "text": "<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">",
                            "pretext": "_Status successfully changed_", #if self._pm._instance.transition_issue(self.key,s.name) else "_Status wasn't changed. Couldn't update Issue. Please try again.",
                            "fields": [
                                {
                                    "title": "Status",
                                    "value": value.title(),
                                    "short": True
                                },
                            ],
                            "mrkdwn_in": ["pretext", "text", "fields"]
                        }
                    ]
                }
        return {
            "text": value.title()+" is not valid.",
            "attachments": [
                {
                    "title": "Available Jira Issue Statuses",
                    "text": ", ".join([s.name+" " for s in statuses])
                }
            ]
        }

    @property
    def priority(self):
        """ Return the Issue Priority. """
        return {
            "text": "_/jira issue "+str(self.key)+" priority_",
            "attachments":[
                {
                    "text": "<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">",
                    "fields": [
                        {
                            "title": "Priority",
                            "value": self._priority,
                            "short": True
                        },
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                }
            ]
        }

    @property
    def assignee(self):
        """ Return the Issue Assignee.  """
        return {
            "text": "_/jira issue "+str(self.key)+" assignee_",
            "attachments":[
                {
                    "text": "<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+"#"+str(self.key)+" "+self._summary+">",
                    "fields": [
                        {
                            "title": "Assignee",
                            "value": self._assignee,
                            "short": True
                        },
                    ],
                    "mrkdwn_in": ["pretext", "text", "fields"]
                }
            ]
        }

    @property
    def subtasks(self):
        """ Return the Issue subtasks. """
        self.__get_subtasks()
        if not self._subtasks:
            return {
                "text": "_/jira issue "+str(self.key)+" subtasks_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nNo subtasks."
            }
        subtasks = []
        for task in self._subtasks:
            subtasks.append({
                "title": "<"+self._pm._provider_url+"/issues/"+str(task.key)+"|"+task._issuetype+" "+str(task.key)+" "+task._summary+">"
            })
        return {
            "text": "_/jira issue "+str(self.key)+" subtasks_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nSubtasks:",
            "attachments": subtasks
        }

    def __get_subtasks(self):
        # This should hit JIRA and bring just the subtasks, as self._instance wouldn't have them cause performance
        for task in self._instance.fields.subtasks:
            self._subtasks.append(JiraIssue(self._pm,task.key))

    @property
    def related(self):
        """ Return the Issue related. """
        self.__get_related()
        if not self._related:
            return {
                "text": "_/jira issue "+str(self.key)+" related_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nNo related issues.",
            }
        related = []
        for rel in self._related:
            related.append({
                "title": "<"+self._pm._provider_url+"/issues/"+str(rel.key)+"|"+rel._issuetype+" "+str(rel.key)+" "+rel._summary+">"
            })
        return {
            "text": "_/jira issue "+str(self.key)+" related_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nRelated Issues:",
            "attachments": related
        }

    def __get_related(self):
        """
        Fill-in related list with JiraIssue's.
        """
        # This should hit JIRA and bring just the related issues, as self._instance wouldn't have them cause performance
        for rel in self._instance.fields.issuelinks:
            if rel.type.name == 'Relates':
                self._related.append(JiraIssue(self._pm,rel.outwardIssue.key))

    @property
    def comments(self):
        """ Return the Issue Comments """
        self.__get_comments()
        if not self._comments:
            return {
                "text": "_/jira issue "+str(self.key)+" comments_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nNo comments."
            }
        return {
            "text": "_/jira issue "+str(self.key)+" comments_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nComments:",
            "attachments": self._comments
        }

    def last_comment(self):
        """ Return the last Issue Comment. """
        self.__get_comments(last=True)
        if not self._comments:
            return {
                "text": "_/jira issue "+str(self.key)+" comments_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nNo comments."
            }
        return {
            "text": "_/jira issue "+str(self.key)+" comments last_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nLast comment:",
            "attachments": self._comments
        }

    def __get_comments(self, **kwargs):
        """ Get Issue Comments from Provider. """
        comments = self._instance.fields.comment.comments
        for comment in comments:
            self._comments.append({
                "pretext": "_"+str(comment.updated)+" "+comment.author.displayName+" wrote:_",
                "text": comment.body,
                "mrkdwn_in": ["pretext", "text"]
            })
        if (kwargs.get('last', False) and self._comments):
            self._comments = [self._comments[-1]]

    @property
    def time_entries(self):
        """ Return the Issue Time Entries. """
        self.__get_time_entries()
        if not self._time_entries:
            return {
                "text": "_/jira issue "+str(self.key)+" time_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nNo time entries."
            }
        entries = []
        for entry in self._time_entries:
            entries.append({
                "pretext": "_"+str(entry._created_on)+" "+entry._user+" has spent *"+str(entry._hours)+":*_",
                "text": entry._comments,
                "mrkdwn_in": ["pretext", "text"]
            })
        return {
            "text": "_/jira issue "+str(self.key)+" time_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\nTime entries:",
            "attachments": entries
        }

    def __get_time_entries(self):
        """ Get Issue Time Entries from Provider. """
        for log in self._instance.fields.worklog.worklogs:
            self._time_entries.append(JiraTimeEntry(self, log.timeSpent,log.comment,log.author.displayName,log.created))

    def add_time_entry(self, hours, comments):
        """ Add a new Issue Time Entry.  """
        time_entry = JiraTimeEntry(self,hours,comments).save()
        if not time_entry:
            return {
            "text": "_/jira issue "+str(self.key)+" time add "+hours+" "+comments+"_\n"+"<"+self._pm._provider_url+"/issues/"+str(issue.key)+"|"+issue._issuetype+" "+str(issue.key)+" "+issue._summary+">\nCouldn't add entry",
            }
        return {
            "text": "_/jira issue "+str(self.key)+" time add "+str(hours)+" "+comments+"_\n"+"<"+self._pm._provider_url+"/issues/"+str(self.key)+"|"+self._issuetype+" "+str(self.key)+" "+self._summary+">\n_New Entry Time added:_",
            "attachments": [
                {
                    "pretext": "_"+str(time_entry._created_on)+" "+time_entry._user+" has spent *"+str(time_entry._hours)+" hours*:_",
                    "text": time_entry._comments,
                    "mrkdwn_in": ["pretext", "text"]
                }
            ]
        }