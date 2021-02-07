class Poll(object):

    def __init__(self, name, poll_number, poll_questions=None, ):
        if poll_questions is None:
            poll_questions = []

        self.poll_time = None
        self.poll_number = poll_number
        self.poll_questions = poll_questions
        self.name = name

    def __str__(self):
        return self.name
