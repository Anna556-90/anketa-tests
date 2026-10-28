from registry import Registry

INPUT_FILE = "ankety.txt"

def print_table(reg):
    print(f"{'№':<4}{'ФИО':<32}{'Роль':<16}{'Группа/кафедра':<18}{'Телефон':<20}")
    print("-" * 90)

    for i, p in enumerate(reg.sorted_people(), 1):
        print(f"{i:<4}{p.fio:<32}{p.role():<16}{p.extra():<18}{p.masked_phone():<20}")

def print_errors(reg):
    print("Отклонено строк:", len(reg.errors))
    for num, line, reason in reg.errors:
        print("строка", str(num) + ":", reason)
        print(" " + line)

def print_statistics(reg):
    print()
    print("Принято:", len(reg), "| Отклонено:", len(reg.errors))

    roles = reg.stats_by_role()
    print("По ролям:", ", ".join(f"{r} {n}" for r, n in sorted(roles.items())))

    groups = reg.stats_by_group()
    print("По группам:", " ".join(sorted(groups.keys())))

def main():
    reg = Registry()

    if not reg.load(INPUT_FILE):
        print(f"Файл {INPUT_FILE} не найден. Положите его рядом с main.py и запустите снова.")
        return

    print("ПРИНЯТЫЕ АНКЕТЫ")
    print_table(reg)
    print()
    print_errors(reg)
    print_statistics(reg)

    reg.save_ok("ok.txt")
    reg.save_errors("errors.txt")

    print()
    print("Сохранено: ok.txt и errors.txt")

if __name__ == "__main__":
    main()