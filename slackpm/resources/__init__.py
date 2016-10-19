from ..exceptions import *

class SlackPMResource(object):
    """Abstract class Resource."""
    def __init__(self):
        """Abstarct Resource constructor."""
        raise NotImplementedError()


class SlackPMIssue(SlackPMResource):
    """Abstract class Issue."""

    def __init__(self):
        """Abstarct Issue constructor."""
        raise NotImplementedError()

    def show(self):
        """Abstract Issue show def."""
        raise NotImplementedError()

    def status(self):
        """Abstract Issue status def"""
        raise NotImplementedError()


    def tracker(self):
        """function tracker

        returns JSONResponse
        """
        raise NotImplementedError()

    def priority(self):
        """function priority

        returns JSONResponse
        """
        raise NotImplementedError()

    def assignee(self):
        """function assignee

        returns JSONResponse
        """
        raise NotImplementedError()

    def subtasks(self):
        """function subtasks

        returns JSONResponse
        """
        raise NotImplementedError()

    def related(self):
        """function related

        returns JSONResponse
        """
        raise NotImplementedError()

    def comments(self, last):
        """function comments

        last: Bool

        returns JSONResponse
        """
        raise NotImplementedError()

    def time_entries(self):
        """function time_entries

        returns JSONResponse
        """
        raise NotImplementedError()

    def time_entries(self, hours, comment):
        """function time_entries

        hours: Int
        comment: Char

        returns JSONResponse
        """
        raise NotImplementedError()

class SlackPMComment(SlackPMResource):
    """Class Comment
    """
    # Attributes:
    text = None  # (Char)
    __date = None  # (Date)
    __author = None  # (Char)

    # Operations
    def __init__(self):
        """function __init__

        returns
        """
        return None # should raise NotImplementedError()


class SlackPMProject(SlackPMResource):
    """Abstract class Project
    """
    # Attributes:
    __id = None  # (Int)
    __name = None  # (Char)
    __issues = None  # (list(Issue))

    # Operations
    def __init__(self,name):
        """function __init__

        returns
        """
        raise NotImplementedError()

    def todo(self):
        """function todo

        returns JSONResponse
        """
        raise NotImplementedError()



class SlackPMTimeEntry(SlackPMResource):
    """Class TimeEntry
    """
    # Attributes:
    date = None  # (Date)
    hours = None  # (Int)
    comment = None  # (Char)

    # Operations



