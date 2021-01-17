class Attendance:

    def __init__(self, session, base_time, is_poll_question):
        self.session = session
        self.base_time = base_time
        self.is_poll_question = is_poll_question
        self.student_numbers = []
