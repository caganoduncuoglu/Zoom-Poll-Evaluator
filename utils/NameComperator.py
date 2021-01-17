import itertools

from utils.Singleton import Singleton


class NameComparator(metaclass=Singleton):
    # TODO: Try to think more edge cases for finding students.

    # FIXME: Possible logical errors may occur because of first time of use without testing.
    def consider_multiple_names_and_surnames(self, username: str, name: str, surname: str):
        username_tokens = self.filter_non_alpha_chars(username).lower().split(" ")
        name_tokens = name.lower().split(" ")
        surname_tokens = surname.lower().split(" ")

        fullname_tokens = name_tokens + surname_tokens

        subset_found = False
        for l in range(2, len(username_tokens) + 1):
            for subset_username in itertools.combinations(username_tokens, l):
                for lf in range(2, len(fullname_tokens) + 1):
                    for subset_fullname in itertools.combinations(fullname_tokens, lf):
                        if subset_username == subset_fullname:
                            subset_found = True
                            break
                    if subset_found:
                        break
                if subset_found:
                    break
            if subset_found:
                break

        return subset_found

    def filter_non_alpha_chars(self, username: str):
        res = ''.join([i for i in username if i.isalpha() or i.isspace()]).split(' ')
        res = list(filter(None, res))
        fixed_user_name = " ".join(res)
        return fixed_user_name  # Return with removal fo last whitespace.
