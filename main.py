import os

from creators.AttendanceCreator import AttendanceCreator
from creators.PollCreator import PollCreator
from creators.StudentCreator import StudentCreator
from creators.SubmissionCreator import SubmissionCreator
from utils.ExcelParser import ExcelParser
from utils.JsonParser import JsonParser

ExcelParser().read_students("CES3063_Fall2020_rptSinifListesi.XLS")
print(StudentCreator().students)
ExcelParser().read_key("CSE3063 OOSD Weekly Session 1 - Monday Quizzes ANSWER KEY.txt")
ExcelParser().read_key("CSE3063 OOSD Weekly Session 2 - Tuesday Quizzes ANSWER KEY.txt")

print(PollCreator().polls)
attendancefilename = "attendances.json"
if os.path.exists(attendancefilename):
    JsonParser().read_attendances(StudentCreator().students, attendancefilename)

ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (1).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (3).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (5).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (7).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (8).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (9).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (12).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (14).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (16).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (17).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (20).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (21).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport (22).csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport_18-01-2021.csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport_19-10-2020.csv")
# ExcelParser().read_submissions("New Poll Reports/94502073867_PollReport_26-10-2020.csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (1).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (3).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (4).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (6).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (10).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (15).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (16).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (23).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (27).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport (28).csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport_12-01-2021.csv")
# ExcelParser().read_submissions("New Poll Reports/97056655049_PollReport_20-10-2020.csv")

print(SubmissionCreator().submissions)
JsonParser().write_attendances(AttendanceCreator().attendances, attendancefilename)
ExcelParser().write_session_attendance(StudentCreator().students, AttendanceCreator().attendances)
ExcelParser().write_all_students(StudentCreator().students)
poll_count = 1
for poll in PollCreator().polls:
    ExcelParser().write_poll_outcomes(StudentCreator().students, SubmissionCreator().submissions,
                                      poll)
    ExcelParser().write_poll_statistics(poll, poll_count)
    ExcelParser().write_all_poll_outcomes(StudentCreator().students, SubmissionCreator().submissions, poll, poll_count)
    poll_count += 1



