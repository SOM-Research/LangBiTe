import re

def clean_string(input: str):
    return re.sub('\n',' ',input.strip()).lower()

def lower_string_list(str_list: list[str]):
    return list(map(lambda e : e.lower(), str_list))