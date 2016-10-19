from .managers import *


class SlackProjectManagerFactory(object):
    """
    Factory class SlackProjectManagerFactory
    """
    # Attributes

    # Operations
    def __init__(self):
        """function __init__

        returns ProjectManager
        """

    @classmethod
    def create(cls,pm):
        """function connect

        pm: {}

        returns cls
        """
        managers = {
            "Redmine": RedmineProjectManager,
            "Jira": JiraProjectManager
        }
        return managers[pm['provider_name'].title()](pm)


class SlackProjectFactory(object):
    """
    Factory class SlackProjectFactory
    """
    # Attributes

    # Operations
    def __init__(self):
        """function __init__

        returns Project
        """


    @classmethod
    def create(cls,project):
        """function connect

        project: string

        returns cls
        """
        projects = {
            "Redmine": RedmineProject,
            "Jira": JiraProject
        }
        return projects[project.title()]()
