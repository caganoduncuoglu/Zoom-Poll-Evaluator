class Submission:

    def __init__(self, submitted_datetime, student, poll, student_answers = None):
        if student_answers is None:
            student_answers = []
        self.student_answers = student_answers
        #there should be a check with question answers for Number of answer Selection
        self.submitted_datetime = submitted_datetime
        self.student = student
        self.poll = poll