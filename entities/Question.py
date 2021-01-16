class Question(object):

    def __init__(self, description, true_answers, poll, all_answers=None):
        if all_answers is None:
            all_answers = []
        self.description = description
        self.true_answers = true_answers
        self.poll = poll
        self.all_answers = all_answers
