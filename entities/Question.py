class Question(object):

    def __init__(self, description, true_answer, poll, all_answers=None, number_of_answer_selection=None):
        if all_answers is None:
            all_answers = []
        if number_of_answer_selection is None:
            number_of_answer_selection = []
        self.description = description
        self.true_answer = true_answer
        self.poll = poll
        self.all_answers = all_answers
