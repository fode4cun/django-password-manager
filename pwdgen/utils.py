import re
import requests
from cryptography.fernet import Fernet
from environs import Env

env = Env()
env.parser_for('CRYPT_KEY')

CRYPT_KEY = Fernet(bytes(env('CRYPT_KEY'), 'utf-8'))


def get_icons(param: str) -> list:
    images = []
    extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    ]
    pattern = re.compile(r"<img\s[^>]*?data-src\s*=\s*['\"]([^'\"]*?)['\"][^>]*?>")

    resp = requests.get(f'https://www.flaticon.com/search?word={param}')

    if resp.status_code == 200:
        txt = resp.text
        image_urls = pattern.findall(txt)

        for url in image_urls:
            if url.startswith('https') and any([url.endswith(e) for e in extensions]):
                images.append(url)

    return images


def encrypt_password(password):
    """
    Crypting password with CRYPT_KEY and Fernet cryptography
    """
    pwd_bin = password.encode('utf-8')
    coded_pwd = CRYPT_KEY.encrypt(pwd_bin).decode('utf-8')
    return coded_pwd


def decrypt_password(coded_pwd):
    """
    Decoding password with CRYPT_KEY and Fernet cryptography
    """
    decoded_pwd = CRYPT_KEY.decrypt(coded_pwd.encode('utf-8'))
    password = decoded_pwd.decode('utf-8')
    return password
