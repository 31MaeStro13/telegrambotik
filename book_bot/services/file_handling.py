import logging
import os

logger = logging.getLogger(__name__)


def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    punctuation = '.,!:;?'

    # Если текст заканчивается раньше максимального размера
    if start + page_size >= len(text):
        return text[start:], len(text) - start

    # Ищем подходящее место для обрыва
    for end in range(start + page_size, start, -1):
        if text[end - 1] in punctuation:
            # Проверяем, не является ли это частью последовательности знаков
            # Смотрим вперед, чтобы захватить всю последовательность
            next_pos = end
            while next_pos < len(text) and text[next_pos] in punctuation:
                next_pos += 1

            # Если вся последовательность помещается в размер страницы
            if next_pos <= start + page_size:
                return text[start:next_pos], next_pos - start
            # Если не помещается - ищем дальше

    # Если не нашли подходящего знака (по условию не должно произойти)
    return text[start:start+page_size], page_size

# Функция, формирующая словарь книги
def prepare_book(path: str, page_size: int = 1050) -> dict[int, str]:
    """
    Читает файл книги и разбивает его на страницы заданного размера.

    Аргументы:
        path: путь к файлу с книгой
        page_size: количество символов на странице (по умолчанию 1050)

    Возвращает:
        Словарь {номер_страницы: текст_страницы}
    """

    # Читаем весь текст из файла
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()

    book = {}  # Результирующий словарь
    page_number = 1  # Номер текущей страницы
    current_pos = 0  # Текущая позиция в тексте

    # Пока не дошли до конца текста
    while current_pos < len(text):
        # Получаем страницу и её реальный размер
        page_text, page_len = _get_part_text(text, current_pos, page_size)

        # Удаляем лишние пробельные символы в начале страницы
        page_text = page_text.lstrip()

        # Добавляем страницу в словарь
        book[page_number] = page_text

        # Переходим к следующей странице
        current_pos += page_len
        page_number += 1

    return book
