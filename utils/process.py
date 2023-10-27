import markdown2
from bs4 import BeautifulSoup
import re
import os

def write_code_from_response(response, directory, filename):
    code_blocks = re.findall(r'```(python|javascript|java)(.*?)```', response, re.DOTALL)

    if code_blocks.__len__() > 0:
        language = code_blocks[0][0]
        code = code_blocks[0][1]

        if code is not None:
            extension = ".txt"
            match language:
                case "python":
                    extension = ".py"
                case "java":
                    extension = ".java"
                case "javascript":
                    extension = ".js"

            filename += extension
            create_and_write_code_file(directory, filename, code)
        return 1

    else:
        return 0


def create_and_write_code_file(directory, filename, code):
    file_path = os.path.join(directory, filename)

    try:
        with open(file_path, 'w') as file:
            file.write(code)

    except Exception as e:
        print(f"Error: {e}")
