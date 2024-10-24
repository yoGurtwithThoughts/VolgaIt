import pandas as pd
import spacy
import os

def load_addresses(data_dir):
    """Загрузка адресов из CSV файла."""
    addresses_file = os.path.join(data_dir, "volgait2024-semifinal-addresses.csv")
    try:
        return pd.read_csv(addresses_file, sep=";", encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{addresses_file}' не найден.")
    except pd.errors.ParserError as e:
        raise ValueError(f"Ошибка при парсинге файла: {e}")

def recognize_addresses(comment, addresses_df):
    """Распознавание адресов в комментарии с использованием spaCy."""
    try:
        nlp = spacy.load("ru_core_news_sm")
    except OSError:
        raise RuntimeError("Модель 'ru_core_news_sm' не найдена. Установите её с помощью 'python -m spacy download ru_core_news_sm'.")

    doc = nlp(comment)
    recognized_uuids = []

    # Итерация по распознанным сущностям в комментарии
    for ent in doc.ents:
        if ent.label_ == "ADDRESS":  # Убедитесь, что у вас есть модель с меткой "ADDRESS"
            address = ent.text.strip()
            # Используйте метод `str.contains` с учетом отсутствия символов в конце
            match = addresses_df[addresses_df['house_full_address'].str.contains(re.escape(address), case=False)]
            if not match.empty:
                recognized_uuids.extend(match['house_uuid'].values)

    return recognized_uuids