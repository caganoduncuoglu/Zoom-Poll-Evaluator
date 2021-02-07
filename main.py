import os

from creators.AttendanceCreator import AttendanceCreator
from creators.PollCreator import PollCreator
from creators.StudentCreator import StudentCreator
from creators.SubmissionCreator import SubmissionCreator
from utils.ExcelParser import ExcelParser
from utils.JsonParser import JsonParser

config = JsonParser().read_config("config.json")

ExcelParser().read_students(config["student_list_filename"])  # Create students from bys file.

for filename in config["read_key_filenames"]:
    print("Processing " + filename + " answer key file.", )
    ExcelParser().read_key(filename)

if os.path.exists(config["attendance_json_filename"]):  # Read attendance information from json.
    print("Reading attendance information from " + config["attendance_json_filename"])
    JsonParser().read_attendances(StudentCreator().students, config["attendance_json_filename"])

for filename in config["poll_report_filenames"]:  # Reading submission for each report.
    print("Reading " + filename + " submission file.")
    ExcelParser().read_submissions(filename)

# Writing attendances of all students as json for another run.
JsonParser().write_attendances(AttendanceCreator().attendances, config["attendance_json_filename"])
# Writing attendances as excel.
ExcelParser().write_session_attendance(StudentCreator().students, AttendanceCreator().attendances)

ExcelParser().write_all_students(StudentCreator().students)

if not os.path.exists(config["quiz_reports_student_filename"]):
    os.makedirs(config["quiz_reports_student_filename"])

poll_count = 1
for poll in PollCreator().polls:
    isExist = False
    for sub in SubmissionCreator().submissions:
        if sub.poll == poll:
            isExist = True
            break

    if not isExist:
        continue
    ExcelParser().write_student_quiz_report(StudentCreator().students, SubmissionCreator().submissions,
                                      poll)
    ExcelParser().write_poll_outcomes(StudentCreator().students, SubmissionCreator().submissions,
                                      poll)
    ExcelParser().write_poll_statistics(poll, poll_count)

    ExcelParser().write_all_poll_outcomes(StudentCreator().students, SubmissionCreator().submissions, poll, poll_count)

    poll_count += 1
