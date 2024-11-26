import json
import os
from dataclasses import dataclass, field

data_file = 'db_library.json'  # Путь к файлу с данными книг


@dataclass
class Book:
    title: str
    author: str
    year: int
    id: int = field(default_factory=lambda: Book.generate_id())
    status: str = "в наличии"

    @staticmethod
    def generate_id() -> int:
        books = load_books()
        if books:
            return max(book.id for book in books) + 1
        return 1

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data: dict):
        return Book(**data)


def load_books() -> list[Book]:
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as file:
            return [Book.from_dict(book) for book in json.load(file)]
    return []


def save_books(books: list[Book]):
    with open(data_file, 'w', encoding='utf-8') as file:
        json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=4)


def add_book(title: str, author: str, year: int):
    books = load_books()
    book = Book(title, author, year)
    books.append(book)
    save_books(books)
    print(f"Книга '{title}' добавлена с ID {book.id}.")


def del_book(book_id: int):
    books = load_books()
    if any(book.id == book_id for book in books):
        books = [book for book in books if book.id != book_id]
        save_books(books)
        print(f"Книга с ID {book_id} удалена.")
    else:
        print(f"Книга с ID {book_id} не найдена.")


def search_books(query: str, field: str):
    books = load_books()
    results = []
    if field == "title":
        results = [book for book in books if query.lower() in book.title.lower()]
    elif field == "author":
        results = [book for book in books if query.lower() in book.author.lower()]
    elif field == "year":
        results = [book for book in books if book.year == int(query)]
    else:
        print("Неправильное поле для поиска. Используйте 'title', 'author' или 'year'.")
        return

    if results:
        for book in results:
            print(f'{book.id}. {book.title}, автор: {book.author}, {book.year}')
    else:
        print("Ничего не найдено по вашему запросу!")


def show_books():
    books = load_books()
    for book in books:
        print(f'{book.id}. {book.title}, автор: {book.author}, {book.year} - {book.status}')


def update_book_status(book_id: int, status: str):
    books = load_books()
    for book in books:
        if book.id == book_id:
            book.status = status
            save_books(books)
            print(f"Статус книги с ID {book_id} изменен на '{status}'.")
            return
    print(f"Книга с ID {book_id} не найдена.")


def main():
    while True:
        print("\nМеню управления библиотекой:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':  # Добавить
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            add_book(title, author, year)

        elif choice == '2':  # Удалить
            book_id = int(input("Введите ID книги для удаления: "))
            del_book(book_id)

        elif choice == '3':  # Найти
            field = input("Введите поле для поиска (title, author, year): ")
            query = input("Введите запрос: ")
            search_books(query, field)

        elif choice == '4':  # Показать все
            show_books()

        elif choice == '5':  # Изменить статус (в наличии, выдана)
            book_id = int(input("Введите ID книги: "))
            status = input("Введите новый статус (в наличии, выдана): ")
            update_book_status(book_id, status)

        elif choice == '6':  # Выход
            print("Выход из программы.")
            break

        else:
            print("Неправильный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()
