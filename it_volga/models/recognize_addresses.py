def recognize_addresses(comment, addresses_df):
    recognized = []
    for index, row in addresses_df.iterrows():
        if row['house_full_address'] in comment:
            recognized.append({
                'house_uuid': row['house_uuid'],
                'house_full_address': row['house_full_address']
            })
    return recognized