from entities.Answer import Answer
from entities.Poll import Poll
from entities.Question import Question
from utils.Singleton import Singleton


class PollCreator(metaclass=Singleton):
    def __init__(self):
        self.polls = []

    def create_poll(self, name, question, answer):
        poll = Poll(name)
        # TODO: Might an error occur here because of a warning, look here later.
        new_question = Question(question, None, poll, None)
        new_answer = Answer(answer, new_question)

        new_question.true_answer = new_answer
        new_question.all_answers.append(new_answer)

        poll.poll_questions.append(new_question)
        self.polls.append(poll)
        return poll
