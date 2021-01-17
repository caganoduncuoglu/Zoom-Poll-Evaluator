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
for poll in PollCreator().polls:
    ExcelParser().write_poll_outcomes(StudentCreator().students, SubmissionCreator().submissions,
                                      poll)
    ExcelParser().write_poll_statistics(poll)

