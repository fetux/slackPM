from . import SlackPMProject

class RedmineProject(SlackPMProject):
    """
    Class RedmineProject
    """
    # Operations
    def __init__(self, pm, identifier):
        self._pm_instance = pm._instance
        self.url = pm._provider_url
        if not identifier: raise BadAttributesError()
        self._identifier = identifier
        self._instance = self._pm_instance.project.get(identifier) # Could raise ResourceNotFoundError
        self.name = self._instance.name
        return None

    def todo(self):
        # Get issues with status "In Progress"
        issues = self._pm_instance.issue.filter(project_id=self._identifier,assigned_to_id="me",status_id=2, limit=3)
        if not issues:
            # Get issues with status "New"
            issues = self._pm_instance.issue.filter(project_id=self._identifier,assigned_to_id="me",status_id=7,limit=3)
            if not issues:

                return {"text": "It seems there are not issues here."}
        todo = []
        for issue in issues:
            todo.append({
                "pretext": "<"+self.url+"/issues/"+str(issue.id)+"|"+issue.tracker.name+"#"+str(issue.id)+" "+issue.subject+">"+"\n_created by "+issue.author.name+"_",
                "title": "Description",
                "text": issue.description,
                "fields":[
                    {
                        "title": "Status",
                        "value": issue.status.name,
                        "short": True
                    },
                    {
                        "title": "Priority",
                        "value": issue.priority.name,
                        "short": True
                    },
                    {
                        "title": "Assignee",
                        "value": (issue.assigned_to.name if "assigned_to" in dir(issue) else "Not assigned"),
                        "short": True
                    },
                    {
                        "title": "Estimated hours",
                        "value": (issue.estimated_hours if "estimated_hours" in dir(issue) else "-"),
                        "short": True
                    },
                ],
                "mrkdwn_in": ["pretext", "text", "fields"]
            })
        return {
            "text": "_/redmine todo_",
            "attachments": todo
        }

class JiraProject(SlackPMProject):
    """
    Class JiraProject
    """
    # Operations
    def __init__(self, pm, key):
        self._pm = pm
        self._url = pm._url
        if not key: raise BadAttributesError()
        self._key = key
        self._instance = self._pm._instance.project(key) # Could raise JIRAError
        self._name = self._instance.name
        return None

    def todo(self):
        # Top 3 issues due by the end of the week, ordered by priority
        issues = self._pm._instance.search_issues('assignee = currentUser() and due < endOfWeek() order by priority desc', maxResults=3)
        if not issues:
            # Top 3 issues "In Progress", ordered by priority
            issues = self._pm._instance.search_issues('assignee = currentUser() and status = "In Progress" order by priority desc', maxResults=3)
            if not issues:

                return ({
                    "text": "It seems there are not issues here."
                })
        todo = []
        for issue in issues:
            todo.append({
                "pretext": "<"+self._url+"/browse/"+str(issue.key)+"|"+issue.fields.issuetype.name+" "+issue.key+" "+issue.fields.summary+">"+"\n_created by "+issue.fields.creator.displayName+"_",
                "title": "Description",
                "text": issue.fields.description,
                "fields":[
                    {
                        "title": "Status",
                        "value": issue.fields.status.name,
                        "short": True
                    },
                    {
                        "title": "Priority",
                        "value": issue.fields.priority.name,
                        "short": True
                    },
                    {
                        "title": "Assignee",
                        "value": (issue.fields.assignee.displayName if "assignee" in dir(issue.fields) else "Not assigned"),
                        "short": True
                    },
                    {
                        "title": "Story Points",
                        "value": (issue.fields.customfield_10024 if "customfield_10024" in dir(issue.fields) else "-"),
                        "short": True
                    },
                ],
                "mrkdwn_in": ["pretext", "text", "fields"]
            })
        return {
            "text": "_/redmine todo_",
            "attachments": todo
        }



