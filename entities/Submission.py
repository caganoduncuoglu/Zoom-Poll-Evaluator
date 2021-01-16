class Submission:

    def __init__(self, student_answers, submitted_datetime, student, poll):
        self.student_answers = student_answers
        #there should be a check with question answers for Number of answer Selection
        self.submitted_datetime = submitted_datetime
        self.student = student
        self.poll = poll
