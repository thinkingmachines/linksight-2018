def create_search_tuple(row, columns):
    locations = row[list(columns.values())].dropna().str.lower()
    locations = locations.str.replace(r'NOT A PROVINCE|CAPITAL|\(|\)|CITY OF|CITY', '', case=False)
    locations = locations.str.replace('ñ', 'n', case=False)
    locations = locations.str.replace(r'BARANGAY|BGY', 'bgy', case=False)
    locations = locations.str.replace('POBLACION', 'pob', case=False)
    locations = locations.str.replace(r'[^A-Z0-9\s]', '', case=False).str.strip()
    values = locations.values.tolist()
    lowest_interlevel = None
    # Check lowest interlevel with values to determine lowest interlevel
    for lowest_interlevel in 'bgy', 'municity', 'prov':
        col = columns.get(lowest_interlevel)
        if col and row.dropna().get(col):
            break
    return tuple(values + [lowest_interlevel])


def to_index(t):
    # FIXME: Improve this
    return ','.join(t)
