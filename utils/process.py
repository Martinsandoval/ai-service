import markdown2
from bs4 import BeautifulSoup
import re
import os

language_extensions = {
    'python': 'py',
    'javascript': 'js',
    'java': 'java',
}


def write_code_from_response(response, directory, filename):
    code_blocks = extract_code_from_response(response)

    if code_blocks.__len__() > 0:
        language = code_blocks[0][0]
        code = code_blocks[0][1]

        if code is not None:
            extension = ".txt"
            for lang, ext in language_extensions.items():
                if lang == language:
                    extension = '.' + ext
                    break

            filename += extension
            result = create_and_write_code_file(directory, filename, code)
            return result
    else:
        return 0


def create_and_write_code_file(directory, filename, code):
    file_path = os.path.join(directory, filename)

    try:
        with open(file_path, 'w') as file:
            file.write(code)
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 0


def extract_code_from_response(response):
    regex_pattern = r'```(' + '|'.join(f'{language}' for language, ext in language_extensions.items()) + r')(.*?)```'
    code_blocks = re.findall(regex_pattern, response, re.DOTALL)

    return code_blocks
