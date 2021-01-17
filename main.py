import os

from pandas import DataFrame

from creators.AttendanceCreator import AttendanceCreator
from utils.ExcelParser import ExcelParser

from creators.StudentCreator import StudentCreator
from creators.PollCreator import PollCreator
from creators.SubmissionCreator import SubmissionCreator
from utils.JsonParser import JsonParser

ExcelParser().read_students("CES3063_Fall2020_rptSinifListesi.XLS")
print(StudentCreator().students)
ExcelParser().read_key("design_poll.csv")
# ExcelParser().read_key("development_poll.csv")
print(PollCreator().polls)
attendancefilename = "attendances.json"
if os.path.exists(attendancefilename):
    JsonParser().read_attendances(StudentCreator().students, attendancefilename)
ExcelParser().read_submissions("CSE3063_20201123_Mon_zoom_PollReport.csv")
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



