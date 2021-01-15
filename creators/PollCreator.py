from entities.Poll import Poll
from utils.Singleton import Singleton


class PollCreator(metaclass=Singleton):
    def __init__(self):
        self.polls = []

    def create_poll(self, name):
        poll = Poll(name)
        self.polls.append(poll)
        return poll
