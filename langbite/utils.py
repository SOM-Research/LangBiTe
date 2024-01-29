import re

def clean_string(input: str):
    return re.sub('\n',' ',input.strip()).lower()