from pandas import DataFrame

from utils.ExcelParser import ExcelParser

from creators.StudentCreator import StudentCreator
from creators.PollCreator import PollCreator
from creators.SubmissionCreator import SubmissionCreator

ExcelParser().read_students("CES3063_Fall2020_rptSinifListesi.XLS")
print(StudentCreator().students)
ExcelParser().read_key("design_poll.csv")
ExcelParser().read_key("development_poll.csv")
print(PollCreator().polls)
ExcelParser().read_submissions("CSE3063_20201116_Mon_zoom_PollReport.csv")
print(SubmissionCreator().submissions)
ExcelParser().write_all_students(StudentCreator().students)
poll_count = 1
for poll in PollCreator().polls:
    ExcelParser().write_poll_outcomes(StudentCreator().students, SubmissionCreator().submissions,
                                      poll)
    ExcelParser().write_poll_statistics(poll)
    ExcelParser().write_all_poll_outcomes(StudentCreator().students, SubmissionCreator().submissions, poll, poll_count)
    poll_count += 1

