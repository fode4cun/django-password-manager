import re
from io import BytesIO

import requests
from django.core.files.base import ContentFile


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


def retrieve_image(url):
    response = requests.get(url)
    return BytesIO(response.content)


def pil_to_django(image):
    fobject = BytesIO()
    image.save(fobject, format=image.format)
    return ContentFile(fobject.getvalue())
