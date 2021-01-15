class Question(object):

    def __init(self, description, true_answer, poll, all_answers=None):
        if all_answers is None:
            all_answers = []

        self.__description = description
        self.__true_answer = true_answer
        self.__poll = poll
        self.__all_answers = all_answers
