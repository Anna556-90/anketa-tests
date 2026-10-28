class AnketaError(Exception):
    """Анкета не прошла проверку."""
    pass


class Person:
    def __init__(self, fio, mail, phone):
        self.fio = self.check_fio(fio)
        self.mail = self.check_mail(mail)
        self.phone = self.check_phone(phone)

    @staticmethod
    def check_fio(raw):
        parts = raw.split()
        if len(parts) < 2:
            raise AnketaError("В ФИО меньше двух слов")
        # ИСПРАВЛЕНИЕ 1: title() делает заглавными буквы после дефиса
        # ("петров-водкин" -> "Петров-Водкин")
        return " ".join(parts).title()

    @staticmethod
    def check_mail(raw):
        mail = raw.strip().lower()
        good = True

        # ИСПРАВЛЕНИЕ 2: Проверяем, что внутри нет пробелов
        if " " in mail:
            good = False
        elif mail.count("@") != 1:
            good = False
        else:
            left, right = mail.split("@")
            if left == "" or right == "":
                good = False
            elif "." not in right:
                good = False
            elif right[0] == "." or right[-1] == ".":
                good = False

        if not good:
            raise AnketaError("почта неверная: " + raw.strip())
        return mail

    @staticmethod
    def check_phone(raw):
        digits = ""
        for ch in raw:
            if ch.isdigit():
                digits += ch
        if len(digits) != 11:
            raise AnketaError("В телефоне " + str(len(digits)) + " цифр, а надо 11")
        if digits[0] != "7" and digits[0] != "8":
            raise AnketaError("телефон должен начинаться с 7 или 8")
        return "7" + digits[1:]

    def masked_phone(self):
        return "+7 (" + self.phone[1:4] + ") ***-**-" + self.phone[-2:]

    def short_fio(self):
        parts = self.fio.split()
        result = parts[0]
        for word in parts[1:]:
            result += " " + word[0].upper() + "."
        return result

    def role(self):
        return "-"

    def extra(self):
        return "-"

    def group_name(self):
        return None

    def type_code(self):
        return "-"

    def __str__(self):
        return f"{self.fio} | {self.mail} | {self.masked_phone()}"

    def __lt__(self, other):
        # ИСПРАВЛЕНИЕ 3: Сортировка с учетом буквы Ё (заменяем ё на е при сравнении)
        fio_self = self.fio.replace("Ё", "Е").replace("ё", "е")
        fio_other = other.fio.replace("Ё", "Е").replace("ё", "е")
        return fio_self < fio_other


class Student(Person):
    def __init__(self, fio, mail, phone, group):
        super().__init__(fio, mail, phone)
        self.group = self.check_group(group)

    @staticmethod
    def check_group(raw):
        group = raw.strip().lower()
        if group == "":
            raise AnketaError("пустая группа")
        return group

    def role(self):
        return "студент"

    def extra(self):
        return self.group

    def group_name(self):
        return self.group

    def type_code(self):
        return "s"


class Teacher(Person):
    def __init__(self, fio, mail, phone, department):
        super().__init__(fio, mail, phone)
        self.department = self.check_department(department)

    @staticmethod
    def check_department(raw):
        department = raw.strip()
        if department == "":
            raise AnketaError("пустая кафедра")
        return department

    def role(self):
        return "преподаватель"

    def extra(self):
        return self.department

    def type_code(self):
        return "t"