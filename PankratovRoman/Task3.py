from csv import DictReader, DictWriter
from typing import Iterator


def get_top_performers(filepath: str, num_of_students: int = 5) -> Iterator[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        dict_reader = DictReader(f)

        sorted_students = sorted(
            dict_reader, key=lambda student_info: float(student_info.get("average mark", 0)), reverse=True
        )

    return (students_info.get("student name", "") for students_info in sorted_students[:num_of_students])


def write_sorted_students_by_age_to_file(input_filepath: str, output_filepath: str) -> None:
    with open(input_filepath, "r", encoding="utf-8") as f_to_read:
        dict_reader = DictReader(f_to_read)
        sorted_students = sorted(dict_reader, key=lambda student_info: float(student_info.get("age", 0)), reverse=True)

    with open(output_filepath, "w", encoding="utf-8") as f_to_write:
        dict_writer = DictWriter(f_to_write, tuple(sorted_students[0].keys()))
        dict_writer.writeheader()
        dict_writer.writerows(sorted_students)


if __name__ == "__main__":
    print(tuple(get_top_performers("../data/students.csv")))
    write_sorted_students_by_age_to_file("../data/students.csv", "../data/sorted_students.csv")
