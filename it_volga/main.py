import os
import logging
import pandas as pd
import re
import flet as ft

logging.basicConfig(level=logging.INFO)

def create_task_file(data_dir):
    """Создание директории данных, если она не существует."""
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def load_addresses(data_dir):
    """Загрузка адресов из CSV файла."""
    addresses_file = os.path.join(data_dir, "volgait2024-semifinal-addresses.csv")
    try:
        addresses_df = pd.read_csv(addresses_file, sep=";", encoding="utf-8", on_bad_lines='skip')
        logging.info(f"Файл загружен. Количество записей: {len(addresses_df)}")
        return addresses_df
    except FileNotFoundError:
        logging.error(f"Файл '{addresses_file}' не найден.")
        raise
    except pd.errors.ParserError as e:
        logging.error(f"Ошибка при парсинге файла: {e}")
        raise

def recognize_addresses(comment, addresses_df):
    """Распознавание адресов в комментарии с использованием регулярных выражений."""
    recognized_info = []
    addresses_list = addresses_df['house_full_address'].tolist()

    for address in addresses_list:
        if re.search(re.escape(address), comment, re.IGNORECASE):
            comment_for_address = addresses_df.loc[addresses_df['house_full_address'] == address, 'comment']
            if not comment_for_address.empty:
                recognized_info.append((address, comment_for_address.values[0]))
            else:
                recognized_info.append((address, "Комментарий отсутствует"))

    return recognized_info

def main_page(page: ft.Page):
    page.title = "Проверка адресов"

    # Получение пути к директории данных
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    create_task_file(data_dir)

    # Загрузка адресов
    try:
        addresses_df = load_addresses(data_dir)
        logging.info(f"Загружено {len(addresses_df)} адресов.")
    except (FileNotFoundError, ValueError) as e:
        page.add(ft.Text(str(e)))
        return

    address_input = ft.TextField(label="Введите адрес улицы", width=300)
    suggestions_list = ft.ListView(width=300, height=200, spacing=2, padding=10)
    result_text = ft.Text()

    page.add(
        address_input,
        suggestions_list,
        ft.ElevatedButton("Проверить адреса", on_click=lambda e: check_addresses()),
        result_text
    )

    def check_addresses():
        comment = address_input.value.strip()
        recognized_info = recognize_addresses(comment, addresses_df)

        if recognized_info:
            result_lines = [
                f"Адрес: {addr}, Комментарий: {comment}" for addr, comment in recognized_info
            ]
            result_text.value = "\n".join(result_lines)
        else:
            result_text.value = "Нет данных"

        page.update()

    def on_address_change(e):
        input_text = address_input.value.strip().lower()
        
        if input_text:
            suggestions = addresses_df[addresses_df['house_full_address'].str.contains(input_text, case=False, na=False)]
            suggestions_list.controls.clear()
            for suggestion in suggestions['house_full_address']:
                suggestions_list.controls.append(
                    ft.ListTile(title=ft.Text(suggestion), on_click=lambda e, s=suggestion: select_address(s))
                )
            suggestions_list.visible = len(suggestions) > 0
        else:
            suggestions_list.controls.clear()
            suggestions_list.visible = False

        page.update()

    def select_address(selected_address):
        address_input.value = selected_address 
        suggestions_list.controls.clear()
        suggestions_list.visible = False
        page.update()

    address_input.on_change = on_address_change

ft.app(target=main_page)