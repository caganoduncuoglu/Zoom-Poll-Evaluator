from entities.Question import Question


class Attendance(Question):

    def __init__(self, session, description, true_answer, poll):
        super().__init__(description, true_answer, poll)
        self.session = session
