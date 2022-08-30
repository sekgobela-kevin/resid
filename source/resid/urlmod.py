from . import exceptions

from urllib import parse


def urlparse(url):
    return parse.urlparse(url)

def urlparse_dict(url):
    return urlparse(url)._asdict()

def url_unparse(url):
    return parse.urlparse(url)._asdict()

def urljoin(base_url, url):
    return parse.urljoin(base_url, url)

def quote(url, *args, **kwargs):
    return parse.quote(url, *args, **kwargs)

def unquote(url, *args, **kwargs):
    return parse.unquote(url, *args, **kwargs)

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
    # Extracts scheme of url
    return parse.urlparse(url).scheme

def extract_params(url: str):
    # Extracts parameter passed to url
    return parse.urlparse(url).params

def extract_query(url: str):
    return parse.urlparse(url).query

def extract_port(url: str):
    port = parse.urlparse(url).port
    if port == None:
        return ""
    else:
        return str(port)

def extract_fragment(url: str):
    return parse.urlparse(url).fragment

def is_url(_source, schemes=None):
    # Checks if source is url for web resource
    if isinstance(_source, (str, bytes)):
        scheme = extract_scheme(_source)
        netloc = extract_netloc(_source)
        path = extract_path(_source)
        any_items = (netloc, path)
        if schemes != None:
            return scheme in schemes and any(any_items)
        else:
            return bool((scheme)) and any(any_items)
    else:
        return False

def resembles_scheme(_url, scheme):
    # Checks if url resembles containing scheme
    # It does not mean that scheme is real scheme of url.
    if "//" in _url[:20] and not _url.startswith("//"):
        if scheme != None:
            return _url.startswith(scheme)
        else:
            return True
    return False

def resembles_hostname(_url, hostname):
    # Checks if url resembles containing hostname
    url_hostname = extract_hostname(_url)
    if hostname != None:
        return url_hostname == hostname
    else:
        return bool(url_hostname)

def resembles_schemes(_url, schemes):
    # Checks if url resembles containing schemes
    for scheme in schemes:
        if resembles_scheme(_url, scheme):
            return True
    return False

def resembles_url(_source, schemes=None):
    # Checks if source resembles url
    # 1. source should 2 of any of url parts excluding path and hostname.
    # 2. Or source should have scheme(or resemble) and path.
    # 2. Or source should have atleast hostname.
    if isinstance(_source, (str, bytes)):
        if schemes != None:
            # URL needs to have atleast one of provided schemes
            scheme_satisfied = resembles_schemes(_source, schemes)
        else:
            # Dont care if url has scheme if schemes not provided
            scheme_satisfied = True

        if scheme_satisfied and resembles_hostname(_source, None):
            # Hostname is enough to satify url
            return True
        elif scheme_satisfied and extract_path(_source):
            # scheme and path satisfies url
            return True
        else:
            # source satifying scheme and atleast another part of url
            # can be considered resmbling url.
            any_items = [
                extract_query(_source),
                extract_params(_source),
                extract_port(_source),
                extract_fragment(_source)
            ]
            any_items_filtered = list(filter(None, any_items))
            return scheme_satisfied and len(any_items_filtered) >= 2
    return False


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
    
    # URL is complete and should have everything
    elif is_url(url):
        return url
    else:
        raise exceptions.InvalidURLError(url + " is not a valid url")


if __name__ == "__main__":
    base_url = "parsy.readthedocs.io/en/latest?name#10/name"
    relative_url = "tutorial.html"
    print(resembles_url(base_url, None))
    print(make_url_absolute(base_url, base_url))