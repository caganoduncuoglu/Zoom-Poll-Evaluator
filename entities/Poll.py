class Poll(object):

    def __init__(self, name, poll_questions=None):

        if poll_questions is None:
            poll_questions = []

        set.__poll_questions = poll_questions
        self.__name = name
