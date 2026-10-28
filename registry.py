from people import AnketaError, Student, Teacher

def parse_line(line):
    fields = [f.strip() for f in line.strip().split(";")]

    if len(fields) != 5:
        raise AnketaError("ожидалось 5 полей, а в строке " + str(len(fields)))

    typ, fio, mail, phone, last = fields

    if typ == "s":
        return Student(fio, mail, phone, last)
    if typ == "t":
        return Teacher(fio, mail, phone, last)

    raise AnketaError("неизвестный тип: " + typ)

class Registry:
    def __init__(self):
        self.people = []
        self.errors = []

    def add(self, person):
        self.people.append(person)

    def load(self, filename):
        try:
            f = open(filename, "r", encoding="utf-8")
        except FileNotFoundError:
            return False

        with f:
            for num, line in enumerate(f, 1):
                line = line.rstrip("\n")
                if line.strip() == "":
                    continue

                try:
                    person = parse_line(line)
                except AnketaError as e:
                    self.errors.append((num, line, str(e)))
                else:
                    self.add(person)

        return True

    def sorted_people(self):
        return sorted(self.people)

    def stats_by_role(self):
        counts = {}
        for p in self.people:
            r = p.role()
            counts[r] = counts.get(r, 0) + 1
        return counts

    def stats_by_group(self):
        counts = {}
        for p in self.people:
            g = p.group_name()
            if g is not None:
                counts[g] = counts.get(g, 0) + 1
        return counts

    def save_ok(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            for p in self.sorted_people():
                f.write(";".join([
                    p.type_code(),
                    p.fio,
                    p.mail,
                    p.phone,
                    p.extra()
                ]) + "\n")

    def save_errors(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            for num, line, reason in self.errors:
                f.write("строка " + str(num) + " : " + reason + "\n")
                f.write(line + "\n\n")

    def __len__(self):
        return len(self.people)