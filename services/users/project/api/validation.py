import re


def validate_phone_numbers(value):
    phone_number_pattern = r"\(?\d{3}\)?-?.?\s?\d{3}\s?-?\s?.?\s?\d{4}"
    compile_numbers = re.compile(phone_number_pattern)
    find_numbers = compile_numbers.findall(value)

    numbers_list = list(find_numbers)

    clean_list = []
    for obj in numbers_list:
        clean_list.append(re.sub(r"\(?\)?\.?-?", "", obj))

    formatted_list = []
    for obj in clean_list:
        try:
            int(obj)
            area_code = obj[0:3]
            line_prefix = obj[3:6]
            line_number = obj[6:10]

            formatted_list.append(f"({area_code}) {line_prefix}-{line_number}")

        except ValueError:
            continue

    return formatted_list
