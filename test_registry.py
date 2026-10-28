import pytest
from registry import Registry, parse_line
from people import Student, Teacher


# Фикстура для создания временного журнала
@pytest.fixture
def reg(tmp_path):
    # Создаем временный файл
    put = tmp_path / "anketa.txt"
    # 3 верные строки и 3 бракованные
    text = (
        "s;Иванов Иван;ivanov@mail.ru;79211112233;09c33\n"  # 1 (ok)
        "t;Петров Петр;petrov@mail.ru;79212223344;Кафедра ИС\n"  # 2 (ok)
        "s;Сидоров Сидор;sidorov@mail.ru;79213334455;09c34\n"  # 3 (ok)
        "s;Ошибка;bad_mail;7921;09c33\n"  # 4 (ошибка)
        "x;Неизвестный;unknown@mail.ru;79211112233;group\n"  # 5 (ошибка)
        "s;Без группы;bez@mail.ru;79211112233;\n"  # 6 (ошибка)
    )
    put.write_text(text, encoding="utf-8")

    r = Registry()
    r.load(str(put))
    return r


# Тесты

def test_empty_registry():
    r = Registry()
    assert len(r) == 0


def test_load_count(reg):
    assert len(reg) == 3


def test_errors_count(reg):
    assert len(reg.errors) == 3


def test_errors_line_numbers(reg):
    # Проверяем, что ошибки записались с правильными номерами строк (4, 5, 6)
    assert reg.errors[0][0] == 4
    assert reg.errors[1][0] == 5
    assert reg.errors[2][0] == 6


def test_load_nonexistent():
    r = Registry()
    assert r.load("nonexistent_file.txt") is False


def test_stats_by_role(reg):
    stats = reg.stats_by_role()
    assert stats["студент"] == 2
    assert stats["преподаватель"] == 1


def test_stats_by_group(reg):
    stats = reg.stats_by_group()
    assert stats["09c33"] == 1
    assert stats["09c34"] == 1
    assert len(stats) == 2  # только студенты


def test_iteration(reg):
    # Проверка, что журнал можно перебрать
    count = 0
    for person in reg.people:
        count += 1
    assert count == 3


def test_sort_yo():
    # Этот тест найдет 3-ю ошибку (Ёлкин впереди Абрамова)
    r = Registry()
    p1 = Student("Ёлкин Иван", "yo@mail.ru", "79211112233", "09c33")
    p2 = Student("Абрамов Петр", "ab@mail.ru", "79211112233", "09c33")
    p3 = Student("Яковлев Семен", "ya@mail.ru", "79211112233", "09c33")
    r.add(p1)
    r.add(p2)
    r.add(p3)

    familii = [p.fio.split()[0] for p in r.sorted_people()]
    # Ожидаем правильный алфавитный порядок
    assert familii == ["Абрамов", "Ёлкин", "Яковлев"]


def test_save_ok(reg, tmp_path):
    out = tmp_path / "ok.txt"
    reg.save_ok(str(out))
    lines = out.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 3


def test_save_errors(reg, tmp_path):
    out = tmp_path / "errors.txt"
    reg.save_errors(str(out))
    text = out.read_text(encoding="utf-8")
    assert "строка 4" in text
    assert "строка 5" in text
    assert "строка 6" in text