import re


def recognize_addresses(comment, addresses_df):
    """Распознавание адресов в комментарии с использованием регулярных выражений."""
    recognized_info = []
    addresses_list = addresses_df['house_full_address'].tolist()

    for address in addresses_list:
        if re.search(re.escape(address), comment, re.IGNORECASE):
            # Check if 'comment' column exists
            if 'comment' in addresses_df.columns:
                comment_for_address = addresses_df.loc[addresses_df['house_full_address'] == address, 'comment']
                if not comment_for_address.empty:
                    recognized_info.append((address, comment_for_address.values[0]))
                else:
                    recognized_info.append((address, "Комментарий отсутствует"))
            else:
                recognized_info.append((address, "Комментарий не найден в данных"))

    return recognized_info