import json
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Palindrome:
    """
    Класс для представления палиндромов.

    Атрибуты:
    word : str
        Строка, содержащая слово.
    meaning : str
        Строка, описывающая значение слова.
    """
    word: str
    meaning: str

    def __bool__(self) -> bool:
        """
        Проверяет, является ли word палиндромом.

        Возвращаемое значение:
        bool
            True, если слово является палиндромом; иначе False.
        """
        return self.word.lower() == self.word[::-1].lower()

    @classmethod
    def from_json(cls, filename: str) -> List['Palindrome']:
        """
        Читает данные из JSON и создает список объектов Palindrome.

        Параметры:
        filename : str
            Имя файла JSON.

        Возвращаемое значение:
        List[Palindrome]
            Список объектов Palindrome.
        """
        with open(filename, 'r', encoding='utf-8') as file:
            data: List[Dict[str, str]] = json.load(file)
            return [cls(entry['слово'], entry['значение']) for entry in data]


def main() -> None:
    """
    Создает список объектов Palindrome с использованием классового метода.
    Проходит в цикле по всем объектам, проверяя их на палиндромность.
    Подсчитывает количество палиндромов и не-палиндромов.
    Выводит число палиндромов и не-палиндромов.
    """
    palindromes: List[Palindrome] = Palindrome.from_json('palindromes.json')
    palindrome_count: int = 0
    non_palindrome_count: int = 0

    for palindrome in palindromes:
        if palindrome:
            palindrome_count += 1
        else:
            non_palindrome_count += 1

    print(f'Количество палиндромов: {palindrome_count}')
    print(f'Количество не-палиндромов: {non_palindrome_count}')


if __name__ == "__main__":
    main()
