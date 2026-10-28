import pytest
from people import Person, Student, Teacher, AnketaError

# Тесты для ФИО

@pytest.mark.parametrize("raw, expected", [
    ("иванов иван", "Иванов Иван"),
    (" петров пётр ", "Петров Пётр"),
    ("СИДОРОВА АННА", "Сидорова Анна"),
    ("петров-водкин кузьма", "Петров-Водкин Кузьма"), # Этот тест найдет 1-ю ошибку!
])
def test_check_fio(raw, expected):
    assert Person.check_fio(raw) == expected

def test_check_fio_one_word():
    with pytest.raises(AnketaError):
        Person.check_fio("Иванов")

# Тесты для Почты

@pytest.mark.parametrize("raw, expected", [
    ("IVANOV@MAIL.RU", "ivanov@mail.ru"),
    (" Petrov@Yandex.Ru ", "petrov@yandex.ru"),
])
def test_check_mail_lower(raw, expected):
    assert Person.check_mail(raw) == expected

@pytest.mark.parametrize("bad_mail", [
    "mail.ru",           # нет собаки
    "ivanov@mail",       # нет точки в домене
    "@mail.ru",          # пустая левая часть
    "ivanov@.ru",        # точка в начале домена
    "iv anov@mail.ru",   # пробел внутри (найдет 2-ю ошибку!)
])
def test_check_mail_bad(bad_mail):
    with pytest.raises(AnketaError):
        Person.check_mail(bad_mail)

# Тесты для Телефона

@pytest.mark.parametrize("phone", [
    "89211112233",
    "+7 (921) 111-22-33",
    "8 921 111 22 33",
    "7-921-111-22-33"
])
def test_check_phone_formats(phone):
    assert Person.check_phone(phone) == "79211112233"

@pytest.mark.parametrize("bad_phone", [
    "12345",             # мало цифр
    "8921111223344",     # много цифр
    "99211112233",       # начинается не с 7 или 8
])
def test_check_phone_bad(bad_phone):
    with pytest.raises(AnketaError):
        Person.check_phone(bad_phone)

# Тесты для методов Person

def test_masked_phone():
    p = Person("Иванов Иван", "ivanov@mail.ru", "89211112233")
    assert p.masked_phone() == "+7 (921) ***-**-33"

def test_short_fio():
    p = Person("Иванов Иван Петрович", "ivanov@mail.ru", "89211112233")
    assert p.short_fio() == "Иванов И. П."

def test_roles():
    s = Student("Иванов Иван", "s@mail.ru", "89211112233", "09c33")
    t = Teacher("Петров Петр", "t@mail.ru", "89211112233", "Кафедра ИС")
    assert s.role() == "студент"
    assert t.role() == "преподаватель"

def test_student_empty_group():
    with pytest.raises(AnketaError):
        Student("Иванов Иван", "s@mail.ru", "89211112233", "   ")

# --- Тесты для parse_line ---

def test_parse_line_student():
    line = "s;Иванов Иван;ivanov@mail.ru;89211112233;09c33"
    p = Person.check_fio # заглушка, чтобы не ругался линтер, но импортируем из registry
    from registry import parse_line
    res = parse_line(line)
    assert isinstance(res, Student)
    assert res.group_name() == "09c33"

def test_parse_line_teacher():
    line = "t;Петров Петр;petrov@mail.ru;89211112233;Кафедра ИС"
    from registry import parse_line
    res = parse_line(line)
    assert isinstance(res, Teacher)
    assert res.extra() == "Кафедра ИС"

@pytest.mark.parametrize("bad_line", [
    "x;Иванов Иван;ivanov@mail.ru;89211112233;09c33",  # неизвестный тип
    "s;Иванов Иван;ivanov@mail.ru;89211112233",        # мало полей
    "",                                                # пустая строка
])
def test_parse_line_bad(bad_line):
    from registry import parse_line
    with pytest.raises(AnketaError):
        parse_line(bad_line)