class Student:

    def __init__(self, number, name, surname, description, submissions=None):
        if submissions is None:
            submissions = []
        self.number = number
        self.email = ""
        self.name = name
        self.surname = surname
        self.description = description
        self.submissions = submissions
        self.attendances = []

    def __str__(self):
        return self.number + ": " + self.name + " " + self.surname
