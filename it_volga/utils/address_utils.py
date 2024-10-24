def get_suggestions(input_text, address_list):
    """Возвращает адреса, которые начинаются с введенного текста."""
    suggestions = [address for address in address_list if address.lower().startswith(input_text.lower())]
    return suggestions