from creators.PollCreator import PollCreator
from creators.StudentCreator import StudentCreator
from entities.Answer import Answer
from entities.Submission import Submission
from utils.Singleton import Singleton


class SubmissionCreator(metaclass=Singleton):

    def __init__(self):
        self.submissions = []

    def create_submission(self, username, email, submit_date, q_and_a):  # Creates a new submission from a student.
        poll = None
        all_polls = PollCreator().polls
        for curr_poll in all_polls:  # Finding poll by looking answered questions are the same or not.
            for question in curr_poll.questions:
                is_match = False
                for key in q_and_a:
                    if key == question.description:
                        is_match = True
                if not is_match:  # Check is this poll a match.
                    continue

            poll = curr_poll  # If this poll is a match, assign it and break loop.
            break

        if poll is None:  # Error check for poll.
            print("Poll could not matched with existing ones.")
            exit(-1)

        student_answers = []
        for key in q_and_a:  # Iterating through each question and answer pairs.
            question_to_insert = None
            answer_to_insert = None

            for question in poll.poll_questions:  # Finding question for current answer.
                if question.description == key:
                    question_to_insert = question

            for answer in question_to_insert.all_answers:  # Checking existence of question.
                if answer.description == q_and_a[key]:
                    answer_to_insert = answer

            if answer_to_insert is None:
                answer_to_insert = Answer(q_and_a[key],
                                          question_to_insert)  # Creating answer for the poll if not exist.

            student_answers.append(answer_to_insert)

        student = None
        all_students = StudentCreator().students

        # TODO: Try to think edge cases for finding students.
        for currStudent in all_students:  # Finding student coming from submission list inside BYS student list.
            if currStudent.name.lower() + " " + currStudent.surname.lower() == username:
                student = currStudent

        if student is None:  # Error check for student.
            print(username + " student couldn't find in BYS document.")
            exit(-2)

        if student.email == "":  # Add email information coming from submission list.
            student.email = email

        submission = Submission(student_answers, submit_date, student, poll)
        self.submissions.append(submission)
        return submission
