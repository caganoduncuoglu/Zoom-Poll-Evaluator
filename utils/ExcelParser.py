import glob
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

    def _get_tokenized_answers(self, answerstr: str):
        if ";" not in answerstr:
            return [answerstr]
        else:
            return answerstr.split(';')

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
                description=not pd.isna(row['repeat'])
            )

    def read_key(self, filename: str = None):
        if filename is None:
            filename = input("Please enter a filename for an answer key file:\n")

        f = open(filename, "r", encoding="utf-8")

        pc = PollCreator()
        q_and_a = dict()

        curr_poll_name = None
        curr_question_desc = None
        poll_number = None
        for line in f:
            if "poll " in line.lower() and "polls" not in line.lower():
                if curr_poll_name is not None:
                    pc.create_poll(curr_poll_name, poll_number,
                                   q_and_a)  # Create a poll with completed read operations.
                q_and_a.clear()  # Clear questions for a new poll.
                full_poll_name = line.split("\t")[0]
                poll_number = full_poll_name.split(":")[0].split(" ")[2]
                curr_poll_name = full_poll_name.split(":")[1]
            elif "choice" in line.lower():
                curr_line = line[3:-1]
                curr_line = curr_line.replace(" ( Multiple Choice)", "")
                curr_line = curr_line.replace(" ( Single Choice)", "")
                curr_question_desc = curr_line
            elif "answer" in line.lower():
                answerstr = line.split(":")[1][:-1].strip()
                if curr_question_desc in q_and_a.keys():
                    q_and_a[curr_question_desc].append(answerstr)
                else:
                    q_and_a[curr_question_desc] = [answerstr]

        pc.create_poll(curr_poll_name, poll_number, q_and_a)

    def read_submissions(self, filename: str = None):
        if filename is None:
            filename = input("Please enter a filename for an answer key file:\n")

        # next line is for debugging
        # pd.set_option('display.max_rows', None, 'display.max_columns', None, 'display.width', None)
        df: pd.DataFrame = pd.read_csv(filename, sep=',', index_col=False, header=None, names=range(
            self._read_max_file_column_count(filename)))
        mask = df.applymap(type) != bool
        d = {True: "True", False: "False"}
        df = df.where(mask, df.replace(d))

        df.dropna(axis=1, how='all', inplace=True)
        df.drop(labels=0, axis=1, inplace=True)
        df.drop(labels=0, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        sc = SubmissionCreator()

        poll_time = df.iloc[2][2]
        for index, row in df.iterrows():
            if index < 5:
                continue
            q_and_a = dict()
            for colindex, cell in row.iteritems():
                if colindex < 4 or colindex % 2 == 1:
                    continue
                if pd.isna(row[colindex + 1]):
                    break
                else:
                    q_and_a[cell] = self._get_tokenized_answers(str(row[colindex + 1]))
            sc.create_submission(row[1], row[2], row[3], q_and_a, filename, poll_time)

    def write_session_attendance(self, students, attendances):
        columns = ['Student No', 'Name', 'Surname', 'Description', 'Poll Attendances', 'Total Attendance',
                   'Attendance Rate']
        rows = []
        for student in students:
            row = [student.number, student.name, student.surname, student.description, len(student.attendances),
                   len(attendances), (len(student.attendances) * 1.0) / len(attendances)]
            rows.append(row)

        output = pd.DataFrame(rows, columns=columns)
        output.to_excel("student_attendances.xlsx")

    def write_student_quiz_report(self, students, submissions, poll):

        for student in students:
            rows = []  # rows will be added to this list
            columns = ['Question Text', 'Given Answer', 'Correct Answer', 'Correct']

            for submission in submissions:  # find current poll submissions
                if submission.poll == poll:
                    if submission.student == student:  # find student in submission list.
                        for question in submission.poll.poll_questions:
                            row = []
                            is_correct = 0

                            related_student_answers = []

                            row.append(question.description)  # question text

                            for answer in submission.student_answers:  # collect student's answers
                                if answer.question.description == question.description:
                                    related_student_answers.append(answer)

                            student_answers = ';'.join(map(str, related_student_answers))  # concat multiple answers
                            true_answers = ';'.join(map(str, question.true_answers))
                            row.append(student_answers)  # student answers
                            row.append(true_answers)  # true answers

                            is_truly_answered = False

                            for related_student_curr_answer in related_student_answers:
                                for question_true_answer in question.true_answers:  # check if student answer and true answer match
                                    if related_student_curr_answer.description.lower().strip() == question_true_answer.description.lower().strip():
                                        is_truly_answered = True
                                        is_correct = 1
                                        break

                                if is_truly_answered:
                                    break

                            row.append(is_correct)
                            rows.append(row)  # append row elements to row

                        break


            output = pd.DataFrame(rows, columns=columns)  # output as excel
            poll_time = poll.poll_time.replace("-", "_")
            name_of_poll = poll.name.replace(" ", "_") + "_" + poll_time.replace(":", "_")
            student_name = student.name.replace(" ", "_") + "_" + student.surname.replace(" ", "_")
            poll_name = "Quiz Reports For Each Student" + "/" + name_of_poll + "_" + student_name + ".xlsx"
            output.to_excel(poll_name)  # output


    def write_poll_outcomes(self, students, submissions, poll):
        rows = []  # rows will be added to this list
        columns = ['Student No', 'Name', 'Surname', 'Description', 'Num of Questions', 'Num of Correct Ans', 'Num of Wrong Ans', 'Num of Empty Ans']

        num_of_questions = 0  # find number of questions for that poll
        for questions in poll.poll_questions:
            num_of_questions += 1

        max_num_of_questions = 0
        for student in students:
            num_of_empty_ans = 0
            num_of_correct_ans = 0
            row = [student.number, student.name, student.surname, student.description, num_of_questions]
            student_found = False

            for submission in submissions:  # find current poll submissions
                if submission.poll == poll:
                    if submission.student == student:  # find student in submission list.
                        student_found = True
                        for question in submission.poll.poll_questions:
                            related_student_answers = []

                            for answer in submission.student_answers:
                                if answer.question.description == question.description:
                                    related_student_answers.append(answer)

                            is_truly_answered = False
                            for related_student_curr_answer in related_student_answers:
                                for question_true_answer in question.true_answers:
                                    if related_student_curr_answer.description.lower().strip() == question_true_answer.description.lower().strip():
                                        num_of_correct_ans += 1
                                        is_truly_answered = True
                                        break
                                if is_truly_answered:
                                    break

                        break

            if student_found == False:  # if student didn't attend the poll
                num_of_empty_ans = num_of_questions

            row.append(num_of_correct_ans)
            row.append(num_of_questions - num_of_correct_ans - num_of_empty_ans)  # it will change
            row.append(num_of_empty_ans)

            # calculating rate and percentage
            success_rate = 0
            success_percentage = 0.0
            if num_of_questions == 0:
                success_rate = 0
            else:
                max_num_of_questions = num_of_questions
                success_rate = (num_of_correct_ans * 1.0) / num_of_questions
                success_percentage = success_rate * 100.0

            for i in range(len(row), len(columns) ):
                row.append(0)

            row.append(success_rate)
            row.append(success_percentage)
            rows.append(row)

        columns.append('Rate of Correct Answers')  # continue appending column tags
        columns.append('Accuracy Percentage')

        output = pd.DataFrame(rows, columns=columns)  # output as excel
        poll_name = poll.name + ".xlsx"  # TODO: Name will change
        output.to_excel(poll_name)  # output

    def write_poll_statistics(self, poll, poll_counter):

        poll_excel = xlsxwriter.Workbook(poll.name + "-graphs" + '.xlsx')

        if poll == poll:  # checks current poll
            question_counter = 1
            for question in poll.poll_questions:  # find question in questions of that poll

                list_number_selected_choice = []
                # correct_answers = question.true_answers

                for answer in question.all_answers:
                    # appends the number of student selections of answers at that question in the list.
                    list_number_selected_choice.append(answer.number_of_answer_selection)

                # creates histogram as its desired
                fig, ax = plt.subplots()
                width = 0.5  # the width of the bars
                ind = np.arange(len(list_number_selected_choice))  # the x locations for the groups

                pylist = ax.barh(ind, list_number_selected_choice, width, color="red")

                for my_answer in question.true_answers:  # Green bar for the more than one correct answers.
                    index = question.all_answers.index(my_answer)
                    pylist[index].set_color('green')

                ax.set_yticks(ind + width / 2)
                ax.set_yticklabels(question.all_answers, minor=False)
                for i, v in enumerate(list_number_selected_choice):
                    ax.text(v, i, " " + str(v) + " times", color='red', va='center', fontweight='normal')

                plt.title(question.description,
                          fontsize=10,
                          color="green")

                plt.legend(["True Answer"], loc="upper right")
                plt.savefig(
                    os.path.join("Poll" + str(poll_counter) + " " + "Question" + str(question_counter) + '.png'),
                    dpi=300, format='png', bbox_inches='tight')
                plt.close()
                # Insert image of the questions of polls to the excel sheet.
                question_sheet = poll_excel.add_worksheet(
                    "Poll" + str(poll_counter) + " " + "Question" + str(question_counter))
                question_sheet.insert_image('A1', "Poll" + str(poll_counter) + " " + "Question" + str(
                    question_counter) + '.png')
                question_counter = question_counter + 1
        poll_excel.close()
        for pngfile in glob.glob("./*.png"):
            os.remove(pngfile)

    def write_all_poll_outcomes(self, students, submissions, poll, poll_count):
        rows = []  # rows will be added to this list
        columns = []

        max_num_of_questions = 0
        for student in students:
            num_of_questions = 0  # each field will reset for each student
            num_of_correct_ans = 0
            row = []

            is_this_student_answered = False
            for submission in submissions:  # find current poll submissions
                if submission.poll == poll:
                    if submission.student == student:  # find student in submission list.
                        is_this_student_answered = True
                        # answered = []
                        if poll.name not in columns:
                            columns.append(poll.name)

                        for question in submission.poll.poll_questions:
                            related_student_answers = []

                            for answer in submission.student_answers:
                                if answer.question.description == question.description:
                                    related_student_answers.append(answer)

                            is_truly_answered = False
                            for related_student_curr_answer in related_student_answers:
                                for question_true_answer in question.true_answers:
                                    if related_student_curr_answer.description.lower().strip() == question_true_answer.description.lower().strip():
                                        num_of_correct_ans += 1
                                        is_truly_answered = True
                                        break
                                if is_truly_answered:
                                    break

                            num_of_questions += 1
                        break

            row.append(num_of_correct_ans)
            rows.append(row)

        output2 = pd.DataFrame(rows, columns=columns, index=np.arange(1, len(rows) + 1))
        output = pd.read_excel('GlobalList.xlsx', index_col=0)
        output = output.join(output2, rsuffix=poll_count)
        output['Student No'] = output['Student No'].astype(str)
        output.to_excel('GlobalList.xlsx')

    def write_all_students(self, students):
        rows = []  # rows will be added to this list
        columns = ['Student No', 'Full Name', 'Repeat']

        for student in students:
            row = [student.number, student.name + ' ' + student.surname, student.description]
            rows.append(row)

        output = pd.DataFrame(rows, columns=columns, index=np.arange(1, len(rows) + 1))  # output as excel
        output['Student No'] = output['Student No'].astype(str)
        output.to_excel('GlobalList.xlsx')  # output
