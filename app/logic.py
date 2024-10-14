import re

# Исходный текст
text = """

"""

# Регулярное выражение для поиска идентификаторов
pattern = r'TTN-\d{10}'

# Поиск всех идентификаторов
identifiers = re.findall(pattern, text)

# Запись в файл
with open('identifiers.txt', 'w') as f:
    for identifier in identifiers:
        #f.write(f"{identifier}\n")
        print(f"{identifier}")

