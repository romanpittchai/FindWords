import re
from typing import List


def find_words_re(pattern, text) -> List[str]:
    """
    Ищет все совпадения с регулярным выражением в тексте.

    Аргументы:
    pattern (str): Регулярное выражение для поиска.
    text (str): Текст, в котором нужно искать совпадения.

    Возвращает:
    List[str]: Список строк, соответствующих регулярному выражению.

    ************************************************

    Searches for all matches with the regular expression in the text.

    Arguments:
    pattern (str): A regular expression for the search.
    text (str): The text in which to look for matches.

    Returns:
    List[str]: A list of strings matching the regular expression.
    """

    return re.findall(pattern, text)






