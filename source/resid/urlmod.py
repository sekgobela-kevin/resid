from . import exceptions

from urllib import parse


def urlparse(url):
    return parse.urlparse(url)

def urlparse_dict(url):
    return urlparse(url)._asdict()

def url_unparse(url):
    return parse.urlparse(url)._asdict()

def urljoin(parse_result):
    return parse.urljoin(parse_result)


def extract_path(url: str):
    # Extracts path part of url
    return parse.urlparse(url).path

def extract_hostname(url: str):
    # Extracts hostname part of url
    return parse.urlparse(url).hostname

def extract_netloc(url: str):
    # Extracts netloc part of url
    return parse.urlparse(url).netloc

def extract_scheme(url: str):
    # Extracts path part of url
    return parse.urlparse(url).scheme


def is_url(_source, schemes=None):
    # Checks if source is url for web resource
    if isinstance(_source, (str, bytes)):
        scheme = extract_scheme(_source)
        netloc = extract_netloc(_source)
        path = extract_path(_source)
        if schemes != None:
            return scheme in schemes and any((netloc, path))
        else:
            return bool((scheme)) and any((netloc, path))
    else:
        return False

def resembles_url(_source, schemes=None):
    return is_url(_source, schemes)


def make_url_absolute(url:str, base_url:str):
    # Makes url absolute by adding missing parts from base_url
    # inspired by: requests-html requests_html.BaseParse._make_absolute()

    # Parse url componets into dictionary
    parsed = urlparse(url)._asdict()

    # url almost complete but missing scheme
    if url.startswith("//"):
        parsed['scheme'] = urlparse(base_url).scheme

        # Recreates url with new scheme
        parsed = [value for value in parsed.values()]
        return url_unparse(parsed)

    # Link is absolute; its just missing scheme and netloc
    elif url.startswith("/"):
        parsed['scheme'] = urlparse(base_url).scheme
        parsed['netloc'] = urlparse(base_url).netloc

        # Recreates url with new scheme and netloc
        parsed = [value for value in parsed.values()]
        return url_unparse(parsed)

    # The link is relative to current url
    elif not parsed['netloc']:
        # parse.urljoin() is intelligent than os.path.join()
        return urljoin(base_url, url)
    
    # Url is complete and should have everything
    elif is_url(url):
        return url
    else:
        raise exceptions.InvalidUrlError(url + " is not a valid url")


if __name__ == "__main__":
    base_url = "https://parsy.readthedocs.io/en/latest/"
    relative_url = "tutorial.html"
    print(extract_path(base_url))
    print(make_url_absolute(base_url, base_url))