class Answer(object):

    def __init__(self, description, question):

        self.description = description
        self.question = question
        self.number_of_answer_selection = 0

    def __str__(self):
        return self.description
