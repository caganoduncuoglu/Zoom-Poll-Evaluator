from entities.Student import Student
from utils.Singleton import Singleton


class StudentCreator(metaclass=Singleton):

    def __init__(self):
        self.students = []

    def create_student(self, number, name, surname, description):
        student = Student(number, name, surname, description)
        self.students.append(student)
        return student

    def getstudent(self, searchstring: str):
        student = None
        curstudent: Student
        for curstudent in self.students:
            if curstudent.name + " " + curstudent.surname == searchstring:
                student = curstudent
                break
        return student
