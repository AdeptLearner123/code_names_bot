def split_by_column(dict):
    dict1 = { key: col1 for key, (col1, _) in dict.items() }
    dict2 = { key: col2 for key, (_, col2) in dict.items() }
    return dict1, dict2


def merge(*col_dicts):
    _, dict0 = col_dicts[0]
    keys = dict0.keys()
    return { key: { col: dict[key] for col, dict in col_dicts } for key in keys }
