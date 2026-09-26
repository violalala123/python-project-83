from urllib.parse import urlparse
import validators


def normalize_url(url_string):
    
    parsed = urlparse(url_string)
    return f"{parsed.scheme}://{parsed.netloc}"


def validate_url(url_string):
    
    errors = []
    if not url_string:
        errors.append("URL обязателен для заполнения")
    elif len(url_string) > 255:
        errors.append("URL превышает 255 символов")
    elif not validators.url(url_string):
        errors.append("Некорректный URL")
    return errors