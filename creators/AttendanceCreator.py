from entities.Attendance import Attendance
from utils.Singleton import Singleton


class AttendanceCreator(metaclass=Singleton):

    def __init__(self):
        self.attendances = []

    def create_attendance(self, session, base_time, is_poll_question=False):
        # TODO: There should be a check about returning same attendance if base time and session variables are equal.
        exist_attendance = None
        for attendance in self.attendances:
            if attendance.session == session and attendance.base_time == base_time:
                exist_attendance = attendance

        if exist_attendance is None:
            attendance = Attendance(session, base_time, is_poll_question)
            self.attendances.append(attendance)
            return attendance
        else:
            return exist_attendance
