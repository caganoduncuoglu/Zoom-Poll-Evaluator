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

ExcelParser().read_submissions("94502073867_PollReport (1).csv")

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



