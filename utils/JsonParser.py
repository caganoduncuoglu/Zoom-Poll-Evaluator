import json
from types import SimpleNamespace

from creators.AttendanceCreator import AttendanceCreator
from utils.Singleton import Singleton


class JsonParser(metaclass=Singleton):

    def read_attendances(self, students, filename):
        with open(filename) as f:
            attendances = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
            AttendanceCreator().attendances = attendances

            for attendance in attendances:
                for student_number in attendance.student_numbers:
                    for student in students:
                        if student.number == student_number:
                            student.attendances(attendance)
                            break

    def write_attendances(self, attendances, filename):
        with open(filename, "w") as f:
            json.dump(attendances, f, ensure_ascii=False)
