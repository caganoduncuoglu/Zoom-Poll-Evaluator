import json

from creators.AttendanceCreator import AttendanceCreator
from utils.Singleton import Singleton


class JsonParser(metaclass=Singleton):

    def read_attendances(self, students, filename):
        with open(filename) as f:
            data = json.load(f)
            for student_data in data:
                student_id = student_data.id
                student = None
                for currStudent in students:
                    if currStudent.number == student_id:
                        student = currStudent

                if student is None:
                    print("Student with " + student_id + " can't load from json file.")
                    exit(-1)

                attendances = []
                for attendance in student_data.attendances:
                    new_attendance = AttendanceCreator().create_attendance(attendance, None, None)
                    attendances.append(new_attendance)

                student.attendances = attendances

    def write_attendances(self, students, filename):
        students_data = []
        for student in students:
            data = {id: student.number}
            attendances_names = []
            for attendance in student.attendances:
                attendances_names.append(attendance.session)

            data["attendances"] = attendances_names
            students_data.append(data)
        with open(filename, "w") as f:
            json.dump(students_data, f, ensure_ascii=False)
