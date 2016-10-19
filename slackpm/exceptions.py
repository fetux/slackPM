class SlackPMErrorBase(Exception):
    """
    Base exception class for Redmine exceptions.
    """
    def __init__(self, *args, **kwargs):
        super(SlackPMErrorBase, self).__init__(*args, **kwargs)

class SlackPMAppTokenError(SlackPMErrorBase):
    """
    Invalid Application Token.
    """
    def __init__(self):
        super(SlackPMAppTokenError, self).__init__('Invalid Application Token')


class SlackPMAuthError(SlackPMErrorBase):
    """
    Invalid authentication details.
    """
    def __init__(self):
        super(SlackPMAuthError, self).__init__('Invalid authentication details')


class SlackPMProjectNotFoundError(SlackPMErrorBase):
    """
    Project resource not found.
    """
    def __init__(self):
        super(SlackPMProjectNotFoundError, self).__init__('Ups! Project not found dude :/')

class SlackPMIssueNotFoundError(SlackPMErrorBase):
    """
    Project resource not found.
    """
    def __init__(self):
        super(SlackPMIssueNotFoundError, self).__init__('Ups! Issue not found dude :/')

