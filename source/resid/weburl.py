from . import urlmod


WEB_URL_SCHEMES = {"http", "https", "ftp"}
LOCAL_HOST_NAMES = {"localhost", "127.0.0.1"}


def is_web_url(_source):
    # Checks if source is url for web resource
    return urlmod.is_url(_source, WEB_URL_SCHEMES)

def is_local_host(_url):
    if is_web_url(_url):
        hostname = urlmod.extract_hostname(_url)
        return hostname in LOCAL_HOST_NAMES
    else:
        return False

def is_remote_host(_url):
    return is_web_url(_url) and not is_local_host(_url)

def is_local(_url):
    return is_local_host(_url)

def is_remote(_url):
    return is_remote_host(_url)

if __name__ == "__main__":
    base_url = "https://parsy.readthedocs.io/en/latest/"
    print(is_web_url(base_url, ["http"]))