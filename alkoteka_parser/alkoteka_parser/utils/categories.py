from urllib.parse import urlparse


def extract_slug(url: str) -> str:
    """
    Берёт настоящий slug категории из URL каталога.
    Пример:
    /catalog/vino/options-cvet_rozovoe -> vino
    """
    path = urlparse(url).path  # /catalog/vino/options...
    parts = path.strip("/").split("/")  # ['catalog', 'vino', 'options-cvet_rozovoe']

    if len(parts) < 2:
        return ""

    # parts[0] == 'catalog'
    # parts[1] == реальный slug категории
    return parts[1]
