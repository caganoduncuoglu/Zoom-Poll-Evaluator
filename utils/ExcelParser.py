

from utils.Singleton import Singleton
from entities.Student import Student
from entities.Submission import Submission
from entities.Answer import Answer
from entities.Question import Question

class ExcelParser(metaclass=Singleton):

    def __init__(self, poll):
        self.poll = poll

    def write_poll_outcomes(self, students, submissions):
        for student in students:
            q_a_list = []  # each poll has specific amount of questions, this list holds 1 or 0 depending on answers.
            num_of_questions = None  # each field will reset for each student
            num_of_correct_ans = None
            success_rate = None
            success_percentage = None

            for submission in submissions and submission.poll == self.poll:  # find current poll submissions
                if submission.student == student:  # find student in submission list.

                    for answer in submission.student_answers:  # for each answer in this submission check if it is true.
                        num_of_questions = len(submission.student_answers)

                        if answer.question.trueAnswer == answer:
                            q_a_list.append(1)  # answer matches with true answer
                            num_of_correct_ans += 1
                        else:
                            q_a_list.append(0)  # false

            # calculating rate and percentage
            success_rate = num_of_correct_ans / num_of_questions
            success_percentage = success_rate / 100

            # TODO: This will be printed on excel with pandas.
            print(student.number, student.name, student.surname, student.description, question_list,
                  success_rate, success_percentage, end='\n')

    def write_poll_statistics(self,poll):
        if poll == self.poll:
            for question in poll.poll_questions:
                print(question.description)#bura bak
                for answers in question.all_answers:
                  # TODO: This will be printed on excel with pandas.
                    print(answers +"--->"+ answers.number_of_answer_selection)
                    #There should be a selection counter for Question to determine how many times answer is chosen.
                    #For instance,  first choice is selected by 25 students, second one is 3, third 76, fourth 12 ...

    def write_all_poll_outcomes(self,polls):
        #poll adları dönen for loop
            #write_poll_outcomes(students, submissions):

