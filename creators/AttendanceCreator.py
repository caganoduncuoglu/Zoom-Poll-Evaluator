from entities.Attendance import Attendance
from utils.Singleton import Singleton


class AttendanceCreator(metaclass=Singleton):

    def __init__(self):
        self.attendance = []

    def create_attendance(self, session, question, poll):
        attendance = Attendance(session, question, None, poll)
        self.attendance.append(attendance)
        return attendance
