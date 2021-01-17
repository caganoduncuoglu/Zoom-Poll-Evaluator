from creators.AttendanceCreator import AttendanceCreator
from creators.PollCreator import PollCreator
from creators.StudentCreator import StudentCreator
from entities.Answer import Answer
from entities.Poll import Poll
from entities.Submission import Submission
from utils.NameComperator import NameComparator
from utils.Singleton import Singleton


class SubmissionCreator(metaclass=Singleton):

    def __init__(self):
        self.submissions = []

    def create_submission(self, username, email, submit_date, q_and_a,
                          filename):  # Creates a new submission from a student.
        poll = None
        all_polls = PollCreator().polls
        curr_poll: Poll
        is_attendance_question = False
        for curr_poll in all_polls:  # Finding poll by looking answered questions are the same or not.
            for question in curr_poll.poll_questions:
                is_match = False
                for key in q_and_a:
                    if key == "Are you attending this lecture?":
                        is_attendance_question = True
                        break

                    if key == question.description:
                        is_match = True
                if is_attendance_question:
                    break

                if not is_match:  # Check is this poll a match.
                    continue
            if is_attendance_question:
                break

            poll = curr_poll  # If this poll is a match, assign it and break loop.
            break

        if poll is None and not is_attendance_question:  # Error check for poll.
            print("Poll could not matched with existing ones.")
            exit(-1)

        submit_date_parsed = submit_date.split(" ")
        base_time = submit_date_parsed[0:2]
        attendance = AttendanceCreator().create_attendance(filename, base_time, is_attendance_question)

        student_answers = []
        for key in q_and_a:  # Iterating through each question and answer pairs.
            question_to_insert = None
            answers_to_insert = []

            # TODO Maybe some wrapper methods in PolLCreator for getting question instances would make things easier
            for question in poll.poll_questions:  # Finding question for current answer.
                if question.description == key:
                    question_to_insert = question
                    break

            for answer_from_student in q_and_a[key]:
                is_answer_exist = False
                for answer in question_to_insert.all_answers:  # Checking existence of answer.
                    if answer.description == answer_from_student:
                        answers_to_insert.append(answer)
                        is_answer_exist = True
                        break
                if not is_answer_exist:
                    new_answer = Answer(answer_from_student,
                                        question_to_insert)  # Creating answer for the poll if not exist.
                    answers_to_insert.append(new_answer)

            for answer in answers_to_insert:
                student_answers.append(answer)

        student = None
        all_students = StudentCreator().students

        # FIXME: The usage of NameComparator singleton class may be wrong and possible errors may occur.
        for currStudent in all_students:  # Finding student coming from submission list inside BYS student list.
            if NameComparator(username, currStudent.name, currStudent.surname).consider_multiple_names_and_surnames():
                student = currStudent
                break

        if student is None:  # Error check for student.
            print(username + " student couldn't find in BYS document.")
            exit(-2)

        if student.email == "":  # Add email information coming from submission list.
            student.email = email

        if attendance not in student.attendances:  # Add attendance if not exist in student attendances list.
            student.attendances.append(attendance)
            attendance.student_numbers.append(student.number)

        submission = Submission(student_answers, submit_date, student, poll)
        self.submissions.append(submission)
        return submission
