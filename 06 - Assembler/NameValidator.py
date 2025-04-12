def is_valid_name(s):
    allowed_symbols = {'_', '$', ':', '.'}
    return all(char.isalnum() or char in allowed_symbols for char in s)
