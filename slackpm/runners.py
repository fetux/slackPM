import re
import time
import logging

class CommandRunner(object):

    def benchmark(next, *args):
        def log(*args):
            requests_log = logging.getLogger("requests")
            requests_log.addHandler(logging.NullHandler())
            requests_log.propagate = False
            logging.basicConfig(filename='slackpm/slackpm.log', level=logging.INFO, format='%(asctime)-15s %(message)s')
            t1 = time.time()
            r = next(*args)
            t2 = time.time()
            logging.info('Benchmark: %s : %s', str(args[1])+" "+args[2], str(t2 - t1)+"s")
            return r
        return log

    @classmethod
    @benchmark
    def run(cls, manager, command):
        # For not auth commands decompress kwargs with **
        def __help(manager, kwargs=None): return manager.help()
        def __connect_key(manager, kwargs): return manager.connect(kwargs['url'], kwargs['key'])
        def __connect_passwd(manager, kwargs): return manager.connect(url=kwargs['url'], user=kwargs['user'], passwd=kwargs['passwd'])
        # For auth command do NOT decompress kwargs
        def __project_todo(manager, kwargs): return None
        def __issue_show(manager, kwargs): return manager.issue(kwargs['id']).show()
        def __issue_status(manager, kwargs): return manager.issue(kwargs['id']).status
        def __issue_set_status(manager, kwargs): return manager.issue(kwargs['id']).set_status(kwargs['value'])
        def __issue_priority(manager, kwargs): return manager.issue(kwargs['id']).priority
        def __issue_assignee(manager, kwargs): return manager.issue(kwargs['id']).assignee
        # def __issue_target(manager, kwargs): return
        def __issue_comments(manager, kwargs): return manager.issue(kwargs['id']).comments
        def __issue_subtasks(manager, kwargs): return manager.issue(kwargs['id']).subtasks
        def __issue_related(manager, kwargs): return manager.issue(kwargs['id']).related
        def __issue_comments_last(manager, kwargs): return manager.issue(kwargs['id']).last_comment()
        def __issue_time(manager, kwargs): return manager.issue(kwargs['id']).time_entries
        def __issue_add_time(manager, kwargs): return manager.issue(kwargs['id']).add_time_entry(kwargs['hours'], kwargs['comment'])
        commands = {
            __connect_key : r"^connect (?P<url>.\S+) (?P<key>[0-z]+)$",
            __connect_passwd : r"^connect (?P<url>.\S+) (?P<user>.\S+) (?P<passwd>.\S+)$",
            __project_todo : r"^todo (.\S+)$",
            __issue_show : r"^issue (?P<id>[0-Z\-]+)$",
            __issue_status : r"^issue (?P<id>[0-Z\-]+) status$",
            __issue_set_status : r"^issue (?P<id>[0-Z\-]+) status (?P<value>[A-z]+)$",
            __issue_priority : r"^issue (?P<id>[0-Z\-]+) priority$",
            __issue_assignee : r"^issue (?P<id>[0-Z\-]+) assignee$",
            # __issue_target : r"^issue (?P<id>[0-Z\-]+) target$",
            __issue_comments : r"^issue (?P<id>[0-Z\-]+) comments$",
            __issue_subtasks : r"^issue (?P<id>[0-Z\-]+) subtasks$",
            __issue_related : r"^issue (?P<id>[0-Z\-]+) related$",
            __issue_comments_last : r"^issue (?P<id>[0-Z\-]+) comments last$",
            __issue_time : r"^issue (?P<id>[0-Z\-]+) time$",
            __issue_add_time : r"^issue (?P<id>[0-Z\-]+) time add (?P<hours>\d+) (?P<comment>.+)$",
            __help: r"^help$"
        }
        for function, pattern in commands.items():
            m = re.search(pattern, command)
            if m:
                kwargs = m.groupdict()
                return function(manager, kwargs)
        return __help(manager)
