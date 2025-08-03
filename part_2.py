from dataclasses import dataclass, field
from typing import List, Optional, Set


@dataclass
class Teacher:
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: Set[str]
    assigned_subjects: Set[str] = field(default_factory=set)


def create_schedule(
    subjects: Set[str], teachers: List[Teacher]
) -> Optional[List[Teacher]]:
    uncovered = set(subjects)
    remaining = teachers.copy()
    schedule: List[Teacher] = []

    while uncovered:
        best_teacher = None
        best_cover: Set[str] = set()

        for t in remaining:
            covers = t.can_teach_subjects & uncovered
            if not covers:
                continue
            if (len(covers) > len(best_cover)
                or (len(covers) == len(best_cover)
                    and best_teacher is not None
                    and t.age < best_teacher.age)):
                best_teacher, best_cover = t, covers

        if best_teacher is None:
            return None

        best_teacher.assigned_subjects = best_cover
        schedule.append(best_teacher)
        uncovered -= best_cover
        remaining.remove(best_teacher)

    return schedule


if __name__ == "__main__":
    # Множина предметів
    subjects = {"Математика", "Фізика", "Хімія", "Інформатика", "Біологія"}

    # Створення списку викладачів
    teachers = [
        Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com",
                {"Математика", "Фізика"}),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com",
                {"Хімія"}),
        Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com",
                {"Інформатика", "Математика"}),
        Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com",
                {"Біологія", "Хімія"}),
        Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com",
                {"Фізика", "Інформатика"}),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com",
                {"Біологія"}),
    ]

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule:
        print("\nРозклад занять:\n")
        for t in schedule:
            subj = ", ".join(sorted(t.assigned_subjects))
            print(f"- {t.first_name} {t.last_name}, {t.age} років, {t.email}")
            print(f"\tВикладає: {subj}\n")
    else:
        print("Неможливо покрити всі предмети наявними викладачами.")
