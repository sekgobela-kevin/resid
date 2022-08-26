from . import urlmod
from . import exceptions

import socket


WEB_URL_SCHEMES = {"http", "https", "ftp"}
LOCAL_HOST_NAMES = {"localhost", "127.0.0.1"}



def is_web_url(_source):
    # Checks if source is url for web resource
    if isinstance(_source, str):
        return urlmod.is_url(_source, WEB_URL_SCHEMES)
    else:
        return False

def resembles_web_url(_source):
    return is_web_url(_source)

def _get_local_adress():
    # Gets ip adress of local machine
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def _get_local_ip_adresses():
    # Gets ip adresses of local machine.
    # Functions is not reliable and shouldnt be depended.
    # source: https://stackoverflow.com/questions/270745/
    addreses = set()
    for info in socket.getaddrinfo(socket.gethostname(), None):
        addreses.add(info[4][0])
    return addreses

def is_local_ip_address(_url):
    # Checks if url is built on local ip address
    hostname = urlmod.extract_hostname(_url) 
    return hostname in _get_local_ip_adresses()

def is_local_host(_url):
    # Checks if url is served in localhost
    hostname = urlmod.extract_hostname(_url)
    return hostname in LOCAL_HOST_NAMES

def is_remote_host(_url):
    # Checks if url served in remote host
    return not is_local_host(_url)

def is_local(_url):
    # Checks if url is served in local machine.
    # Functions is not reliable and shouldnt be depended.
    return is_local_host(_url) or is_local_ip_address(_url)

def is_remote(_url):
    # Checks if url is served in remote machine.
    # Functions is not reliable and shouldnt be depended.
    return is_remote_host(_url)


if __name__ == "__main__":
    base_url = "https://parsy.readthedocs.io/en/latest/"
    print(is_web_url(base_url))
    print(is_local_ip_address("http://172.18.128.1/"))
