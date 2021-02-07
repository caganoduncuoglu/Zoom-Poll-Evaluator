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
        if len(q_and_a) == 1 and next(iter(q_and_a.keys())) == "Are you attending this lecture?":
            is_attendance_question = True

        if not is_attendance_question:
            for curr_poll in all_polls:  # Finding poll by looking answered questions are the same or not.
                stu_set = set(
                    [str(k).replace(" ", "").lower().replace("\n", "").replace("\t", "") for k in q_and_a.keys()])
                poll_set = set([str(q).replace(" ", "").lower().replace("\n", "").replace("\t", "") for q in
                                curr_poll.poll_questions])
                is_match = True
                for set_item in stu_set:
                    if set_item not in poll_set:
                        is_match = False
                        break

                if is_match:
                    # Found matching poll
                    poll = curr_poll

            if poll is None:  # Error check for poll.
                print("Poll could not matched with existing ones.")
                exit(-1)

        submit_date_parsed = submit_date.split(" ")
        base_time = submit_date_parsed[1]
        attendance = AttendanceCreator().create_attendance(filename, base_time, is_attendance_question)

        if not is_attendance_question:
            student_answers = []
            for key in q_and_a:  # Iterating through each question and answer pairs.
                question_to_insert = None
                answers_to_insert = []

                # TODO Maybe some wrapper methods in PolLCreator for getting question instances would make things easier
                for question in poll.poll_questions:  # Finding question for current answer.
                    if question.description.replace(" ", "").lower().replace("\n", "").replace("\t", "") \
                            == key.replace(" ", "").lower().replace("\n", "").replace("\t", ""):
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
                    if answer not in question_to_insert.all_answers:
                        question_to_insert.all_answers.append(answer)
                    answer.number_of_answer_selection += 1

        student = None
        all_students = StudentCreator().students

        student = NameComparator().fuzzy_find(username, all_students)

        if student is None:  # Error check for student.
            print(username + " student couldn't find in BYS document.")
            exit(-2)

        if student.email == "":  # Add email information coming from submission list.
            student.email = email

        if attendance not in student.attendances:  # Add attendance if not exist in student attendances list.
            student.attendances.append(attendance)
            attendance.student_numbers.append(student.number)

        submission = None
        if not is_attendance_question:
            submission = Submission(student_answers, submit_date, student, poll)
            self.submissions.append(submission)
        return submission
