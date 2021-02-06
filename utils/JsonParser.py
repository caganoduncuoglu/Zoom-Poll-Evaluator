import json

import jsonpickle

from creators.AttendanceCreator import AttendanceCreator
from utils.Singleton import Singleton


class JsonParser(metaclass=Singleton):

    def read_attendances(self, students, filename):
        with open(filename) as f:
            attendances = jsonpickle.decode(f.read())
            AttendanceCreator().attendances = attendances

            for attendance in attendances:
                for student_number in attendance.student_numbers:
                    for student in students:
                        if student.number == student_number:
                            student.attendances.append(attendance)
                            break

    def write_attendances(self, attendances, filename):
        with open(filename, "w") as f:
            f.write(jsonpickle.encode(attendances))

    def read_config(self, filename):
        with open(filename) as f:
            config_dict = json.load(f)
            return config_dict
