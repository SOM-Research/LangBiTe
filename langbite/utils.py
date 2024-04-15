import re
import itertools

def clean_string(input: str):
    return re.sub('\n',' ',input.strip()).lower()

def lower_string_list(str_list: list[str]):
    return list(map(lambda e : e.lower(), str_list))

def merge_unique(list_of_lists: list[list[str]]):
    return list(set(itertools.chain.from_iterable(list_of_lists)))