from entities.Answer import Answer
from entities.Poll import Poll
from entities.Question import Question
from utils.Singleton import Singleton


class PollCreator(metaclass=Singleton):
    def __init__(self):
        self.polls = []

    def create_poll(self, name, poll_number, q_and_a):
        poll = Poll(name, poll_number)
        # TODO: Might an error occur here because of a warning, look here later.
        for key in q_and_a:
            new_question = Question(key, list(), poll, None)
            for each_answer in q_and_a[key]:
                new_answer = Answer(each_answer, new_question)
                new_question.true_answers.append(new_answer)
                new_question.all_answers.append(new_answer)

            poll.poll_questions.append(new_question)
        self.polls.append(poll)
        return poll
