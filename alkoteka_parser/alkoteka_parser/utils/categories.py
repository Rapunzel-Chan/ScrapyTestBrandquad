from urllib.parse import urlparse


def extract_slug(url: str) -> str:
    """
    Берёт настоящий slug категории из URL каталога.
    """
    path = urlparse(url).path
    parts = path.strip("/").split("/")

    if len(parts) < 2:
        return ""
    return parts[1]
