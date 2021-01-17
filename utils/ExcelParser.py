
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xlsxwriter

from creators.PollCreator import PollCreator
from creators.StudentCreator import StudentCreator
from creators.SubmissionCreator import SubmissionCreator
from utils.Singleton import Singleton


class ExcelParser(metaclass=Singleton):
    def __init__(self):
        self.poll = None

    def _read_max_file_column_count(self, filename: str, delimiter=','):
        # The max column count a line in the file could have
        largest_column_count = 0

        # Loop the data lines
        with open(filename, 'r', encoding='utf-8') as temp_f:
            # Read the lines
            lines = temp_f.readlines()

            for line in lines:
                # Count the column count for the current line
                column_count = len(line.split(delimiter)) + 1

                # Set the new most column count
                largest_column_count = column_count if largest_column_count < column_count else largest_column_count
        return largest_column_count

    def read_students(self, filename: str):
        # next line is for debugging
        # pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.width', None)
        df: pd.DataFrame = pd.read_excel(filename, header=None)
        df.drop([0, 1, 3, 5, 6, 8, 9], axis=1, inplace=True)
        df = df[pd.to_numeric(df[2], errors='coerce').notnull()]
        df.reset_index(drop=True, inplace=True)
        df.columns = ['studentid', 'firstname', 'lastname', 'repeat']
        sc = StudentCreator()
        for index, row in df.iterrows():
            sc.create_student(
                number=row['studentid'], name=row['firstname'], surname=row['lastname'],
                description=pd.isna(row['repeat'])
            )

    def read_key(self, filename: str = None):
        if filename is None:
            filename = input("Please enter a filename for an answer key file:\n")

        # next line is for debugging
        # pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.width', None)
        df: pd.DataFrame = pd.read_csv(filename, sep=';', header=None)
        pollname = df[0][0]
        df.drop(inplace=True, axis=0, labels=0)
        df.reset_index(inplace=True, drop=True)
        pc = PollCreator()
        pc.create_poll(pollname)
        # TODO Poll creation logic is flawed, how do we add questions to polls?

    def read_submissions(self, filename: str = None):
        if filename is None:
            filename = input("Please enter a filename for an answer key file:\n")

        # next line is for debugging
        # pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.width', None)
        df: pd.DataFrame = pd.read_csv(filename, sep=',', index_col=False, header=None, names=range(
            self._read_max_file_column_count(filename)))
        df.dropna(axis=1, how='all', inplace=True)
        df.drop(labels=0, axis=1, inplace=True)
        df.drop(labels=0, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        sc = SubmissionCreator()
        for index, row in df.iterrows():
            q_and_a = dict()
            for colindex, cell in row.iteritems():
                if colindex < 4 or colindex % 2 == 1:
                    continue
                q_and_a[cell] = row[colindex + 1]
            sc.create_submission(row[1], row[2], row[3], q_and_a)

    def write_poll_outcomes(self, students, submissions):
        rows = []  # rows will be added to this list
        columns = ['Student No', 'Name', 'Surname', 'Description']

        for student in students:
            q_a_list = []  # each poll has specific amount of questions, this list holds 1 or 0 depending on answers.
            num_of_questions = None  # each field will reset for each student
            num_of_correct_ans = 0
            success_rate = None
            success_percentage = None
            row = [student.number, student.name, student.surname, student.description]

            for submission in submissions:   # find current poll submissions
                if submission.poll == self.poll:
                    if submission.student == student:  # find student in submission list.

                        for answer in submission.student_answers:
                            # for each answer in this submission check if it is true.
                            num_of_questions = len(submission.student_answers)

                            if answer.question.true_answer == answer:
                                row.append(1)  # answer matches with true answer
                                num_of_correct_ans += 1
                            else:
                                row.append(0)  # false

            # calculating rate and percentage
            success_rate = num_of_correct_ans / num_of_questions
            success_percentage = success_rate * 100
            row.append(success_rate)
            row.append(success_percentage)
            rows.append(row)

        for i in range(num_of_questions):  # column tag for Q1, Q2 ...
            tag = "Q" + str(i)
            columns.append(tag)

        columns.append('Success Rate')  # continue appending column tags
        columns.append('Success Percentage')

        output = pd.DataFrame(rows, columns=columns)  # output as excel
        output.to_excel('./output.xlsx')  # TODO: This will change to poll name

    def write_poll_statistics(self, poll):

        poll_excel = xlsxwriter.Workbook(poll.name + '.xlsx')

        if poll == self.poll:  # checks current poll
            for question in poll.poll_questions:  # find question in questions of that poll
                question_counter = 1
                list_number_selected_choice = []
                correct_answer = question.true_answer
                plt.title(question.description)

                for answer in question.all_answers:
                    # appends the number of student selections of answers at that question in the list.
                    list_number_selected_choice.append(answer.number_of_answer_selection)

                # creates histogram as its desired
                fig, ax = plt.subplots()
                width = 0.75  # the width of the bars
                ind = np.arange(len(list_number_selected_choice))  # the x locations for the groups
                index = question.all_answers.index(correct_answer)
                pylist = ax.barh(ind, list_number_selected_choice, width, color="blue")
                pylist[index].set_color('g')
                ax.set_yticks(ind + width / 2)
                ax.set_yticklabels(question.all_answers, minor=False)
                for i, v in enumerate(list_number_selected_choice):
                    ax.text(v, i, " " + str(v) + " times", color='blue', va='center', fontweight='bold')
                plt.xlabel('x')
                plt.ylabel('y')
                plt.savefig(os.path.join("Question" + question_counter + '.png'),
                            dpi=300, format='png', bbox_inches='tight')

                # Insert image of the questions of polls to the excel sheet.
                question_sheet = poll_excel.add_worksheet("Question"+question_counter)
                question_sheet.insert_image('A1', "Question"+question_counter + '.png')
                question_counter = question_counter+1
        poll_excel.close()

    def write_all_poll_outcomes(self, polls):
        print()
# poll adları dönen for loop
# write_poll_outcomes(students, submissions):

