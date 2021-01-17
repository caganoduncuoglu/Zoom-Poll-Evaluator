import itertools
from fuzzywuzzy import process

from creators.StudentCreator import StudentCreator
from entities.Student import Student
from utils.Singleton import Singleton


class NameComparator(metaclass=Singleton):
    # TODO: Try to think more edge cases for finding students.

    def fuzzy_find(self, username: str, all_students):
        lower_map = {
            ord(u'I'): u'ı',
            ord(u'İ'): u'i',
        }
        username = self.filter_non_alpha_chars(username)
        allmatches = process.extractBests(username, [(s.name + " " + s.surname) for s in all_students])
        bestmatch = allmatches[0]
        if bestmatch[1] < 87:
            for secondbestmatch in allmatches:
                if secondbestmatch[0].split(' ')[-1].translate(lower_map).lower() == username.split(' ')[-1].translate(lower_map).lower():
                    bestmatch = secondbestmatch
                    break

        student: Student
        if "Ahmet Menguc" == username:
            student = StudentCreator().getstudent("AHMET TAYYİB MENGÜÇ")
        elif "hamiorak" in username:
            student = StudentCreator().getstudent("AHMED HAMİ ORAK")
        else:
            student = StudentCreator().getstudent(bestmatch[0])
        return student


    def filter_non_alpha_chars(self, username: str):
        res = ''.join([i for i in username if i.isalpha() or i.isspace()]).split(' ')
        res = list(filter(None, res))
        fixed_user_name = " ".join(res)
        return fixed_user_name  # Return with removal fo last whitespace.
