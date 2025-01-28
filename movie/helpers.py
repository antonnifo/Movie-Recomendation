import re

def clean_title(title: str) -> str:
    """
    Clean movie title by removing non-alphanumeric chars, converting to lowercase, etc.
    """
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s]', '', title)
    return title


