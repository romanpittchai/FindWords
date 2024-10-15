import re



def find_words_re(pattern, text):
    identifiers = re.findall(pattern, text)
    print(identifiers)
    with open('identifiers.txt', 'w') as f:
        for identifier in identifiers:
        #f.write(f"{identifier}\n")
            print(f"{identifier}")






