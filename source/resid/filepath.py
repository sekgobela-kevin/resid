import os
import mimetypes


if not mimetypes.inited:
    mimetypes.init()

def guess_content_type(file_path: str):
    return mimetypes.guess_type(file_path, False)[0]

def guess_encoding(file_path: str):
    return mimetypes.guess_type(file_path, False)[1]

def guess_extension(content_type):
    return mimetypes.guess_extension(content_type, False)

def guess_extensions(content_type):
    return mimetypes.guess_all_extensions(content_type, False)

def content_type_same(file_path, other_file_path: str):
    # Returns True if files paths have same content type
    file_path_type = guess_content_type(file_path)
    other_file_path_type = guess_content_type(other_file_path)
    if file_path_type and other_file_path_type:
        return file_path_type == other_file_path_type
    else:
        return False

def split(file_path: str):
    return file_path.split(os.sep)

def extract_extension(file_path: str):
    return os.path.splitext(file_path)[1]

def extract_filename(file_path: str):
    return os.path.split(file_path)[1]

def remove_extension(filename: str):
    return os.path.splitext(filename)[0]

def file_exists(file_path: str):
    return os.path.isfile(file_path)

# def is_file_path(_source):
#     if isinstance(_source, (str, bytes)) and _source:
#         if _source.endswith("/") or _source.endswith("\\"):
#             return False
#         elif "/" in _source and "\\" in _source:
#             return False
#         elif weburl.is_web_url(_source):
#             return False
#         else:
#             # Setup path separator for path
#             if _source.endswith("/"):
#                 path_sep = "/"
#             elif _source.endswith("\\"):
#                 path_sep = "\\"
#             else:
#                 path_sep = None
            
#             # Split source by the path seperator
#             source_split = _source.split(path_sep)
#             source_split.sort(key=lambda elem: len(elem))

#             # checks if largest dir is less than MAX_DIRNAME_LENGTH.
#             return len(source_split[-1]) < MAX_DIRNAME_LENGTH
#     else:
#         return False


def is_file(_source, strict=True):
    if isinstance(_source, (str, bytes)):
        if strict:
            return file_exists(_source)
        else:
            if file_exists(_source):
                return True
            else:
                try:
                    with open(_source, 'w'):
                        pass
                except OSError:
                    return False
                else:
                    os.unlink(_source)
                    return True
    else:
        return False

def is_file_recursive(_source, strict=True):
    if isinstance(_source, (str, bytes)):
        path_names = filter(None, split(os.sep))
        return all([is_file(path_name, strict) for path_name in path_names])
    else:
        return False
    
def is_pdf_file(file_path: str):
    return content_type_same(file_path, " .pdf")

def is_docx_file(file_path: str):
    return content_type_same(file_path, " .docx")

def is_doc_file(file_path: str):
    return content_type_same(file_path, " .doc")

def is_word_file(file_path: str):
    return is_docx_file(file_path) or is_doc_file(file_path)

def is_pptx_file(file_path: str):
    return content_type_same(file_path, " .pptx")

def is_ppt_file(file_path: str):
    return content_type_same(file_path, " .ppt")

def is_html_file(file_path: str):
    if content_type_same(file_path, " .html"):
        return True
    elif content_type_same(file_path, " .htm"):
        return True
    else:
        return False

def is_json_file(file_path: str):
    return content_type_same(file_path, " .json")

def is_csv_file(file_path: str):
    return content_type_same(file_path, " .csv")

def is_plain_text_file(file_path: str):
    return content_type_same(file_path, " .txt")

def is_text_file(file_path: str):
    content_type = guess_content_type(file_path)
    if content_type:
        return "text/" in content_type
    else:
        return False


if __name__ == "__main__":
    path = "/projects/resid.com"
    print(is_file_recursive(path, False))
    print(is_file_recursive("/name/file.htm", False))
